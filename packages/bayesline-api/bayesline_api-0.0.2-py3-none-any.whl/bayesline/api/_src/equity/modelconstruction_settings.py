from typing import Literal

from pydantic import BaseModel, Field

from bayesline.api._src.registry import SettingsMenu

WeightingScheme = Literal["SqrtCap"]


class ModelConstructionSettings(BaseModel, frozen=True, extra="forbid"):
    """
    Defines settings to build a factor risk model.
    """

    @classmethod
    def default(cls) -> "ModelConstructionSettings":
        return cls(weights="SqrtCap")

    weights: WeightingScheme = Field(
        description="The regression weights used for the factor risk model.",
        default="SqrtCap",
        examples=["SqrtCap"],
    )


class ModelConstructionSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """
    Defines available modelconstruction settings to build a factor risk model.
    """

    weights: list[WeightingScheme] = Field(
        description="""
        The available regression weights that can be used for the factor risk model.
        """,
    )

    def describe(self, settings: ModelConstructionSettings | None = None) -> str:
        if settings is not None:
            return f"Weights: {settings.weights}"
        else:
            return f"Weights: {', '.join(self.weights)}"

    def validate_settings(self, settings: ModelConstructionSettings) -> None:
        if settings.weights not in self.weights:
            raise ValueError(f"Invalid weights: {settings.weights}")
