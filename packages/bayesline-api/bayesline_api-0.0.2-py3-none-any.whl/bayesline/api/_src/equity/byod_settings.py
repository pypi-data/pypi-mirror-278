import datetime as dt

import pandas as pd
from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

from bayesline.api._src.registry import SettingsMenu
from bayesline.api._src.types import IdType


class ByodSettings(BaseModel, frozen=True, extra="forbid"):
    description: str | None
    extra_cols: list[str] = Field(default_factory=list)
    date_col: str
    asset_id_col: str
    asset_id_type: IdType
    styles: dict[str, list[str]] = Field(default_factory=dict)
    portfolios: list[str] = Field(default_factory=list)
    start_date: dt.date
    end_date: dt.date

    @staticmethod
    def _validate_dupes(v: list[str], info: ValidationInfo) -> list[str]:
        v = v
        f = info.field_name
        counts = pd.Series(v).value_counts()
        dupes = ", ".join(counts[counts > 1].keys())
        if dupes:
            raise ValueError(f"{f} has duplicates {dupes}")
        return v

    @field_validator("extra_cols", "portfolios")
    @classmethod
    def validate_dupes(
        cls: type["ByodSettings"], v: list[str], info: ValidationInfo
    ) -> list[str]:
        return cls._validate_dupes(v, info)

    @field_validator("styles")
    @classmethod
    def validate_substyle_dupes(
        cls: type["ByodSettings"], v: dict[str, list[str]], info: ValidationInfo
    ) -> dict[str, list[str]]:
        v = v or {}
        cls._validate_dupes([e for sublist in v.values() for e in sublist], info)
        return v

    @model_validator(mode="after")
    def check_model(self) -> "ByodSettings":
        if not self.styles and not self.portfolios:
            raise ValueError("Styles and/or portfolios must be given")

        meta_cols = set([self.date_col, self.asset_id_col])
        if meta_cols & set(self.extra_cols):
            raise ValueError(
                f"Extra cols cannot contain {', '.join(sorted(meta_cols))}"
            )

        if meta_cols & set(self.portfolios):
            raise ValueError(
                f"Portfolios cannot contain {', '.join(sorted(meta_cols))}"
            )

        substyles = self.substyles
        if meta_cols & set(substyles):
            raise ValueError(f"Styles cannot contain {', '.join(sorted(meta_cols))}")

        style_port_overlap = set(self.portfolios) & set(substyles)
        if style_port_overlap:
            raise ValueError(
                f"Styles and portfolios cannot overlap {style_port_overlap}"
            )

        port_extra_overlap = set(self.portfolios) & set(self.extra_cols)
        if port_extra_overlap:
            raise ValueError(
                f"Portfolios and extra cols cannot overlap {port_extra_overlap}"
            )

        style_extra_overlap = set(substyles) & set(self.extra_cols)
        if style_extra_overlap:
            raise ValueError(
                f"Styles and extra cols cannot overlap {style_extra_overlap}"
            )

        return self

    @property
    def raw_cols(self) -> list[str]:
        return (
            [self.date_col, self.asset_id_col]
            + (self.substyles)
            + (self.portfolios)
            + (self.extra_cols)
        )

    @property
    def substyles(self) -> list[str]:
        return [st for sts in (self.styles or {}).values() for st in sts]

    def substyle_mappings(self, name: str, style: str | None = None) -> dict[str, str]:
        """
        Parameters
        ----------
        name: str
            The name of this byod
        style : str, optional
            The style for which to return substyle mappings.
            If None, all substyle mappings are returned.

        Returns
        -------
        Mappings from the underlying column name to a unique reference.
        """
        result = {}
        for style_, substyles in self.styles.items():
            if style is not None and style != style_:
                continue

            for substyle in substyles:
                result[substyle] = f"{name}.{substyle}"
        return result

    def validate_df(self, df: pd.DataFrame) -> None:
        df = df.reset_index()
        columns = list(df.columns)
        errors = []
        for col in self.raw_cols:
            if col not in columns:
                errors.append(f"{col} is missing in dataframe")

        for col in (self.portfolios) + (self.substyles):
            if not pd.api.types.is_numeric_dtype(df[col].dtype):
                errors.append(f"{col} is not a numeric column")

        if self.date_col in columns:
            if not pd.api.types.is_datetime64_any_dtype(df[self.date_col].dtype):
                errors.append(f"{self.date_col} is not a datetime column")

            if pd.to_datetime(self.start_date).date() < df[self.date_col].min().date():
                errors.append(f"start_date {self.start_date} is before min date")

            if pd.to_datetime(self.end_date).date() > df[self.date_col].max().date():
                errors.append(f"end_date {self.end_date} is after max date")
        if errors:
            raise ValueError("\n".join(errors))


class ByodSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """
    Contains the available settings that can be used for custom exposures.
    """

    id_types: list[IdType] = Field(
        description="""
        A list of all the id types that are supported for the universe.
        """,
    )

    def describe(self, settings: ByodSettings | None = None) -> str:
        return settings.model_dump_json(indent=2) if settings else "N/A"

    def validate_settings(self, settings: ByodSettings) -> None:
        if settings.asset_id_type not in self.id_types:
            raise ValueError(
                f"asset_id_type {settings.asset_id_type} not in {', '.join(self.id_types)}"
            )
