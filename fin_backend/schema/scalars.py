import strawberry as st
import dateutil
from typing import NewType


def parse_datetime(value):
    dt = dateutil.parser.parse(value)
    return dt.isoformat(timespec="milliseconds").split("+")[0]


DateTimeCustom = st.scalar(
    NewType("DateTimeCustom", str),
    serialize=lambda k: k,
    parse_value=parse_datetime,
)
