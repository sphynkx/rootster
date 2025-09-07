from config import PERMIT_DELETE_EXCLUDE_TABLES, EDITABLE_FIELDS
import re


def inject_config():
    return dict(
        EDITABLE_FIELDS=EDITABLE_FIELDS,
        PERMIT_DELETE_EXCLUDE_TABLES=list(PERMIT_DELETE_EXCLUDE_TABLES)
    )


