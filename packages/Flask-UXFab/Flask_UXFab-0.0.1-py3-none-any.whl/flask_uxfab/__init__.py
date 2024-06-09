import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort

class UXFab:
    def __init__(
        self, app=None, db=None, url_prefix='/forms'
    ):
        """
        Handles form formatting and on the fly creation
        """
        self.db = db
        self.url_prefix = url_prefix
        #if self.db:
        #    self.models = UXModels(db)

        self.blueprint = Blueprint(
            'ux_blueprint', __name__,
            url_prefix=url_prefix,
            template_folder='templates',
            static_folder='static'
        )
        self.blueprint.add_url_rule("/", 'uxf', view_func=self.uxf_index, methods=['GET'])
        if db:
            self.blueprint.add_url_rule("/", 'cms_forms', view_func=self.cms_forms, methods=['GET'])
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)
        app.extensions['uxfab'] = self

    def uxf_index(self):
        return render_template('base.html', title='UX forms')

def create_app():
    from flask import Flask
    from flask_fefset import FEFset
    fef = FEFset()
    uxf = UXFab()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(12).hex()
    app.config['FEFSET_BRAND_NAME'] = 'THE BRAND'
    fef.init_app(app)
    uxf.init_app(app)
    @app.route('/')
    def index():
        return redirect('/forms')
    return app


