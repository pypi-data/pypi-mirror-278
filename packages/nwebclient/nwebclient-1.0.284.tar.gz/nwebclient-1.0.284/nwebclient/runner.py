import math
import sys
import json
import time
import traceback
import importlib
import requests
import datetime
import subprocess
import base64
import io
import os
import os.path
import inspect
from threading import Thread
from io import BytesIO

from nwebclient import web
from nwebclient import base
from nwebclient import util
from nwebclient import ticker
from nwebclient import machine
from nwebclient import NWebClient


ERROR_SERVER = 500
ERROR_UNKNOWN_JOB_TYPE = 599

class MoreJobs(Exception):
    """ raise MoreJobs([...]) """
    def __init__(self, jobs=[]):
        self.data = {'jobs': jobs}


def js_functions():
    return web.js_fn('base_url', [], [
        '  var res = location.protocol+"//"+location.host;',
        '  res += "/";'
        '  return res;'
    ]) + web.js_fn('post_url_encode', ['data'], [
        'var formBody = [];',
        'for (var property in data) {',
        '  var encodedKey = encodeURIComponent(property);',
        '  var encodedValue = encodeURIComponent(data[property]);',
        '  formBody.push(encodedKey + "=" + encodedValue);}',
        'return formBody.join("&");'
    ]) + web.js_fn('post', ['data'], [
        'return {method:"POST",',
        ' headers: {'
        '  "Content-Type": "application/x-www-form-urlencoded"',
        ' },',
        ' body: post_url_encode(data)'
        '};'
    ]) + web.js_fn('exec_job', ['data', 'on_success=null'], [
        'fetch(base_url(), post(data)).then((response) => response.json()).then( (result_data) => { ',
        '  document.getElementById("result").innerHTML = JSON.stringify(result_data); ',
        '  if (on_success!==null) {',
        '    on_success(result_data)',
        '  }',
        '});'
    ]) + web.js_fn('exec_job_p', ['data', 'on_success=null'], [
        'for (const [key, value] of Object.entries(data)) {',
        '  if (value.startsWith("#")) {',
        '    data[key] = document.querySelector(value).value;',
        '  }',
        '}',
        'fetch(base_url(), post(data)).then((response) => response.json()).then( (result_data) => { ',
        '  document.getElementById("result").innerHTML = JSON.stringify(result_data); ',
        '  if (on_success!==null) {',
        '    on_success(result_data)',
        '  }',
        '});'
    ]) + web.js_fn('observe_value', ['type', 'name', 'selector=null', 'interval=5000'], [
        'if (selector == null) selector = "#"+name;',
        'setInterval(function() {',
        '  exec_job({type:type,getvar:name}, function(result) {',
        '    document.querySelector(selector).innerHTML = result["value"];'
        '  });',
        '}, interval);'
    ])


class Mqtt:

    topic = 'main'
    mqtt = None

    def __init__(self, args={}, topic='main', on_message=None):
        try:
            from paho.mqtt import client as mqtt_client
            self.mqtt = mqtt_client.Client('NPyJobRunner', transport='tcp')
            self.topic = topic
            self.on_message = on_message
            # client.username_pw_set(username, password)
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    #self.info("Connected to MQTT Broker. Subscribe to Topic: " + self.MQTT_TOPIC)
                    self.mqtt.subscribe(self.topic)
                else:
                    print("Failed to connect, return code %d\n", rc)

            def on_message_func(client, userdata, msg):
                #print("Received MQTT Message")
                #data = json.loads(msg.payload.decode())
                #client.publish(self.MQTT_RESULT_TOPIC, '')
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                if self.on_message is not None:
                    self.on_message(msg.payload.decode())

            # def on_log(client, userdata, level, buf):
            #    print("MQTT Log")
            self.mqtt.on_connect = on_connect
            self.mqtt.on_message = on_message_func
            # client.on_log = on_log
            self.mqtt.connect_async(args.get('MQTT_HOST', '127.0.0.1'), args.get('MQTT_PORT', 1883), keepalive=65530)
            #if forever:
            #    self.mqtt.loop_forever()
            #else:
            self.mqtt.loop_start()
        except Exception:
            pass

    def publish(self, topic, message):
        if self.mqtt is not None:
            self.mqtt.publish(topic, message)

    def __call__(self, *args, **kwargs):
        if self.mqtt is not None:
            self.mqtt.publish(self.topic, args[0])


class BaseJobExecutor(base.Base):

    param_names = {}
    var_names = []

    def __init__(self):
        super().__init__()
        self.param_names = {}
        self.var_names = []
    def __call__(self, data={}):
        return self.execute(data)
    def js(self):
        return js_functions()

    def execute(self, data):
        if 'setvar' in data and data['setvar'] in self.var_names:
            setattr(self, data['setvar'], data['value'])
            return {'success': True, 'message': 'Var Set (BaseJobExecutor)'}
        elif 'getvar' in data and data['getvar'] in self.var_names:
            return {'success': True, 'value': getattr(self, data['getvar'], '')}
        else:
            return {'success': False, 'message': 'Unknown Operation (BaseJobExecutor)', 'request_keys': data.keys()}

    def canExecute(self, data):
        return True

    def setupRestApp(self, app):
        pass

    def action_btn(self, data):
        return web.button_js(data['title'], 'exec_job('+json.dumps(data)+');')

    def to_text(self, result):
        return json.dumps(result, indent=2)

    @classmethod
    def pip_install(cls):
        print("PIP Install")
        try:
            m = ' '.join(cls.MODULES)
            exe = sys.executable + ' -m pip install ' + m
            print("Install: " + exe)
            subprocess.run(exe.split(' '), stdout=subprocess.PIPE)
            print("Install Done.")
        except AttributeError:
            print("No Modules to install.")


class LazyDispatcher(BaseJobExecutor):
    key = 'type'
    classes = {}
    instances = {}
    args = None
    def __init__(self, key='type',**kwargs):
        self.key = key
        self.loadDict(kwargs)

    def supported_types(self):
        return set([*self.classes.keys(), *self.instances.keys()])

    def support_type(self, type):
        return type in self.supported_types()

    def loadDict(self, data):
        self.info("loadDict("+str(data)+")")
        if data is None:
            return
        for k in data.keys():
            v = data[k]
            if isinstance(v, str):
                try:
                    self.info("type:"+k+" "+v)
                    self.classes[k] = self.create_class(v)
                except ModuleNotFoundError as e:
                    self.error(f"Error: type: {k}, Modul {v} not found. (LazyDispatcher) Exception: {e}")
            elif isinstance(v, dict) and 'type' in v:
                self.execute(v)
            else:
                self.loadRunner(k, v)

    def create_class(self, v):
        obj = util.load_class(v, True, {}, self.args)
        # self.info("create_class: " + str(getattr(obj, 'args', '---')))
        return obj

    def loadRunner(self, key, spec):
        self.info(f"Load runner: " + str(spec) + " key: " + str(key))
        if isinstance(spec, dict) and 'py' in spec:
            runner = eval(spec['py'], globals())
            self.setupRunner(runner)
            self.instances[key] = runner
        else:
            spec.type = key
            self.instances[key] = spec
            self.setupRunner(spec)
        return {'success': True, 'type': key}

    def setupRunner(self, runner):
        self.addChild(runner)
        webapp = getattr(self.owner(), 'web', None)
        if webapp is not None:
            self.info("Loading Routes " + str(webapp) + " on " + str(runner))
            runner.setupRestApp(webapp)
        return runner

    def execute(self, data):
        if self.key in data:
            t = data[self.key]
            if t in self.instances:
                data = self.instances[t].execute(data)
            elif t in self.classes:
                c = self.classes[t]
                self.instances[t] = self.setupRunner(self.create_class(c))
                data = self.instances[t].execute(data)
            elif 'list_runners' == t:
                return {'names': self.classes.keys()}
            # TODO elif: loadClass directly
            else:
                data['success'] = False
                data['error_code'] = ERROR_UNKNOWN_JOB_TYPE
                data['message'] = 'Unkown Type (LazyDispatcher)'
        else:
            data['message'] = "LazyDispatcher, No Dispatch Key, " + self.key
            data['success'] = False
        return data

    def get_runner(self, type) -> BaseJobExecutor:
        if type in self.instances:
            return self.instances[type]
        elif type in self.classes:
            c = self.classes[type]
            self.instances[type] = self.setupRunner(c())
            return self.instances[type]
        return None

    def get_runner_by_class(self, cls_name):
        res = []
        for c in self.instances.values():
            if c.__class__.__name__ == cls_name:
                res.append(c)
        return res

    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.classes or data[self.key] in ['list_runners']
        return False

    def write_to(self, p: base.Page, summary=False):
        p.h2('Dispatcher: ' + str(self.classes))
        for key in self.instances:
            p.h3("Runner: " + key)
            p.div("Parameter: " + ','.join(self.instances[key].param_names.keys()))
            p.div("Vars: " + ','.join(self.instances[key].var_names))
            if isinstance(self.instances[key], BaseJobExecutor) and self.instances[key].has_method('write_to'):
                self.instances[key].write_to(p, summary=True)
            p.div(web.a(key, f'/pysys/dispatcher?type={key}')+' - '+web.a("Exec", f'/pysys/runner-ui?type={key}'))
        p.h2('Loading Runner')
        for key in self.classes:
            if key not in self.instances:
                p.div("Load: " + self.action_btn({'title': key, 'type': key}))
        p.h2('Execute')
        p.js_html('return "<a href=\\\"\"+'+web.js_base_url_exp()+'+\"pysys/runner-ui\\\">Runner-UI</a>"')
        p.js_html('return "<a href=\\\"\"+' + web.js_base_url_exp() + '+\"pysys/job-results\\\">Results</a>"')
        p.a("All Runners", '/pysys/registry')

    def nav(self, p:base.Page):
        p.a("Runner", '/pysys/runner')

    def page_dispatch(self, params={}):
        runner = self.get_runner(params['type'])
        page = getattr(runner, 'page', None)
        if page is not None:
            return page(params)
        else:
            return "404, no page() in Runner"

    def page_dispatch_cls(self, params={}):
        runner = self.get_runner_by_class(params['cls'])
        p = base.Page(owner=self)
        params['page'] = p
        for r in runner:
            page = getattr(r, 'page', None)
            if page is not None:
                page(params)
        self.nav(p)
        return p.nxui()

    def page_dispatch_multi(self, params={}):
        ts = params.get('types', '').split(',')
        p = base.Page(owner=self)
        params['page'] = p
        for t in ts:
            r = self.get_runner(t)
            page = getattr(r, 'page', None)
            if page is not None:
                page(params)
        self.nav(p)
        return p.nxui()

    def page(self, params={}):
        p = base.Page(owner=self)
        opts = {}
        if 'type' in params:
            return self.page_dispatch(params)
        else:
            opts['title'] = 'Dispatcher'
            self.write_to(p)
        return p.nxui(opts)

    def nxitems(self):
        res = []
        for key in self.instances:
            res.append({'title': key, 'url': '/pysys/dispatcher?type='+key})
        return res

    def setupRestApp(self, app):
        from flask import request
        app.add_url_rule('/pysys/dispatcher', 'dispatcher', view_func=lambda: self.page_dispatch(request.args))
        app.add_url_rule('/pysys/cls', 'dispatcher_cls', view_func=lambda: self.page_dispatch_cls({**request.args}))
        app.add_url_rule('/pysys/multi', 'dispatcher_multi', view_func=lambda: self.page_dispatch_multi({**request.args}))
        for runner in self.instances.values():
            runner.setupRestApp(app)


