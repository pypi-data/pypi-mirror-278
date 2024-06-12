import os.path

from nwebclient import util
from nwebclient import base as b
import base64
import uuid

def tag(tag_name, content, **kw):
    a = ''
    if '_class' in kw:
        kw['class'] = kw['_class']
        kw.pop('_class', None)
    for k in kw.keys():
        a += ' ' + k + '="' + str(kw[k]) + '"'
    return '<'+tag_name+a+'>'+content+'</'+tag_name+'>'

def a(content, href):
    if isinstance(href, str):
        return tag('a', content, href=href)
    else:
        return tag('a', content, **href)
    
def pre(content, **kw):
    return tag('pre', content, **kw)

def div(content, **kw):
    return tag('div', content, **kw)

def input(name, **attrs):
    attrs['name'] = name
    return tag('input', '', **attrs)

def table(content, **kw):
    s = '<table>'
    if isinstance(content, list):
        for rows in content:
            s += '<tr>'
            for cell in rows:
                s += '<td>'+str(cell)+'<td>'
            s += '</tr>'
    else:
        s += content
    s += '</table>'
    return s


def js_ready(js):
    return 'document.addEventListener("DOMContentLoaded", function() { '+js+' }, false);';

def js_fn(name, args, code=[]):
    return 'function '+name+'('+','.join(args)+') {\n'+'\n'.join(code)+'\n}\n\n'
def js_add_event_for_id(id, event_js):
    return 'document.getElementById("'+id+'").addEventListener("click", function(e) {\n '+event_js+' \n});\n'
def button_js(title, js_action):
    id = 'btn' + str(uuid.uuid4()).replace('-', '')
    js = js_ready(js_add_event_for_id(id, js_action))
    res = '<button id="'+id+'">'+str(title)+'</button><script type="text/javascript">'+js+'</script>'
    return res

def js_base_url_exp():
    # (location.port==""?"":":"+location.port)+
    return 'location.protocol+"//"+location.host+"/"'


def route_root(web, root):
    web.add_url_rule('/pysys/root', 'r_root', view_func=lambda: root.getHtmlTree())
    res = NwFlaskRoutes()
    res.addTo(web)
    return res


class WebRoute(b.Base, b.WebPage):
    def __init__(self, route, name, func):
        self.route = route
        self.name = name
        self.func = func
    def page(self, params={}):
        return self.func()

def all_params():
    from flask import request
    return {**request.args.to_dict(), **request.form.to_dict()}

class NwFlaskRoutes(b.Base):
    """
        Definition on /nw und /nws
    """

    routes = {}

    routes_added = False

    def __init__(self, childs=[]):
        super().__init__()
        self.app = None
        for child in childs:
            self.addChild(child)

    def requestParams(self):
        from flask import request
        data = {}
        for tupel in request.files.items():
            name = tupel[0]
            f = tupel[1]
            #print(str(f))
            data[name] = base64.b64encode(f.read()).decode('ascii')
        params = {
            **request.cookies.to_dict(),
            **request.args.to_dict(), 
            **request.form.to_dict(),
            **data,
            **{'request_url': request.url}}
        return params
    def addTo(self, app):
        self.web = app
        if self.routes_added is True:
            return
        self.routes_added = True
        app.add_url_rule('/nw/<path:p>', 'nw', lambda p: self.nw(p), methods=['GET', 'POST'])
        app.add_url_rule('/nws/', 'nws', self.nws)
    def nws(self):
        p = b.Page().h1("Module")
        for e in b.Plugins('nweb_web'):
            p.div('<a href="{0}" title="Plugin">{1}</a>'.format('/nw/'+e.name, e.name))
        for e in self.childs():
            p.div('<a href="{0}" title="Object">{1}</a>'.format('/nw/' + e.name, e.name))
        return p.simple_page()

    def add_url_rule(self, route, name, view_func):
        print("Route" + route + " via add_url_rule")
        self.routes[route] = view_func
        self.addChild(WebRoute(route, name, view_func))

    def load_flask_blueprints(self, app):
        for e in b.Plugins('flask_blueprints'):
            blueprint = util.load_class(e)
            app.register_blueprint(blueprint)


    def nw(self, path):
        params = self.requestParams()
        n = path.split('/')[0]
        if self.hasName(n):
            return self.getChildByName(n).page(params)
        plugin = b.Plugins('nweb_web')[n]
        if plugin is not None:
            obj = util.load_class(plugin.value, create=True)
            w = self.addChild(b.WebObject(obj, {**{'path': path}, **params}))
            w.name = n
            return w.page(params)
        else:
            return "Error: 404 (NwFlaskRoutes)"

    def handleRoute(self, path, request):
        # add and serv via error404
        return "Route " + str(path), 200

    def error404(self):
        from flask import Flask, request
        if request.path in self.routes.keys():
            return self.handleRoute(request.path, request)
        else:
            status = 404
            return "Error: 404 Not Found, nwebclient.web:NwFlaskRoutes", status

    def create_app(self):
        from flask import Flask, request
        self.app = Flask(__name__)
        self.app.register_error_handler(404, lambda: self.error404())
        # @app.route('/')
        self.addTo(self.app)

    def serv(self, args={},  port=8080):
        self.create_app()
        self.run(port=port)

    def redirect_static(self):
        from flask import Flask, request, redirect
        route = '/static/<path:p>'
        self.app.add_url_rule(route, 'static', lambda p: redirect('https://bsnx.net' + request.path), methods=['GET', 'POST'])
        # AssertionError -> dann gibt es die static route schon

    def serv_dir(self, route, path):
        from flask import send_file
        e = route.replace('/', '')
        p = route + '<path:filename>'
        kwa = {}
        kwa['static_url_path'] = route
        kwa['static_folder'] = path
        #self.app.add_url_rule(p, endpoint=e, view_func=lambda **kwa: self.app.send_static_file(**kwa))  #
        self.app.add_url_rule(p, endpoint=e, view_func=lambda filename: send_file(path + filename))

    def run(self, app=None, port=8080):
        print('NwFlaskRoutes::run(...) in ' + os.getcwd())
        if app is not None:
            self.app = app
        kw = {}
        if os.path.isdir('../app'):  # Debug
            self.serv_dir('/app/', os.getcwd() + '/../app/')
        if os.path.isdir('../static'): # Debug
            self.serv_dir('/static/', os.getcwd()+'/../static/')
        elif os.path.isdir('/var/www/html/static'):
            # git@gitlab.com:bsalgert/static.git
            # https://gitlab.com/bsalgert/static.git
            # https://gitlab.com/bsalgert/static/-/archive/main/static-main.zip
            self.serv_dir('/static/', '/var/www/html/static/')
            #kwa = {}
            #kwa['static_url_path'] = '/static'
            #kwa['static_folder'] = '/var/www/html/static'
            #self.app.add_url_rule(f"/static/<path:filename>", endpoint="static", view_func=lambda **kwa: self.app.send_static_file(**kwa))  #
        else:
            self.redirect_static()
        self.app.run(host='0.0.0.0', port=int(port), **kw)
