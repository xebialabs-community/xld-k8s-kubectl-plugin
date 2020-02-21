from k8s.kubectl.kubectl import Kubectl
from k8s.kubectl.waiter import Waiter
from overtherepy import OverthereHostSession
from com.xebialabs.overthere import OperatingSystemFamily
from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, SshConnectionOptions,BashScriptBuilder
import json

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
ctl.apply(json.load(open('src/test/resources/json/front-1.0.83.json')))
Waiter(ctl, sleep=1).wait_for_up_deployment('Deployment','front-deployment-0.0.83')
try:
    ctl.apply(json.load(open('src/test/resources/json/front-1.0.99-fail.json')))
    Waiter(ctl, sleep=1, limit=2).wait_for_up('Deployment','front-deployment-0.0.99')
except:
    print "fail.....099"
Waiter(ctl, sleep=1).wait_for_up('Deployment','front-deployment-0.0.83')
ctl.delete(json.load(open('src/test/resources/json/front-1.0.83.json')), None)
Waiter(ctl, sleep=1).wait_for_down('Deployment','front-deployment-0.0.83')

ctl.delete(json.load(open('src/test/resources/json/front-1.0.99-fail.json')), None)

