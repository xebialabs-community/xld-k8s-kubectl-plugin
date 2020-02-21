#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from k8s.kubectl.kubectl import Kubectl
from k8s.kubectl.waiter import Waiter
from overtherepy import OverthereHostSession
from com.xebialabs.overthere import OperatingSystemFamily
from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, SshConnectionOptions,BashScriptBuilder
import json
import sys

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
if ctl.exists('deployment','front-deployment-0.0.99'):
    ctl.delete(json.load(open('src/test/resources/json/front-1.0.99-fail.json')), None)
sys.exit(0)

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

