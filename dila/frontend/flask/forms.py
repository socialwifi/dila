import flask_wtf
import wtforms


class PoFileUpload(flask_wtf.FlaskForm):
    po_file = wtforms.FileField('po file')


class TranslationForm(flask_wtf.FlaskForm):
    translation = wtforms.StringField()
