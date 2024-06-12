from .. import DixaResource, DixaVersion


class TeamResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/
    """

    resource = "teams"
    dixa_version: DixaVersion = "v1"

    def add_members(self, team_id: str, body):
        """Add members to a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/patchTeamsTeamidAgents
        """
        return self.client.post(f"{self.url}/{team_id}/agents", body)

    def create(self, body):
        """Create a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/postTeams
        """
        return self.client.post(self.url, body)

    def delete(self, team_id: str):
        """Delete a team by ID.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/deleteTeamsTeamid
        """
        return self.client.delete(f"{self.url}/{team_id}")

    def get(self, team_id: str):
        """Get a team by ID.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeamsTeamid
        """
        return self.client.get(f"{self.url}/{team_id}")

    def list_members(self, team_id: str):
        """List members of a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeamsTeamidAgents
        """
        return self.client.get(f"{self.url}/{team_id}/agents")

    def list_presence(self, team_id: str):
        """List presence of a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeamsTeamidPresence
        """
        return self.client.get(f"{self.url}/{team_id}/presence")

    def list(self):
        """List teams.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeams
        """
        return self.client.get(self.url)

    def remove_members(self, team_id: str, body):
        """Remove members from a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/deleteTeamsTeamidAgents
        """
        return self.client.delete(f"{self.url}/{team_id}/agents", body)
