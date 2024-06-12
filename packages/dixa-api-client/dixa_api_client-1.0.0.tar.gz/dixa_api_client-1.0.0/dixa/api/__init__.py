from typing import Literal
from ..client import DixaClient

DixaVersion = Literal["v1", "beta"]


class DixaResource:
    """Generic Dixa API resource."""

    base_url = "https://dev.dixa.io"
    resource = None
    dixa_version: DixaVersion = "v1"

    def __init__(self, client: DixaClient):
        """Initializes the Dixa API resource."""

        self.client = client

    @property
    def url(self) -> str:
        """Returns the resource URL."""

        return f"{self.base_url}/{self.dixa_version}/{self.resource}"
