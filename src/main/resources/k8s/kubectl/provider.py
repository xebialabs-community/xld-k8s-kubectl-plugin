#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import time
import json
from overtherepy import OverthereHostSession
from k8s.kubectl.kubectl import Kubectl
import traceback
import sys
from java.lang import System


class KubectlResourceProvider(object):
    def __init__(self, container, kind, api_version):
        self.kind = kind
        self.api_version = api_version
        self.container = container

    def create(self, namespace, resource_definition):
        print 'kubectl create {0} {1}'.format(namespace,resource_definition['metadata']['name'])
        Kubectl(namespace, self.container.container).apply(resource_definition)

    def modify(self, namespace, resource_definition, patch_type='strategic', update_method='patch'):
        print 'kubectl modify {0} {1}'.format(namespace,resource_definition['metadata']['name'])
        Kubectl(namespace, self.container.container).apply(resource_definition)

    def delete(self, namespace, resource_definition, propagation_policy='Foreground'):
        print 'kubectl delete {0} {1}'.format(namespace,resource_definition['metadata']['name'])
        kubectl=Kubectl(namespace, self.container.container)
        if kubectl.exists(self.kind,resource_definition['metadata']['name']):
            kubectl.delete(resource_definition, propagation_policy)
        else:
            print "the resource doesn't exist"


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

