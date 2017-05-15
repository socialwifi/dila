import polib

from dila import data
from dila.application import po_entry_savers


def get_po_file(language_code, resource_pk):
    po = polib.POFile()
    for string in data.get_translated_strings(language_code, resource_pk):
        po.append(build_po_entry(string))
    po.metadata = data.get_po_metadata(language_code, resource_pk)
    return str(po)


def build_po_entry(string):
    if string.plural:
        return polib.POEntry(
            msgid=string.base_string,
            msgid_plural=string.plural,
            msgstr_plural={
                '0': string.translation,
                '1': string.plural_translations.few,
                '2': string.plural_translations.many,
                '3': string.plural_translations.other,
            },
            msgctxt=string.context,
            comment=string.comment,
            tcomment=string.translator_comment,
        )
    else:
        return polib.POEntry(
            msgid=string.base_string,
            msgstr=string.translation,
            msgctxt=string.context,
            comment=string.comment,
            tcomment=string.translator_comment,
        )


def upload_po_file(resource_pk, content, translated_language_code=None):
    po = polib.pofile(content)
    used_pks = []
    for entry in po:
        if not entry.obsolete:
            string_pk = po_entry_savers.UniversalEntrySaver(entry).save(resource_pk, translated_language_code)
            used_pks.append(string_pk)
    data.delete_old_strings(resource_pk, keep_pks=used_pks)
    if translated_language_code:
        data.update_po_metadata(translated_language_code, resource_pk, po.metadata)


def get_translated_strings(language_code, resource_pk):
    return data.get_translated_strings(language_code, resource_pk)


def get_translated_string(language_code, pk):
    return data.get_translated_string(language_code, pk)


def set_translated_string(language_code, pk, **kwargs):
    data.set_translated_string(language_code, pk, **kwargs)
