import polib

from dila import data


def get_po_file():
    po = polib.POFile()
    for string in data.get_translated_strings():
        po.append(polib.POEntry(
            msgid=string.base_string,
            msgstr=string.translation,
            msgctxt=string.context,
            comment=string.comment,
            tcomment=string.translator_comment,
        ))
    return str(po)


def upload_translated_po_file(content):
    po = polib.pofile(content)
    for entry in po:
        if not entry.obsolete:
            data.add_translated_string(
                entry.msgid,
                context=entry.msgctxt,
                translation=entry.msgstr,
                comment=entry.comment,
                translator_comment=entry.tcomment,
            )


def get_translated_strings():
    return data.get_translated_strings()


def get_translated_string(pk):
    return data.get_translated_string(pk)


def set_translated_string(pk, **kwargs):
    data.set_translated_string(pk, **kwargs)
