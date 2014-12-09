import json

import requests

from local_conf import *

# https://github.com/modouwifi/doc-modouwifi-api
class Request(object):
    def __init__(self, modou, method='get'):
        self._modou = modou
        self._method = method

    def __getattr__(self, *args, **kwargs):
        #print args, kwargs
        name = args[0]
        if name.startswith('_'):
            return super(Request, self).__getattr__(*args, **kwargs)
        else:
            self.api_url = name.replace('__', '/')
            return self

    def __call__(self, *args, **kwargs):
        #print args, kwargs, self.method, self.api_url
        data = kwargs
        if self._modou._userid:
            cookies = dict(userid=self._modou._userid)
        else:
            cookies = {}
        if self._method == 'post':
            r = requests.post('http://modouwifi.net/api/%s' % self.api_url, data=json.dumps(data))
        else:
            r = requests.get('http://modouwifi.net/api/%s' % self.api_url, cookies=cookies)
        if r.status_code == 200:
            result = r.json()
            print result
            if self.api_url == 'auth/login':
                code = result['code']
                if code!=0:
                    msg = result['msg']
                    print code, msg
                else:
                    userid = r.cookies['userid']
                    self._modou._userid = userid
        else:
            print r.status_code

class Modou(object):
    def __init__(self):
        self._userid = None

    def __getattr__(self, *args, **kwargs):
        #print args, kwargs
        name = args[0]
        if name == 'post':
            return Request(self, method='post')
        elif name == 'get':
            return Request(self)
        elif name.startswith('_'):
            print name
            return super(Modou, self).__getattr__(*args, **kwargs)
        assert False

if __name__ == '__main__':
    modou = Modou()
    modou.post.auth__login(password=PASSWORD)
    modou.get.system__get_version_info()
    #modou.get.system__upgrade_get_latest_version() # not supported yet
    modou.get.system__check_upgrade_global_status()
    modou.get.system__check_remote_version_upgrade()
    modou.get.system__get_ucode()