class JobRunner(base.Base):

    MQTT_TOPIC = 'jobs'
    MQTT_RESULT_TOPIC = 'result'

    """
      Werte aus dem JobAuftrag die nach einer Ausführung übernommen werden
    """
    result_job_keys = ['guid']
    
    counter = 0 
    
    # Start Time
    start = None
    last_job_time = None
    
    jobexecutor = None
    
    web = None
    
    def __init__(self, jobexecutor):
        super().__init__()
        self.jobexecutor = jobexecutor
        self.addChild(self.jobexecutor)
    def info(self, msg):
        #out = lambda msg: "[JobRunner] "+str(msg)
        print("[JobRunner] " + msg)
    def __call__(self, job):
        return self.execute_job(job)
    def execute(self, job):
        return self.execute_job(job)
    def execute_job(self, job):
        self.last_job_time = datetime.datetime.now()
        try:
            result = self.jobexecutor(job)
        except MoreJobs as mj:
            result = self.execute_data(mj.data)
        except Exception as e:
            self.info('Error: Job faild')
            result = job
            result['success'] = False
            result['error'] = True
            result['error_code'] = ERROR_SERVER
            result['error_message'] = str(e)
            result['trace'] = str(traceback.format_exc())
        if 'type' in job:
            result['job_type'] = job['type']
        for key in self.result_job_keys:
            if key in job:
                result[key] = job[key]
        # TODO check if inputs defined
        return result
    def execute_data(self, data):
        self.start = datetime.datetime.now()
        result = {'jobs': []}
        for job in data['jobs']:
            job_result = self.execute_job(job)
            result['jobs'].append(job_result)
            self.counter = self.counter + 1
        delta = (datetime.datetime.now()-self.start).total_seconds() // 60
        self.info("Duration: "+str(delta)+"min")
        return result
    def execute_file(self, infile, outfile=None):
        try:
            data = json.load(open(infile))
            result = self.execute_data(data)
            outcontent = json.dumps(result)
            print(outcontent)
            if not outfile is None:
                if outfile == '-':
                    print(outcontent)
                else:
                    with open(outfile, 'w') as f:
                        f.write(outcontent)
        except Exception as e:
            self.info("Error: " + str(e))
            self.info(traceback.format_exc());
            self.info("Faild to execute JSON-File "+str(infile))
    def execute_mqtt(self, args, forever=False):
        from paho.mqtt import client as mqtt_client
        if 'mqtt_topic' in args:
            self.MQTT_TOPIC = args['mqtt_topic']
        if 'mqtt__result_topic' in args:
            self.MQTT_RESULT_TOPIC = args['mqtt_result_topic']
        self.mqtt = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, 'NPyJobRunner', transport='tcp')
        self.info("Starting MQTT")

        # client.username_pw_set(username, password)
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker. Subscribe to Topic: " + self.MQTT_TOPIC)
                self.mqtt.subscribe(self.MQTT_TOPIC)
            else:
                self.info("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print("Received MQTT Job")
            data = json.loads(msg.payload.decode())
            result = self.execute(data)
            client.publish(self.MQTT_RESULT_TOPIC, json.dumps(result))
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        # def on_log(client, userdata, level, buf):
        #    print("MQTT Log")
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message
        # client.on_log = on_log
        self.mqtt.connect_async(args['MQTT_HOST'], args.get('MQTT_PORT', 1883), keepalive=65530)
        if forever:
            self.mqtt.loop_forever()
        else:
            self.mqtt.loop_start()

    def execute_rest_job(self):
        from flask import Flask, request
        data = {**request.args.to_dict(), **request.form.to_dict()}
        if len(data) == 0:
            return "Job Endpoint. " + web.a("Runner", '/pysys/runner')
        return json.dumps(self.execute_job(data))

    def execute_rest(self, port=8080, run=True, route='/', app=None):
        self.info("Starting webserver")
        from flask import Flask, request
        if app is None:
            app = Flask(__name__, static_folder=None)
        #@app.route('/')
        #def home():
        #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
        # Add To Root
        self.info("Executor: " + str(type(self.jobexecutor).__name__))
        self.jobexecutor.setupRestApp(app)
        app.add_url_rule(route, 'job_runner', view_func=lambda: self.execute_rest_job(), methods=['GET', 'POST'])
        app.add_url_rule('/pysys/job-counter', 'job_counter', view_func=lambda: str(self.counter))
        app.add_url_rule('/pysys/job-results', 'job_results', view_func=lambda: self.page_results())
        app.add_url_rule('/pysys/runner-ui', 'r_runner_ui', view_func=lambda: self.page_ui(request.args.to_dict()))
        app.add_url_rule('/pysys/runner', 'r_runner', view_func=lambda: self.jobexecutor.page(web.all_params()))
        app.add_url_rule('/pysys/registry', 'r_registry', view_func=lambda: self.page_registry(request.args.to_dict()))
        app.add_url_rule('/pysys/registry_show', 'r_registry_show', view_func=lambda: self.page_registry_show(request.args.to_dict()))
        app.add_url_rule('/pysys/last_job_time', 'r_last_job_time', view_func=lambda: str(self.last_job_time))
        self.web = web.route_root(app, self.getRoot())
        if run:
            self.info("Flask.run(...)")
            #app.run(host='0.0.0.0', port=int(port))
            self.web.run(app, port=port)
        return app

    def nxitems(self):
        return [{'title': "Registry", 'url': '/pysys/registry'}, {'title': "Create Job Ui", 'url': '/pysys/runner-ui'},
                {'title': "Runner", 'url': '/pysys/runner'}]

    def page_ui(self, params={}):
        p = base.Page(owner=self)
        p.h1("Runner UI")
        p.script(js_functions()+web.js_fn('add', ['name=""', 'value=""'], [
            'var $ctrls = document.getElementById("ctrls");',
            'var $d = document.createElement("div");',
            '$d.classList.add("entry");'
            '$d.innerHTML = "<input class=\\"name\\" value=\\""+name+""""\\" placeholder=\\"Key\\" /><input class=\\"value\\" value=\\""+value+""""\\" placeholder=\\"Value\\" />";'
            '$ctrls.appendChild($d);'
            ])+
            web.js_fn('run', [], [
                'var data = {};'
                'document.querySelectorAll("#ctrls .entry").forEach(function(node) {',
                '  data[node.querySelector(".name").value] = node.querySelector(".value").value;'
                '});',
                'console.log(data);',
                'exec_job(data);'
            ])
        )
        if 'type' in params:
            r = self.jobexecutor.get_runner(params['type'])
            p.div("Job for " + str(params['type']))
            p.div(r.__doc__)
            n = r.param_names
            for key in n:
                p.div(key + ': ' + n[key])
            p.script(web.js_ready('add("type", "'+params['type']+'")'))
        p.div(web.button_js("+", 'add()'), id='ctrls')
        p.div(web.button_js("Run", 'run()'))
        p.div(id='result')
        p.hr()
        p.a("PyModule", 'pymodule')
        p.a("Runner", '/pysys/runner')
        p.h2("About Runner")
        p.div("Job-Count: " + str(self.counter))
        return p.nxui()

    def page_registry(self, params={}):
        p = base.Page(owner=self)
        from importlib.metadata import entry_points
        eps = entry_points()
        p.h1("Runner Regsitry")
        if 'install' in params:
            try:
                e = eps.select(group='nweb_runner', name=params['install'])[0]
                runner = e.load()
                p.div('Runner geladen')
                #if isinstance(self.jobexecutor, LazyDispatcher):
                res = self.jobexecutor.loadRunner(e.name, runner())
                p.pre(str(res))
                #else:
                #    p.div("Invalid Runner: " +str(type(self.jobexecutor).__name__) + " Valid: LazyDispatcher")
            except ImportError as exception:
                p.div("Runner konnte nicht geladen werden. (ImportError)")
                p.div("Modul: " + str(exception.name))
                p.div(str(exception))
        parts = eps.select(group='nweb_runner')
        for name in parts.names:
            part = parts[name]
            install = web.a("Load", '?install=' + part.name)
            show = web.a("Show", '/pysys/registry_show?p_name=' + part.name)
            p.div(part.name + " = " + str(part.value) + " " + install + " " + show)
        p.hr()
        p.a("Runner", '/pysys/runner')
        return p.nxui()

    def page_registry_show(self, params={}):
        p = base.Page(owner=self)
        from importlib.metadata import entry_points
        eps = entry_points()
        try:
            part = eps.select(group='nweb_runner', name=params['p_name'])[0]
            runner = part.load()
            p.h2("Runner: " + params['name'])
            p.div(runner.__doc__)
            # TODO install
            p.div("Module: " + ','.join(getattr(runner, 'MODULES', [])))
            p.div("Constructor")
            spec = inspect.getfullargspec(runner)
            for arg in spec.args:
                if arg != 'self':
                    p.div(" - " + arg)
        except Exception as e:
            p.div("Error: " + str(e))
        return p.nxui()


    def page_results(self):
        p = base.Page()
        p.h1("Results")
        n = NWebClient(None)
        results = n.group('F954BAE7FE404ACE1A40140D66B637DC')
        for result in results.docs():
            p.div("Name: " + str(result.name()))
            p.div("Kind: " + str(result.kind()))
            if result['llm']:
                p.div("Prompt: " + str(result['prompt']))
                p.div("Response: " + str(result['response']))
            #p.div("Type: " + str(result['type']))
            #p.div("Content: " + str(result.content()))
        p.hr()
        p.div(web.a("Runner", '/pysys/runner'))
        return p.nxui()


class MultiExecutor(BaseJobExecutor):
    executors = []
    def __init__(self, *executors):
        self.executors = executors

    def execute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                exe(data)

    def canExecute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                return True
        return False


class SaveFileExecutor(BaseJobExecutor):
    filename_key = 'filename'
    content_key = 'content'

    def execute(self, data):
        with open(data[self.filename_key], 'w') as f:
            f.write(data[self.content_key])

    def canExecute(self, data):
        return 'type' in data and data['type'] == 'savefile'

    @staticmethod
    def run(data):
        r = SaveFileExecutor()
        return r(data)


class Pipeline(BaseJobExecutor):
    executors = []
    def __init__(self, *args):
        self.executors.extend(args)
        for item in self.executors:
            self.addChild(item)
    def execute(self, data):
        for item in self.executors:
            data = item(data)
        return data


class Dispatcher(BaseJobExecutor):
    key = 'type'
    runners = {}
    def __init__(self, key='type',**kwargs):
        #for key, value in kwargs.items():
        self.key = key
        self.runners = kwargs
        for item in self.runners.values():
            self.addChild(item)
    def execute(self, data):
        if self.key in data:
            runner = self.runners[data[self.key]]
            return runner(data)
        else:
            return {'success': False, 'message': "Key not in Data", 'data': data}
    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.runners
        return False


class AutoDispatcher(LazyDispatcher):
    """
       python -m nwebclient.runner --rest --mqtt --executor nwebclient.runner:AutoDispatcher
    """
    def __init__(self, key='type', **kwargs):
        super().__init__(key, **kwargs)
        self.args = util.Args()
        data = self.args.env('runners')
        if isinstance(data, dict):
            self.loadDict(data)
            self.info("Runner-Count: " + str(len(data)))
        elif len(self.classes) == 0:
            print("===================================================================================")
            self.info("Warning: No Runners configurated.")
            self.info("")
            self.info("Edit /etc/nweb.json")
            self.info("{")
            self.info("  \"runners\": {")
            self.info("      <name>: <class>,")
            self.info("      \"print\": \"nwebclient.runner:PrintJob\"")
            self.info("   }")
            self.info("}")
            list_runners()
            print("===================================================================================")


class MainExecutor(AutoDispatcher):
    """
      python -m nwebclient.runner --executor nwebclient.runner:MainExecutor --rest --mqtt
    """
    def __init__(self, **kwargs):
        super().__init__(key='type', pymodule='nwebclient.runner:PyModule')
        self.execute({'type': 'pymodule'})


class RestRunner(BaseJobExecutor):
    ssl_verify = False
    def __init__(self, url):
        self.url = url
    def execute(self, data):
        response = requests.post(self.url, data=data, verify=self.ssl_verify)
        return json.load(response.content)
    

class PrintJob(BaseJobExecutor):
    """ nwebclient.runner.PrintJob """
    def execute(self, data):
        print(json.dumps(data, indent=2))
        return data


class ImageExecutor(BaseJobExecutor):
    """

    """
    image = None
    image_key = 'image'
    def load_image(self, filename):
        with open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode('ascii')
    def image_filename(self):
        filename = 'image_executor.png'
        self.image.save(filename)
        return filename
    def get_image(self, key, data):
        """
          URL/Pfad/Base64
        """
        from PIL import Image
        if key + '_url' in data:
            response = requests.get(data[key + '_url'])
            return Image.open(BytesIO(response.content))
        elif key in data:
            if len(data[key])> 1000:
                image_data = base64.b64decode(data[key])
                return Image.open(io.BytesIO(image_data))
            elif data[key].startswith('/'):
                with open(data[key], "rb") as f:
                    return Image.open(io.BytesIO(f.read()))
            else:
                image_data = base64.b64decode(data[key])
                return Image.open(io.BytesIO(image_data))
        else:
            return None

    def read_str(self, s):
        return base64.b64decode(s)

    def is_unset_image(self, data):
        try:
            return 'unset_image' in data and self.image_key in data
        except:
            return False

    def execute(self, data):
        from PIL import Image
        if 'image_filename' in data:
            #data[self.image_key] = self.load_image(data['image_filename'])
            return self.executeImage(Image.open(data['image_filename']), data)
        if 'image_url' in data:
            response = requests.get(data['image_url'])
            self.image = Image.open(BytesIO(response.content))
            data = self.executeImage(self.image, data)
        elif self.image_key in data:
            image_data = base64.b64decode(data[self.image_key])
            self.image = Image.open(io.BytesIO(image_data))
            data = self.executeImage(self.image, data)
        elif 'file0' in data:
            self.image = Image.open(io.BytesIO(self.read_str(data['file0'])))
            data = self.executeImage(self.image, data)
        if self.is_unset_image(data):
            data.pop(self.image_key)
        return data

    def executeImage(self, image, data):
        return data
    

class NWebDocMapJob(BaseJobExecutor):
    def execute(self, data):
        # python -m nwebclient.nc --map --meta_ns ml --meta_name sexy --limit 100 --meta_value_key sexy --executor nxml.nxml.analyse:NsfwDetector --base nsfw.json
        from nwebclient import nc
        n = NWebClient(None)
        exe = util.load_class(data['executor'], create=True)
        filterArgs = data['filter']
        meta_ns = data['meta_ns']
        meta_name = data['meta_name']
        meta_value_key = data['meta_value_key']
        base  = data['base']
        dict_map = data['dict_map']
        update = data['update']
        limit = data['limit']
        fn = nc.DocMap(exe, meta_value_key, base, dict_map)
        n.mapDocMeta(meta_ns=meta_ns, meta_name=meta_name, filterArgs=filterArgs, limit=limit, update=update, mapFunction=fn)
        data['count'] = fn.count
        return data


class TickerCmd(BaseJobExecutor):
    type = 'ticker_cmd'
    def execute(self, data):
        args = data['args']
        if isinstance(args, str):
            args = args.split(' ')
        data['result'] = self.onParentClass(ticker.Cpu, lambda cpu: cpu.cmd(args))
        return data
        
        
class PyModule(BaseJobExecutor):
    """
      nwebclient.runner:PyModule
    """
    type = 'pymodule'
    def js(self):
        return super().js()
    def page_ui(self):
        p = base.Page(owner=self)
        p.h1("PyModule Executor")
        # eval_runner
        # eval_ticker
        p.div('modul.GpioExecutor(17)')
        p.input('py', id='py', placeholder='Python')
        p.input('modul', id='modul', placeholder='Module', value='nwebclient.runner')
        p += web.button_js("Add Runner", 'exec_job({type:"pymodule",modul:document.getElementById("modul").value,eval_runner:document.getElementById("py").value});')
        p += web.button_js("Add Ticker", 'exec_job({type:"pymodule",modul:document.getElementById("modul").value,eval_ticker:document.getElementById("py").value});')
        p.div('', id='result')
        p.tag('textarea', id='code', spellcheck='false')
        p += web.button_js("Exec", 'exec_job({type:"pymodule",exec:document.getElementById("code").value});')
        return p.simple_page()

    def setupRestApp(self, app):
        super().setupRestApp(app)
        route = '/pysys/pymodule'
        self.info("Route: " + route)
        app.add_url_rule(route, 'py_module', view_func=lambda: self.page_ui())
    def execute(self, data):
        if 'modul' in data:
            modul = importlib.import_module(data['modul'])
            if 'run' in data:
                exe = getattr(modul, data['run'], None)
                return exe(data)
            if 'eval_runner' in data:
                runner = eval(data['eval_runner'], globals(), {'modul': modul})
                r_type = data['new_type'] if 'new_type' in data else runner.type
                return self.owner().loadRunner(r_type, runner)
            if 'file_runner' in data:
                runner = eval(util.file_get_contents(data['file_runner']), globals(), {'modul': modul})
                r_type = data['new_type'] if 'new_type' in data else runner.type
                runner.type = r_type
                return self.owner().loadRunner(r_type, runner)
            if 'eval_ticker' in data:
                ticker = eval(data['eval_ticker'], globals(), {'modul': modul})
                self.getRoot().add(ticker)
                return {'success': True}
            if 'eval' in data:
                res = eval(data['eval'], globals(), {'modul': modul})
                return {'success': True}
        elif 'exec' in data:
            code = data['exec']
            self.info("exec:" + str(code))
            result = {}
            exec(code, globals(), {
                'owner': self,
                'result': result
            })
            return result
        elif 'file' in data:
            self.execute_file(data, data['file'])
        self.info("Module Unknown")
        return {'success': False, 'message': 'PyModule Unknown', 'request': data}

    def execute_file(self, data, file):
        with open(file, 'r') as f:
            result = {}
            exec(f.read(), globals(), {
                'owner': self,
                'result': result
            })
            return result


class PyEval(BaseJobExecutor):
    """
        Besser code.InteractiveConsole(variables) verwenden, um auch variablen definieren zu können
    """
    type = 'eval'
    def execute(self, data):
        return eval(data['eval'], globals(), {'data': data, 'runner': self.owner()})


class CmdExecutor(BaseJobExecutor):
    """
      "cmd": "nwebclient.runner:CmdExecutor",
    """
    pids = []
    type = 'cmd'
    def execute(self, data):
        if 'async' in data:
            pid = subprocess.Popen(data['cmd'], stderr=subprocess.STDOUT, shell=True)
            self.pids.append(pid)
        else:
            try:
                data['output'] = subprocess.check_output(data['cmd'])
            except Exception as e:
                data['error_source'] = "CmdExecutor"
                data['error_message'] = str(e)
                #data['output'] = str(e.output)
        return data


class ProcessExecutor(BaseJobExecutor):

    type = 'process'

    stdout = []

    restart = False
    exit_code = None

    cmd = 'uptime'
    cwd = None

    start_count = 0
    p = None

    line_listener = []
    end_listener = []

    def __init__(self, cmd=None, start=True, restart=False, cwd=None, on_line=None, on_end=None):
        super().__init__()
        if cmd is None:
            start = False
        self.var_names.append('restart')
        self.var_names.append('start_count')
        self.cmd = cmd
        self.cwd = cwd
        self.stdout = []
        self.start_count = 0
        self.restart = restart
        self.line_listener = []
        if on_line is not None:
            self.line_listener.append(on_line)
        self.end_listener = []
        if on_end is not None:
            self.end_listener.append(on_end)
        if start:
            self.start()

    def start(self):
        self.thread = Thread(target=lambda: self.loop())
        self.thread.start()
        return {'success': True, 'message': 'Process Start'}

    def loop(self):
        #print("Start ")
        self.start_count += 1
        self.info("Starting " + self.cmd)
        self.p = subprocess.Popen(self.cmd, cwd=self.cwd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.errReader = Thread(target=lambda: self.loopErr()).start()
        while self.p.poll() is None:
            self.on_new_line(self.p.stdout.readline().decode('ascii'))
        self.exit_code = self.p.returncode
        self.on_process_ended()

    def loopErr(self):
        while self.p.poll() is None:
            self.on_new_line(self.p.stderr.readline().decode('ascii'))

    def on_process_ended(self):
        self.info("Process ended.")
        for action in self.end_listener:
            action(self)
        if self.restart:
            self.start()

    def on_new_line(self, line):
        self.stdout.append(line)
        for listener in self.line_listener:
            listener(line)

    def pid(self):
        if self.p is None:
            return None
        else:
            return self.p.pid

    def kill(self):
        self.kill()
        return {'success': True}

    def is_alive(self):
        if self.p is None:
            return False
        poll = self.p.poll()
        return poll is None

    def waitForEnd(self):
        time.sleep(0.1)
        while self.is_alive():
            time.sleep(0.1)
        return self

    def lines(self):
        res = map(lambda s: s.strip(), self.stdout)
        def filter_fn(s):
            return s != ''
        return filter(filter_fn, res)

    def execute(self, data):
        data['stdout'] = '\n'.join(self.stdout)
        data['pid'] = self.pid()
        data['start_count'] = self.start_count
        if 'start' in data:
            return self.start()
        elif 'kill' in data:
            return self.kill()
        return data

    def text(self):
        return '\n'.join(self.lines())

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h2("Process " + self.cmd)
        p += web.button_js("Start", 'exec_job({type:"' + self.type + '",start:1});')
        p.pre(str('\n'.join(self.stdout)))
        return p.simple_page(params)

    
class WsExecutor(BaseJobExecutor):
    type = 'ws'
    def execute(self, data):
        from nwebclient import ws
        w = ws.Website(data['url'])
        if 'py' in data:
            data['result'] = eval(data['py'], globals(), {'w': w})
            data['success'] = True
        if 'selector' in data:
            data['result'] = w.select_text(data['selector'])
            data['success'] = True
        return data

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("Website")
        return p.nxui()

    
    
class ThreadedQueueExecutor(BaseJobExecutor):
    queue = []
    thread = None
    job_count = 0
    def __init__(self, start_thread=True):
        super().__init__()
        self.queue = []
        self.job_count = 0
        self.thread = Thread(target=lambda: self.thread_main())
        self.thread.setName(self.__threadName())
        if start_thread:
            self.thread.start()
    def __threadName(self):
        return 'ThreadedQueueExecutor'
    def thread_start(self):
        self.info("Thread begin")
    def thread_main(self):
        self.info("Thread started")
        self.thread_start()
        while True:
            try:
                self.thread_tick()
            except Exception as e:
                self.error(str(e))
                traceback.print_exc()

    def thread_tick(self):
        try:
            if not len(self.queue) == 0:
                print("In Thread Job Tick")
                first = self.queue[0]
                self.queue.remove(first)
                self.thread_execute(first)
                self.job_count += 1
                if len(self.queue) == 0:
                    self.thread_queue_empty()
        except Exception as e:
            self.error("Exception: " + str(e))
    def thread_execute(self, data):
        pass

    def thread_queue_empty(self):
        pass

    def is_busy(self):
        return len(self.queue) > 0
    def execute(self, data):
        if 'start_thread' in data:
            self.thread.start()
            return {'success': True}
        elif 'queue' in data:
            self.queue.append(data)
        else:
            return super().execute(data)


class SerialExecutor(ThreadedQueueExecutor):
    """
      python -m nwebclient.runner --executor nwebclient.runner:SerialExecutor --rest --mqtt

      Connect:
        curl -X GET "http://192.168.178.79:8080/?port=/dev/ttyS0"
        curl -X GET "http://192.168.178.79:8080/?start_thread=true"
        curl -X GET "http://192.168.178.79:8080/?send=Hallo"
        curl -X GET "http://192.168.178.79:8080/?enable=rs485"
        curl -X POST https://reqbin.com/ -H "Content-Type: application/x-www-form-urlencoded"  -d "param1=value1&param2=value2"

    """
    MODULES = ['pyserial']
    type = 'serial'
    #port = '/dev/ttyUSB0'
    # S0
    port = '/dev/ttyAMA0'
    baudrate = 9600
    serial = None
    send = None
    buffer = ''
    buffer_size = 0
    rs485 = False
    send_pin = 17 #S3
    gpio = None
    line_listener = []

    def __init__(self, start_thread=False, port=None, baudrate=None):
        super().__init__(start_thread=start_thread)
        self.line_listener = []
        self.param_names['send'] = "Sendet Daten über den Serial Port (Alias: print)"
        self.param_names['port'] = ""
        self.param_names['info'] = ""
        self.param_names['getbuffer'] = ""
        self.param_names['readbuffer'] = "Gibt den Inhalt zurueck und löscht den Buffer"
        self.param_names['enable'] = ""
        self.var_names.append('port')
        self.var_names.append('baudrate')
        self.var_names.append('rs485')
        self.var_names.append('send_pin')
        self.var_names.append('buffer_size')
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate

    @property
    def port_name(self):
        return self.port.split('/')[-1]

    def _sendData(self):
        if self.send is not None:
            if self.rs485:
                self.gpio.output(self.send_pin, True)
            self.serial.write((self.send + "\n").encode())
            self.send = None
            if self.rs485:
                self.gpio.output(self.send_pin, False)
    def thread_tick(self):
        self._sendData()
        line = self.serial.readline()
        if line != -1:
            line_str = line.decode('utf8') # UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128)
            self.info(line_str)
            self.on_line(line_str)
            self.buffer += line_str + "\n"
            self.buffer_size = len(self.buffer)

    def on_line(self, line):
        for listener in self.line_listener:
            listener(line)

    def thread_start(self):
        import serial
        #from serial.tools import list_ports
        # https://github.com/ShyBoy233/PyGcodeSender/blob/main/pyGcodeSender.py
        self.info("Connect to " + self.port)
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.on_conected()
        except Exception as e:
            self.error("Connection failed. " + str(e))

    def on_conected(self):
        self.info("Connected.")

    def enableRs485(self, data):
        import RPi.GPIO as GPIO
        # sudo apt-get install python-rpi.gpio
        if 'pin' in data:
            self.send_pin = int(data['pin'])
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.send_pin, GPIO.OUT)
        GPIO.output(self.send_pin, False)
        self.gpio = GPIO
        self.rs485 = True
        return {'success': self.rs485, 'pin': self.send_pin, 'mode': 'BCM'}

    def read_buffer(self):
        buf = self.buffer
        self.buffer = ''
        return {'buffer': buf}

    def execute(self, data):
        if 'send' in data:
            self.send = data['send']
            return {'success': True, 'result': 'queued'}
        if 'print' in data:
            self.send = data['print']
            self._sendData()
            return {'success': True, 'result': 'sended'}
        elif 'port' in data:
            self.port = data['port']
            return {'success': True}
        elif 'baud' in data:
            self.baudrate = int(data['baud'])
            return {'success': True}
        elif 'info' in data:
            return {'baud': self.baudrate, 'port': self.port}
        elif 'getbuffer' in data:
            return {'buffer': self.buffer}
        elif 'readbuffer' in data:
            return self.read_buffer()
        elif 'enable' in data and data['enable'] == 'rs485':
            return self.enableRs485(data)
        else:
            return super().execute(data)

    def list_ports(self):
        import serial.tools.list_ports as t
        ports = t.comports()
        res = []
        for p in ports:
            res.append(p.name) # p.dev
        return res

    def page_ctrl(self):
        p = base.Page(owner=self)
        p.h1("Serial Executor")
        self.write_to(p)
        p.div(f'Buffer: <span id="buffer_size">{self.buffer_size}</span>')
        p.js_ready(f'observe_value("{self.type}", "buffer_size", "#buffer_size");');
        p.div(f"RS485-Pin: {self.send_pin}")
        p.div("Ports: " + str(self.list_ports()))
        p += web.button_js("Connect", 'exec_job({type:"serial",start_thread:true});')
        p += web.button_js("Enable RS485", 'exec_job({type:"serial",enable:"rs485"});')
        p += web.button_js("Send", 'exec_job({type:"serial",send:"Hallo"});')
        p += web.button_js("Info", 'exec_job({type:"serial",info:1});')
        p += web.button_js("Get Buffer", 'exec_job({type:"serial",getbuffer:1});')
        p += web.input('baudrate', value='9600', id='baudrate')
        p += web.button_js("Set Baud", 'exec_job_p({type:"serial",baud:"#baudrate"});')
        p += web.input('port', value='/dev/serial0', id='port')
        p += web.button_js("Set Port", 'exec_job_p({type:"serial",port:"#port"});')
        p += web.button_js("ttyS0", 'exec_job({type:"serial",port:"/dev/ttyS0"});')
        p += web.button_js("ttyUSB0", 'exec_job({type:"serial",port:"/dev/ttyUSB0"});')

        p.div('', id='result')
        p.hr()
        p += web.input('data', value='Hallo Welt', id='data')
        p += web.button_js("Send", 'exec_job_p({type:"serial",print:"#data"});')
        p.hr()
        p.div(web.a("Runner", '/pysys/runner'))
        p.hr()
        p.div("Baudrate: 9600, 14400, 19200, 115200, 250000")
        return p.nxui()

    def write_to(self, p: base.Page, summary=False):
        c = "False" if self.serial is None else f"True (Buffer:{len(self.buffer)})"
        p.div(f"Connected: {c}")
        p.div(f"Port: {self.port}")
        p.div(f"Baudrate: {self.baudrate}")
        if summary is True:
            p.right(web.a("Open", f'/pysys/{self.type}_ctrl'))

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule(f'/pysys/{self.type}_ctrl', self.type+'_ctrl', view_func=lambda: self.page_ctrl())

    def page(self, params={}):
        # link to action
        return self.page_ctrl()


class GCodeExecutor(ThreadedQueueExecutor):
    """
      python -m nwebclient.runner --executor nwebclient.runner:GCodeExecutor --rest

      git -C ~/nwebclient/ pull && pip3 install ~/nwebclient/ && python3 -m nwebclient.runner --executor nwebclient.runner:GCodeExecutor --rest

      
      UI: http://127.0.0.1:8080/runner
    """
    MODULES = ['pyserial']
    type = 'gcode'
    port = '/dev/ttyUSB0'
    # 250000
    baudrate = 250000
    serial = None
    timeout_count = 0
    log = None
    mqtt_topic = 'main'
    posAbs = None
    steppers = None
    last_command = 0
    pos = None

    def __init__(self, start_thread=False, args: util.Args = None):
        super().__init__(start_thread=start_thread)
        self.timeout_count = 0
        self.args = util.Args() if args is None else args
        self.steppers = None
        self.baudrate = args.get(self.type + '_baud', 115200)
        self.pos = machine.Instruction('G0')
        self.initMqtt()
        self.param_names['gcode'] = "Execute GCode"
        self.param_names['connect'] = "Verbinden"
        self.var_names.append('port')
        self.var_names.append('baudrate')
        self.var_names.append('speed')
        self.var_names.append('lenkung')
        self.var_names.append('interval')
        self.var_names.append('robo_f')

    def initMqtt(self):
        mqtt_host = self.args.env('MQTT_HOST')
        if mqtt_host is not None: 
            self.log = ticker.MqttPub(host=mqtt_host)
            self.log(self.mqtt_topic, '__init__')
    def __len__(self):
        return len(self.queue)
    def prn(self, msg):
        print(msg)
        if self.log is not None:
            self.log(self.mqtt_topic, msg)

    def thread_start(self):
        import serial
        #from serial.tools import list_ports
        # https://github.com/ShyBoy233/PyGcodeSender/blob/main/pyGcodeSender.py
        self.info("Connect to " + self.port)
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.info("Connected.")
        except Exception as e:
            self.error("Connection faild. " + str(e))

    def thread_execute(self, data):
        if 'gcode' in data:
            self.execGCode(data['gcode'])

    def thread_queue_empty(self):
        self.info("Queue is empty.")

    def processOnOff(self, gcode, on_start, off_start, state):
        if gcode.startswith(on_start):
            return True
        elif gcode.startswith(off_start):
            return False
        else:
            return state

    def processGCode(self, gcode):
        try:
            self.last_command = time.time()
            self.steppers = self.processOnOff(gcode, 'M17', 'M18', self.posAbs)
            self.posAbs = self.processOnOff(gcode, 'M82', 'M83', self.posAbs)
            if gcode.startswith('G0') or gcode.startswith('G1'):
                if self.posAbs is False:
                    pass # add pos
                if self.posAbs is True:
                    self.pos.update_pos(gcode)
            elif gcode.startswith('G92'):
                self.pos = machine.Instruction('G0 X0 Y0 Z0')
        except Exception as e:
            self.error("Error in processGCode")
            self.error(e)


    def execGCode(self, gcode):
        if gcode.strip().startswith(';') or gcode.isspace() or len(gcode) <= 0:
            return
        self.info("Exec G-Code: " + gcode)
        self.processGCode(gcode)
        self.serial.write((gcode+'\n').encode())
        while 1: # Wait untile the former gcode has been completed.
            try:
                line = self.serial.readline()
                self.info("Response: " + line.decode('ascii'))
                if line.startswith(b'ok'):
                    break
                self.timeout_count += 1
                # print("readline timeout")
            except Exception as e:
                self.error("Error in execGCode")
                self.error(e)
                break
    def is_connected(self):
        return self.serial is not None
    def queueGCode(self, gcode):
        self.queue.append({'gcode': gcode})
    def moveX(self, val = 10):
        self.queueGCode('G0 X'+str(val))
    def moveY(self, val = 10):
        self.queueGCode('G0 Y'+str(val))
    def moveZ(self, val = 10):
        self.queueGCode('G0 Z'+str(val))
    def heatBed(self, temp):
        self.queueGCode('M190 S'+str(temp)) # M140 for without wait
    def heatE0(self, temp):
        self.queueGCode('M109 T0 S'+str(temp)) # M104
    # G92 X0 Y0 Z0 ; Set Home
    def __repr__(self):
        return "GCode(queue({0}),thread, port:{1} count:{2})".format(len(self), self.port, self.job_count)
    def moveControls(self):
        return """
          <table>
            <tr>
              <td></td>
              <td><a href="?gcode=G1%20Y10">Y+</a></td>
              <td></td>
              <td><a href="?gcode=G1%20Z10">Z+</a></td>
            </tr>
            <tr>
              <td><a href="?gcode=G1%20X-10">X-</a></td>
              <td></td>
              <td><a href="?gcode=G1%20X10">X+</a></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td><a href="?gcode=G1%20Y-10">Y-</a></td>
              <td></td>
              <td><a href="?gcode=G1%20Z-10">Z-</a></td>
            </tr>
          <table>
          <div>
            <a href="?gcode=M109%20T0%20S205">Heat E0 205</a>
            <a href="?gcode=M190%20S60">Heat Bed 60</a>
            <a href="?gcode=G1%20E5">Extrude</a>
            <a href="?gcode=G92%20X0%20Y0%20Z0">Set Home</a>
            <a href="?a=connect">Connect</a>
          </div>
          <div>
            Einstellungen:
            <a href="?gcode=M17">M17 Steppers On</a><br />
            <a href="?gcode=M18">M18 Steppers Off</a><br />
            <a href="?gcode=M82">M82 E Absolute Pos</a><br />
            <a href="?gcode=M83">M83 E Relativ Pos</a><br />
            <a href="?gcode=M92%20E10%20X10%20Y10%20Z50">M92 Steps per Unit</a><br />
            <a href="?gcode=G90">G90 Absolute Pos</a><br />
            <a href="?gcode=G91">G91 Relativ Pos</a><br />
            <a href="?gcode=G92%20X0%20Y0%20Z0">G92 Set Home here</a><br />
            <a href="?gcode=M121">M121 Disable Endstops</a><br />
            <a href="?gcode=M204%20T10">M204 Setze Beschleunigung</a><br />
            GCode: """ + str(self.args.env('GCODE_PATH')) + """
          </div>
          <button id="btnFocus">Tastatur</button>
        """
    def gcodes(self):
        path = self.args.env('GCODE_PATH')
        if path is None:
            path = '.'
        files = [f for f in os.listdir(path) if os.path.isfile(path+'/'+f)]
        html = ''
        for f in files:
            html += '<li><a href="?file='+str(f)+'">'+str(f)+'</a></li>'
        return '<div><span title="'+path+'">GCodes:</span><br /><ul>'+html+'</ul></div>'
    def queueFile(self, file):
        path = self.args.env('GCODE_PATH')
        if path is None:
            path = '.'
        f = path + '/' + file
        with open(f, 'r') as fh:
            for line in fh.readlines():
                self.queueGCode(line)
    def handleActions(self, params):
        try:
            if 'gcode' in params:
                self.queue.append(params)
            if 'a' in params and params['a'] == 'connect':
                self.execute({'connect': 1})
            if 'a' in params and 'port' in params and params['a'] == 'set_port':
                self.port = params['port']
            if 'a' in params and 'baudrate' in params and params['a'] == 'set_baudrate':
                self.port = params['baudrate']
            if 'file' in params:
                self.queueFile(params['file'])
        except Exception as e:
            return "Error: " + str(e)
        return ""
    def js(self):
        return super().js() + """
         $(function() {
               function gcode(code) {
                 console.log(code);
                 $.get('?gcode='+encodeURI(code));
               };
               $('#btnFocus').click(function() {
                $(document).bind('keydown', function (evt) {
                    console.log(evt.keyCode);
                    switch (evt.keyCode) {
                        case 40: // Pfeiltaste nach unten
                        case 98: // Numpad-2
                            gcode('G0 Y-1');
                            return false; break;
                        case 38: // nach oben
                        case 104: // Numpad-8
                            gcode('G0 Y1');
                            return false; break;
                        case 37: // Pfeiltaste nach links
                        case 100: // Numpad-4
                            gcode('G0 X-1');
                            return false; break;
                        case 39: 
                        case 102: // NumPad-6
                            gcode('G0 X1');
                            return false; break;
                        // w=87
                        // S=83
                        // NumPad+ = 107
                        // NumPad- = 109
                    }		
                });
               });
            });
        """
    def page(self, params):
        p = base.Page()
        p += '<script src="https://bsnx.net/4.0/templates/sb-admin-4/vendor/jquery/jquery.min.js"></script>'
        p += '<script>'+self.js()+'</script>'
        p += self.handleActions(params) + self.__repr__() + self.moveControls() + self.gcodes()
        return p.simple_page()

    def connect(self, data={}):
        self.thread.start()
        if 'port' in data:
            self.port = data['port']
        return {'success': True, 'result': 'connected'}

    def param_maxqueue(self, data):
        return (not 'maxqueue' in data) or (int(data['maxqueue']) < len(self.queue))

    def executeGCode(self, data):
        if 'clear' in data:
            self.queue = []
        self.queueGCode(data['gcode'])
        return {'success': True, 'result': 'gcode queued.'}

    def executeGCodes(self, data):
        if 'clear' in data:
            self.queue = []
        if isinstance(data['gcodes'], str):
            for gcode in data['gcodes'].split(','):
                self.queueGCode(gcode)
        else:
            for gcode in data['gcodes']:
                self.queueGCode(gcode)
        return {'success': True, 'result': 'gcode queued.'}

    def execute(self, data):
        if 'gcode' in data and self.param_maxqueue(data):
            return self.executeGCode(data)
        elif 'gcodes' in data and self.param_maxqueue(data):
            return self.executeGCodes(data)
        elif 'connect' in data:
            return self.connect(data)
        else:
            return super().execute(data)

    def setupRestApp(self, app):
        from flask import request
        super().setupRestApp(app)
        app.add_url_rule('/pysys/gcode', 'gcode', view_func=lambda: self.page(request.args))
        app.add_url_rule('/pysys/robot', 'robot', view_func=lambda: self.page_robot())
        app.add_url_rule('/pysys/gsetup', 'gsetup', view_func=lambda: self.page_setup())

    def btn_gcode(self, title, gcode):
        return web.button_js(title, 'exec_job({"type":"gcode", "gcode": "'+gcode+'"});')

    def btn_gcodes(self, title, gcodes):
        gcodes = map(lambda gcode: '"'+gcode+'"', gcodes)
        return web.button_js(title, 'exec_job({"type":"gcode", "gcodes": ['+','.join(gcodes)+']});')

    def joystick(self):
        # /static/js/joystick/joystick.js
        return """
/* Name          : joy.js
 * @author       : Roberto D'Amico (Bobboteck)
 * Last modified : 09.06.2020
 * Revision      : 1.1.6
 * URL           : https://github.com/bobboteck/JoyStick 
 */

let StickStatus = { xPosition: 0, yPosition: 0, x: 0, y: 0, cardinalDirection: "C"};

/**
 * @desc Principal object that draw a joystick, you only need to initialize the object and suggest the HTML container
 * @costructor
 * @param container {String} - HTML object that contains the Joystick
 * @param parameters (optional) - object with following keys:
 *  title {String} (optional) - The ID of canvas (Default value is 'joystick')
 *  width {Int} (optional) - The width of canvas, if not specified is setted at width of container object (Default value is the width of container object)
 *  height {Int} (optional) - The height of canvas, if not specified is setted at height of container object (Default value is the height of container object)
 *  internalFillColor {String} (optional) - Internal color of Stick (Default value is '#00AA00')
 *  internalLineWidth {Int} (optional) - Border width of Stick (Default value is 2)
 *  internalStrokeColor {String}(optional) - Border color of Stick (Default value is '#003300')
 *  externalLineWidth {Int} (optional) - External reference circonference width (Default value is 2)
 *  externalStrokeColor {String} (optional) - External reference circonference color (Default value is '#008000')
 *  autoReturnToCenter {Bool} (optional) - Sets the behavior of the stick, whether or not, it should return to zero position when released (Default value is True and return to zero)
 * @param callback {StickStatus} - 
 */
var JoyStick = (function(container, parameters, callback) {
    parameters = parameters || {};
    var title = (typeof parameters.title === "undefined" ? "joystick" : parameters.title),
        width = (typeof parameters.width === "undefined" ? 0 : parameters.width),
        height = (typeof parameters.height === "undefined" ? 0 : parameters.height),
        internalFillColor = (typeof parameters.internalFillColor === "undefined" ? "#00AA00" : parameters.internalFillColor),
        internalLineWidth = (typeof parameters.internalLineWidth === "undefined" ? 2 : parameters.internalLineWidth),
        internalStrokeColor = (typeof parameters.internalStrokeColor === "undefined" ? "#003300" : parameters.internalStrokeColor),
        externalLineWidth = (typeof parameters.externalLineWidth === "undefined" ? 2 : parameters.externalLineWidth),
        externalStrokeColor = (typeof parameters.externalStrokeColor ===  "undefined" ? "#008000" : parameters.externalStrokeColor),
        autoReturnToCenter = (typeof parameters.autoReturnToCenter === "undefined" ? true : parameters.autoReturnToCenter);

    callback = callback || function(StickStatus) {};

    // Create Canvas element and add it in the Container object
    var objContainer = document.getElementById(container);
    
    // Fixing Unable to preventDefault inside passive event listener due to target being treated as passive in Chrome [Thanks to https://github.com/artisticfox8 for this suggestion]
    objContainer.style.touchAction = "none";

    var canvas = document.createElement("canvas");
    canvas.id = title;
    if(width === 0) { width = objContainer.clientWidth; }
    if(height === 0) { height = objContainer.clientHeight; }
    canvas.width = width;
    canvas.height = height;
    objContainer.appendChild(canvas);
    var context=canvas.getContext("2d");

    var pressed = 0; // Bool - 1=Yes - 0=No
    var circumference = 2 * Math.PI;
    var internalRadius = (canvas.width-((canvas.width/2)+10))/2;
    var maxMoveStick = internalRadius + 5;
    var externalRadius = internalRadius + 30;
    var centerX = canvas.width / 2;
    var centerY = canvas.height / 2;
    var directionHorizontalLimitPos = canvas.width / 10;
    var directionHorizontalLimitNeg = directionHorizontalLimitPos * -1;
    var directionVerticalLimitPos = canvas.height / 10;
    var directionVerticalLimitNeg = directionVerticalLimitPos * -1;
    // Used to save current position of stick
    var movedX=centerX;
    var movedY=centerY;

    // Check if the device support the touch or not
    if("ontouchstart" in document.documentElement) {
        canvas.addEventListener("touchstart", onTouchStart, false);
        document.addEventListener("touchmove", onTouchMove, false);
        document.addEventListener("touchend", onTouchEnd, false);
    } else {
        canvas.addEventListener("mousedown", onMouseDown, false);
        document.addEventListener("mousemove", onMouseMove, false);
        document.addEventListener("mouseup", onMouseUp, false);
    }
    // Draw the object
    drawExternal();
    drawInternal();

    /******************************************************
     * Private methods
     *****************************************************/

    /**
     * @desc Draw the external circle used as reference position
     */
    function drawExternal() {
        context.beginPath();
        context.arc(centerX, centerY, externalRadius, 0, circumference, false);
        context.lineWidth = externalLineWidth;
        context.strokeStyle = externalStrokeColor;
        context.stroke();
    }

    /**
     * @desc Draw the internal stick in the current position the user have moved it
     */
    function drawInternal() {
        context.beginPath();
        if(movedX<internalRadius) { movedX=maxMoveStick; }
        if((movedX+internalRadius) > canvas.width) { movedX = canvas.width-(maxMoveStick); }
        if(movedY<internalRadius) { movedY=maxMoveStick; }
        if((movedY+internalRadius) > canvas.height) { movedY = canvas.height-(maxMoveStick); }
        context.arc(movedX, movedY, internalRadius, 0, circumference, false);
        // create radial gradient
        var grd = context.createRadialGradient(centerX, centerY, 5, centerX, centerY, 200);
        // Light color
        grd.addColorStop(0, internalFillColor);
        // Dark color
        grd.addColorStop(1, internalStrokeColor);
        context.fillStyle = grd;
        context.fill();
        context.lineWidth = internalLineWidth;
        context.strokeStyle = internalStrokeColor;
        context.stroke();
    }

    /**
     * @desc Events for manage touch
     */
    let touchId = null;
    function onTouchStart(event) {
        pressed = 1;
        touchId = event.targetTouches[0].identifier;
    }

    function onTouchMove(event) {
        if(pressed === 1 && event.targetTouches[0].target === canvas) {
            movedX = event.targetTouches[0].pageX;
            movedY = event.targetTouches[0].pageY;
            // Manage offset
            if(canvas.offsetParent.tagName.toUpperCase() === "BODY") {
                movedX -= canvas.offsetLeft;
                movedY -= canvas.offsetTop;
            } else {
                movedX -= canvas.offsetParent.offsetLeft;
                movedY -= canvas.offsetParent.offsetTop;
            }
            // Delete canvas
            context.clearRect(0, 0, canvas.width, canvas.height);
            // Redraw object
            drawExternal();
            drawInternal();
            // Set attribute of callback
            StickStatus.xPosition = movedX;
            StickStatus.yPosition = movedY;
            StickStatus.x = (100*((movedX - centerX)/maxMoveStick)).toFixed();
            StickStatus.y = ((100*((movedY - centerY)/maxMoveStick))*-1).toFixed();
            StickStatus.cardinalDirection = getCardinalDirection();
            callback(StickStatus);
        }
    }

    function onTouchEnd(event) {
        if (event.changedTouches[0].identifier !== touchId) return;
        pressed = 0;
        // If required reset position store variable
        if(autoReturnToCenter) {
            movedX = centerX;
            movedY = centerY;
        }
        // Delete canvas
        context.clearRect(0, 0, canvas.width, canvas.height);
        // Redraw object
        drawExternal();
        drawInternal();
        // Set attribute of callback
        StickStatus.xPosition = movedX;
        StickStatus.yPosition = movedY;
        StickStatus.x = (100*((movedX - centerX)/maxMoveStick)).toFixed();
        StickStatus.y = ((100*((movedY - centerY)/maxMoveStick))*-1).toFixed();
        StickStatus.cardinalDirection = getCardinalDirection();
        callback(StickStatus);
    }

    /**
     * @desc Events for manage mouse
     */
    function onMouseDown(event) {
        pressed = 1;
    }

    /* To simplify this code there was a new experimental feature here: https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/offsetX , but it present only in Mouse case not metod presents in Touch case :-( */
    function onMouseMove(event) {
        if(pressed === 1) {
            movedX = event.pageX;
            movedY = event.pageY;
            // Manage offset
            if(canvas.offsetParent.tagName.toUpperCase() === "BODY") {
                movedX -= canvas.offsetLeft;
                movedY -= canvas.offsetTop;
            } else {
                movedX -= canvas.offsetParent.offsetLeft;
                movedY -= canvas.offsetParent.offsetTop;
            }
            // Delete canvas
            context.clearRect(0, 0, canvas.width, canvas.height);
            // Redraw object
            drawExternal();
            drawInternal();

            // Set attribute of callback
            StickStatus.xPosition = movedX;
            StickStatus.yPosition = movedY;
            StickStatus.x = (100*((movedX - centerX)/maxMoveStick)).toFixed();
            StickStatus.y = ((100*((movedY - centerY)/maxMoveStick))*-1).toFixed();
            StickStatus.cardinalDirection = getCardinalDirection();
            callback(StickStatus);
        }
    }

    function onMouseUp(event) {
        pressed = 0;
        // If required reset position store variable
        if(autoReturnToCenter)
        {
            movedX = centerX;
            movedY = centerY;
        }
        // Delete canvas
        context.clearRect(0, 0, canvas.width, canvas.height);
        // Redraw object
        drawExternal();
        drawInternal();
        // Set attribute of callback
        StickStatus.xPosition = movedX;
        StickStatus.yPosition = movedY;
        StickStatus.x = (100*((movedX - centerX)/maxMoveStick)).toFixed();
        StickStatus.y = ((100*((movedY - centerY)/maxMoveStick))*-1).toFixed();
        StickStatus.cardinalDirection = getCardinalDirection();
        callback(StickStatus);
    }

    function getCardinalDirection() {
        let result = "";
        let orizontal = movedX - centerX;
        let vertical = movedY - centerY;
        
        if(vertical >= directionVerticalLimitNeg && vertical <= directionVerticalLimitPos) {
            result = "C";
        }
        if(vertical < directionVerticalLimitNeg) {
            result = "N";
        }
        if(vertical > directionVerticalLimitPos) {
            result = "S";
        }
        if(orizontal < directionHorizontalLimitNeg) {
            if(result === "C") { 
                result = "W";
            } else {
                result += "W";
            }
        }
        if(orizontal > directionHorizontalLimitPos) {
            if(result === "C") { 
                result = "E";
            } else {
                result += "E";
            }
        }
        return result;
    }

    /******************************************************
     * Public methods
     *****************************************************/

    /**
     * @desc The width of canvas
     * @return Number of pixel width 
     */
    this.GetWidth = function () {
        return canvas.width;
    };

    /**
     * @desc The height of canvas
     * @return Number of pixel height
     */
    this.GetHeight = function () {
        return canvas.height;
    };

    /**
     * @desc The X position of the cursor relative to the canvas that contains it and to its dimensions
     * @return Number that indicate relative position
     */
    this.GetPosX = function () {
        return movedX;
    };

    /**
     * @desc The Y position of the cursor relative to the canvas that contains it and to its dimensions
     * @return Number that indicate relative position
     */
    this.GetPosY = function () {
        return movedY;
    };

    /**
     * @desc Normalizzed value of X move of stick
     * @return Integer from -100 to +100
     */
    this.GetX = function () {
        return (100*((movedX - centerX)/maxMoveStick)).toFixed();
    };

    /**
     * @desc Normalizzed value of Y move of stick
     * @return Integer from -100 to +100
     */
    this.GetY = function () {
        return ((100*((movedY - centerY)/maxMoveStick))*-1).toFixed();
    };

    /**
     * @desc Get the direction of the cursor as a string that indicates the cardinal points where this is oriented
     * @return String of cardinal point N, NE, E, SE, S, SW, W, NW and C when it is placed in the center
     */
    this.GetDir = function() {
        return getCardinalDirection();
    };
});  
"""

    speed = 12
    lenkung = 6
    interval = 1100
    robo_f = 900

    def page_robot(self):
        if not self.is_connected():
            self.connect()
        p = base.Page(owner=self)
        p += '<script src="https://bsnx.net/4.0/templates/sb-admin-4/vendor/jquery/jquery.min.js"></script>'
        if self.posAbs is False:
            p.right("Relative Positioning activ")
        if self.is_connected():
            p.right("Verbunden", title="Baud: " + str(self.baudrate))
        g_vor = f'G0 X{self.speed} Y{self.speed} F{self.robo_f}'
        g_left = f'G0 X{(self.speed+self.lenkung)} Y0 F{self.robo_f}'
        g_left_b = f'G0 X{self.speed} Y{-self.speed} F{self.robo_f}'
        g_right = f'G0 X0 Y{(self.speed+self.lenkung)} F' + str(self.robo_f)
        g_right_b = f'G0 X{-self.speed} Y{self.speed} F{self.robo_f}'
        g_back = 'G0 X' + str(-self.speed) + ' Y' + str(-self.speed) + ' F' + str(self.robo_f)
        h = 'G92 X0 Y0'
        left = self.btn_gcodes("Links", [g_left, h])
        left_b = self.btn_gcodes("Links", [g_left_b, h])
        vor = self.btn_gcodes("Vor", [g_vor, h])
        right = self.btn_gcodes("Rechts", [g_right, h])
        right_b = self.btn_gcodes("Rechts", [g_right_b, h])
        back = self.btn_gcodes("Zurück", [g_back, h])
        p += web.table([
            [left,   vor,  right],
            [left_b, back, right_b]
        ])
        # Joystick von Dir NW N NE, In der Mitte is C
        p.div('', id='result')
        p.div('', id='joystick', style="width:200px;height:200px;margin:50px;position:fixed;bottom:30px;left:30px;")
        p.script(self.joystick())
        p.script(web.js_ready('var joy = new JoyStick("joystick"); \n' +
            'setInterval(function(){ '+
                'if (joy.GetDir()=="N") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["'+g_vor+'", "G92 X0 Y0"]}); }'+
                'if (joy.GetDir()=="NW") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["'+g_left+'", "G92 X0 Y0"]}); }' +
                'if (joy.GetDir()=="NE") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["'+g_right+'", "G92 X0 Y0"]}); }' +
                'if (joy.GetDir()=="S") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["' + g_back + '", "G92 X0 Y0"]}); }' +
            '}, '+str(self.interval)+');'))
        for v in self.var_names:
            p.div(v+": " + str(getattr(self, v, '')))
        p.hr()
        p += web.input('robo_f', value=self.robo_f, id='robo_f')
        p += web.button_js("Set F", 'exec_job_p({type:"'+self.type+'",setvar:"robo_f", value:"#robo_f"});')
        p += web.input('speed', value=self.speed, id='speed')
        p += web.button_js("Set speed", 'exec_job_p({type:"' + self.type + '",setvar:"speed", value:"#speed"});')
        p += web.input('interval', value=self.interval, id='interval')
        p += web.button_js("Set interval", 'exec_job_p({type:"' + self.type + '",setvar:"interval", value:"#interval"});')
        p += web.button_js("Steppers On", 'exec_job({type:"' + self.type + '",gcode:"M17"});')
        p += web.button_js("Steppers Off", 'exec_job({type:"' + self.type + '",gcode:"M18"});')
        p += web.button_js("X-", 'exec_job({type:"' + self.type + '",gcodes:["M17", "G92 X0", "'+f'G0 X-{self.speed} F{self.robo_f}'+'", "M18"]});')
        p += web.button_js("X+", 'exec_job({type:"' + self.type + '",gcodes:["M17", "G92 X0", "'+f'G0 X{self.speed} F{self.robo_f}'+'", "M18"]});')

        return p.simple_page()

    def page_setup(self):
        p = base.Page(owner=self)
        # TODO ls /dev | grep ttyUSB
        return p.simple_page()

    def write_to(self, p: base.Page, summary=False):
        p.div(web.a("Roboter", '/pysys/robot'))


class MqttLastMessages(BaseJobExecutor):

    type = 'lastmessages'
    client_id = 'MqttLastMessages'
    port = 1883

    def __init__(self, host='127.0.0.1', topic='main', maxsize=50):
        super().__init__()
        from queue import Queue
        self.queue = Queue(maxsize=maxsize)
        self.topic = topic
        self.host = host
        self.connect()

    def connect(self):
        from paho.mqtt import client as mqtt_client
        print("[MqttSub] Connect to " + self.host + " Topic: " + self.topic)
        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id, transport='tcp')

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker!")
                client.subscribe(self.topic)
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.queue.put(msg.payload.decode())

        client.on_connect = on_connect
        client.on_message = on_message
        client.connect_async(self.host, self.port, keepalive=6000)
        client.loop_start()

    def items(self):
        result_list = []
        while not self.queue.empty():
            result_list.append(str(self.queue.get()))
        for item in result_list:
            self.queue.put(item)
        return result_list

    def ips(self):
        res = set()
        for line in self.items():
            if line.startswith('nxudp'):
                a = line.split(' ')
                res.add(a[2]) # name:a[1]
        return list(res)

    def value(self, name):
        res = set()
        for line in self.items():
            n = name+':'
            if line.startswith(n):
                a = line[len(n):]
                res.add(a.strip())
        return res

    def execute(self, data):
        res = {}
        if 'guid' in data:
            res['guid'] = data['guid']
        if 'ips' in data:
            res['ips'] = self.ips()
        if 'var' in data:
            res['value'] = self.value(data['var'])
        else:
            res['items'] = list(self.items())
        return res

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("MqttLastMessages")
        opts = {'title': 'MqttLastMessages'}
        for item in self.items():
            p.div(item)
        return p.nxui(opts)


