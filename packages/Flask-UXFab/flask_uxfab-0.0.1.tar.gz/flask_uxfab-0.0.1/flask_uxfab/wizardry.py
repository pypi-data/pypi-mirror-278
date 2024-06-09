from abc import ABC, abstractmethod
from flask.views import View
from flask import request, session, render_template, redirect
from flask_wtf import FlaskForm
from inspect import isclass

class Wizard(ABC, View):
    methods = ["GET", "POST"]

    def __init__(self, model, template, forms=None):
        self.model = model
        self.template = template
        self.forms = [
            getattr(self,a) for a in dir(self)
            if not a.startswith('_')
            and isclass(getattr(self,a))
            and issubclass(getattr(self,a), FlaskForm)
        ] + (forms if forms else [])
        self.last_page = len(self.forms)-1

    def dispatch_request(self, page):
        form = self.forms[page]()
        if form.validate_on_submit():
            if page == self.last_page:
                data = []
                for i in range(self.last_page):
                    data.append(session['wizard'][str(i)])
                data.append({
                    k:v for k,v in form.data.items()
                    if k not in ('submit', 'csrf_token')
                })
                self.process(data)
                return redirect('/')
            else:
                if page == 0:
                    session['wizard'] = {}
                session['wizard'][str(page)] = {
                    k:v for k,v in form.data.items()
                    if k not in ('submit', 'csrf_token')
                }
                path = str(request.url_rule)
                next_url = path[
                    :path.rindex('/')
                ]+f'/{page+1}'
                return redirect(next_url)
        else:
            return render_template(self.template, form=form)

    @abstractmethod
    def process(self, data):
        """Define this class method in the inheriting
        class to process the data, after submission of
        the last form page
        """

