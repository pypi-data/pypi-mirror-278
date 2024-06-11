from dixa.api import DixaResource, DixaVersion


class ContactEndpointResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Contact-Endpoints/
    """

    object_list_key = "contact-endpoints"
    dixa_version: DixaVersion = "v1"

    def get(self, contact_endpoint_id: str):
        """Get contact endpoint.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Contact-Endpoints/#tag/Contact-Endpoints/operation/getContact-endpointsContactendpointid
        """
        return self._http_get(f"{self.url}/{contact_endpoint_id}")

    def list(self, query: dict | None = None):
        """List contact endpoints.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Contact-Endpoints/#tag/Contact-Endpoints/operation/getContact-endpoints
        """
        return self._http_get(self.url, query=query)
