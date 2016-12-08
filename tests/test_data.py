import pytest
import sh

from dila import data
from dila.data import translated_strings


def test_data_preserves_translated_strings(db_connection):
    data.add_translated_string('x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_strings = list(data.get_translated_strings())
    assert preserved_strings == [
        translated_strings.TranslatedStringData(
            base_string='x',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
        )]
