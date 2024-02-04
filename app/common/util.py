import re
from typing import Union
from uuid import UUID


def uuid_masker(exposed_uuid: Union[str, UUID]) -> str:
    uuid_str = str(exposed_uuid)
    return re.sub(
        r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-",
        "********-****-****-****-",
        uuid_str,
    )