class MqttSend(BaseJobExecutor):

    type = 'mqttsend'
    client_id = 'MqttSend'
    port = 1883
    topic = 'main'
    host = '127.0.0.1'

    def __init__(self, host=None, topic=None, args: util.Args = {}):
        self.param_names['topic'] = 'MQTT-Topic an das gesendet wird, optional'
        self.param_names['message'] = ''
        if args is not None:
            self.host = args.get('MQTT_HOST', self.host)
            self.port = args.get('MQTT_PORT', self.port)
        if topic is not None:
            self.topic = topic
        if host is not None:
            self.host = host
        self.connect()

    def connect(self):
        from paho.mqtt import client as mqtt_client
        print("[MqttSend] Connect to " + self.host + " Topic: " + self.topic)
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id, transport='tcp')

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker for sending")
                #client.subscribe(self.topic)
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            pass

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect_async(self.host, self.port, keepalive=6000)
        self.client.loop_start()

    def execute(self, data):
        topic = self.topic
        if 'topic' in data:
            topic = data['topic']
        if 'message' in data:
            self.client.publish(topic, data['message'])
            return {'success': True, 'message': 'From MQTT-Send'}
        else:
            return super().execute(data)


class ProxyRunner(BaseJobExecutor):
    """

    """ 
    def __init__(self, pre_cmd=None, runner=None, runner_install=False, url=None, runner_cmd=None):
        super().__init__()
        if pre_cmd is not None:
            os.system(pre_cmd)
        if runner is not None:
            self._start_runner(runner, runner_install)
        elif url is not None:
            self.url = url
        elif runner_cmd is not None:
            self._start_runner_cmd(runner_cmd)
        else:
            self.error("No Runner defined")
            self.error("    runner = nwebclient.runner:SerialExecutor")
            self.error("    url = http://192.168.178.2")
            self.error("    runner_cmd = docker run -p {port}:7070 --rm -it nxml")
            self.error("")

    def _start_runner_cmd(self, cmd):
        p = util.find_free_port()
        c = cmd.replace('{port}', str(p))
        self.info("Process: " + c)
        self.process = ProcessExecutor(c, start=True)
        self.url = 'http://127.0.0.1:' + str(p) + '/'

    def _start_runner(self, runner, runner_install=True):
        if runner_install:
            pass # TODO call static install
        p = util.find_free_port()
        cmd = sys.executable + '-m' + 'nwebclient.runner' + '--rest' + '--port ' + str(p)+'--executor' + runner
        self.process = ProcessExecutor(cmd, start=True)
        self.url = 'http://127.0.0.1:' + str(p) + '/'

    def execute(self, data):
        s = requests.post(self.url, data=data).text
        return json.loads(s)


