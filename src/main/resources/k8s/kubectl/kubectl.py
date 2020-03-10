#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

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

    def _action(self, verb,data):
        session = OverthereHostSession(self.cluster.kubectlHost)
        data_str = self.data_to_string(data)
        print data_str
        remote_file = session.upload_text_content_to_work_dir(data_str,'k8s_{0}_resource.json'.format(verb))
        command_line = "{0} {1} -f {2}".format(self.get_kubectl_command(),verb, remote_file.path)
        print command_line
        self._execute(session, command_line)

    def apply(self, data):
        return self._action('apply',data)

    def create(self, data):
        return self._action('create',data)

    def replace(self, data ):
        return self._action('replace',data)

    def delete(self, data, propagation_policy):
        return self._action('delete',data)

    def get(self, kind, metadata_name):
        return self.run('get','{0} --field-selector metadata.name={1}'.format(kind, metadata_name),json_output=True)

    def exists(self, kind, metadata_name):
        result = self.get(kind,metadata_name)
        return len(result['items']) > 0

    def describe(self, kind, metadata_name):
        return self.run('describe','{0} {1}'.format(kind, metadata_name))

    def run(self,verb, parameters,json_output=False, raise_on_fail=False):
        session = OverthereHostSession(self.cluster.kubectlHost)
        command_line = "{0} {1} {2}".format(self.get_kubectl_command(), verb, parameters)
        if json_output:
            command_line = command_line + " -o json"
        print command_line
        response = session.execute(command_line, suppress_streaming_output=True, check_success=False)
        if response.rc == 0:
            stdout =  "\n".join(response.stdout)
            if json_output:
                return json.loads(stdout)
            else:
                return stdout
        else:
            if raise_on_fail:
                raise Exception("Kubectl Error when running '{0}':{1}".format(command_line,'\n'.join(response.stderr)))
            else:
                return '\n'.join(response.stderr)

    def _execute(self, session, command_line):
        print command_line
        builder = BashScriptBuilder( )
        builder.add_line(command_line,check_rc=True)
        shell_file_content = builder.build()
        xld_apply_sh_file=session.upload_text_content_to_work_dir(shell_file_content,'xld_kubectl.sh',executable=True)
        print '-'*60
        response = session.execute(xld_apply_sh_file.path, check_success=False, suppress_streaming_output=True)
        self._dump_response(response)
        if response.rc != 0:
            raise Exception("Failed to apply the resource definition :{0}".format(" ".join(response.stdout)))

    def _dump_response(self, response):
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


