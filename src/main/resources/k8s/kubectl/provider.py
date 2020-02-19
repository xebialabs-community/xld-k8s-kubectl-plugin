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
from kubernetes.client.rest import ApiException


class KubectlResourceProvider(object):
    def __init__(self, container, kind, api_version):
        self.kind = kind
        self.api_version = api_version
        self.container = container

    def create(self, namespace, resource_definition):
        print 'kubectl create {0} {1}'.format(namespace,resource_definition['metadata']['name'])
        Kubectl(namespace, self.container.container).apply(resource_definition)

    def modify(self, namespace, resource_definition, patch_type='strategic', update_method='patch'):
        return "kubectl modify {0} {1}".format(namespace,resource_definition)

    def delete(self, namespace, resource_definition, propagation_policy='Foreground'):
        return "kubectl delete {0} {1}".format(namespace,resource_definition)

    def filter_resources_by_definition(self, namespace, resource_definition):
        return {'xx':'yy'}

    def wait_until_deleted(self, namespace, resource_definition):
        exists = True
        resource_name = resource_definition["metadata"]["name"]
        while exists:
            time.sleep(5)
            print("Checking for existence of '{}'.".format(resource_name))
            resources = self.filter_resources_by_definition(namespace=namespace, resource_definition=resource_definition)
            if 'items' not in dir(resources) or not bool(resources.items):
                exists = False
                print("Resource '{}' deleted.".format(resource_name))
            else:
                print("Resource '{}' still exists.".format(resource_name))


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

