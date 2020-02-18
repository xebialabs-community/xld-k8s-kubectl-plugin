#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#

import importlib

from k8s.kubectl.provider import KubectlResourceProvider


class K8SKubeCtlResourceFactory(object):
    def __init__(self, deployed):
        self.__deployed = deployed

    def get_resource_order(self):
        return {
            'Default': {'Create': self.__deployed.createOrder, 'Modify': self.__deployed.modifyOrder, 'Destroy': self.__deployed.destroyOrder}
        }

    @staticmethod
    def get_recreate_resources():
        return ['PersistentVolumeClaim']

    @staticmethod
    def get_resource_wait_details():
        return {
            "Create": {
                "Default": {'script': 'k8s/kubectl/create_update_wait', 'action': "created"},
                "Pod": {'script': 'k8s/kubectl/create_update_wait', 'action': "in running state"},
                "Deployment": {'script': 'k8s/kubectl/deployment/create_update_wait', 'action': "in running state"},
                "StatefulSet": {'script': 'k8s/kubectl/deployment/create_update_wait', 'action': "in running state"},
                "PersistentVolumeClaim": {'script': 'k8s/kubectl/create_update_wait', 'action': "in Bound phase"}
            },
            "Destroy": {
                "Default": {'script': 'k8s/kubectl/delete_wait', 'action': "destroyed completely"}
            },
            "Modify": {
                "Default": {'script': 'k8s/kubectl/create_update_wait', 'action': "modified"},
                "Pod": {'script': 'k8s/kubectl/create_update_wait', 'action': "in running state"},
                "Deployment": {'script': 'k8s/kubectl/deployment/create_update_wait', 'action': "in running state"},
                "StatefulSet": {'script': 'k8s/kubectl/deployment/create_update_wait', 'action': "in running state"}
            }
        }

    def get(self, data):
        return self._resolve(data)

    def _resolve(self, data):
        return KubectlResourceProvider(self.__deployed.container, data["kind"], data['apiVersion'] if 'apiVersion' in data else 'v1')

