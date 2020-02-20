#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#
from k8s.kubectl.kubectl import Kubectl
from k8s.kubectl.waiter import Waiter
from xld.kubernetes.factories.handler_factory import ContainerHelperFactory

container_helper = ContainerHelperFactory(deployed.container).create()
namespace=container_helper.get_container_name(deployed.container)

kubectl = Kubectl(namespace, deployed.container.container)

kind=data['kind']
metadata_name=data['metadata']['name']

Waiter(kubectl).wait_for_up(kind,metadata_name)

