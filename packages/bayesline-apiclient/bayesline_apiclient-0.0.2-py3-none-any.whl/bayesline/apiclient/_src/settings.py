from bayesline.api import (AsyncSettingsRegistry, SettingsMenuType,
                           SettingsMetaData, SettingsRegistry, SettingsType)

from .apiclient import ApiClient, AsyncApiClient


class HttpSettingsRegistryClient(SettingsRegistry[SettingsType, SettingsMenuType]):

    def __init__(
        self,
        client: ApiClient,
        settings_type: type[SettingsType],
        settings_menu_type: type[SettingsMenuType],
    ):
        self._client = client
        self._settings_type = settings_type
        self._settings_menu_type = settings_menu_type

    def available_settings(self) -> SettingsMenuType:
        content = self._client.get("available-settings")
        return self._settings_menu_type.model_validate_json(content.text)

    def ids(self) -> dict[int, str]:
        return {v: k for k, v in self.names().items()}

    def names(self) -> dict[str, int]:
        return self._client.get("settings").json()

    def get(self, name: str | int) -> SettingsType:
        content = self._client.get(f"settings/{name}")
        return self._settings_type.model_validate_json(content.text)

    def get_all(self) -> dict[str, SettingsType]:
        content = self._client.get("all-settings").json()
        return {
            name: self._settings_type.model_validate(settings)
            for name, settings in content.items()
        }

    def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        content = self._client.get("all-settings-metadata").json()
        return {
            name: SettingsMetaData.model_validate(metadata)
            for name, metadata in content.items()
        }

    def get_metadata(self, name: str | int) -> SettingsMetaData:
        content = self._client.get(f"settings/{name}/metadata")
        return SettingsMetaData.model_validate_json(content.text)

    def _do_save(self, name: str, settings: SettingsType) -> int:
        content = self._client.post(f"settings/{name}", settings)
        return content.json()

    def _do_update(self, name: str | int, settings: SettingsType) -> SettingsType:
        content = self._client.put(f"settings/{name}", settings)
        return self._settings_type.model_validate_json(content.text)

    def delete(self, name: str | int) -> SettingsType:
        content = self._client.delete(f"settings/{name}")
        return self._settings_type.model_validate_json(content.text)


class AsyncHttpSettingsRegistryClient(
    AsyncSettingsRegistry[SettingsType, SettingsMenuType]
):

    def __init__(
        self,
        client: AsyncApiClient,
        settings_type: type[SettingsType],
        settings_menu_type: type[SettingsMenuType],
    ):
        self._client = client
        self._settings_type = settings_type
        self._settings_menu_type = settings_menu_type

    async def available_settings(self) -> SettingsMenuType:
        content = await self._client.get("available-settings")
        return self._settings_menu_type.model_validate_json(content.text)

    async def ids(self) -> dict[int, str]:
        return {v: k for k, v in (await self.names()).items()}

    async def names(self) -> dict[str, int]:
        return (await self._client.get("settings")).json()

    async def get(self, name: str | int) -> SettingsType:
        content = await self._client.get(f"settings/{name}")
        return self._settings_type.model_validate_json(content.text)

    async def get_all(self) -> dict[str, SettingsType]:
        content = (await self._client.get("all-settings")).json()
        return {
            name: self._settings_type.model_validate(settings)
            for name, settings in content.items()
        }

    async def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        content = (await self._client.get("all-settings-metadata")).json()
        return {
            name: SettingsMetaData.model_validate(metadata)
            for name, metadata in content.items()
        }

    async def get_metadata(self, name: str | int) -> SettingsMetaData:
        content = await self._client.get(f"settings/{name}/metadata")
        return SettingsMetaData.model_validate_json(content.text)

    async def _do_save(self, name: str, settings: SettingsType) -> int:
        content = await self._client.post(f"settings/{name}", settings)
        return content.json()

    async def _do_update(self, name: str | int, settings: SettingsType) -> SettingsType:
        content = await self._client.put(f"settings/{name}", settings)
        return self._settings_type.model_validate_json(content.text)

    async def delete(self, name: str | int) -> SettingsType:
        content = await self._client.delete(f"settings/{name}")
        return self._settings_type.model_validate_json(content.text)
