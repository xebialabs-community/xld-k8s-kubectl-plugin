#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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

