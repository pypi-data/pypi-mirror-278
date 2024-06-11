"""BEMServer API client services cleanup resources tests"""

from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources.services import (
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
)
from bemserver_api_client.response import BEMServerApiClientResponse


class TestAPIClientResourcesServicesCleanup:
    def test_api_client_resources_services_cleanup(self):
        assert issubclass(ST_CleanupByCampaignResources, BaseResources)
        assert ST_CleanupByCampaignResources.endpoint_base_uri == (
            "/st_cleanups_by_campaigns/"
        )
        assert ST_CleanupByCampaignResources.disabled_endpoints == []
        assert hasattr(ST_CleanupByCampaignResources, "get_full")
        assert ST_CleanupByCampaignResources.client_entrypoint == (
            "st_cleanup_by_campaign"
        )

        assert issubclass(ST_CleanupByTimeseriesResources, BaseResources)
        assert ST_CleanupByTimeseriesResources.endpoint_base_uri == (
            "/st_cleanups_by_timeseries/"
        )
        assert ST_CleanupByTimeseriesResources.disabled_endpoints == [
            "create",
            "update",
            "delete",
        ]
        assert ST_CleanupByTimeseriesResources.client_entrypoint == (
            "st_cleanup_by_timeseries"
        )
        assert hasattr(ST_CleanupByTimeseriesResources, "get_full")

    def test_api_client_resources_services_cleanup_endpoints(self, mock_request):
        cleanup_camp_res = ST_CleanupByCampaignResources(mock_request)
        resp = cleanup_camp_res.get_full()
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert len(resp.data) == 3

        cleanup_ts_res = ST_CleanupByTimeseriesResources(mock_request)
        resp = cleanup_ts_res.get_full()
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert len(resp.data) == 5
