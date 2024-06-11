"""BEMServer API client services download weather data resources tests"""

from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources.services import (
    ST_DownloadWeatherDataBySiteResources,
    ST_DownloadWeatherForecastDataBySiteResources,
)
from bemserver_api_client.response import BEMServerApiClientResponse


class TestAPIClientResourcesServicesDownloadWeatherData:
    def test_api_client_resources_services_download_weather(self):
        assert issubclass(ST_DownloadWeatherDataBySiteResources, BaseResources)
        assert ST_DownloadWeatherDataBySiteResources.endpoint_base_uri == (
            "/st_download_weather_data_by_sites/"
        )
        assert ST_DownloadWeatherDataBySiteResources.disabled_endpoints == []
        assert hasattr(ST_DownloadWeatherDataBySiteResources, "get_full")
        assert ST_DownloadWeatherDataBySiteResources.client_entrypoint == (
            "st_download_weather_by_site"
        )

    def test_api_client_resources_services_download_weather_endpoints(
        self, mock_request
    ):
        dwl_weather_res = ST_DownloadWeatherDataBySiteResources(mock_request)
        resp = dwl_weather_res.get_full()
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert len(resp.data) == 3
        assert resp.data[0]["is_enabled"]
        assert not resp.data[1]["is_enabled"]
        assert not resp.data[2]["is_enabled"]


class TestAPIClientResourcesServicesDownloadWeatherForecastData:
    def test_api_client_resources_services_download_weather_forecast(self):
        assert issubclass(ST_DownloadWeatherForecastDataBySiteResources, BaseResources)
        assert ST_DownloadWeatherForecastDataBySiteResources.endpoint_base_uri == (
            "/st_download_weather_forecast_data_by_sites/"
        )
        assert ST_DownloadWeatherForecastDataBySiteResources.disabled_endpoints == []
        assert hasattr(ST_DownloadWeatherForecastDataBySiteResources, "get_full")
        assert ST_DownloadWeatherForecastDataBySiteResources.client_entrypoint == (
            "st_download_weather_forecast_by_site"
        )

    def test_api_client_resources_services_download_weather_forecast_endpoints(
        self, mock_request
    ):
        dwl_weather_res = ST_DownloadWeatherForecastDataBySiteResources(mock_request)
        resp = dwl_weather_res.get_full()
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert len(resp.data) == 3
        assert not resp.data[0]["is_enabled"]
        assert resp.data[1]["is_enabled"]
        assert not resp.data[2]["is_enabled"]
