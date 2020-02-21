import json
import sys
import time
from overtherepy import OverthereHostSession

from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, SshConnectionOptions,BashScriptBuilder
from com.xebialabs.overthere import OperatingSystemFamily
from com.xebialabs.overthere.cifs import CifsConnectionType


class Waiter(object):

    def __init__(self,  ctl, limit=10, sleep=10):
        self.ctl = ctl
        self.limit = limit
        self.index = limit
        self.sleep = sleep

    def wait_for_up(self, kind,name):
        if kind.lower() == 'deployment':
            return self.wait_for_up_deployment(kind,name)

        print "wait_for_up {0},{1}".format(kind,name)
        while self.index > 0:
            result = self.ctl.get(kind,name)
            if len(result['items']) == 0:
                print "The {0} {1} doesn't exist {2}/{3}".format(name,kind, self.limit-self.index+1, self.limit)
                self.index = self.index - 1
            else:
                print "The {0} {1} exists".format(name,kind)
                print self.ctl.describe(kind,name)
                return 0
            time.sleep(self.sleep)
        return 1

    def wait_for_up_deployment(self, kind,name):
        print "wait_for_up_deployment {0},{1}".format(kind,name)
        while self.index > 0:
            result = self.ctl.get(kind,name)
            if len(result['items']) == 0:
                print "The {0} {1} doesn't exist {2}/{3}".format(name,kind, self.limit-self.index+1, self.limit)
            else:
                print "The {0} {1} exists {2}/{3}".format(name,kind, self.limit-self.index+1, self.limit)
                data = result['items'][0]
                for condition in data['status']['conditions']:
                    print "Status {status} {reason}: {message}".format(**condition)
                availableReplicas = self.get_available_replicas(data)
                replicas=data['spec']['replicas']
                print "availableReplicas {0}/ replicas {1}".format(availableReplicas, replicas)
                if availableReplicas >= int(replicas):
                    print "DONE replicas"
                    self.ctl.describe(kind,name)
                    self.dump_events(data)
                    return 0
            self.index = self.index - 1
            time.sleep(self.sleep)
        print "Too many attempts...."
        self.dump_events(data)
        raise Exception("Fail to wait for {0},{1}".format(kind,name))

    def dump_events(self,deployment):
        for pod in self.get_associated_pods(deployment):
            print "Pod {0}".format(pod)
            print "-------------------"
            for event in self.get_pod_events(pod):
                print event

    def get_associated_pods(self,deployment):
        deployment_labels = deployment['spec']['template']['metadata']['labels']
        selector = ','.join(x+'='+deployment_labels[x] for x in deployment_labels)
        pods = []
        data = self.ctl.run('get','pods -l={0}'.format(selector),json_output=True)
        return [item['metadata']['name'] for item in data['items']]

    def get_pod_events(self, pod_name):
        data = self.ctl.run('get','event  --field-selector involvedObject.name={0}'.format(pod_name),json_output=True)
        return ["{type} {message}".format(**item) for item in data['items']]

    def get_available_replicas(self,data):
        try:
            return int(data['status']['availableReplicas'])
        except:
            return -1



    def wait_for_down(self, kind,name):
        print "wait_for_down {0},{1}".format(kind,name)
        while self.index > 0:
            result = self.ctl.get(kind,name)
            if len(result['items']) == 0:
                print "The {0} {1} doesn't exist.".format(name,kind)
                return 0
            else:
                print "The {0} {1} still exists {2}/{3}".format(name,kind,self.limit-self.index+1, self.limit)
                self.index = self.index - 1
            time.sleep(self.sleep)
        return 1








