from dixa.api import DixaResource, DixaVersion


class TagResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Tags/
    """

    object_list_key = "tags"
    dixa_version: DixaVersion = "v1"

    def activate(self, tag_id: str):
        """Activate a tag.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Tags/#tag/Tags/operation/patchTagsTagidActivate
        """
        return self._http_patch(f"{self.url}/{tag_id}/activate")

    def create(self, body):
        """Create a tag.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Tags/#tag/Tags/operation/postTags
        """
        return self._http_post(self.url, body)

    def deactivate(self, tag_id: str):
        """Deactivate a tag.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Tags/#tag/Tags/operation/patchTagsTagidDeactivate
        """
        return self._http_patch(f"{self.url}/{tag_id}/deactivate")

    def get(self, tag_id: str):
        """Get a tag by id.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Tags/#tag/Tags/operation/getTagsTagid
        """
        return self._http_get(f"{self.url}/{tag_id}")

    def list(self):
        """List tags.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Tags/#tag/Tags/operation/getTags
        """
        return self._http_get(self.url)
