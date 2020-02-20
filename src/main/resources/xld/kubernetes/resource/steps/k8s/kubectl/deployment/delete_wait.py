#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#
from k8s.kubectl.kubectl import Kubectl
from k8s.kubectl.waiter import Waiter
from xld.kubernetes.factories.handler_factory import ContainerHelperFactory

container_helper = ContainerHelperFactory(previousDeployed.container).create()
namespace=container_helper.get_container_name(previousDeployed.container)

kubectl = Kubectl(namespace, previousDeployed.container.container)

kind=data['kind']
metadata_name=data['metadata']['name']

Waiter(kubectl).wait_for_down(kind,metadata_name)

