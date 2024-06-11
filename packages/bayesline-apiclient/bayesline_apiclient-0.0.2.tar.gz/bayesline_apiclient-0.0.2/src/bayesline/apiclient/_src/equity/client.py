import asyncio
import datetime as dt
import importlib.util
import io
from typing import Any

import pandas as pd
from bayesline.api import AsyncSettingsRegistry, SettingsRegistry
from bayesline.api.equity import (AssetExposureApi, AssetUniverseApi,
                                  AsyncAssetExposureApi, AsyncAssetUniverseApi,
                                  AsyncBayeslineEquityApi,
                                  AsyncBayeslineEquityByodApi,
                                  AsyncBayeslineEquityExposureApi,
                                  AsyncBayeslineEquityUniverseApi,
                                  AsyncBayeslineFactorRiskModelsApi,
                                  AsyncBayeslineModelConstructionApi,
                                  AsyncBayeslinePortfolioReportApi,
                                  AsyncByodApi, AsyncFactorRiskEngineApi,
                                  AsyncFactorRiskModelApi,
                                  AsyncModelConstructionEngineApi,
                                  AsyncPortfolioReportApi, BayeslineEquityApi,
                                  BayeslineEquityByodApi,
                                  BayeslineEquityExposureApi,
                                  BayeslineEquityUniverseApi,
                                  BayeslineFactorRiskModelsApi,
                                  BayeslineModelConstructionApi,
                                  BayeslinePortfolioReportApi, ByodApi,
                                  ByodSettings, ByodSettingsMenu,
                                  ExposureSettings, ExposureSettingsMenu,
                                  FactorRiskEngineApi, FactorRiskModelApi,
                                  FactorRiskModelSettings,
                                  FactorRiskModelSettingsMenu, FactorType,
                                  InferAssetIdException,
                                  ModelConstructionEngineApi,
                                  ModelConstructionSettings,
                                  ModelConstructionSettingsMenu,
                                  PortfolioReportApi, ReportSettings,
                                  ReportSettingsMenu, UniverseSettings,
                                  UniverseSettingsMenu)
from bayesline.api.types import DataFrameFormat, DateLike, IdType

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.settings import (AsyncHttpSettingsRegistryClient,
                                               HttpSettingsRegistryClient)

tqdm = lambda x: x  # noqa: E731
if importlib.util.find_spec("tqdm"):
    from tqdm import tqdm  # type: ignore


