import flask_wtf
import wtforms


class PoFileUpload(flask_wtf.FlaskForm):
    po_file = wtforms.FileField('Select po file')
    apply_translations = wtforms.BooleanField('Apply translations')


class TranslationForm(flask_wtf.FlaskForm):
    translation = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})


class NewResourceForm(flask_wtf.FlaskForm):
    new_resource_name = wtforms.StringField('New resource')


class NewLanguageForm(flask_wtf.FlaskForm):
    new_language_name = wtforms.StringField('New language')
    new_language_short = wtforms.StringField('Language code')
    next = wtforms.HiddenField()
