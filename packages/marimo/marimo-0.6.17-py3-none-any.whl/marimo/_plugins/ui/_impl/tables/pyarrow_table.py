# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

import io
from typing import Any, Union, cast

from marimo._data.models import ColumnSummary
from marimo._plugins.ui._impl.tables.table_manager import (
    FieldType,
    FieldTypes,
    TableManager,
    TableManagerFactory,
)


class PyArrowTableManagerFactory(TableManagerFactory):
    @staticmethod
    def package_name() -> str:
        return "pyarrow"

    @staticmethod
    def create() -> type[TableManager[Any]]:
        import pyarrow as pa  # type: ignore
        import pyarrow.compute as pc  # type: ignore

        class PyArrowTableManager(
            TableManager[Union[pa.Table, pa.RecordBatch]]
        ):
            type = "pyarrow"

            def to_csv(self) -> bytes:
                import pyarrow.csv as csv  # type: ignore

                buffer = io.BytesIO()
                csv.write_csv(self.data, buffer)
                return buffer.getvalue()

            def to_json(self) -> bytes:
                # Arrow does not have a built-in JSON writer
                return (
                    self.data.to_pandas()
                    .to_json(orient="records")
                    .encode("utf-8")
                )

            def select_rows(self, indices: list[int]) -> PyArrowTableManager:
                if not indices:
                    return PyArrowTableManager(
                        pa.Table.from_pylist([], schema=self.data.schema)
                    )
                return PyArrowTableManager(self.data.take(indices))

            def select_columns(
                self, columns: list[str]
            ) -> PyArrowTableManager:
                if isinstance(self.data, pa.RecordBatch):
                    return PyArrowTableManager(
                        pa.RecordBatch.from_arrays(
                            [
                                self.data.column(
                                    self.data.schema.get_field_index(col)
                                )
                                for col in columns
                            ],
                            names=columns,
                        )
                    )
                return PyArrowTableManager(self.data.select(columns))

            def get_row_headers(
                self,
            ) -> list[tuple[str, list[str | int | float]]]:
                return []

            @staticmethod
            def is_type(value: Any) -> bool:
                import pyarrow as pa  # type: ignore

                return isinstance(value, pa.Table) or isinstance(
                    value, pa.RecordBatch
                )

            def get_field_types(self) -> FieldTypes:
                return {
                    column: PyArrowTableManager._get_field_type(
                        cast(Any, self.data)[idx]
                    )
                    for idx, column in enumerate(self.data.schema.names)
                }

            def limit(self, num: int) -> PyArrowTableManager:
                if num < 0:
                    raise ValueError("Limit must be a positive integer")
                return PyArrowTableManager(self.data.take(list(range(num))))

            def get_summary(self, column: str) -> ColumnSummary:
                # If column is not in the dataframe, return an empty summary
                if column not in self.data.schema.names:
                    return ColumnSummary()
                idx = self.data.schema.get_field_index(column)
                col: Any = self.data.column(idx)

                field_type = self._get_field_type(col)
                if field_type == "unknown":
                    return ColumnSummary()
                if field_type == "string":
                    return ColumnSummary(
                        total=self.data.num_rows,
                        nulls=col.null_count,
                        unique=pc.count_distinct(col).as_py(),  # type: ignore[attr-defined]
                    )
                if field_type == "boolean":
                    return ColumnSummary(
                        total=self.data.num_rows,
                        nulls=col.null_count,
                        true=pc.sum(col).as_py(),  # type: ignore[attr-defined]
                        false=self.data.num_rows
                        - pc.sum(col).as_py()  # type: ignore[attr-defined]
                        - col.null_count,
                    )
                if field_type == "integer":
                    return ColumnSummary(
                        total=self.data.num_rows,
                        nulls=col.null_count,
                        unique=pc.count_distinct(col).as_py(),  # type: ignore[attr-defined]
                        min=pc.min(col).as_py(),  # type: ignore[attr-defined]
                        max=pc.max(col).as_py(),  # type: ignore[attr-defined]
                        mean=pc.mean(col).as_py(),  # type: ignore[attr-defined]
                    )
                if field_type == "number":
                    return ColumnSummary(
                        total=self.data.num_rows,
                        nulls=col.null_count,
                        min=pc.min(col).as_py(),  # type: ignore[attr-defined]
                        max=pc.max(col).as_py(),  # type: ignore[attr-defined]
                        mean=pc.mean(col).as_py(),  # type: ignore[attr-defined]
                    )
                if field_type == "date":
                    return ColumnSummary(
                        total=self.data.num_rows,
                        nulls=col.null_count,
                        min=pc.min(col).as_py(),  # type: ignore[attr-defined]
                        max=pc.max(col).as_py(),  # type: ignore[attr-defined]
                    )
                return ColumnSummary()

            def get_num_rows(self) -> int:
                return self.data.num_rows

            def get_num_columns(self) -> int:
                return self.data.num_columns

            def get_column_names(self) -> list[str]:
                return self.data.schema.names

            @staticmethod
            def _get_field_type(column: pa.Array[Any, Any]) -> FieldType:
                if isinstance(column, pa.NullArray):
                    return "unknown"
                elif pa.types.is_string(column.type):
                    return "string"
                elif pa.types.is_boolean(column.type):
                    return "boolean"
                elif pa.types.is_integer(column.type):
                    return "integer"
                elif pa.types.is_floating(column.type) or pa.types.is_decimal(
                    column.type
                ):
                    return "number"
                elif pa.types.is_date(column.type) or pa.types.is_timestamp(
                    column.type
                ):
                    return "date"
                else:
                    return "unknown"

        return PyArrowTableManager
