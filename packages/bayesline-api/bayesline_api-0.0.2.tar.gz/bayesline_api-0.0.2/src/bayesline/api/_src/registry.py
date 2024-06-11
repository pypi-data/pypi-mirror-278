import abc
import datetime as dt
import re
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")
SettingsType = TypeVar("SettingsType", bound=BaseModel)


class SettingsMetaData(BaseModel, frozen=True, extra="allow"):

    created_on: dt.datetime
    last_updated: dt.datetime


class SettingsMenu(
    abc.ABC,
    BaseModel,
    Generic[SettingsType],
    frozen=True,
    extra="forbid",
):

    @abc.abstractmethod
    def describe(self, settings: SettingsType | None = None) -> str:
        """
        Parameters
        ----------
        settings : SettingsType | None
                   The settings to describe.
                   If None, then the description is not evaluated against any settings.

        Returns
        -------
        A human readable description of the settings menu,
        optionally evaluated against the given settings.
        """

    @abc.abstractmethod
    def validate_settings(self, settings: SettingsType) -> None:
        """
        Validates if the given settings are valid for this settings menu.

        Parameters
        ----------
        settings : SettingsType
                   The settings to validate.

        Raises
        ------
        ValidationError if invalid.
        """


SettingsMenuType = TypeVar("SettingsMenuType", bound=SettingsMenu)


class Registry(abc.ABC, Generic[T]):

    @abc.abstractmethod
    def ids(self) -> dict[int, str]:
        """
        Returns
        -------
        A dictionary of the unique identifiers to the unique names.
        """

    @abc.abstractmethod
    def names(self) -> dict[str, int]:
        """
        Returns
        -------
        A dictionary of the unique names to the unique identifiers.
        """

    @abc.abstractmethod
    def get(self, name: str | int) -> T:
        """
        Parameters
        ----------
        name : str | int
               The unique name or int identifier of the item to retrieve.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The item for the given name.
        """

    @abc.abstractmethod
    def get_metadata(self, name: str | int) -> SettingsMetaData:
        """
        Parameters
        ----------
        name : str | int
               The unique name or int identifier of the item to retrieve.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The metadata for the given name.
        """

    def get_all(self) -> dict[str, T]:
        """
        Returns
        -------
        A dictionary of all available settings.
        """
        return {name: self.get(name) for name in self.names()}

    def get_all_with_metadata(self) -> dict[str, tuple[T, SettingsMetaData]]:
        """
        Returns
        -------
        A dictionary of all available settings with metadata.
        """
        all_settings = self.get_all()
        all_metadata = self.get_all_metadata()

        return {
            name: (all_settings[name], all_metadata[name])
            for name in all_settings.keys()
        }

    def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        """
        Returns
        -------
        A dictionary of all available settings metadata.
        """
        return {name: self.get_metadata(name) for name in self.names()}

    @abc.abstractmethod
    def save(self, name: str, settings: T) -> int:
        """
        Parameters
        ----------
        name     : str
                   The unique name of the item to save.
                   The name cannot be all numbers.
        settings : T
                   The item to save.

        Raises
        ------
        ValueError
            If the item name already exists or is all numbers.

        Returns
        -------
        a unique identifier for the saved item.
        """

    @abc.abstractmethod
    def update(self, name: str | int, settings: T) -> T:
        """
        Parameters
        ----------
        name     : str | int
                   The unique name or int identifier of the item to update.
        settings : T
                   The item to update.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The previous item for the given name.
        """

    @abc.abstractmethod
    def delete(self, name: str | int) -> T:
        """
        Parameters
        ----------
        name : str | int
               The unique name or int identifier of the settings to delete.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The deleted item for the given name.
        """


