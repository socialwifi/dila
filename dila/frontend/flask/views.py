import flask
from cached_property import cached_property
from flask import views

from dila import application
from dila.frontend.flask import forms
from dila.frontend.flask import languages

blueprint = flask.Blueprint('main', __name__)


class HomeView(views.MethodView):
    def dispatch_request(self, *args, language_code=None):
        self.language_code = language_code
        return super().dispatch_request(*args)

    def get(self):
        return flask.render_template('home.html', **self.context)

    def post(self):
        if self.form.validate():
            application.add_resource(self.form.new_resource_name.data)
            flask.flash('Resource created')
            return flask.redirect(flask.url_for('main.home'))
        else:
            return self.get()

    @property
    def context(self):
        return {
            'resources': self.resources,
            'form': self.form,
        }

    @cached_property
    def resources(self):
        return application.get_resources()

    @cached_property
    def form(self):
        return forms.NewResourceForm()

home = HomeView.as_view('home')

blueprint.add_url_rule('/', view_func=home)
blueprint.add_url_rule('/lang/<language_code>/', view_func=home)


class AddLanguageView(views.MethodView):

    def post(self):
        if self.form.validate():
            application.add_language(
                self.form.data['new_language_name'], self.form.data['new_language_short'])
            flask.flash('Language added.')
            return flask.redirect(self.form.data['next'])
        else:
            flask.flash('Failed to add language.')
            return flask.redirect(self.form.data['next'])

    @cached_property
    def form(self):
        return languages.get_new_form()


blueprint.add_url_rule('/add-language/', view_func=AddLanguageView.as_view('add_language'))


class ResourceView(views.MethodView):
    def dispatch_request(self, *args, language_code=None, resource_pk):
        self.resource_pk = resource_pk
        self.language_code = language_code
        return super().dispatch_request(*args)

    def get(self):
        if self.language_code:
            return flask.render_template('resource.html', **self.context)
        else:
            return flask.render_template('resource-no-language.html')

    def post(self):
        if self.language_code and self.form.validate():
            po_content = flask.request.files[self.form.po_file.name].read().decode()
            application.upload_translated_po_file(self.resource_pk, po_content)
            flask.flash('File uploaded')
            return flask.redirect(flask.url_for('main.resource', resource_pk=self.resource_pk))
        else:
            return self.get()

    @property
    def context(self):
        return {
            'translated_strings': self.translated_strings,
            'form': self.form,
            'resource_pk': self.resource_pk,
        }

    @cached_property
    def form(self):
        return forms.PoFileUpload()

    @cached_property
    def translated_strings(self):
        return application.get_translated_strings(self.resource_pk)


resource = ResourceView.as_view('resource')
blueprint.add_url_rule('/res/<resource_pk>/', view_func=resource)
blueprint.add_url_rule('/lang/<language_code>/res/<resource_pk>/', view_func=resource)


class TranslatedStringEditor(views.MethodView):
    def dispatch_request(self, *args, language_code, pk):
        self.language_code = language_code
        self.pk = pk
        return super().dispatch_request(*args)

    def get(self):
        return flask.render_template('translated_string.html', **self.context)

    def post(self):
        if self.form.validate():
            application.set_translated_string(self.language_code, self.pk, translation=self.form.data['translation'])
            flask.flash('Translation changed')
            return flask.redirect(flask.url_for('main.resource', resource_pk=self.translated_string.resource_pk))
        else:
            return self.get()

    @property
    def context(self):
        return {
            'form': self.form,
            'translated_string': self.translated_string,
            'resource_pk': self.translated_string.resource_pk,
        }

    @cached_property
    def form(self):
        return forms.TranslationForm(obj=self.translated_string)

    @cached_property
    def translated_string(self):
        return application.get_translated_string(self.pk)


blueprint.add_url_rule('/lang/<language_code>/edit/<pk>/', view_func=TranslatedStringEditor.as_view('translated_string'))


class PoFileDownload(views.MethodView):
    def get(self, *args, language_code, resource_pk):
        response = flask.make_response(application.get_po_file(resource_pk))
        response.headers["Content-Disposition"] = "attachment; filename=translations.po"
        return response


blueprint.add_url_rule('/lang/<language_code>/res/<resource_pk>/po-file/', view_func=PoFileDownload.as_view('po_file_download'))
