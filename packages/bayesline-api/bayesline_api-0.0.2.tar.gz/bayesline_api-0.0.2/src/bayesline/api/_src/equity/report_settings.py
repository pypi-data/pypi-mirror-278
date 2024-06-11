import os
from abc import ABC
from typing import ClassVar, Literal, Type, TypeAlias, Union

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

from bayesline.api._src.equity.riskmodels_settings import FactorRiskModelSettings
from bayesline.api._src.registry import SettingsMenu


class MeasureSettings(BaseModel, ABC, frozen=True, extra="forbid"):
    """Defines settings for a measure."""

    type: str

    @property
    def columns(self):
        return [self.type]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # check that every field has a default value, so we can instantiate settings
        # without any argument. Fields defined as a: int = 1, a: int = Field(1), and
        # a: list[int] = Field(default_factory=list) are all valid.
        for f in cls.__annotations__:
            msg = f"{f} not does not have a default value"
            assert f in cls.__dict__, msg  # fields without ... = Field(...)
            if isinstance(cls.__dict__[f], FieldInfo):
                assert not cls.__dict__[f].is_required(), msg  # with = Field(...)


class PassThroughMeasureSettings(MeasureSettings):
    type: Literal["PassThrough"] = Field("PassThrough", repr=False)
    name: str = Field("PassThrough", description="The name of the measure.")

    @property
    def columns(self):
        return [self.name]


class ExposureMeasureSettings(MeasureSettings):
    type: Literal["Exposure"] = Field("Exposure", repr=False)


class XSigmaRhoMeasureSettings(MeasureSettings):
    type: Literal["XSigmaRho"] = Field("XSigmaRho", repr=False)

    @property
    def columns(self):
        return [
            "Exposure (X)",
            "Volatility (σ)",
            "Correlation (ρ)",
            "Contribution (Xσρ)",
        ]


class HVaRMeasureSettings(MeasureSettings):
    type: Literal["Historical VaR"] = Field("Historical VaR", repr=False)
    alpha: list[float] = Field([0.1, 0.05])

    @property
    def columns(self):
        return [f"HistVaR {a:.0%}" for a in self.alpha]


class AVaRMeasureSettings(MeasureSettings):
    type: Literal["Analytical VaR"] = Field("Analytical VaR", repr=False)
    alpha: list[float] = Field([0.1, 0.05])

    @property
    def columns(self):
        return [f"AnVaR {a:.0%}" for a in self.alpha]


