import polib

from dila import data


def setup():
    data.setup()


def shutdown_session(exception=None):
    data.shutdown_session(exception=exception)


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
