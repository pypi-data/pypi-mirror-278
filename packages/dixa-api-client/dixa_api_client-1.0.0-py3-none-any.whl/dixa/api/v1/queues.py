from .. import DixaResource, DixaVersion


class QueueResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/
    """

    resource = "queues"
    dixa_version: DixaVersion = "v1"

    def assign(self, queue_id: str, body):
        """Assign agents
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/#tag/Queues/operation/patchQueuesQueueidMembers
        """
        return self.client.patch(f"{self.url}/{queue_id}/members", body)

    def create(self, body):
        """Create a queue.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/#tag/Queues/operation/postQueues
        """
        return self.client.post(self.url, body)

    def get(self, queue_id: str):
        """Get a queue by id.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/#tag/Queues/operation/getQueuesQueueid
        """
        return self.client.get(f"{self.url}/{queue_id}")

    def list_agents(self, queue_id: str):
        """List agents.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/#tag/Queues/operation/getQueuesQueueidMembers
        """
        return self.client.get(f"{self.url}/{queue_id}/members")

    def list(self):
        """List queues.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/#tag/Queues/operation/getQueues
        """
        return self.client.get(self.url)

    def remove(self, queue_id: str, body):
        """Remove agents.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Queues/#tag/Queues/operation/deleteQueuesQueueidMembers
        """
        return self.client.delete(f"{self.url}/{queue_id}/members", body)
