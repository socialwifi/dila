import flask_wtf
import wtforms


class PoFileUpload(flask_wtf.FlaskForm):
    po_file = wtforms.FileField('po file')
