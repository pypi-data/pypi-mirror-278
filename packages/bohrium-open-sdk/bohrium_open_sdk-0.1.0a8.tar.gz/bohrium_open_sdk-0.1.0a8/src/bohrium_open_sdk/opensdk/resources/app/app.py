from bohrium_open_sdk.opensdk.resources.app.app_job import AppJob
from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse


class App(SyncAPIResource):
    job: AppJob

    def __init__(self, _client) -> None:
        self.job = AppJob(_client)
        super().__init__(_client)

    def get_app_info(self, app_key: str):
        response = self._client.get(
            "/openapi/v1/square/app/schema", params={"appKey": app_key}
        )
        return APIResponse(response).json
