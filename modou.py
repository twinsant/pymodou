import json

import requests

from local_conf import *

if __name__ == '__main__':
    data = {'password':PASSWORD}
    r = requests.post('http://modouwifi.net/api/auth/login', data=json.dumps(data))
    if r.status_code == 200:
        result = r.json()
        code = result['code']
        if code!=0:
            msg = result['msg']
            print code, msg
        else:
            print result
