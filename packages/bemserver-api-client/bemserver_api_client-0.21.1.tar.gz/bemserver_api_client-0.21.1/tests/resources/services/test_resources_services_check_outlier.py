"""BEMServer API client services check outliers data resources tests"""

from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources.services import (
    ST_CheckOutlierByCampaignResources,
)
from bemserver_api_client.response import BEMServerApiClientResponse


class TestAPIClientResourcesServicesOutlier:
    def test_api_client_resources_services_check_outlier(self):
        assert issubclass(ST_CheckOutlierByCampaignResources, BaseResources)
        assert ST_CheckOutlierByCampaignResources.endpoint_base_uri == (
            "/st_check_outliers_by_campaigns/"
        )
        assert ST_CheckOutlierByCampaignResources.disabled_endpoints == []
        assert ST_CheckOutlierByCampaignResources.client_entrypoint == (
            "st_check_outlier_by_campaign"
        )
        assert hasattr(ST_CheckOutlierByCampaignResources, "get_full")

    def test_api_client_resources_services_check_outlier_endpoints(self, mock_request):
        check_outlier_res = ST_CheckOutlierByCampaignResources(mock_request)
        resp = check_outlier_res.get_full()
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert len(resp.data) == 3