class AsyncRegistry(abc.ABC, Generic[T]):

    @abc.abstractmethod
    async def ids(self) -> dict[int, str]:
        """
        Returns
        -------
        A dictionary of the unique identifiers to the unique names.
        """

    @abc.abstractmethod
    async def names(self) -> dict[str, int]:
        """
        Returns
        -------
        A dictionary of the unique names to the unique identifiers.
        """

    @abc.abstractmethod
    async def get(self, name: str | int) -> T:
        """
        Parameters
        ----------
        name : str | int
               The unique name or int identifier of the item to retrieve.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The item for the given name.
        """

    @abc.abstractmethod
    async def get_metadata(self, name: str | int) -> SettingsMetaData:
        """
        Parameters
        ----------
        name : str | int
               The unique name or int identifier of the item to retrieve.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The metadata for the given name.
        """

    async def get_all(self) -> dict[str, T]:
        """
        Returns
        -------
        A dictionary of all available settings.
        """
        return {name: await self.get(name) for name in await self.names()}

    async def get_all_with_metadata(self) -> dict[str, tuple[T, SettingsMetaData]]:
        """
        Returns
        -------
        A dictionary of all available settings with metadata.
        """
        all_settings = await self.get_all()
        all_metadata = await self.get_all_metadata()

        return {
            name: (all_settings[name], all_metadata[name])
            for name in all_settings.keys()
        }

    async def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        """
        Returns
        -------
        A dictionary of all available settings metadata.
        """
        return {name: await self.get_metadata(name) for name in await self.names()}

    @abc.abstractmethod
    async def save(self, name: str, settings: T) -> int:
        """
        Parameters
        ----------
        name     : str
                   The unique name of the item to save.
                   The name cannot be all numbers.
        settings : T
                   The item to save.

        Raises
        ------
        ValueError
            If the item name already exists or is all numbers.

        Returns
        -------
        a unique identifier for the saved item.
        """

    @abc.abstractmethod
    async def update(self, name: str | int, settings: T) -> T:
        """
        Parameters
        ----------
        name     : str | int
                   The unique name or int identifier of the item to update.
        settings : T
                   The item to update.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The previous item for the given name.
        """

    @abc.abstractmethod
    async def delete(self, name: str | int) -> T:
        """
        Parameters
        ----------
        name : str | int
               The unique name or int identifier of the settings to delete.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        The deleted item for the given name.
        """


class SettingsRegistry(Registry[SettingsType], Generic[SettingsType, SettingsMenuType]):

    @abc.abstractmethod
    def available_settings(self) -> SettingsMenuType:
        """
        Returns
        -------
        A description of valid settings for this registry.
        """

    def save(self, name: str, settings: SettingsType) -> int:
        if re.sub(r"\d", "", name) == "":
            raise ValueError(
                f"The model model name cannot consist of only numbers: {name}",
            )
        self.available_settings().validate_settings(settings)
        return self._do_save(name, settings)

    @abc.abstractmethod
    def _do_save(self, name: str, settings: SettingsType) -> int: ...

    def update(self, name: str | int, settings: SettingsType) -> SettingsType:
        self.available_settings().validate_settings(settings)
        return self._do_update(name, settings)

    @abc.abstractmethod
    def _do_update(self, name: str | int, settings: SettingsType) -> SettingsType: ...


class AsyncSettingsRegistry(
    AsyncRegistry[SettingsType], Generic[SettingsType, SettingsMenuType]
):

    @abc.abstractmethod
    async def available_settings(self) -> SettingsMenuType:
        """
        Returns
        -------
        A description of valid settings for this registry.
        """

    async def save(self, name: str, settings: SettingsType) -> int:
        if re.sub(r"\d", "", name) == "":
            raise ValueError(
                f"The model model name cannot consist of only numbers: {name}",
            )
        if name in await self.names():
            raise ValueError(f"Name {name} already exists.")
        (await self.available_settings()).validate_settings(settings)
        return await self._do_save(name, settings)

    @abc.abstractmethod
    async def _do_save(self, name: str, settings: SettingsType) -> int: ...

    async def update(self, name: str | int, settings: SettingsType) -> SettingsType:
        (await self.available_settings()).validate_settings(settings)
        return await self._do_update(name, settings)

    @abc.abstractmethod
    async def _do_update(
        self, name: str | int, settings: SettingsType
    ) -> SettingsType: ...


