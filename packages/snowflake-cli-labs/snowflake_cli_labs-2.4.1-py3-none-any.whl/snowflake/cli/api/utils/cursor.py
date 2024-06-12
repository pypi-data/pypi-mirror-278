from __future__ import annotations

from typing import Callable, List, Optional

from snowflake.connector.cursor import DictCursor


def _rows_generator(cursor: DictCursor, predicate: Callable[[dict], bool]):
    return (row for row in cursor.fetchall() if predicate(row))


def find_all_rows(cursor: DictCursor, predicate: Callable[[dict], bool]) -> List[dict]:
    return list(_rows_generator(cursor, predicate))


def find_first_row(
    cursor: DictCursor, predicate: Callable[[dict], bool]
) -> Optional[dict]:
    """Returns the first row that matches the predicate, or None."""
    return next(_rows_generator(cursor, predicate), None)
