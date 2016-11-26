import datetime
import json
import logging
from base64 import b64encode
from binascii import unhexlify
import requests

logging.basicConfig(filename='chainclient.log', level=logging.WARNING)


class MultiChainClient(object):
    __id_count = 0

    def __init__(self, rpcuser, rpcpassword, rpchost, rpcport, chainname, rpc_call=None):
        self.__rpcuser = rpcuser
        self.__rpcpassword = rpcpassword
        self.__rpchost = rpchost
        self.__rpcport = rpcport
        self.__chainname = chainname

        auth_pair = self.__rpcuser.encode('utf-8') + b':' + self.__rpcpassword.encode('utf-8')
        self.__auth_header = b"Basic " + b64encode(auth_pair)

        headers = {
            'Authorization': self.__auth_header,
            'Host': self.__rpchost,
            'User-Agent': 'Savior v0.1',
            'Content-type': 'application/json',
        }

        self.__headers = headers
        self.__rpc_call = rpc_call

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):  # Python internal stuff
            raise AttributeError
        if self.__rpc_call is not None:
            name = "{0}.{1}".format(self.__rpc_call, name)
        return MultiChainClient(self.__rpcuser, self.__rpcpassword, self.__rpchost, self.__rpcport, self.__chainname, name)

    def __call__(self, *args):
        MultiChainClient.__id_count += 1
        url = 'http://{0}:{1}'.format(self.__rpchost, self.__rpcport)
        postdata = {
            'chain_name': self.__chainname,
            'version': '1.1',
            'params': args,
            'method': self.__rpc_call,
            'id': MultiChainClient.__id_count
        }
        r = requests.post(url, data=json.dumps(postdata), headers=self.__headers)
        if r.status_code == 200:
            return_objects = {
                'liststreams': StreamObject,
                'liststreamitems': ListStreamItem,
                'liststreampublisheritems': ListStreamItem,
            }
            if self.__rpc_call in return_objects:
                return return_objects[self.__rpc_call](r.json()['result'])
            return r.json()['result']
        else:
            return r.text


class ListStreamObject(object):
    jsons = None
    objects = None

    def __init__(self, stream_list):
        self.jsons = stream_list
        objects = []
        for each in self.jsons:
            objects.append(StreamObject(each))
        self.objects = objects


class ListStreamItem(object):
    jsons = None
    objects = None

    def __init__(self, stream_list):
        self.jsons = stream_list
        objects = []
        for each in self.jsons:
            objects.append(StreamItem(each))
        self.objects = objects


class StreamObject(object):
    attrs = [
        'keys',
        'subscribed',
        'confirmed',
        'createtxid',
        'publishers',
        'items',
        'details',
        'open',
        'synchronized',
        'name',
        'streamref',
    ]

    def __init__(self, stream):
        for k, v in stream.items():
            if k in self.attrs:
                setattr(self, k, v)

    def __repr__(self):
        return self.name


class StreamItem(object):
    attrs = [
        'blocktime',
        'confirmations',
        'publishers',
        'data',
        'key',
        'txid',
    ]

    def __init__(self, json):
        for k, v in json.items():
            if k in self.attrs:
                setattr(self, '_{0}'.format(k), v)

    def __repr__(self):
        return '{0} - {1}: {2}'.format(self.blocktime, self._key, self.data)

    @property
    def blocktime(self):
        return datetime.datetime.fromtimestamp(self._blocktime).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def data(self):
        return unhexlify(self._data).decode('utf-8')

    @property
    def publishers(self):
        return self._publishers

try:
    from local_settings import rpcuser, rpcpassword, rpchost, rpcport, chainname
    api = MultiChainClient(rpcuser, rpcpassword, rpchost, rpcport, chainname)
except ImportError:
    raise ImportError('Failed to import local settings.')
