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
        print "wait_for_up {0},{1}".format(kind,name)
        while self.index > 0:
            result = self.ctl.get(kind,name)
            if len(result['items']) == 0:
                print "The {0} {1} doesn't exist {2}/{3}".format(name,kind, self.limit-self.index+1, self.limit)
                self.index = self.index - 1
            else:
                print "The {0} {1} exists".format(name,kind)
                self.ctl.describe(kind,name)
                return 0
            time.sleep(self.sleep)
        return 1


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








