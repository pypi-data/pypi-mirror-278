from dixa.api import DixaResource, DixaVersion


class TeamResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/
    """

    object_list_key = "teams"
    dixa_version: DixaVersion = "v1"

    def add_members(self, team_id: str, body):
        """Add members to a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/patchTeamsTeamidAgents
        """
        return self._http_post(f"{self.url}/{team_id}/agents", body)

    def create(self, body):
        """Create a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/postTeams
        """
        return self._http_post(self.url, body)

    def delete(self, team_id: str):
        """Delete a team by ID.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/deleteTeamsTeamid
        """
        return self._http_delete(f"{self.url}/{team_id}")

    def get(self, team_id: str):
        """Get a team by ID.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeamsTeamid
        """
        return self._http_get(f"{self.url}/{team_id}")

    def list_members(self, team_id: str):
        """List members of a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeamsTeamidAgents
        """
        return self._http_get(f"{self.url}/{team_id}/agents")

    def list_presence(self, team_id: str):
        """List presence of a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeamsTeamidPresence
        """
        return self._http_get(f"{self.url}/{team_id}/presence")

    def list(self):
        """List teams.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/getTeams
        """
        return self._http_get(self.url)

    def remove_members(self, team_id: str, body):
        """Remove members from a team.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Teams/#tag/Teams/operation/deleteTeamsTeamidAgents
        """
        return self._http_delete(f"{self.url}/{team_id}/agents", body)
