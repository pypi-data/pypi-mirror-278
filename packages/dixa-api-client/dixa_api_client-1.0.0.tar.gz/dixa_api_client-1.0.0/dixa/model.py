from typing import Any, TypedDict


class DixaAPIResponse(TypedDict):
    """Dixa API response."""

    data: dict[str, Any] | list[Any]
