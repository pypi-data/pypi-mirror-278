from dixa.api import DixaResource, DixaVersion


class CustomAttributeResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Custom-Attributes/
    """

    object_list_key = "custom-attributes"
    dixa_version: DixaVersion = "v1"

    def list(self):
        """List custom attributes definitions.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Custom-Attributes/#tag/Custom-Attributes/operation/getCustom-attributes
        """
        return self._http_get(self.url)
