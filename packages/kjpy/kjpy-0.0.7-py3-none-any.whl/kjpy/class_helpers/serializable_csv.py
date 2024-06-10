from typing import Any, Dict, List, Optional

from ..data.unit_test_handler import UnitTestWithTestData


from ..collections.serializable_class import Serializable
from ..collections.sequence_class import SequenceAbstract
from ..collections.mapping_class import MappingAbstract


# TODO: Wrap unsafe cells with quotes

_TEST_DIRECTORY = "class_helpers"
_DEBUG = True


class _CsvRow(Serializable):
    def __init__(self, column_values: List[str]) -> None:
        super().__init__()
        self._column_values = column_values

    def serialize(self):
        output = []
        for column_value in self._column_values:
            output.append(str(column_value))
        return ",".join(output)


class _Record(Serializable, MappingAbstract[str, Any]):
    def serialize(self, column_names: List[str]):
        column_values = []
        for column_name in column_names:
            column_values.append(self.get(column_name) or "")
        return _CsvRow(column_values=column_values).serialize()


class SerializableCsv(Serializable, SequenceAbstract[_Record]):
    def __init__(
        self,
        all_data: Optional[List[Dict]] = None,
        column_names: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self._provided_column_names = column_names

        self._column_names = set()
        self._column_names_ordered: List[str] = []
        if all_data:
            for datum in all_data:
                self.append(datum)

    def _add_columns(self, columns: List[str]):
        if self._provided_column_names:
            return
        for column in columns:
            if column not in self._column_names:
                self._column_names.add(column)
                self._column_names_ordered.append(column)

    @property
    def column_names(self):
        if self._provided_column_names:
            return self._provided_column_names
        return self._column_names_ordered

    def append(self, item: Dict[str, Any]):
        self._add_columns(list(item.keys()))
        self._items.append(_Record(item))

    def _serialize_rows(self):
        column_names = self.column_names
        return [r.serialize(column_names) for r in self._items]

    def serialize(self) -> str:
        csv_header = _CsvRow(self.column_names).serialize()
        csv_rows: List[str] = self._serialize_rows()
        csv_rows.insert(0, csv_header)

        return "\n".join(csv_rows)

    def save(self, filepath):
        csv_data = self.serialize()
        with open(filepath, "w") as f:
            f.write(csv_data)


class TestSerializableCsv(UnitTestWithTestData):
    def setUp(self) -> None:
        return super().setUp(debug=_DEBUG, test_directory=_TEST_DIRECTORY)

    def test_serializable_csv(self):
        _input = [{"name": "kj", "age": 12}]
        serializable_csv = SerializableCsv(all_data=_input)
        self.assertEqualsTestData(
            serializable_csv.serialize(),
            "serializable_csv_simple_response.csv",
        )
