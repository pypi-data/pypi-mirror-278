
import os
import os.path
import sys
import importlib
import inspect
import json
import socket
import time
from contextlib import closing

class Args:
    """
      Arg-Parser der eine Überprüfung der Argument vornimmt. 
      Wenn man beim aufruf noch nicht weiß welche Argument abgefragt werden sollen
    """
    argv = []
    i = 0
    cfg = None
    def __init__(self, argv = None):
        if argv is None:
            self.argv = sys.argv
        else:    
            self.argv = argv

    def __str__(self):
        return f"Args(frist: {self.first()})"

    def __len__(self):
        return len(self.argv)

    def help_requested(self):
        return self.hasFlag('help') or self.hasShortFlag('h') or '?' in self.argv
    def hasFlag(self, name):
        return '--'+name in self.argv

    def shift(self):
        if len(self.argv) <= self.i:
            return ''
        res = self.argv[self.i]
        self.i += 1
        return res

    def first(self):
        if len(self.argv) <= self.i:
            return ''
        else:
            return self.argv[self.i]

    def hasName(self, name):
        return name in self.argv

    def hasShortFlag(self, name):
        return '-'+name in self.argv

    def get(self, key, default=None):
        return self.val(key, default)

    def getValue(self, name, default=None):
        """
            liest --name value Parameter
        """
        for i in range(len(self.argv)-1):
            if self.argv[i] == '--'+name:
                return self.argv[i+1]
        return default
    def val(self, name, default=None):
        if self.hasFlag(name):
            return self.getValue(name, default)
        else:
            return self.env(name, default)
    def getValues(self, name):
        res = []
        for i in range(len(self.argv)-1):
            if self.argv[i] == '--'+name:
                res.append(self.argv[i+1])
        return res

    def to_dict(self):
        res = {}
        for i in range(len(self.argv)-1):
            if self.argv[i].startswith('--'):
                res[self.argv[i][2:]] = self.argv[i+1]
        return res

    def __read_cfg(self):
        if os.path.isfile('nweb.json'):
            with open('nweb.json') as f:
                self.cfg = json.load(f)
        elif os.path.isfile('/etc/nweb.json'):
            with open('/etc/nweb.json') as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {}
    def env(self, name, default=None):
        self.__read_cfg();
        if name in self.cfg:
            return self.cfg[name]
        return os.getenv(name, default)

    def __contains__(self, item):
        return (self.cfg is not None and item in self.cfg) or self.hasFlag(item)
    def __getitem__(self, name):
        if isinstance(name, int):
            return self.argv[name]
        elif self.hasFlag(name):
            return self.getValue(name)
        else:
            return self.env(name)
    def __get__(self, i):
        return self.argv[i]
    def dispatch(self, **kwargs):
        arg = self.shift()
        if arg == sys.argv[0]:
            arg = self.shift()
        arg = arg.replace('-', '_')
        if arg in kwargs:
            kwargs[arg](self)
        else:
            print("Unknown Argument. " + arg)
            print("Valid Options: " + ", ".join(kwargs.keys()))
            if 'help' in kwargs:
                kwargs['help']()

class LimitStrList:
    def __init__(self, limit=100, auto_trim=False):
        self.limit = limit
        self.auto_trim = auto_trim
        self.list = []

    def append(self, item):
        if self.auto_trim:
            item = item.strip()
        self.list.append(item)
        if len(self.list) > self.limit:
            self.list.pop(0)

    def clear(self):
        self.list = []

    def __str__(self):
        s = ''
        for line in self.list:
            s += line + "\n"
        return s

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __iter__(self):
        return self.list.__iter__()


def has_typed_arg(spec, name, cls):
    ano = spec.annotations.get(name, None)
    if ano is not None:
        return ano == cls
    else:
        return False

def load_class(spec, create=False, args={}, run_args:Args=None):
    """ spec = 'module:ClassName' """
    if args is None:
        args = {}
    if isinstance(spec, type):
        c_spec = inspect.getfullargspec(spec)
        if run_args is not None and has_typed_arg(c_spec, 'args', Args):
            args['args'] = run_args
        return spec(**args)
    elif not isinstance(spec, str):
        return spec
    try:
        a = spec.split(':')
        m = importlib.import_module(a[0])
        c = getattr(m, a[1])
        if create:
            spec = inspect.getfullargspec(c)
            if run_args is not None and has_typed_arg(spec, 'args', Args):
                args['args'] = run_args
            return c(**args)
        else:
            return c
    except ModuleNotFoundError as e:
        print("[nwebclient.util.load_class] ModuleNotFoundError Spec: " + str(spec), file=sys.stderr)
        print("[nwebclient.util.load_class] PWD: " + str(os.getcwd()), file=sys.stderr)
        raise e
       
def load_resource(module, filename):
    # https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
    import importlib.resources as pkg_resources
    #try:
    #    inp_file = (pkg_resources.files(module) / filename)
    #    with inp_file.open("rb") as f:  # or "rt" as text file with universal newlines
    #        return f.read()
    #except AttributeError:
    #    # Python < PY3.9, fall back to method deprecated in PY3.11.
    return pkg_resources.read_text(module, filename)

def exists_module(module_name):
    """
      itertools = importlib.import_module('itertools')
      import pkg_resources
      pkg_resources.get_distribution('requests').version
    """
    import importlib.util
    module_spec = importlib.util.find_spec(module_name)
    found = module_spec is not None
    return found

def download(url, filename, ssl_verify=True):
    import requests
    r = requests.get(url, stream=True, verify=ssl_verify) 
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
                
def file_get_contents(filename):
    with open(filename, 'rb') as f:
        return f.read()

def file_get_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()
    
def file_put_contents(filename, contents):
    if isinstance(contents, bytes):
        with open(filename, "wb") as f:
            f.write(contents)
    else:
        with open(filename, "w") as f:
            f.write(contents)

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def is_port_free(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    return result != 0

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def run_async(op):
    from threading import Thread
    t = Thread(target=op)
    t.start()
    return t

def setInterval(function, interval):
    def loop():
        while True:
            time.sleep(interval/1000)
            function()

    from threading import Thread
    t = Thread(target=loop)
    t.start()
    return t

def split(a, n):
    """
        Teilt eine Liste in gleich große Teile
    """
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def is_subclass_of(obj, cls_name):
    class_names = []
    while getattr(obj, '__base__', None) is not None:
        class_names.append(obj.__name__)
        obj = obj.__base__
    return cls_name in class_names
