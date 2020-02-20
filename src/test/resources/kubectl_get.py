from k8s.kubectl.kubectl import Kubectl
from k8s.kubectl.waiter import Waiter
from overtherepy import OverthereHostSession
from com.xebialabs.overthere import OperatingSystemFamily
from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, SshConnectionOptions,BashScriptBuilder

class MyK8S(object):
    """docstring for MyK8S"""
    def __init__(self ):
        self.kubectlPath="/usr/local/bin"
        self.kubeConfigContext = "minikube"
        localOpts = LocalConnectionOptions(os=OperatingSystemFamily.UNIX)
        self.kubectlHost = OverthereHost(localOpts)

namespace='simpledev'
kind='service'
metadata_name = 'back-web-service'
ctl = Kubectl(namespace, MyK8S())
Waiter(ctl, sleep=1).wait_for_up(kind,metadata_name)
#Waiter(ctl, sleep=1).wait_for_down(kind,metadata_name)