class TimeSeriesVolatilityMeasureSettings(MeasureSettings):
    type: Literal["TimeSeriesVolatility"] = Field("TimeSeriesVolatility", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    ddof: int = Field(1, description="The degrees of freedom to use for the volality")


class CumsumMeasureSettings(MeasureSettings):
    type: Literal["Cumsum"] = Field("Cumsum", repr=False)


class DrawdownMeasureSettings(MeasureSettings):
    type: Literal["Drawdown"] = Field("Drawdown", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")


class MovingAverageMeasureSettings(MeasureSettings):
    type: Literal["MovingAverage"] = Field("MovingAverage", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    var: Literal["r2", "sigma2", "sigma", "abs_t", "p", "p1", "p5"] = Field(
        "r2", description="The variable to average"
    )

    @property
    def columns(self):
        return [f"{self.type} {self.var}"]


class MovingAverageRSquaredMeasureSettings(MeasureSettings):
    type: Literal["MovingAverageRSquared"] = Field("MovingAverageRSquared", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")


class VolForecastMeasureSettings(MeasureSettings):
    type: Literal["VolForecast"] = Field("VolForecast", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    metric: Literal["qlike", "mse", "mae", "bias"] = Field(
        "qlike", description="The metric to use"
    )
    ddof: int = Field(1, description="The degrees of freedom to use for the stability")

    @property
    def columns(self):
        return [
            "VolForecast",
            "VolForecastRealized",
            "VolForecastStability",
            "VolForecastLoss",
        ]


class FactorVolForecastMeasureSettings(MeasureSettings):
    type: Literal["FactorVolForecast"] = Field("FactorVolForecast", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    metric: Literal["qlike", "mse", "mae", "bias"] = Field(
        "qlike", description="The metric to use"
    )
    ddof: int = Field(1, description="The degrees of freedom to use for the stability")

    @property
    def columns(self):
        return [
            "VolForecast",
            "VolForecastRealized",
            "VolForecastStability",
            "VolForecastLoss",
        ]


class FactorIdioMeasureSettings(MeasureSettings):
    type: Literal["FactorIdio"] = Field("FactorIdio", repr=False)


MeasureSettingsType: TypeAlias = Union[tuple(MeasureSettings.__subclasses__())]  # type: ignore
MeasureSettingsClassType = Type[MeasureSettingsType]


ALL_XSR_MEASURE_TYPES = [
    XSigmaRhoMeasureSettings,
]
ALL_VAR_MEASURE_TYPES = [
    HVaRMeasureSettings,
    AVaRMeasureSettings,
]
ALL_FACTOR_TS_MEASURE_TYPES = [
    TimeSeriesVolatilityMeasureSettings,
    CumsumMeasureSettings,
    DrawdownMeasureSettings,
]
ALL_RISK_MODEL_FIT_MEASURE_TYPES = [
    MovingAverageMeasureSettings,
]
ALL_RISK_MODEL_FIT_FACTOR_MEASURE_TYPES = [
    MovingAverageMeasureSettings,
]
ALL_RISK_MODEL_PORTFOLIO_FIT_MEASURE_TYPES = [
    MovingAverageRSquaredMeasureSettings,
]
ALL_FACTOR_FORECAST_LOSS_MEASURE_TYPES = [
    FactorVolForecastMeasureSettings,
]
ALL_FORECAST_LOSS_MEASURE_TYPES = [
    VolForecastMeasureSettings,
]
ALL_FACTOR_IDIO_MEASURE_TYPES = [
    FactorIdioMeasureSettings,
]
ALL_STYLE_CORRELATION_MEASURE_TYPES = [
    PassThroughMeasureSettings,
]
ALL_STYLE_INDUSTRY_EXPOSURE_MEASURE_TYPES = [
    PassThroughMeasureSettings,
]


def _get_default_measures(
    measure_types: list[MeasureSettingsClassType],
) -> list[MeasureSettingsType]:
    return [m() for m in measure_types]


class ConcreteReportSettings(BaseModel, ABC, frozen=True, extra="forbid"):
    type: str
    measures: list[MeasureSettingsType] = Field(
        description="The measures to include in the report.",
    )


class XSRReportSettings(ConcreteReportSettings):
    """Defines settings to build an XSR report."""

    type: Literal["XSR report"] = Field("XSR report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_XSR_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_cor: int = Field(
        42, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )


class VaRReportSettings(ConcreteReportSettings):
    """Defines settings to build a VaR report."""

    type: Literal["VaR report"] = Field("VaR report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_VAR_MEASURE_TYPES),
        description="The measures to include in the report.",
    )


class FactorTSReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor time-series report."""

    type: Literal["Factor TS report"] = Field("Factor TS report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FACTOR_TS_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )


class RiskModelFitReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk model fit report."""

    type: Literal["Risk Model Fit report"] = Field("Risk Model Fit report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_RISK_MODEL_FIT_MEASURE_TYPES),
        description="The measures to include in the report.",
    )


class RiskModelFitFactorReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk model fit report at the factor level."""

    type: Literal["Risk Model Fit Factor report"] = Field(
        "Risk Model Fit Factor report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_RISK_MODEL_FIT_FACTOR_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )


class RiskModelPortfolioFitReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk model fit report at the portfolio level."""

    type: Literal["Risk Model Portfolio Fit report"] = Field(
        "Risk Model Portfolio Fit report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_RISK_MODEL_PORTFOLIO_FIT_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )


class FactorForecastLossReportSettings(ConcreteReportSettings):
    """Defines settings to build a forecast loss report."""

    type: Literal["Factor Forecast Loss report"] = Field(
        "Factor Forecast Loss report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FACTOR_FORECAST_LOSS_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )
    horizons: list[int] = Field([1, 5, 21], description="The forecast horizons to use.")
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )


class AssetForecastLossReportSettings(ConcreteReportSettings):
    """Defines settings to build a forecast loss report."""

    type: Literal["Forecast Loss report"] = Field("Forecast Loss report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FORECAST_LOSS_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )
    horizons: list[int] = Field([1, 5, 21], description="The forecast horizons to use.")
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_cor: int = Field(
        42, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )


class FactorIdioReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor vcov and idio report."""

    type: Literal["Factor Idio report"] = Field("Factor Idio report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FACTOR_IDIO_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_cor: int = Field(
        42, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )


class StyleCorrelationReportSettings(ConcreteReportSettings):
    """Defines settings to build a style correlation report."""

    type: Literal["Style Correlation report"] = Field(
        "Style Correlation report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_STYLE_CORRELATION_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )


class StyleIndustryExposureReportSettings(ConcreteReportSettings):
    """Defines settings to build a style industry exposure report."""

    type: Literal["Style Industry Exposure report"] = Field(
        "Style Industry Exposure report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_STYLE_INDUSTRY_EXPOSURE_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )


ConcreteReportSettingsType: TypeAlias = Union[tuple(ConcreteReportSettings.__subclasses__())]  # type: ignore


class ReportSettings(BaseModel, frozen=True, extra="forbid"):
    """
    Defines settings to build a report.
    """

    report: ConcreteReportSettingsType
    lookback: int = Field(1000, description="The lookback period for the report.")
    risk_model: str | int | FactorRiskModelSettings = Field(
        description="The risk model to use for the report.",
    )


class ConcreteReportSettingsMenu(SettingsMenu, ABC):

    measure_types: ClassVar[list[MeasureSettingsClassType]] = []

    def validate_settings(self, settings: ReportSettings) -> None:
        # TODO implement
        pass

    def describe(self, settings: ReportSettings | None = None) -> str:
        # TODO importment
        return ""


class XSRReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_XSR_MEASURE_TYPES


class VaRReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_VAR_MEASURE_TYPES


class FactorTSReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_TS_MEASURE_TYPES  # type: ignore
    )


class RiskModelFitReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_MODEL_FIT_MEASURE_TYPES
    )


class RiskModelFitFactorReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_MODEL_FIT_FACTOR_MEASURE_TYPES
    )


class RiskModelPortfolioFitReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_MODEL_FIT_MEASURE_TYPES
    )


class FactorForecastLossReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FORECAST_LOSS_MEASURE_TYPES  # type: ignore
    )


class AssetForecastLossReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FORECAST_LOSS_MEASURE_TYPES  # type: ignore
    )


class FactorIdioReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_IDIO_MEASURE_TYPES
    )


class StyleCorrelationReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_STYLE_CORRELATION_MEASURE_TYPES
    )


class StyleIndustryExposureReportSettingsMenu(ConcreteReportSettingsMenu):
    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_STYLE_INDUSTRY_EXPOSURE_MEASURE_TYPES
    )


class ReportSettingsMenu(SettingsMenu[ReportSettings]):
    """
    Defines available report settings to build a report.
    """

    xsr: ConcreteReportSettingsMenu = XSRReportSettingsMenu()
    var: ConcreteReportSettingsMenu = VaRReportSettingsMenu()
    fts: ConcreteReportSettingsMenu = FactorTSReportSettingsMenu()
    rmf: ConcreteReportSettingsMenu = RiskModelFitReportSettingsMenu()
    rms: ConcreteReportSettingsMenu = RiskModelFitFactorReportSettingsMenu()
    rmp: ConcreteReportSettingsMenu = RiskModelPortfolioFitReportSettingsMenu()
    ffl: ConcreteReportSettingsMenu = FactorForecastLossReportSettingsMenu()
    afl: ConcreteReportSettingsMenu = AssetForecastLossReportSettingsMenu()
    fni: ConcreteReportSettingsMenu = FactorIdioReportSettingsMenu()
    scr: ConcreteReportSettingsMenu = StyleCorrelationReportSettingsMenu()
    six: ConcreteReportSettingsMenu = StyleIndustryExposureReportSettingsMenu()

    def describe(self, settings: ReportSettings | None = None) -> str:
        # TODO
        if settings is not None:
            return os.linesep.join(
                [
                    f"Risk Model: {settings.risk_model}",
                ]
            )
        else:
            return "NA"

    def validate_settings(self, settings: ReportSettings) -> None:
        # TODO
        pass