class NxEspCommandExecutor(SerialExecutor):
    """
       nwebclient.runner:NxEspCommandExecutor
    """

    type = 'nxesp'

    cmds = {}
    action_list = []

    def __init__(self, port=None, start=True, args: util.Args = None, cam_prefix='rpicam-'):
        if port is None:
            start = False
        SerialExecutor.__init__(self, start, port=port)
        print("NxEspCommandExecutor on " + str(port))
        self.param_names['cmd'] = "NxEsp Command (e.g. setd)"
        self.cam_prefix = cam_prefix
        self.cmds = dict()
        self.cmds['setd'] = lambda a: self.setd(a)
        self.cmds['init'] = lambda a: self.init(a)
        self.cmds['cam_vid'] = lambda a: self.cam_vid(a)
        self.cmds['cam_photo'] = lambda a: self.cam_photo(a)
        self.cmds['cam_usb_photo'] = lambda a: self.cam_usb_photo(a)
        self.cmds['shutdown'] = lambda a: self.shutdown(a)
        self.cmds['reboot'] = lambda a: self.reboot(a)
        self.cmds['ip'] = lambda a: self.ip(a)
        self.cmds['get_actions'] = lambda a: self.get_actions(a)
        from nwebclient import nx
        self.cmds['udp_send'] = nx.udp_send
        self.param_names['cmd'] = "Bearbeitet einen NxESP-Befehl"
        self.param_names['enable_esp_cmd'] = "Start einen Proxy auf Pot 80"
        self.param_names['action_add'] = "Fügt eine Aktion zur Ausführbaren Aktion hinzu, in der UI wird dafür ein Button angezeigt"
        self.action_list = [
            #{"title": "Video", "type": "nxesp", "cmd": "cam_vid ;"},
            #{"title": "Foto", "type": "nxesp", "cmd": "cam_photo ;"},
            #{"title": "Aus", "type": "nxesp", "cmd": "setd 10 0 ;"},
            #{"title": "An", "type": "nxesp", "cmd": "setd 10 1 ;"},
            #{"title": "Shutdown", "type": "nxesp", "cmd": "shutdown ;"}
        ]
        if args is not None:
            cfg = args.env('nxesp', {})
            for action in cfg.get('exposed', []):
                self.action_list.append(action)

    def actions(self):
        # nweb.json nxesp: {"exposed": [...]}
        return self.action_list

    def get_actions(self, args):
        return json.dumps(self.actions())

    def on_conected(self):
        super().on_conected()
        for a in self.actions():
            self.publish(a)
        self.onParentClass(LazyDispatcher, lambda p: self.read_gpio(p))

    def publish_command(self, title, cmd):
        a = {"title": title, "command": cmd}
        self.publish(a)

    def publish(self, obj):
        self.serial.write((json.dumps(obj) + '\n').encode())
    def read_gpio(self, p: LazyDispatcher):
        for r in p.instances:
            if isinstance(r, GpioExecutor):
                self.publish_command("An",  "setd "+str(r.pin)+" 1 ;")
                self.publish_command("Aus", "setd " + str(r.pin) + " 0 ;")

    def on_line(self, line):
        self.info("Received line: " + line)
        self.command(line)
        super().on_line(line)

    def commands(self):
        return self.cmds.keys()

    def command(self, line):
        self.info("Executing: " + str(line))
        for cmd in self.cmds:
            if cmd in line:
                i = line.index(cmd)
                trimed_line = line[i:].strip()
                a = trimed_line.split(' ')
                return self.run_command(a)
        result = self.run_on_runner(line)
        if result is None:
            return 'Error: Unknown Command.'
        else:
            return result

    def run_on_runner(self, line):
        parts = line.split(' ')

        def on_parent(dispatcher):
            if dispatcher.canExecute({'type': parts[0]}):
                r = dispatcher.get_runner(parts[0])
                data = {
                    'parent': self,
                    'nxesp_command': line
                }
                # TODO create data object
                a = parts[1:]
                if len(r.param_names.keys()) > 2:
                    # r.param_names.keys()  TODO for bis len(r.param_names.keys())-2
                    pass
                return r.to_text(r.execute(data))
            else:
                return None
        return self.onParentClass(LazyDispatcher, on_parent)

    def run_command(self, parts):
        self.info("run_command: " + parts[0] + " with " + ' '.join(parts[1:]))
        fn = self.cmds[parts[0]]
        return fn(parts[1:])

    def init(self, args):
        from nxbot import GpioExecutor
        type = 'pin' + str(args[0])
        exec = GpioExecutor(pin=int(args[0]), dir=args[1])
        self.onParentClass(LazyDispatcher, lambda d: d.loadRunner(type, exec))

    def setd(self, args):
        t = 'pin' + str(args[0])
        self.onParentClass(LazyDispatcher, lambda d: d.execute({'type': t, 'args': args}))
        return ''

    def cam_vid(self, args):
        #cmd = 'raspivid -o /home/pi/video.h264 -t 30000'
        cmd = self.cam_prefix + 'vid -o /home/pi/video.h264 -t 30000'
        ProcessExecutor(cmd)
        return 'raspivid'

    def cam_photo(self, args):
        # https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started
        #cmd = 'raspistill -o /home/pi/current.jpg'
        cmd = self.cam_prefix + 'still -t 1000 -o /home/pi/current.jpg'
        ProcessExecutor(cmd, on_line=lambda s: self.info(s))
        return 'raspistill'

    def cam_usb_photo(self, args):
        # https://raspberrypi-guide.github.io/electronics/using-usb-webcams
        cmd = 'fswebcam -r 1280x720 --no-banner /home/pi/current.jpg'
        ProcessExecutor(cmd, on_line=lambda s: self.info(s))
        return 'usb_photo'


    def shutdown(self, args):
        cmd = 'sudo shutdown -t now'
        ProcessExecutor(cmd)
        return 'shutdown'

    def reboot(self, args):
        cmd = 'sudo reboot'
        ProcessExecutor(cmd)
        return 'reboot'

    def ip(self, args):
        from nwebclient import nx
        return nx.get_ip()

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/pysys/' + self.type, self.type, view_func=lambda: self.page_nxesp())
        # web.all_params()

    def page_nxesp(self):
        return "NxESP"

    def write_to(self, p: base.Page, summary=False):
        p.div("NxEsp Command Executor")
        p.div("Commands: " + ','.join(self.cmds.keys()))
        p.input('cmd')
        p.input('exec', type='button', value="Ausführen")
        p.h4("Actions:")
        for action in self.actions():
            p.div(self.action_btn(action))

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("NxEsp Commando")
        opts = {'title': 'NxESP'}
        self.write_to(p)
        return p.nxui(opts)

    def execute(self, data):
        if 'cmd' in data:
            return {'result': self.command(data['cmd'])}
        elif 'enable_esp_cmd' in data:
            self.p80 = ProcessExecutor(sys.executable + ' -m nwebclient.runner --executor nwebclient.runner:NxEspCmdProxy --rest --port 80')
        elif 'action_add' in data:
            self.action_list.append(data['action_add'])
            return {'success': True, 'action_count': len(self.action_list)}
        return super().execute(data)


