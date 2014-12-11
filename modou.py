import json
import urllib

import requests

from local_conf import *

# https://github.com/modouwifi/doc-modouwifi-api
class Request(object):
    API = 'http://modouwifi.net/api/'
    def __init__(self, modou, method='get'):
        self._modou = modou
        self._method = method

    def __getattr__(self, *args, **kwargs):
        #print args, kwargs
        name = args[0]
        if name.startswith('_'):
            return super(Request, self).__getattr__(*args, **kwargs)
        else:
            self._api_path = name.replace('__', '/')
            return self

    def __call__(self, *args, **kwargs):
        #print args, kwargs, self._method, self._api_path
        data = kwargs
        if self._modou._userid:
            cookies = dict(userid=self._modou._userid)
        else:
            cookies = {}
        api_url = self.API + '%s' % self._api_path
        if self._method == 'post':
            r = requests.post(api_url, data=json.dumps(data), cookies=cookies)
        else:
            query = urllib.urlencode(data)
            if query:
                api_url += '?%s' % query
            #print api_url
            r = requests.get(api_url, cookies=cookies)
        if r.status_code == 200:
            result = r.json()
            if self._api_path == 'auth/login':
                code = result['code']
                if code!=0:
                    msg = result['msg']
                    print code, msg
                else:
                    userid = r.cookies['userid']
                    self._modou._userid = userid
            return result
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
    #modou.get.system__get_version_info()
    ##modou.get.system__upgrade_get_latest_version() # not supported yet
    #modou.get.system__check_upgrade_global_status()
    #modou.get.system__check_remote_version_upgrade()
    #modou.get.system__get_ucode()
    #modou.get.security__get_config()
    #modou.get.security__check_permission()
    #modou.get.wan__get_info()
    #modou.get.wan__is_internet_available()
    #modou.get.system__get_cable_connection()
    #modou.get.plugin__installed_plugins()
    #modou.post.commands__run(cmd='echo "Hello, Modou."')
    ##modou.get.screenshot() # very very slow
    r = modou.get.plugin__installed_plugins()
    for plugin in r['plugins']:
        if plugin['name'] == 'modou-weather':
            #print json.dumps(plugin, indent=4)
            #_r = modou.get.plugin__plugin_status(id=plugin['id'])
            modou.post.plugin__config__set(package_id=plugin['package_id'], data={
        "city_name": {
            "group_id": "main_info_display",
            "type": {
                "max": 16,
                "class": "STRING",
                "min": 2
            },
            "name": "\u57ce\u5e02\u540d\u79f0",
            "value": "**\u6b64\u7248\u672c\u4e0d\u652f\u6301**",
            "id": "city_name"
        },
        "state_auto_update": {
            "group_id": "main_info_display",
            "type": {
                "class": "BOOL"
            },
            "name": "\u81ea\u52a8\u66f4\u65b0",
            "value": False,
            "id": "state_auto_update"
        },
        "city_id": {
            "group_id": "main_info_display",
            "type": {
                "max": 101340904,
                "class": "INT",
                "min": 101010100
            },
            "name": "\u57ce\u5e02\u4ee3\u7801",
# http://www.cnblogs.com/wf225/p/4090737.html
            "value": 101010100,
            "id": "city_id"
        }
    })
            _r = modou.get.plugin__config__get(id=plugin['package_id'], type='TP')
            #print json.dumps(_r, indent=4)