class InMemorySettingsRegistry(SettingsRegistry[SettingsType, SettingsMenuType]):

    def __init__(self, settings_menu: SettingsMenuType):
        self._settings_menu = settings_menu
        self._settings: dict[int, SettingsType] = {}
        self._metadata: dict[int, SettingsMetaData] = {}
        self._id_name_map: dict[int, str] = {}
        self._name_id_map: dict[str, int] = {}
        self._next_id = 0

    def ids(self) -> dict[int, str]:
        return dict(self._id_name_map)

    def names(self) -> dict[str, int]:
        return dict(self._name_id_map)

    def available_settings(self) -> SettingsMenuType:
        return self._settings_menu

    def get(self, name: str | int) -> SettingsType:
        try:
            if isinstance(name, int):
                return self._settings[name]
            return self._settings[self.names()[name]]
        except KeyError as e:
            raise KeyError(f"Could not find settings for input: {name}") from e

    def get_metadata(self, name: str | int) -> SettingsMetaData:
        try:
            if isinstance(name, int):
                return self._metadata[name]
            return self._metadata[self.names()[name]]
        except KeyError as e:
            raise KeyError(f"Could not find settings for input: {name}") from e

    def _do_save(self, name: str, settings: SettingsType) -> int:
        if name in self._name_id_map:
            raise ValueError(f"Settings with name '{name}' already exists.")
        self._settings[self._next_id] = settings
        self._metadata[self._next_id] = SettingsMetaData(
            created_on=dt.datetime.now(tz=dt.timezone.utc),
            last_updated=dt.datetime.now(tz=dt.timezone.utc),
        )
        self._id_name_map[self._next_id] = name
        self._name_id_map[name] = self._next_id
        self._next_id += 1
        return self._next_id - 1

    def _do_update(self, name: str | int, settings: SettingsType) -> SettingsType:
        try:
            if isinstance(name, int):
                previous = self._settings[name]
                self._settings[name] = settings
                self._metadata[name] = self._metadata[name].model_copy(
                    update={"last_updated": dt.datetime.now(tz=dt.timezone.utc)}
                )
                return previous
            idx = self.names()[name]
            previous = self._settings[idx]
            self._settings[idx] = settings
            self._metadata[idx] = self._metadata[idx].model_copy(
                update={"last_updated": dt.datetime.now(tz=dt.timezone.utc)}
            )
            return previous
        except KeyError as e:
            raise KeyError(f"Could not find settings for input: {name}") from e

    def delete(self, name: str | int) -> SettingsType:
        try:
            if isinstance(name, int):
                actual_name = self._id_name_map.pop(name)
                self._name_id_map.pop(actual_name)
                self._metadata.pop(name)
                return self._settings.pop(name)
            idx = self.names()[name]
            self._id_name_map.pop(idx)
            self._name_id_map.pop(name)
            self._metadata.pop(idx)
            return self._settings.pop(idx)
        except KeyError as e:
            raise KeyError(f"Could not find settings for input: {name}") from e


class AsyncInMemorySettingsRegistry(
    AsyncSettingsRegistry[SettingsType, SettingsMenuType]
):

    def __init__(self, settings_menu: SettingsMenuType):
        self._settings_menu = settings_menu
        self._delegate: SettingsRegistry[SettingsType, SettingsMenuType] = (
            InMemorySettingsRegistry[SettingsType, SettingsMenuType](settings_menu)
        )

    async def ids(self) -> dict[int, str]:
        return self._delegate.ids()

    async def names(self) -> dict[str, int]:
        return self._delegate.names()

    async def available_settings(self) -> SettingsMenuType:
        return self._delegate.available_settings()

    async def get(self, name: str | int) -> SettingsType:
        return self._delegate.get(name)

    async def get_metadata(self, name: str | int) -> SettingsMetaData:
        return self._delegate.get_metadata(name)

    async def _do_save(self, name: str, settings: SettingsType) -> int:
        return self._delegate._do_save(name, settings)

    async def _do_update(self, name: str | int, settings: SettingsType) -> SettingsType:
        return self._delegate._do_update(name, settings)

    async def delete(self, name: str | int) -> SettingsType:
        return self._delegate.delete(name)


ApiType = TypeVar("ApiType")


class RegistryBasedApi(abc.ABC, Generic[SettingsType, SettingsMenuType, ApiType]):

    @property
    @abc.abstractmethod
    def settings(self) -> SettingsRegistry[SettingsType, SettingsMenuType]: ...

    @abc.abstractmethod
    def load(
        self, ref_or_settings: str | int | SettingsType, *args: Any, **kwargs: Any
    ) -> ApiType: ...


class AsyncRegistryBasedApi(abc.ABC, Generic[SettingsType, SettingsMenuType, ApiType]):

    @property
    @abc.abstractmethod
    def settings(self) -> AsyncSettingsRegistry[SettingsType, SettingsMenuType]: ...

    @abc.abstractmethod
    async def load(
        self, ref_or_settings: str | int | SettingsType, *args: Any, **kwargs: Any
    ) -> ApiType: ...