class BayeslineAssetUniverseApiClient(AssetUniverseApi):

    def __init__(
        self,
        client: ApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
    ):
        self._client = client
        self._universe_settings = universe_settings
        self._id_types = id_types

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    def coverage(self, id_type: IdType | None = None) -> list[str]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = self._client.post(
            "coverage",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        return response.json()

    def dates(self, *, range_only: bool = False) -> list[dt.date]:
        response = self._client.post(
            "dates",
            params={"range_only": range_only},
            json=self._universe_settings.model_dump(),
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    def daily_counts(
        self,
        id_type: IdType | None = None,
    ) -> pd.Series:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = self._client.post(
            "daily-counts",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        result = pd.Series(response.json())
        result.index.name = "date"
        result.name = "count"

        return result

    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        df_format: DataFrameFormat = "unstacked",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        response = self._client.post(
            "",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        df.set_index(list(df.columns[:2]), inplace=True)
        df = df.assign(value=1.0)

        if df_format == "stacked":
            return df
        else:
            return df["value"].unstack()


class AsyncBayeslineAssetUniverseApiClient(AsyncAssetUniverseApi):

    def __init__(
        self,
        client: AsyncApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
    ):
        self._client = client
        self._universe_settings = universe_settings
        self._id_types = id_types

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    async def coverage(self, id_type: IdType | None = None) -> list[str]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = await self._client.post(
            "coverage",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        return response.json()

    async def dates(self, *, range_only: bool = False) -> list[dt.date]:
        response = await self._client.post(
            "dates",
            params={"range_only": range_only},
            json=self._universe_settings.model_dump(),
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    async def daily_counts(
        self,
        id_type: IdType | None = None,
    ) -> pd.Series:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = await self._client.post(
            "daily-counts",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        result = pd.Series(response.json())
        result.index.name = "date"
        result.name = "count"

        return result

    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        df_format: DataFrameFormat = "unstacked",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        response = await self._client.post(
            "",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        df.set_index(list(df.columns[:2]), inplace=True)
        df = df.assign(value=1.0)

        if df_format == "stacked":
            return df
        else:
            return df["value"].unstack()


class BayeslineEquityUniverseApiClient(BayeslineEquityUniverseApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("universe")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            UniverseSettings,
            UniverseSettingsMenu,
        )

    @property
    def settings(self) -> SettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | UniverseSettings) -> AssetUniverseApi:
        id_types = self._settings.available_settings().id_types

        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return BayeslineAssetUniverseApiClient(
                self._client, ref_or_settings, id_types
            )
        else:
            universe_settings = self.settings.get(ref_or_settings)
            return BayeslineAssetUniverseApiClient(
                self._client,
                universe_settings,
                id_types,
            )


class AsyncBayeslineEquityUniverseApiClient(AsyncBayeslineEquityUniverseApi):
    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("universe")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            UniverseSettings,
            UniverseSettingsMenu,
        )

    @property
    def settings(self) -> AsyncSettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | UniverseSettings
    ) -> AsyncAssetUniverseApi:
        settings_menu = await self._settings.available_settings()
        id_types = settings_menu.id_types

        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu.validate_settings(ref_or_settings)
            return AsyncBayeslineAssetUniverseApiClient(
                self._client, ref_or_settings, id_types
            )
        else:
            universe_settings = await self.settings.get(ref_or_settings)
            return AsyncBayeslineAssetUniverseApiClient(
                self._client,
                universe_settings,
                id_types,
            )


class BayeslineAssetExposureApiClient(AssetExposureApi):

    def __init__(
        self,
        client: ApiClient,
        exposure_settings: ExposureSettings,
        id_types: list[IdType],
        universe_api: BayeslineEquityUniverseApi,
    ):
        self._client = client
        self._exposure_settings = exposure_settings
        self._id_types = id_types
        self._universe_api = universe_api

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    def dates(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = self._client.post(
            "dates",
            params={"range_only": range_only},
            json={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    def get(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
        }

        response = self._client.post(
            "",
            params=params,
            json=body,
        )

        def _read_df(r: Any) -> pd.DataFrame:
            return pd.read_parquet(io.BytesIO(r.content), engine="pyarrow")

        if response.headers["content-type"] == "application/json":
            df = pd.concat(
                _read_df(self._client.post(page, json=body, absolute_url=True))
                for page in tqdm(response.json()["urls"])
            )
        else:
            df = _read_df(response)

        df.set_index(list(df.columns[:2]), inplace=True)
        df.columns = pd.MultiIndex.from_tuples(
            df.columns.str.split(".").to_list(), names=["factor_group", "factor"]  # type: ignore
        )

        return df


class AsyncBayeslineAssetExposureApiClient(AsyncAssetExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        exposure_settings: ExposureSettings,
        id_types: list[IdType],
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client
        self._exposure_settings = exposure_settings
        self._id_types = id_types
        self._universe_api = universe_api

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    async def dates(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = await self._client.post(
            "dates",
            params={"range_only": range_only},
            json={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    async def get(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        dummies: bool = False,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
        }

        response = await self._client.post(
            "",
            params=params,
            json=body,
        )

        def _read_df(r: Any) -> pd.DataFrame:
            return pd.read_parquet(io.BytesIO(r.content), engine="pyarrow")

        if response.headers["content-type"] == "application/json":
            tasks = []
            pages = response.json()["urls"]
            results = []
            tasks = [
                self._client.post(page, json=body, absolute_url=True) for page in pages
            ]
            results.extend(await asyncio.gather(*tasks))

            df = pd.concat(_read_df(r) for r in results)
        else:
            df = _read_df(response)

        df.set_index(list(df.columns[:2]), inplace=True)

        if dummies:
            if "industry" in df.columns:
                df = pd.concat(
                    [df, pd.get_dummies(df["industry"], prefix="industry")], axis=1
                )
                df.drop(columns=["industry"], inplace=True)

            if "region" in df.columns:
                df = pd.concat(
                    [df, pd.get_dummies(df["region"], prefix="region")], axis=1
                )
                df.drop(columns=["region"], inplace=True)

        return df


class BayeslineEquityExposureApiClient(BayeslineEquityExposureApi):

    def __init__(self, client: ApiClient, universe_api: BayeslineEquityUniverseApi):
        self._client = client.append_base_path("exposures")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api

    @property
    def settings(self) -> SettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | ExposureSettings) -> AssetExposureApi:
        id_types = self._universe_api.settings.available_settings().id_types

        if isinstance(ref_or_settings, ExposureSettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return BayeslineAssetExposureApiClient(
                self._client,
                ref_or_settings,
                id_types,
                self._universe_api,
            )
        else:
            exposure_settings = self.settings.get(ref_or_settings)
            return BayeslineAssetExposureApiClient(
                self._client,
                exposure_settings,
                id_types,
                self._universe_api,
            )


class AsyncBayeslineEquityExposureApiClient(AsyncBayeslineEquityExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("exposures")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api

    @property
    def settings(self) -> AsyncSettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ExposureSettings
    ) -> AsyncAssetExposureApi:
        id_types = (await self._universe_api.settings.available_settings()).id_types

        if isinstance(ref_or_settings, ExposureSettings):
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return AsyncBayeslineAssetExposureApiClient(
                self._client, ref_or_settings, id_types, self._universe_api
            )
        else:
            exposure_settings = await self.settings.get(ref_or_settings)
            return AsyncBayeslineAssetExposureApiClient(
                self._client,
                exposure_settings,
                id_types,
                self._universe_api,
            )


class FactorRiskModelApiClient(FactorRiskModelApi):

    def __init__(
        self,
        client: ApiClient,
        model_id: int,
        settings: FactorRiskModelSettings,
        asset_exposures: AssetExposureApi,
    ):
        self._client = client
        self._model_id = model_id
        self._settings = settings
        self._asset_exposures = asset_exposures

    def dates(self) -> list[dt.date]:
        response = self._client.get(f"model/{self._model_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    def factors(self, *which: FactorType) -> list[str]:
        response = self._client.get(
            f"model/{self._model_id}/factors",
            params={"which": list(which)},
        )
        return response.json()

    def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        return self._asset_exposures.get(
            self._settings.universe,
            start=start,
            end=end,
            id_type=id_type,
        )

    def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pd.DataFrame:
        response = self._client.get(
            f"model/{self._model_id}/market-stats",
            params={
                "estimation_universe": estimation_universe,
                "industries": industries,
                "regions": regions,
            },
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def t_stats(self) -> pd.DataFrame:
        response = self._client.get(f"model/{self._model_id}/t-stats")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def p_values(self) -> pd.DataFrame:
        response = self._client.get(f"model/{self._model_id}/p-values")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def r2(self) -> pd.Series:
        response = self._client.get(f"model/{self._model_id}/r2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    def sigma2(self) -> pd.Series:
        response = self._client.get(f"model/{self._model_id}/sigma2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = self._client.get(
            f"model/{self._model_id}/style-correlation",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = self._client.get(
            f"model/{self._model_id}/industry-exposures",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def fcov(
        self,
        start: DateLike | int | None = -1,
        end: DateLike | int | None = None,
        dates: list[DateLike] | None = None,
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            if not isinstance(start, int):
                params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
            else:
                params["start"] = start  # type: ignore

        if end is not None:
            if not isinstance(end, int):
                params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
            else:
                params["end"] = end  # type: ignore

        body = {"dates": None}
        if dates is not None:
            body["dates"] = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in dates]  # type: ignore

        response = self._client.post(
            f"model/{self._model_id}/fcov", params=params, json=body
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if freq is not None:
            params["freq"] = freq
        if cumulative:
            params["cumulative"] = cumulative
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = self._client.get(
            f"model/{self._model_id}/fret",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class AsyncFactorRiskModelApiClient(AsyncFactorRiskModelApi):

    def __init__(
        self,
        client: AsyncApiClient,
        model_id: int,
        settings: FactorRiskModelSettings,
        asset_exposures: AsyncAssetExposureApi,
    ):
        self._client = client
        self._model_id = model_id
        self._settings = settings
        self._asset_exposures = asset_exposures

    async def dates(self) -> list[dt.date]:
        response = await self._client.get(f"model/{self._model_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    async def factors(self, *which: FactorType) -> list[str]:
        response = await self._client.get(
            f"model/{self._model_id}/factors",
            params={"which": list(which)},
        )
        return response.json()

    async def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        return await self._asset_exposures.get(
            self._settings.universe,
            start=start,
            end=end,
            id_type=id_type,
        )

    async def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pd.DataFrame:
        response = await self._client.get(
            f"model/{self._model_id}/market-stats",
            params={
                "estimation_universe": estimation_universe,
                "industries": industries,
                "regions": regions,
            },
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def t_stats(self) -> pd.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/t-stats")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def p_values(self) -> pd.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/p-values")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def r2(self) -> pd.Series:
        response = await self._client.get(f"model/{self._model_id}/r2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    async def sigma2(self) -> pd.Series:
        response = await self._client.get(f"model/{self._model_id}/sigma2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    async def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = await self._client.get(
            f"model/{self._model_id}/style-correlation",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = await self._client.get(
            f"model/{self._model_id}/industry-exposures",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def fcov(
        self,
        start: DateLike | int | None = -1,
        end: DateLike | int | None = None,
        dates: list[DateLike] | None = None,
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            if not isinstance(start, int):
                params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
            else:
                params["start"] = start  # type: ignore

        if end is not None:
            if not isinstance(end, int):
                params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
            else:
                params["end"] = end  # type: ignore

        body = {"dates": None}
        if dates is not None:
            body["dates"] = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in dates]  # type: ignore

        response = await self._client.post(
            f"model/{self._model_id}/fcov", params=params, json=body
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if freq is not None:
            params["freq"] = freq
        if cumulative:
            params["cumulative"] = cumulative
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = await self._client.get(
            f"model/{self._model_id}/fret",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class ModelConstructionEngineApiClient(ModelConstructionEngineApi):

    def __init__(
        self,
        client: ApiClient,
        settings: ModelConstructionSettings,
    ):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> ModelConstructionSettings:
        return self._settings


class AsyncModelConstructionEngineApiClient(AsyncModelConstructionEngineApi):

    def __init__(
        self,
        client: AsyncApiClient,
        settings: ModelConstructionSettings,
    ):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> ModelConstructionSettings:
        return self._settings


class FactorRiskEngineApiClient(FactorRiskEngineApi):

    def __init__(
        self,
        client: ApiClient,
        settings: FactorRiskModelSettings,
        asset_exposures: AssetExposureApi,
        model_id: int | None = None,
    ):
        self._client = client
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._model_id = model_id

    @property
    def settings(self) -> FactorRiskModelSettings:
        return self._settings

    def get(self) -> FactorRiskModelApi:
        if self._model_id is None:
            self._model_id = self._client.post(
                "model", json=self._settings.model_dump()
            ).json()

        return FactorRiskModelApiClient(
            self._client, self._model_id, self._settings, self._asset_exposures  # type: ignore
        )


class AsyncFactorRiskEngineApiClient(AsyncFactorRiskEngineApi):

    def __init__(
        self,
        client: AsyncApiClient,
        settings: FactorRiskModelSettings,
        asset_exposures: AsyncAssetExposureApi,
        model_id: int | None = None,
    ):
        self._client = client
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._model_id = model_id

    @property
    def settings(self) -> FactorRiskModelSettings:
        return self._settings

    async def get(self) -> AsyncFactorRiskModelApi:
        if self._model_id is None:
            self._model_id = (
                await self._client.post("model", json=self._settings.model_dump())
            ).json()

        return AsyncFactorRiskModelApiClient(
            self._client, self._model_id, self._settings, self._asset_exposures
        )


class PortfolioReportApiClient(PortfolioReportApi):

    def __init__(self, client: ApiClient, report_id: str, settings: ReportSettings):
        self._client = client
        self._report_id = report_id
        self._settings = settings
        self._settings = settings

    @property
    def settings(self) -> ReportSettings:
        return self._settings

    def get_report(
        self,
        date: DateLike,
        *,
        holdings_overrides: dict[str, float] | None = None,
        extra_cols: list[str] | None = None,
        append_total: bool = True,
        append_subtotals: bool = True,
    ) -> pd.DataFrame:
        holdings_overrides = holdings_overrides or {}
        response = self._client.post(
            self._report_id,
            json=holdings_overrides,
            params={
                "date": date,
                "extra_cols": extra_cols or [],
                "append_total": append_total,
                "append_subtotals": append_subtotals,
            },
        )
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

        return df

    def dates(self) -> list[dt.date]:
        response = self._client.get(f"{self._report_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]


class AsyncPortfolioReportApiClient(AsyncPortfolioReportApi):

    def __init__(
        self, client: AsyncApiClient, report_id: str, settings: ReportSettings
    ):
        self._client = client
        self._report_id = report_id
        self._settings = settings

    @property
    def settings(self) -> ReportSettings:
        return self._settings

    async def get_report(
        self,
        date: DateLike,
        *,
        holdings_overrides: dict[str, float] | None = None,
        extra_cols: list[str] | None = None,
        append_total: bool = True,
        append_subtotals: bool = True,
    ) -> pd.DataFrame:
        holdings_overrides = holdings_overrides or {}
        response = await self._client.post(
            self._report_id,
            json=holdings_overrides,
            params={
                "date": date,
                "extra_cols": extra_cols,
                "append_total": append_total,
                "append_subtotals": append_subtotals,
            },
        )
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df

    async def dates(self) -> list[dt.date]:
        response = await self._client.get(f"{self._report_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]


class BayeslineModelConstructionApiClient(BayeslineModelConstructionApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("modelconstruction")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            ModelConstructionSettings,
            ModelConstructionSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[ModelConstructionSettings, ModelConstructionSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | ModelConstructionSettings
    ) -> ModelConstructionEngineApi:
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
            return ModelConstructionEngineApiClient(self._client, settings)
        else:
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            return ModelConstructionEngineApiClient(self._client, settings_obj)


class AsyncBayeslineModelConstructionApiClient(AsyncBayeslineModelConstructionApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("modelconstruction")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            ModelConstructionSettings,
            ModelConstructionSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[
        ModelConstructionSettings, ModelConstructionSettingsMenu
    ]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ModelConstructionSettings
    ) -> AsyncModelConstructionEngineApi:
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
            return AsyncModelConstructionEngineApiClient(self._client, settings)
        else:
            ref = ref_or_settings
            settings_obj = await self.settings.get(ref)
            return AsyncModelConstructionEngineApiClient(self._client, settings_obj)


class BayeslineFactorRiskModelsApiClient(BayeslineFactorRiskModelsApi):

    def __init__(self, client: ApiClient, exposure_api: BayeslineEquityExposureApi):
        self._client = client.append_base_path("riskmodels")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            FactorRiskModelSettings,
            FactorRiskModelSettingsMenu,
        )
        self._exposure_api = exposure_api

    @property
    def settings(
        self,
    ) -> SettingsRegistry[FactorRiskModelSettings, FactorRiskModelSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | FactorRiskModelSettings
    ) -> FactorRiskEngineApi:
        if isinstance(ref_or_settings, FactorRiskModelSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
            asset_exposures = self._exposure_api.load(settings.exposures)
            return FactorRiskEngineApiClient(self._client, settings, asset_exposures)
        else:
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            if isinstance(ref, str):
                model_id = self.settings.names()[ref]
            else:
                model_id = ref
            asset_exposures = self._exposure_api.load(settings_obj.exposures)
            return FactorRiskEngineApiClient(
                self._client, settings_obj, asset_exposures, model_id
            )


class AsyncBayeslineFactorRiskModelsApiClient(AsyncBayeslineFactorRiskModelsApi):

    def __init__(
        self,
        client: AsyncApiClient,
        exposure_api: AsyncBayeslineEquityExposureApi,
    ):
        self._client = client.append_base_path("riskmodels")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            FactorRiskModelSettings,
            FactorRiskModelSettingsMenu,
        )
        self._exposure_api = exposure_api

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[FactorRiskModelSettings, FactorRiskModelSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | FactorRiskModelSettings
    ) -> AsyncFactorRiskEngineApi:
        if isinstance(ref_or_settings, FactorRiskModelSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
            asset_exposures = await self._exposure_api.load(settings.exposures)
            return AsyncFactorRiskEngineApiClient(
                self._client, settings, asset_exposures
            )
        else:
            ref = ref_or_settings
            settings_obj = await self.settings.get(ref)
            if isinstance(ref, str):
                names = await self.settings.names()
                model_id = names[ref]
            else:
                model_id = ref
            asset_exposures = await self._exposure_api.load(settings_obj.exposures)
            return AsyncFactorRiskEngineApiClient(
                self._client, settings_obj, asset_exposures, model_id
            )


class BayeslinePortfolioReportApiClient(BayeslinePortfolioReportApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("portfolioreport")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            ReportSettings,
            ReportSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[ReportSettings, ReportSettingsMenu]:
        return self._settings

    def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        id_type: IdType,
        portfolio_df: pd.DataFrame,
    ) -> PortfolioReportApi:
        if isinstance(ref_or_settings, ReportSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
        else:
            ref = ref_or_settings
            settings = self.settings.get(ref)

        portfolio_df = portfolio_df.copy()
        portfolio_df.index = portfolio_df.index.astype(str)

        response = self._client.post(
            "/report",
            json={
                "settings": settings.model_dump(),
                "id_type": id_type,
                "portfolio": portfolio_df.to_dict(),
            },
        )
        report_id = response.content.decode("utf-8")
        return PortfolioReportApiClient(self._client, report_id, settings)


class AsyncBayeslinePortfolioReportApiClient(AsyncBayeslinePortfolioReportApi):
    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("portfolioreport")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            ReportSettings,
            ReportSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[ReportSettings, ReportSettingsMenu]:
        return self._settings

    async def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        id_type: IdType,
        portfolio_df: pd.DataFrame,
    ) -> AsyncPortfolioReportApi:
        if isinstance(ref_or_settings, ReportSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
        else:
            ref = ref_or_settings
            settings = await self.settings.get(ref)

        portfolio_df = portfolio_df.copy()
        portfolio_df.index = portfolio_df.index.astype(str)

        response = await self._client.post(
            "/report",
            json={
                "settings": settings.model_dump(),
                "id_type": id_type,
                "portfolio": portfolio_df.to_dict(),
            },
        )
        report_id = response.content.decode("utf-8")
        return AsyncPortfolioReportApiClient(self._client, report_id, settings)


class ByodApiClient(ByodApi):

    def __init__(self, client: ApiClient, identifier: int, settings: ByodSettings):
        self._client = client
        self._identifier = identifier
        self._settings = settings

    @property
    def settings(self) -> ByodSettings:
        return self._settings

    def is_uploaded(self) -> bool:
        response = self._client.get(f"{self._identifier}")
        return response.json()["is_uploaded"]

    def get_raw(self) -> pd.DataFrame:
        response = self._client.get(f"{self._identifier}/raw")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        if id_type is not None:
            params["id_type"] = id_type

        response = self._client.get(f"{self._identifier}/processed", params=params)
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def upload(self, df: pd.DataFrame, overwrite: bool = False) -> None:
        if self.is_uploaded() and not overwrite:
            raise ValueError(
                "Data has already been uploaded. Set overwrite=True to re-upload."
            )
        out = io.BytesIO()
        df.to_parquet(out, engine="pyarrow")
        self._client.post(f"{self._identifier}/upload", data=out.getvalue(), json=None)


class AsyncByodApiClient(AsyncByodApi):

    def __init__(self, client: AsyncApiClient, identifier: int, settings: ByodSettings):
        self._client = client
        self._identifier = identifier
        self._settings = settings

    @property
    def settings(self) -> ByodSettings:
        return self._settings

    async def is_uploaded(self) -> bool:
        response = await self._client.get(f"{self._identifier}")
        return response.json()["is_uploaded"]

    async def get_raw(self) -> pd.DataFrame:
        response = await self._client.get(f"{self._identifier}/raw")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        if id_type is not None:
            params["id_type"] = id_type

        response = await self._client.get(
            f"{self._identifier}/processed", params=params
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def upload(self, df: pd.DataFrame, overwrite: bool = False) -> None:
        if await self.is_uploaded() and not overwrite:
            raise ValueError(
                "Data has already been uploaded. Set overwrite=True to re-upload."
            )
        out = io.BytesIO()
        df.to_parquet(out, engine="pyarrow")
        await self._client.post(
            f"{self._identifier}/upload", data=out.getvalue(), json=None
        )


class BayeslineEquityByodApiClient(BayeslineEquityByodApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("byod")
        self._settings = HttpSettingsRegistryClient(
            self._client, ByodSettings, ByodSettingsMenu
        )

    @property
    def settings(self) -> SettingsRegistry[ByodSettings, ByodSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | ByodSettings, *, name: str | None = None
    ) -> ByodApi:
        if isinstance(ref_or_settings, ByodSettings):
            settings = ref_or_settings

            if name is None:
                raise ValueError("Must provide a name when using inline byod settings.")
            identifier = self.settings.save(name, settings)
        else:
            settings = self.settings.get(ref_or_settings)

            if isinstance(ref_or_settings, str):
                name = ref_or_settings
                identifier = self.settings.names()[ref_or_settings]
            else:
                name = self.settings.ids()[ref_or_settings]
                identifier = ref_or_settings

        settings_menu = self.settings.available_settings()
        settings_menu.validate_settings(settings)

        return ByodApiClient(self._client, identifier, settings)

    def generate_settings(
        self,
        df: pd.DataFrame,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        try:
            return super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=asset_id_col,
                asset_id_type=asset_id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
        except InferAssetIdException as e:
            id_cols = {col: list(df[col].drop_duplicates()) for col in e.id_cols}
            id_types = e.id_types
            inferred_ids = self._client.post(
                "infer-id-type", json=id_cols, params={"id_types": id_types}
            ).json()
            id_col, id_type = inferred_ids["id_col"], inferred_ids["id_type"]
            if id_type is None or id_col is None:
                raise ValueError("No matching id type/column found")
            return super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=id_col,
                asset_id_type=id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )


class AsyncBayeslineEquityByodApiClient(AsyncBayeslineEquityByodApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("byod")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client, ByodSettings, ByodSettingsMenu
        )

    @property
    def settings(self) -> AsyncSettingsRegistry[ByodSettings, ByodSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ByodSettings, *, name: str | None = None
    ) -> AsyncByodApi:
        if isinstance(ref_or_settings, ByodSettings):
            settings = ref_or_settings

            if name is None:
                raise ValueError("Must provide a name when using inline byod settings.")
            identifier = await self.settings.save(name, settings)
        else:
            settings = await self.settings.get(ref_or_settings)

            if isinstance(ref_or_settings, str):
                name = ref_or_settings
                identifier = (await self.settings.names())[ref_or_settings]
            else:
                name = (await self.settings.ids())[ref_or_settings]
                identifier = ref_or_settings

        settings_menu = await self.settings.available_settings()
        settings_menu.validate_settings(settings)

        return AsyncByodApiClient(self._client, identifier, settings)

    async def generate_settings(
        self,
        df: pd.DataFrame,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        try:
            return await super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=asset_id_col,
                asset_id_type=asset_id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
        except InferAssetIdException as e:
            id_cols = {col: list(df[col].drop_duplicates()) for col in e.id_cols}
            id_types = e.id_types
            inferred_ids = (
                await self._client.post(
                    "infer-id-type", json=id_cols, params={"id_types": id_types}
                )
            ).json()
            id_col, id_type = inferred_ids["id_col"], inferred_ids["id_type"]
            if id_type is None or id_col is None:
                raise ValueError("No matching id type/column found")
            return await super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=id_col,
                asset_id_type=id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )


class BayeslineEquityApiClient(BayeslineEquityApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("equity")
        self._universe_client = BayeslineEquityUniverseApiClient(self._client)
        self._exposure_client = BayeslineEquityExposureApiClient(
            self._client,
            self._universe_client,
        )
        self._modelconstruction_client = BayeslineModelConstructionApiClient(
            self._client
        )
        self._factorrisk_client = BayeslineFactorRiskModelsApiClient(
            self._client, self._exposure_client
        )
        self._portfolioreport_client = BayeslinePortfolioReportApiClient(self._client)
        self._byod_client = BayeslineEquityByodApiClient(self._client)

    @property
    def universes(self) -> BayeslineEquityUniverseApi:
        return self._universe_client

    @property
    def exposures(self) -> BayeslineEquityExposureApi:
        return self._exposure_client

    @property
    def modelconstruction(self) -> BayeslineModelConstructionApi:
        return self._modelconstruction_client

    @property
    def riskmodels(self) -> BayeslineFactorRiskModelsApi:
        return self._factorrisk_client

    @property
    def portfolioreport(self) -> BayeslinePortfolioReportApi:
        return self._portfolioreport_client

    @property
    def byod(self) -> BayeslineEquityByodApi:
        return self._byod_client


class AsyncBayeslineEquityApiClient(AsyncBayeslineEquityApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("equity")
        self._universe_client = AsyncBayeslineEquityUniverseApiClient(self._client)

        self._exposure_client = AsyncBayeslineEquityExposureApiClient(
            self._client, self._universe_client
        )
        self._modelconstruction_client = AsyncBayeslineModelConstructionApiClient(
            self._client
        )
        self._factorrisk_client = AsyncBayeslineFactorRiskModelsApiClient(
            self._client, self._exposure_client
        )
        self._portfolioreport_client = AsyncBayeslinePortfolioReportApiClient(
            self._client
        )
        self._byod_client = AsyncBayeslineEquityByodApiClient(self._client)

    @property
    def universes(self) -> AsyncBayeslineEquityUniverseApi:
        return self._universe_client

    @property
    def exposures(self) -> AsyncBayeslineEquityExposureApi:
        return self._exposure_client

    @property
    def modelconstruction(self) -> AsyncBayeslineModelConstructionApi:
        return self._modelconstruction_client

    @property
    def riskmodels(self) -> AsyncBayeslineFactorRiskModelsApi:
        return self._factorrisk_client

    @property
    def portfolioreport(self) -> AsyncBayeslinePortfolioReportApi:
        return self._portfolioreport_client

    @property
    def byod(self) -> AsyncBayeslineEquityByodApi:
        return self._byod_client


def _check_and_add_id_type(
    id_types: list[IdType],
    id_type: IdType | None,
    params: dict[str, Any],
) -> None:
    if id_type is not None:
        if id_type not in id_types:
            raise ValueError(f"given id type {id_type} is not supported")
        params["id_type"] = id_type
