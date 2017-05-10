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
    for entry in po:
        if not entry.obsolete:
            string_pk = data.add_translated_string(
                resource_pk,
                entry.msgid,
                context=entry.msgctxt,
                comment=entry.comment,
            )
            if translated_language_code:
                data.set_translated_string(
                    translated_language_code,
                    string_pk,
                    translation=entry.msgstr,
                    translator_comment=entry.tcomment
                )


def get_translated_strings(language_code, resource_pk):
    return data.get_translated_strings(language_code, resource_pk)


def get_translated_string(language_code, pk):
    return data.get_translated_string(language_code, pk)


def set_translated_string(language_code, pk, **kwargs):
    data.set_translated_string(language_code, pk, **kwargs)
