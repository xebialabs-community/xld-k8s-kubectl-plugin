#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
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

