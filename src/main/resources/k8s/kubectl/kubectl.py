import json
import sys
from overtherepy import OverthereHostSession

from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, SshConnectionOptions,BashScriptBuilder
from com.xebialabs.overthere import OperatingSystemFamily
from com.xebialabs.overthere.cifs import CifsConnectionType


class Kubectl(object):

    def __init__(self,  namespace, cluster):
        self.namespace = namespace
        self.cluster = cluster

    def apply(self, data):
        session = OverthereHostSession(self.cluster.kubectlHost)
        data_str = self.data_to_string(data)
        print data_str
        remote_file = session.upload_text_content_to_work_dir(data_str,'k8s_resource.json')
        builder = BashScriptBuilder( )
        builder.add_line("{0} apply -f {1}".format(self.get_kubectl_command(), remote_file.path),check_rc=True)
        shell_file_content = builder.build()
        print "Executed shell"
        print shell_file_content
        xld_apply_sh_file=session.upload_text_content_to_work_dir(shell_file_content,'xld_apply.sh',executable=True)
        print xld_apply_sh_file
        print '-'*60
        response = session.execute(xld_apply_sh_file.path, check_success=False, suppress_streaming_output=True)
        self.dump_response(response)
        if response.rc != 0:
            raise Exception("Failed to apply the resource definition :{0}".format(" ".join(response.stdout)))

    def dump_response(self, response):
        for r in response.stdout:
           sys.stdout.write("{0}\n".format(r))
        for r in response.stderr:
           sys.stderr.write("{0}\n".format(r))
        if response.rc != 0:
           sys.stderr.write("Exit Code : {0}\n".format(response.rc))


    def data_to_string(self, data):
        return json.dumps(data, indent=2)

    def get_kubectl_command(self):
        kubectl = '{0}/kubectl --namespace={1}'.format(self.cluster.kubectlPath,self.namespace)
        if self.cluster.kubeConfigContext is not None:
            kubectl = kubectl + ' --context={0}'.format(self.cluster.kubeConfigContext)
        return kubectl


class MyK8S(object):
    """docstring for MyK8S"""
    def __init__(self ):
        self.kubectlPath="/usr/local/bin"
        self.kubeConfigContext = "minikube"
        localOpts = LocalConnectionOptions(os=OperatingSystemFamily.UNIX)
        self.kubectlHost = OverthereHost(localOpts)

#kubectl = Kubectl(MyK8S(),'foo')

#print kubectl.get_kubectl_command()
#data = json.load(open('./xebialabs/artifacts/Applications/k8s/xl-front-back-app/0.0.81/back-deployment/back-back-back-deployment-1.0.81.json'))
#print kubectl.apply(data)


