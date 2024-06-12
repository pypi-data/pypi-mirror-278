from .. import DixaResource, DixaVersion


class AgentResource(DixaResource):
    """
    https://developer.rechargepayments.com/2021-01/addresses
    """

    resource = "agents"
    dixa_version: DixaVersion = "v1"

    def create(self, body):
        """Create an agent.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/postAgents
        """
        return self.client.post(self.url, body)

    def create_bulk(self, body):
        """Create agents.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/postAgentsBulk
        """
        return self.client.post(f"{self.url}/bulk", body)

    def get(self, agent_id: str):
        """Get an agent by id.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/getAgentsAgentid
        """
        return self.client.get(f"{self.url}/{agent_id}")

    def update(self, agent_id, body):
        """Update an agent by id.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/putAgentsAgentid
        """
        return self.client.put(f"{self.url}/{agent_id}", body)

    def update_bulk(self, body):
        """Update agents.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/putAgentsBulk
        """
        return self.client.put(self.url, body)

    def delete(self, agent_id: str):
        """Delete an address by ID.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/deleteAgentsAgentid
        """
        return self.client.delete(f"{self.url}/{agent_id}")

    def list(self, query: dict | None = None):
        """List agents.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgents
        """
        return self.client.get(self.url, query)

    def get_presence(self, agent_id: str):
        """Get agent presence.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgentsAgentidPresence
        """
        return self.client.get(f"{self.url}/{agent_id}/presence")

    def list_presence(self):
        """List agent presence.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgentsPresence
        """
        return self.client.get(f"{self.url}/presence")

    def list_teams(self, agent_id: str):
        """List teams.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgentsAgentidTeams
        """
        return self.client.get(f"{self.url}/{agent_id}/teams")

    def patch(self, agent_id: str, body):
        """Patch an agent.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/patchAgentsAgentid
        """
        return self.client.patch(f"{self.url}/{agent_id}", body)

    def patch_bulk(self, body):
        """Patch agents.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/patchAgentsBulk
        """
        return self.client.patch(self.url, body)
