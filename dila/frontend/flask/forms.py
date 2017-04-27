import flask_wtf
import wtforms


class PoFileUpload(flask_wtf.FlaskForm):
    po_file = wtforms.FileField('Select po file')


class TranslationForm(flask_wtf.FlaskForm):
    translation = wtforms.StringField()


class NewResourceForm(flask_wtf.FlaskForm):
    new_resource_name = wtforms.StringField('New resource')
