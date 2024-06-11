from dixa.api import DixaResource, DixaVersion


class AnalyticsResource(DixaResource):
    """
    https://developer.rechargepayments.com/2021-01/addresses
    """

    object_list_key = "analytics"
    dixa_version: DixaVersion = "v1"

    def filter(self, filter_attribute: str, query: dict | None = None):
        """Filter values.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/getAnalyticsFilterFilterattribute
        """
        return self._http_get(f"{self.url}/filter/{filter_attribute}", query)

    def get_metric_data(self, body):
        """Get metric data.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/postAnalyticsMetrics
        """
        return self._http_post(f"{self.url}/metrics", body)

    def get_metric_records_data(self, body):
        """Get metric records data.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/postAnalyticsRecords
        """
        return self._http_post(f"{self.url}/records", body)

    def get_metric_description(self, metric_id: str):
        """Get metric description.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/getAnalyticsMetricsMetricid
        """
        return self._http_get(f"{self.url}/metrics/{metric_id}")

    def get_metric_record_description(self, record_id: str):
        """Get metric record description.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/getAnalyticsRecordsRecordid
        """
        return self._http_get(f"{self.url}/records/{record_id}")

    def get_metric_records_catalogue(self, query: dict | None = None):
        """Get metric record description.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/getAnalyticsRecordsRecordid
        """
        return self._http_get(f"{self.url}/records", query)

    def get_metrics_catalogue(self, query: dict | None = None):
        """Get metrics catalogue.
        https://docs.dixa.io/openapi/dixa-api/v1/tag/Analytics/#tag/Analytics/operation/getAnalyticsMetrics
        """
        return self._http_get(f"{self.url}/metrics", query)
