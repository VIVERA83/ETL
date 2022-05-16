from dataclasses import field
from datetime import datetime
from typing import Any
from typing import ClassVar, Type
from typing import Literal
from typing import Optional

from marshmallow import Schema
from marshmallow.base import FieldABC
from marshmallow_dataclass import dataclass

PRESCRIPTION = Literal["select", "delete"]


@dataclass
class SqlRequestSchema:
    select: str = ""
    where: str = ""
    group_field: str = ""
    order_field: str = ""
    modified: datetime = None  # fields.DateTime(missing=True, default=datetime(year=2000, month=1, day=1))
    offset: int = 0
    limit: int = 100
    index: str = ""
    prescription: PRESCRIPTION = ""

    Schema: ClassVar[Type[Schema]] = Schema

    @property
    def query(self):
        query = self.select
        if self.modified:
            query += "WHERE " + self.where.format(date=self.modified)
        if self.group_field:
            query += """GROUP BY {field_group} """.format(field_group=self.group_field)
        if self.order_field:
            query += """ORDER BY {field_order} """.format(field_order=self.order_field)
        query += """
        OFFSET {offset}
        LIMIT {limit}
        """.format(
            limit=self.limit, offset=self.offset
        )
        return query


@dataclass
class ModifiedSchema(FieldABC):
    offset: int = 0
    modified: datetime = None
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class StateSchema:
    index: Optional[dict[str, ModifiedSchema]] = field(default_factory=dict)
    Schema: ClassVar[Type[Schema]] = Schema

    def update(self, data: dict[str, Any]):
        for index, modified in data.items():
            self.index.update({index: ModifiedSchema.Schema().load(modified)})

