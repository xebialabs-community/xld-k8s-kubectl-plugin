#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#


def resources():
    result = []
    for _delta in specification.deltas:
        print _delta
        if _delta.operation == "NOOP":
            continue
        deployed = _delta.deployedOrPrevious
        if deployed.type == "k8s.Resources" and deployed.container.container.useKubectl:
            result.append(deployed)
    return result

for resource in resources():
    print "PROCESS {0}".format(resource.id)
    print "before:{0}".format(resource.resourceFactory)
    resource.resourceFactory='k8s.kubectl.factory.K8SKubeCtlResourceFactory'
    print "after:{0}".format(resource.resourceFactory)
