import os

from pydantic import BaseModel, Field

from bayesline.api._src.equity.exposure_settings import ExposureSettings
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
)
from bayesline.api._src.equity.universe_settings import UniverseSettings
from bayesline.api._src.registry import SettingsMenu


class FactorRiskModelSettings(BaseModel, frozen=True, extra="forbid"):
    """
    Defines all settings needed to build a factor risk model.
    """

    @classmethod
    def default(cls) -> "FactorRiskModelSettings":
        return cls(
            universe=UniverseSettings.default(),
            exposures=ExposureSettings.default(),
            modelconstruction=ModelConstructionSettings.default(),
        )

    universe: str | int | UniverseSettings = Field(
        description="The universe to build the factor risk model on.",
        default_factory=UniverseSettings.default,
    )

    exposures: str | int | ExposureSettings = Field(
        description="The exposures to build the factor risk model on.",
        default_factory=ExposureSettings.default,
    )

    modelconstruction: str | int | ModelConstructionSettings = Field(
        description="The model construction settings to use for the factor risk model.",
        default_factory=ModelConstructionSettings.default,
    )


class FactorRiskModelSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """
    Defines available settings to build a factor risk model.
    """

    # nothing here yet

    def describe(self, settings: FactorRiskModelSettings | None = None) -> str:
        if settings:
            result = [
                "Universe: " + str(settings.universe),
                "Exposures: " + str(settings.exposures),
                "Model Construction: " + str(settings.modelconstruction),
            ]
            return os.linesep.join(result)
        else:
            return "This settings menu has no description."

    def validate_settings(self, settings: FactorRiskModelSettings) -> None:
        pass
