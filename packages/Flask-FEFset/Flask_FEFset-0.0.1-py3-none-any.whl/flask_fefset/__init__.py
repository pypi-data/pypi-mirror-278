import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort

class FEFset:
    def __init__(
        self, app=None, frontend='bootstrap4', db=None, url_prefix='/front',
        include_footer=False, test=False
    ):
        """
        App configuration keys that should be set:
            FEFSET_LOGO_URL: relative url to the logo that should be displayed
            FEFSET_BRAND_NAME: brand name

        Example:
            app.config['FEFSET_BRAND_NAME'] = 'THE BRAND'
        """
        self.frontend = frontend
        self.nav_menu = []
        self.side_menu = []
        self.settings = {'side_menu_name':''}
        self.db = db
        self.include_footer = include_footer
        self.url_prefix = url_prefix
        #if self.db:
        #    self.models = FModels(db)

        self.blueprint = Blueprint(
            'fef_blueprint', __name__,
            url_prefix=url_prefix,
            template_folder=os.path.join('templates', self.frontend),
            static_folder = os.path.join('static', self.frontend)
        )
        if test:
            self.blueprint.add_url_rule("/", 'fef', view_func=self.fef_index, methods=['GET'])
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.globals.update({
            "nav_items": self.nav_menu,
            "side_nav_items": self.side_menu,
            "include_footer":  self.include_footer,
            "navconfig": self.settings
            #"navconfig": app.config.get_namespace('FEFSET_')
        })
        if self.frontend.startswith('bootstrap'):
            from flask_bootstrap import Bootstrap
            self.bootstrap = Bootstrap(app)
        app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)
        app.extensions['fefset'] = self

    def fef_index(self):
        flash(f"'{self.frontend}' active")
        return render_template('base.html', title='Flask-FEFset for setting your frontend')

    def add_menu_entry(self, name, url, submenu=None):
        if submenu:
            for sm_ix, nav_item in enumerate(self.nav_menu):
                if nav_item['name'] == submenu:
                    break
            if self.nav_menu[sm_ix]['name'] != submenu:
                self.add_submenu(submenu)
                sm_ix+=1
            nav_menu = self.nav_menu[sm_ix]['nav_items']
        else: nav_menu = self.nav_menu
        nav_menu.append({'name':name,'url':url})

    def add_submenu(self, name, url=None):
        self.nav_menu.append({'name':name,'url':url,'nav_items':[]})

    def add_side_menu_entry(self, name, url):
        self.side_menu.append({'name':name,'url':url})

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(12).hex()
    app.config['FEFSET_BRAND_NAME'] = 'THE BRAND'
    fef = FEFset(frontend='bootstrap4', test=True)
    fef.nav_menu.append({'name':'Home','url':'/test/blabla/yadayada'})
    fef.init_app(app)
    fef.nav_menu.append({'name':'Admin','url':'/test/yadayada/blabla'})
    app.extensions['fefset'].add_menu_entry('Admin','/test/yadayada/blabla','Submenu')
    @app.route('/')
    def index():
        return redirect('/front')
    app.run(host='0.0.0.0')

