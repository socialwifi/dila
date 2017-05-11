import polib

from dila import data


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
            string_pk = data.add_or_update_base_string(
                resource_pk,
                entry.msgid,
                context=entry.msgctxt,
                comment=entry.comment,
            )
            used_pks.append(string_pk)
            if translated_language_code:
                data.set_translated_string(
                    translated_language_code,
                    string_pk,
                    translation=entry.msgstr,
                    translator_comment=entry.tcomment
                )
    data.delete_old_strings(resource_pk, keep_pks=used_pks)


def get_translated_strings(language_code, resource_pk):
    return data.get_translated_strings(language_code, resource_pk)


def get_translated_string(language_code, pk):
    return data.get_translated_string(language_code, pk)


def set_translated_string(language_code, pk, **kwargs):
    data.set_translated_string(language_code, pk, **kwargs)