class NxEspCmdProxy(BaseJobExecutor):
    """
        python3 -m nwebclient.runner --executor nwebclient.runner:NxEspCmdProxy --rest --port 80
    """
    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/cmd', 'nxesp', view_func=lambda: self.page_cmd())
    def page_cmd(self):
        from flask import request
        cmd = request.args.get('cmd')
        result = requests.get('http://127.0.0.1:7070', params={'type': 'nxesp', 'cmd': cmd}).json()
        return result.get('result', 'Error: CMD. NxEspCmdProxy')


class FileSend(BaseJobExecutor):
    type = 'file'
    def __init__(self, file):
        super().__init__()
        self.file = file

    def is_image(self):
        return self.file.endswith('.png') or self.file.endswith('.jpg')

    def to_data_uri(self):
        with open(self.file, 'rb') as f:
            binary_fc = f.read()  # fc aka file_content
            base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')
            ext = self.file.split('.')[-1]
            return f'data:image/{ext};base64,{base64_utf8_str}'

    def write_to(self, p: base.Page, summary=False):
        if self.is_image():
            p('<img src="'+self.to_data_uri()+'" style="width:100%;" />')

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("Send File")
        self.write_to(p)
        return p.nxui()

    def execute(self, data):
        return {'src': self.to_data_uri()}


