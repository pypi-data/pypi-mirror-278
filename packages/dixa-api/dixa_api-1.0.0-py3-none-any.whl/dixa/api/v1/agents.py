from dixa.api import DixaResource, DixaVersion


class AgentResource(DixaResource):
    """
    https://developer.rechargepayments.com/2021-01/addresses
    """

    object_list_key = "agents"
    dixa_version: DixaVersion = "v1"

    def create(self, body):
        """Create an agent.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/postAgents
        """
        return self._http_post(self.url, body)

    def create_bulk(self, body):
        """Create agents.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/postAgentsBulk
        """
        return self._http_post(f"{self.url}/bulk", body)

    def get(self, agent_id: str):
        """Get an agent by id.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/getAgentsAgentid
        """
        return self._http_get(f"{self.url}/{agent_id}")

    def update(self, agent_id, body):
        """Update an agent by id.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/putAgentsAgentid
        """
        return self._http_put(f"{self.url}/{agent_id}", body)

    def update_bulk(self, body):
        """Update agents.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/putAgentsBulk
        """
        return self._http_put(self.url, body)

    def delete(self, agent_id: str):
        """Delete an address by ID.
        https://docs.dixa.io/openapi/dixa-api/beta/tag/Agents/#tag/Agents/operation/deleteAgentsAgentid
        """
        return self._http_delete(f"{self.url}/{agent_id}")

    def list(self, query: dict | None = None):
        """List agents.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgents
        """
        return self._http_get(self.url, query)

    def get_presence(self, agent_id: str):
        """Get agent presence.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgentsAgentidPresence
        """
        return self._http_get(f"{self.url}/{agent_id}/presence")

    def list_presence(self):
        """List agent presence.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgentsPresence
        """
        return self._http_get(f"{self.url}/presence")

    def list_teams(self, agent_id: str):
        """List teams.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/getAgentsAgentidTeams
        """
        return self._http_get(f"{self.url}/{agent_id}/teams")

    def patch(self, agent_id: str, body):
        """Patch an agent.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/patchAgentsAgentid
        """
        return self._http_patch(f"{self.url}/{agent_id}", body)

    def patch_bulk(self, body):
        """Patch agents.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Agents/#tag/Agents/operation/patchAgentsBulk
        """
        return self._http_patch(self.url, body)
