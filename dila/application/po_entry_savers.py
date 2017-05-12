from dila import data
from dila.application import structures


class UniversalEntrySaver:
    def __init__(self, entry):
        self.entry = entry

    def save(self, resource_pk, translated_language_code):
        return self.actual_saver.save(resource_pk, translated_language_code)

    @property
    def actual_saver(self):
        if self.entry.msgid_plural:
            return PluralEntrySaver(self.entry)
        else:
            return SingularEntrySaver(self.entry)


class BaseEntrySaver:
    def __init__(self, entry):
        self.entry = entry

    def save(self, resource_pk, translated_language_code):
        string_pk = data.add_or_update_base_string(
            resource_pk,
            self.entry.msgid,
            **self.base_string_kwargs,
        )
        if translated_language_code:
            data.set_translated_string(
                translated_language_code,
                string_pk,
                **self.translated_string_kwargs
            )
        return string_pk

    @property
    def base_string_kwargs(self):
        return {
            'context': self.entry.msgctxt,
            'comment': self.entry.comment,
        }

    @property
    def translated_string_kwargs(self):
        return {
            'translator_comment': self.entry.tcomment
        }


class SingularEntrySaver(BaseEntrySaver):
    @property
    def translated_string_kwargs(self):
        return {
            'translation': self.entry.msgstr,
            **super().translated_string_kwargs,
        }


class PluralEntrySaver(BaseEntrySaver):
    @property
    def base_string_kwargs(self):
        return {
            'plural': self.entry.msgid_plural,
            **super().base_string_kwargs,
        }

    @property
    def translated_string_kwargs(self):
        one = self.entry.msgstr or self.entry.msgstr_plural.get(0, '')
        few = self.entry.msgstr_plural.get(1, one)
        many = self.entry.msgstr_plural.get(2, few)
        other = self.entry.msgstr_plural.get(3, many)
        return {
            'translation': one,
            'plural_translations': structures.PluralTranslations(
                few=few,
                many=many,
                other=other,
            ),
            **super().translated_string_kwargs,
        }