class BluetoothSerial(ProcessExecutor):

    def __init__(self, discoverable=True):
        self.mqtt = ticker.MqttPub()
        self.info("Bluetooth Serial, requires npy system bluetooth-serial-enable")
        super().__init__(cmd='sudo rfcomm watch hci0', start=True, restart=True)
        if discoverable:
            ProcessExecutor(cmd='sudo bluetoothctl discoverable on')
        Thread(target=lambda: self.rfcommWatcher()).start()

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links"""
        try:
            os.stat(path)
        except OSError:
            return False
        return True

    def rfcommWatcher(self):
        while True:
            self.info("rfcomm watch")
            if self.exists('/dev/rfcomm0'):
                self.info("rfcomm exists")
                if not self.is_port_processed('/dev/rfcomm0'):
                    self.on_connection('/dev/rfcomm0')
            time.sleep(10)

    def is_port_processed(self, port):
        for c in self.childs():
            if isinstance(c, SerialExecutor):
                if c.port == port:
                    return True
        return False

    def prn(self, msg):
        super().prn(msg)
        self.mqtt.publish(msg)

    def on_new_line(self, line):
        # Waiting for connection on channel 1
        # Connection from A0:D7:22:6B:24:6D to /dev/rfcomm0
        # Press CTRL-C for hangup
        # Disconnected
        # Waiting for connection on channel 1
        self.info(line)
        if line.strip().startswith('Connection'):
            a = line.split('to')
            dev = a[1].strip()
            self.info("Connection: " + dev)
            self.on_connection(dev)

    def on_connection(self, dev):
        self.info("creating NxEspCommandExecutor")
        self.addChild(NxEspCommandExecutor(dev))
        
    def execute(self, data):
        return super().execute(data)
        # TODO info about /dev/rfcommN


class MessageSaver(BaseJobExecutor):

    type = 'message_saver'

    def __init__(self, host='127.0.0.1', port=1883, topic='ar', connect=True):
        super().__init__()
        self.param_names['emit'] = "Sendet"
        self.param_names['save'] = "Speichert"
        self.param_names['load'] = "Lädt"
        self.param_names['clear'] = "Löscht alle Nachrichten"
        self.param_names['set'] = "Setzt Einstellungen"
        self.host = host
        self.topic = topic
        self.port = port
        self.recording = True
        self.messages = []
        self.extra_delay = None
        self.start = None
        self.client = None
        if connect is True:
            self.connect()

    def connect(self):
        self.client=Mqtt({'MQTT_HOST': self.host}, topic=self.topic, on_message=lambda m: self.on_message(m))
        return {'success': True, 'result': "connected"}

    def get_time(self):
        if self.start is None:
            self.start = time.time()
        return time.time() - self.start

    def on_message(self, message):
        if self.recording is True:
            self.messages.append({
                'time': self.get_time(),
                'message': message
            })

    def emit(self):
        self.recording = False
        for m in self.messages:
            if self.client is not None:
                self.client.publish(self.topic, m['message'])
            if self.extra_delay is not None:
                time.sleep(self.extra_delay)
        return {'success': True, 'result': "Messages Send"}

    def set(self, data):
        if 'extra_delay' in data:
            self.extra_delay = float(data['extra_delay'])
            self.info("Extra Delay: " + str(self.extra_delay))
        return {'success': True, 'result': 'set'}

    def execute(self, data):
        if 'clear' in data:
            self.messages = {}
            return {'success': True, 'result': "No Messages"}
        elif 'save' in data:
            with open(data['save'], 'w') as f:
                json.dump(self.messages, f)
            return {'success': True, 'result': "File written"}
        elif 'emit' in data:
            return self.emit()
        elif 'emit_async' in data:
            util.run_async(lambda: self.emit())
            return {'success': True, 'result': 'thread started'}
        elif 'load' in data:
            self.messages = util.load_json_file(data['load'])
            return {'success': True, 'result': "Messages: " + str(len(self.messages))}
        elif 'start' in data:
            self.recording = True
            return {'success': True, 'result': "start"}
        elif 'stop' in data:
            self.recording = False
            return {'success': True, 'result': "stopped"}
        elif 'set' in data:
            return self.set(data)
        elif 'connect' in data:
            return self.connect()
        return super().execute(data)

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/pysys/message_saver', 'message_saver', view_func=lambda: self.page_ops())

    def btn_exec(self, title, op):
        return web.button_js(title, 'exec_job({"type":"'+self.type+'", "'+op+'":1});')

    def btn_exec_job(self, title, data):
        return web.button_js(title, 'exec_job('+json.dumps(data)+');')

    def page_ops(self):
        p = base.Page(owner=self)
        p.div("Message-Count: " + str(len(self.messages)))
        p += self.btn_exec("Emit", 'emit')
        p += self.btn_exec("Emit (Async)", 'emit_async')
        p += self.btn_exec("Clear", 'clear')
        p += self.btn_exec("Start", 'start')
        p += self.btn_exec("Stop", 'stop')
        p += self.btn_exec_job("Set Delay", {'type': self.type, 'set': 1, 'extra_delay': 0.4})
        p += self.btn_exec_job("Save", {'type': self.type, 'save': '/home/pi/ar.json'})
        p += self.btn_exec_job("Load", {'type': self.type, 'load': '/home/pi/ar.json'})
        return p.simple_page()


class NxMessageProcessor(BaseJobExecutor):

    type='message_processor'

    ips = {}

    def __init__(self, host='127.0.0.1', port=1883, topic='main', connect=True, args: util.Args = {}):
        super().__init__()
        self.ips = {}
        self.host = host
        self.topic = topic
        self.port = port
        self.client = None
        if connect is True:
            self.connect()

    def connect(self):
        from paho.mqtt import client as mqtt_client
        print("[MqttSub] Connect to " + self.host + " Topic: " + self.topic)
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, 'NxMessageProcessor', transport='tcp')

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker!")
                client.subscribe(self.topic)
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.on_message(client, msg.payload.decode())

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect_async(self.host, self.port, keepalive=6000)
        self.client.loop_start()
        return {'success': True, 'result': "connected"}

    def on_message(self, client, message):
        # nxudp Rpi4 192.168.178.44 info from rpi upi cron
        if message.startswith('nxudp'):
            self.on_nxudp(message.split(' '))

    def on_nxudp(self, array):
        self.ips[array[2]] = {'title': array[1]}

    def write_to(self, p: base.Page, summary=False):
        for ip in self.ips.keys():
            p.div(ip)

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("NxMessageProcessor")
        self.write_to(p)
        # TODO display more
        return p.simple_page()

    def execute(self, data):
        # len(data) == 1
        return self.ips


class Tokenizer(BaseJobExecutor):
    """

     See: https://docs.python.org/3/library/tokenize.html#tokenize.generate_tokens
    """
    def execute(self, data):
        from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
        names = {0: 'ENDMARKER', 1: 'NAME', 2: 'NUMBER', 3: 'STRING', 4: 'NEWLINE', 5: 'INDENT', 6: 'DEDENT',
                 7: 'LPAR', 8: 'RPAR', 9: 'LSQB'}
        # RSQB = 10, COLON = 11, COMMA = 12, SEMI = 13, PLUS = 14, MINUS = 15, STAR = 16, SLASH = 17,
        # VBAR = 18, AMPER = 19, LESS = 20, GREATER = 21, EQUAL = 22, DOT = 23, PERCENT = 24, LBRACE = 25, RBRACE = 26
        # EQEQUAL = 27, NOTEQUAL = 28, LESSEQUAL = 29, GREATEREQUAL = 30, TILDE = 31, CIRCUMFLEX = 32
        # LEFTSHIFT = 33, RIGHTSHIFT = 34, DOUBLESTAR = 35, PLUSEQUAL = 36, MINEQUAL = 37, STAREQUAL = 38
        # SLASHEQUAL = 39, PERCENTEQUAL = 40, AMPEREQUAL = 41, VBAREQUAL = 42, CIRCUMFLEXEQUAL = 43
        # LEFTSHIFTEQUAL = 44, RIGHTSHIFTEQUAL = 45, DOUBLESTAREQUAL = 46, DOUBLESLASH = 47, DOUBLESLASHEQUAL = 48
        # AT = 49, ATEQUAL = 50, RARROW = 51, ELLIPSIS = 52, COLONEQUAL = 53, EXCLAMATION = 54, OP = 55, AWAIT = 56
        # ASYNC = 57, TYPE_IGNORE = 58, TYPE_COMMENT = 59, SOFT_KEYWORD = 60, FSTRING_START = 61, FSTRING_MIDDLE = 62
        # FSTRING_END = 63, COMMENT = 64 NL = 65, ERRORTOKEN = 66, ENCODING = 67, N_TOKENS = 68, NT_OFFSET = 256
        s = data['input']
        tokens = []
        g = tokenize(BytesIO(s.encode('utf-8')).readline)
        for toknum, tokval, _, _, _ in g:
            tokens.append({'token': tokval, 'toknum': toknum})
        data['tokens'] = tokens
        data['success'] = True
        return data


class MultiJob:
    """
        nwebclient.ticker:NWebJobFetch

        job_state_group_id

        TODO upload möglich

    """

    stages = []
    state_group_id = 'B05AA14479FBED44BD688748791A4BE5'
    result_group_id = None # TODO
    executor = None
    result = None

    def __init__(self):
        self.stages = []
        self.nweb = NWebClient(None)
        self.init_stages()
        self.cpu = ticker.Cpu()
        self.cpu.add(ticker.NWebJobFetch(delete_jobs=False))
        self.cpu.add(ticker.JobExecutor(executor=JobRunner(self)))
        self.cpu.add(ticker.Ticker(interval=180, fn= lambda: self.downloadResults()))
        self.result = ticker.NWebJobResultUploader(nwebclient=self.nweb)
        self.cpu.loopAsync()

    def downloadResults(self):
        for d in self.nweb.group(self.result_group_id).docs():
            if self.working_on(d.guid()):
                self.intern_execute(json.loads(d.content))

    def set_stages(self):
        self.stage(self.stage2, ['response'])
        self.stage(self.stage1, [])  # Muss an ende

    def stage(self, method, keys):
        self.stages.append({'method': method, 'keys': keys})
        return self

    def canExecuteStage(self, keys, data):
        for key in data:
            if key not in data:
                return False
        return True

    def stage1(self, data):
        # call self.executor.execute()
        return data

    def stage2(self, data):
        # call self.executor.execute()
        return data

    def publishGuid(self, guid):
        d = self.nweb.getOrCreateDoc(self.state_group_id, 'multi_runner_guids')
        c = d.content()
        if c == '':
            d.setContent(json.dumps([guid]))
        else:
            array = json.loads(c)
            if not guid in array:
                array.append(guid)
                d.setContent(json.dumps(array))

    def working_on(self, guid):
        d = self.nweb.getOrCreateDoc(self.state_group_id, 'multi_runner_guids')
        c = d.content()
        if c != '':
            array = json.loads(c)
            return guid in array
        else:
            return False

    def intern_execute(self, data):
        for stage in self.stages:
            if self.canExecuteStage(stage['keys']):
                m = stage['method']
                self.info("Executing Stage " + str(m))
                m(data)
                break

    def execute(self, data):
        self.publishGuid(data['guid'])
        self.intern_execute(data)
        self.nweb.deleteDoc(data['guid'])


restart_process = None

def restart(args):
    global restart_process
    newargs = args.argv[1:]
    newargs.remove('--install')
    newargs = [sys.executable, '-m', 'nwebclient.runner', '--sub'] + newargs
    print("Restart: " + ' '.join(newargs))
    #subprocess.run(newargs, stdout=subprocess.PIPE)
    with subprocess.Popen(newargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        restart_process = p
        for line in p.stdout:
            print(line, end='') # process line here
    exit()

def list_runners():
    import inspect
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    print("Executors: ")
    for c in clsmembers:
        if issubclass(c[1], BaseJobExecutor):
            print("  " + str(c[0]))

def usage(exit_program=False):
    print("Usage: "+sys.executable+" -m nwebclient.runner --install --ticker 1 --executor module:Class --in in.json --out out.json")
    print("")
    print("Options:")
    print("  --install           Installiert die Abhaegigkeiten der Executoren")
    print("  --rest              Startet den Buildin Webserver")
    print("  --mqtt              Verbindet MQTT")
    print("  --ticker 1          Startet einen nwebclient.ticker paralell")
    print("  --executor          Klasse zum Ausführen der Jobs ( nwebclient.runner.AutoDispatcher )")
    print("                          - nwebclient.runner.AutoDispatcher")
    print("                          - nwebclient.runner.MainExecutor")
    print("")
    list_runners()
    if exit_program:
        exit()

def configure_ticker(args, runner: JobRunner):
    if args.hasFlag('ticker'):
        cpu = ticker.create_cpu(args).add(ticker.JobExecutor(executor=runner))
        if args.hasFlag('nweb-jobs'):
            cpu.add(ticker.NWebJobFetch(supported_types=runner.jobexecutor.supported_types(), delete_jobs=True, limit=1))
            #ticker.NWebJobResultUploader()
            # TODO fetch und push  "job_fetch_group_id"
        cpu.loopAsync()

def main_install(executor, args):
    print("Install")
    util.load_class(executor, create=False).pip_install()
    if not args.hasFlag('--exit'):
        restart(args)

def arg_cloud(args):
    from nwebclient import nx
    if 'cloud' in args and ('cloud_ssid' not in args or args['cloud_ssid'] == nx.get_ssid()):
        nc = NWebClient(None)
        d = nc.group('F30C94D566C931AF09D946F2F6665611').doc_by_name(nx.get_name())
        if d is not None:
            print("NWEB:CloudConfig: Update /etc/nweb.json")
            d.save('/etc/nweb.json')
            args = util.Args()
    return args

def run(args:util.Args, executor=None):
    args = arg_cloud(args)
    if args.help_requested():
        usage(exit_program=True)
    if args.hasFlag('list'):
        list_runners()
        exit()
    if executor is None:
        executor = args.getValue('executor')
    if executor is None:
        print("No executor found. Using AutoDispatcher")
        executor = AutoDispatcher()
    print("Executor: " + str(executor))
    if args.hasFlag('cfg') and isinstance(executor, LazyDispatcher):
        executor.loadDict(args.env(args.getValue('name', 'runners'), {}))
    if args.hasFlag('install'):
        main_install(executor, args)
    else:
        jobrunner = util.load_class(executor, create=True, run_args=args)
        runner = JobRunner(jobrunner)
        configure_ticker(args, runner)
        if args.hasFlag('rest'):
            if args.hasFlag('mqtt'):
                runner.execute_mqtt(args)
            runner.execute_rest(port=args.getValue('port', 7070), run=True)
        elif args.hasFlag('mqtt'):
            runner.execute_mqtt(args, True)
        else:
            runner.execute_file(args.getValue('in', 'input.json'), args.getValue('out', 'output.json'))

def main(executor=None):
    try:
        args = util.Args()
        print("nwebclient.runner Use --help for more Options")
        run(args, executor)
    except KeyboardInterrupt:
        print("")
        print("Exit nwebclient.runner")
        if not restart_process is None:
            print("Close Sub")
            restart_process.terminate()

        
if __name__ == '__main__':
    main()
            
#import signal
#def sigterm_handler(_signo, _stack_frame):
#    # Raises SystemExit(0):
#    sys.exit(0)
#
#    signal.signal(signal.SIGTERM, sigterm_handler)
