import flask_wtf
import wtforms

from dila import application
from dila.application import structures


class PoFileUpload(flask_wtf.FlaskForm):
    po_file = wtforms.FileField('Select po file')
    apply_translations = wtforms.BooleanField('Apply translations')


def get_translation_form(translated_string):
    if translated_string.plural:
        return PluralTranslationForm(
            obj=translated_string,
            translation_one=translated_string.translation,
            translation_few=translated_string.plural_translations.few,
            translation_many=translated_string.plural_translations.many,
            translation_other=translated_string.plural_translations.other,
        )
    else:
        return TranslationForm(obj=translated_string)


class BaseTranslationForm(flask_wtf.FlaskForm):
    translator_comment = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})

    def set_translated_string(self, language_code, pk):
        application.set_translated_string(language_code, pk,
                                          **self.get_translated_string_kwargs())

    def get_translated_string_kwargs(self):
        return {
            'translator_comment': self.data['translator_comment'],
        }


class TranslationForm(BaseTranslationForm):
    translation = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})

    def get_translated_string_kwargs(self):
        return {
            'translation': self.data['translation'],
            **super().get_translated_string_kwargs(),
        }


class PluralTranslationForm(BaseTranslationForm):
    translation_one = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})
    translation_few = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})
    translation_many = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})
    translation_other = wtforms.TextAreaField(render_kw={'rows': 5, 'cols': 90})

    def get_translated_string_kwargs(self):
        return {
            'translation': self.data['translation_one'],
            'plural_translations': structures.PluralTranslations(
                few=self.data['translation_few'],
                many=self.data['translation_many'],
                other=self.data['translation_other'],
            ),
            **super().get_translated_string_kwargs(),
        }


class NewResourceForm(flask_wtf.FlaskForm):
    new_resource_name = wtforms.StringField('New resource')


class NewLanguageForm(flask_wtf.FlaskForm):
    new_language_name = wtforms.StringField('New language')
    new_language_short = wtforms.StringField('Language code')
    next = wtforms.HiddenField()


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username')
    password = wtforms.PasswordField('Password')
    user = application.ANONYMOUS_USER

    def validate(self, *args, **kwargs):
        if super().validate(*args, **kwargs):
            self.user = application.authenticate(self.username.data, self.password.data)
            if self.user.authenticated:
                return True
            else:
                self.password.errors.append('Invalid login or password')
        return False
