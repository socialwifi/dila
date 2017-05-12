import polib

from dila import data
from dila.application import structures


def get_po_file(language_code, resource_pk):
    po = polib.POFile()
    for string in data.get_translated_strings(language_code, resource_pk):
        po.append(polib.POEntry(
            msgid=string.base_string,
            msgstr=string.translation,
            msgctxt=string.context,
            comment=string.comment,
            tcomment=string.translator_comment,
        ))
    return str(po)


def upload_po_file(resource_pk, content, translated_language_code=None):
    po = polib.pofile(content)
    used_pks = []
    for entry in po:
        if not entry.obsolete:
            string_pk = UniversalEntrySaver(entry).save(resource_pk, translated_language_code)
            used_pks.append(string_pk)
    data.delete_old_strings(resource_pk, keep_pks=used_pks)


# TODO: Move to separate file
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


def get_translated_strings(language_code, resource_pk):
    return data.get_translated_strings(language_code, resource_pk)


def get_translated_string(language_code, pk):
    return data.get_translated_string(language_code, pk)


def set_translated_string(language_code, pk, **kwargs):
    data.set_translated_string(language_code, pk, **kwargs)
