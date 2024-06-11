from dixa.api import DixaResource, DixaVersion


class WebhookResource(DixaResource):
    """
    https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/
    """

    object_list_key = "webhooks"
    dixa_version: DixaVersion = "v1"

    def create(self, body):
        """Create a webhook.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/postWebhooks
        """
        return self._http_post(self.url, body)

    def delete(self, webhook_subscription_id: str):
        """Delete a webhook.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/deleteWebhooksWebhooksubscriptionid
        """
        return self._http_delete(f"{self.url}/{webhook_subscription_id}")

    def list(self):
        """List webhooks.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/getWebhooks
        """
        return self._http_get(self.url)

    def patch(self, webhook_subscription_id: str, body):
        """Update a webhook.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/patchWebhooksWebhooksubscriptionid
        """
        return self._http_patch(f"{self.url}/{webhook_subscription_id}", body)

    def get(self, webhook_subscription_id: str):
        """Get a webhook.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/getWebhooksWebhooksubscriptionid
        """
        return self._http_get(f"{self.url}/{webhook_subscription_id}")

    def list_event_logs(self, webhook_subscription_id: str, event: str):
        """Get event logs.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/getWebhooksWebhooksubscriptionidDelivery-statusLogsEvent
        """
        return self._http_get(
            f"{self.url}/{webhook_subscription_id}/delivery-status/logs/{event}"
        )

    def list_delivery_statuses(self, webhook_subscription_id: str):
        """Get delivery statuses.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Webhooks/#tag/Webhooks/operation/getWebhooksWebhooksubscriptionidDelivery-status
        """
        return self._http_get(f"{self.url}/{webhook_subscription_id}/delivery-status")
