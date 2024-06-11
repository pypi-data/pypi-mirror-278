import json
import os
from collections.abc import Mapping

from pydantic import BaseModel, Field, field_validator, model_validator

from bayesline.api._src.equity import settings as settings_tools
from bayesline.api._src.equity.universe_settings import (
    IndustrySettings,
    RegionSettings,
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api._src.registry import SettingsMenu

Hierarchy = settings_tools.Hierarchy


class HierarchyDescription(BaseModel):

    hierarchy: str = Field(
        min_length=1,
        description="""
        The name of the hierarchy to use, e.g. 'sic' or 'continent'.
        If it is not given then the default hierarchy will be used.
        """,
        examples=["sic", "gics", "continent"],
    )


class HierarchyLevel(HierarchyDescription):
    """
    The hierarchy level description turns every name at
    the configured level into a separate factor.

    E.g. for industries specifying level `1` would
    create top level sector factors.
    """

    level: int = Field(
        description="""The level of the hierarchy to use, e.g. 1
        to use all level 1 names (i.e. sectors for industries or
        continents for regions) or 2 to use all level 2
        names (i.e. sub-sectors for industries and
        countries for regions).
        """,
        default=1,
        examples=[1, 2],
        ge=1,
    )


class HierarchyGroups(HierarchyDescription):
    """
    The hierarchy group description allows for a nested definition
    of groupings.
    The top level groupings will turn into factors, whereas any nested
    groupings will be retained for other uses (e.g. risk decomposition).
    """

    groupings: Mapping[str, Hierarchy] = Field(
        description="""
        A nested structure of groupings where the keys are the group names
        and the leaf level is a list of hierarchy leaf codes to include
        for this group.
        """,
    )


class ExposureSettings(BaseModel, frozen=True, extra="forbid"):
    """
    Defines exposures as hierarchy of selected styles and substyles.
    """

    @classmethod
    def default(cls: type["ExposureSettings"]) -> "ExposureSettings":
        return cls()

    styles: Mapping[str, list[str]] | None = Field(
        default=None,
        description="""
        A mapping where the keys are style codes or labels and the values are
        lists of included sub-style names or labels.
        By default the entire available style/substyle hierarchy will be used.
        """,
    )

    industries: HierarchyLevel | HierarchyGroups = Field(
        description="""
        The definition of how industry factors are being constructed.
        The default is to use the same hiearchy as was used to define the universe
        at level 1 (i.e. coarse grouping).
        """,
        default_factory=lambda: HierarchyLevel(hierarchy="sic", level=1),
    )

    regions: HierarchyLevel | HierarchyGroups = Field(
        description="""
        The definition of how region factors are being constructed.
        The default is to use the same hiearchy as was used to define the universe
        at level 2 (i.e. granular grouping).
        """,
        default_factory=lambda: HierarchyLevel(hierarchy="continent", level=2),
    )


class ExposureSettingsMenu(SettingsMenu[ExposureSettings], frozen=True, extra="forbid"):
    """
    Contains the available settings that can be used to define exposures.
    """

    styles: Mapping[str, list[str]] = Field(
        description="""
        A mapping where the key is the name of an exposure style codes (e.g. 'LEVERAGE')
        and the value is a list of available sub-style codes (e.g. 'DEBT_TO_ASSETS')
        """,
    )

    industries: Mapping[str, Mapping[str, Hierarchy]] = Field(
        description="""
        A dictionary where the key is the name of the industry hierarchy (e.g. 'GICS')
        and the value is a N-level nested dictionary structure of the industry hierarchy
        codes.
        """,
    )

    regions: Mapping[str, Mapping[str, Hierarchy]] = Field(
        description="""
        A dictionary where the key is the name of the region hierarchy (e.g.
        'CONTINENT') and the value is a N-level nested dictionary structure of the
        region hierarchy codes.
        """,
    )

    style_labels: Mapping[str, str] = Field(
        description="""
        A mapping from unique style/substyle code to a human readable name.
        """,
    )

    industry_labels: Mapping[str, Mapping[str, str]] = Field(
        description="""
        A dictionary where the key is the name of the industry hierarchy and
        the value is a mapping from unique industry code to a human readable name.
        """,
    )

    region_labels: Mapping[str, Mapping[str, str]] = Field(
        description="""
        A dictionary where the key is the name of the region hierarchy and
        the value is a mapping from unique region code to a human readable name.
        """,
    )

    def effective_industry_hierarchy(
        self,
        filter_settings: IndustrySettings,
        settings: HierarchyLevel | HierarchyGroups,
    ) -> Mapping[str, Hierarchy]:
        """
        Parameters
        ----------
        filter_settings: IndustrySettings
                    the settings to use to filter the universe.
        settings: HierarchyLevel | HierarchyGroups
                  the settings to use to determine the industry factors.

        Returns
        -------
        A dict structure where the keys are the industry factor names
        and the values are the industry codes that are included in that factor.
        """

        effective_includes = UniverseSettingsMenu.get_effective_includes(
            self.industries[settings.hierarchy],
            filter_settings.include,
            filter_settings.exclude,
            self.industry_labels[settings.hierarchy],
        )

        return ExposureSettingsMenu._effective_hierarchy(
            self.industries,
            self.industry_labels,
            settings,
            effective_includes,
        )

    def effective_region_hierarchy(
        self,
        filter_settings: RegionSettings,
        settings: HierarchyLevel | HierarchyGroups,
    ) -> Mapping[str, Hierarchy]:
        """
        Parameters
        ----------
        filter_settings: RegionSettings
                the settings to use to filter the universe.
        settings: HierarchyLevel | HierarchyGroups
                  the settings to use to determine the region factors.

        Returns
        -------
        A dict structure where the keys are the region factor names
        and the values are the region codes that are included in that factor.
        """
        effective_includes = UniverseSettingsMenu.get_effective_includes(
            self.regions[settings.hierarchy],
            filter_settings.include,
            filter_settings.exclude,
            self.region_labels[settings.hierarchy],
        )

        return ExposureSettingsMenu._effective_hierarchy(
            self.regions,
            self.region_labels,
            settings,
            effective_includes,
        )

    def normalize(
        self,
        universe_settings: UniverseSettings,
        exposure_settings: ExposureSettings,
    ) -> ExposureSettings:
        """
        Normalizes the given exposure settings by converting all
        style and substyle codes/labels to their corresponding codes/labels.

        Parameters
        ----------
        universe_settings: UniverseSettings
                the universe settings to use for normalization.
        exposure_settings: ExposureSettings
                the exposure settings to normalize.

        Returns
        -------
        A new exposure settings object with all style and
        substyle code/labels converted to codes/labels.
        """
        self.validate_settings(exposure_settings)

        if exposure_settings.styles is None:
            # choose entire style hierarchy by default
            exposure_settings = exposure_settings.model_copy(
                update={"styles": self.styles}
            )

        normalized_styles = self.normalize_styles(exposure_settings.styles)

        industries = exposure_settings.industries
        regions = exposure_settings.regions

        normalized_industries = HierarchyGroups(
            hierarchy=industries.hierarchy,
            groupings=self.effective_industry_hierarchy(
                universe_settings.industry,
                industries,
            ),
        )

        normalized_regions = HierarchyGroups(
            hierarchy=regions.hierarchy,
            groupings=self.effective_region_hierarchy(
                universe_settings.region,
                regions,
            ),
        )

        return ExposureSettings(
            styles=normalized_styles,
            industries=normalized_industries,
            regions=normalized_regions,
        )

    def normalize_styles(
        self, styles: Mapping[str, list[str]] | None
    ) -> dict[str, list[str]]:
        styles = styles or self.styles
        lookup = {label: code for code, label in self.style_labels.items()}

        normalized_styles = {}
        for style, substyles in styles.items():  # type: ignore
            normalized_style = lookup.get(style, style)

            normalized_substyles = []
            for substyle in substyles:
                normalized_substyle = lookup.get(substyle, substyle)
                normalized_substyles.append(normalized_substyle)

            normalized_styles[normalized_style] = normalized_substyles
        return normalized_styles

    def all_substyles(
        self,
        settings: ExposureSettings | None = None,
        *,
        labels: bool = False,
    ) -> list[str]:
        """
        Parameters
        ----------
        settings: ExposureSettings, optional
                  the exposure settings to get all substyles for.
        labels: bool, optional
                whether to return the substyles as labels or codes.

        Returns
        -------
        A sorted flat list of all substyles in this settings menu or all
        configured substyles if a settings object is given.
        """
        result: list[str] = []

        if settings is not None and settings.styles is None:
            # choose entire style hierarchy by default
            settings = settings.model_copy(update={"styles": self.styles})

        if settings is not None:
            self.validate_settings(settings)
            for substyles in settings.styles.values():  # type: ignore
                result.extend(substyles)
        else:
            for substyles in self.styles.values():
                result.extend(substyles)

        if labels:
            result = [
                self.style_labels.get(substyle, substyle) for substyle in set(result)
            ]
        else:
            labels_to_codes = {label: code for code, label in self.style_labels.items()}
            result = [
                labels_to_codes.get(substyle, substyle) for substyle in set(result)
            ]
        return sorted(result)

    @staticmethod
    def _effective_hierarchy(
        hierarchies: Mapping[str, Mapping[str, Hierarchy]],
        labels: Mapping[str, Mapping[str, str]],
        settings: HierarchyLevel | HierarchyGroups,
        effective_includes: list[str],
    ) -> Mapping[str, Hierarchy]:
        if isinstance(settings, HierarchyLevel):
            return ExposureSettingsMenu._effective_hierarchy_from_hierarchy_level(
                hierarchies,
                labels,
                settings,
                effective_includes,
            )
        elif isinstance(settings, HierarchyGroups):
            return ExposureSettingsMenu._effective_hierarchy_from_hierarchy_groups(
                hierarchies,
                labels,
                settings,
                effective_includes,
            )
        else:
            raise NotImplementedError(type(settings))

    @staticmethod
    def _effective_hierarchy_from_hierarchy_level(
        hierarchies: Mapping[str, Mapping[str, Hierarchy]],
        labels: Mapping[str, Mapping[str, str]],
        settings: HierarchyLevel,
        effective_includes: list[str],
    ) -> Mapping[str, Hierarchy]:
        if settings.hierarchy is None:
            raise AssertionError(
                """
                Hierarchy must be given, use `normalize` to
                populate the default hierarchy name.
                """,
            )
        hierarchy = hierarchies[settings.hierarchy]
        hierarchy_labels = labels[settings.hierarchy]

        hierarchy_filtered = settings_tools.filter_leaves(
            hierarchy,
            lambda code: code in effective_includes,
        )

        hierarchy_trimmed = settings_tools.trim_to_depth(
            hierarchy_filtered,
            settings.level,
        )

        groups = settings_tools.flatten({"dummy": hierarchy_trimmed}, only_leaves=True)
        result = {}
        for group in groups:
            sub_hierarchy = settings_tools.find_in_hierarchy(hierarchy, group)
            if sub_hierarchy is None or isinstance(sub_hierarchy, int):
                raise AssertionError(f"could not find {group} in {hierarchy}")

            if isinstance(sub_hierarchy, list):
                result[hierarchy_labels[group]] = [group]
            else:
                result[hierarchy_labels[group]] = settings_tools.flatten(
                    sub_hierarchy[group],
                    only_leaves=True,
                )
        return result

    @staticmethod
    def _effective_hierarchy_from_hierarchy_groups(
        hierarchies: Mapping[str, Hierarchy],
        labels: Mapping[str, Mapping[str, str]],
        settings: HierarchyGroups,
        effective_includes: list[str],
    ) -> Mapping[str, Hierarchy]:
        raise NotImplementedError()

    def describe(self, settings: ExposureSettings | None = None) -> str:
        if settings is not None:
            self.validate_settings(settings)
            hierarchy = settings.styles or self.styles
        else:
            hierarchy = self.styles

        style_hierarchy = {}
        for style, substyles in hierarchy.items():
            style_label = self.style_labels.get(style, style)
            style_hierarchy[style_label] = [
                self.style_labels.get(substyle, substyle) for substyle in substyles
            ]

        description = [
            "Style Hierarchy:",
            json.dumps(style_hierarchy, indent=2),
        ]

        return os.linesep.join(description)

    @field_validator("industries", "regions", "styles")
    @classmethod
    def check_unique_hierarchy(
        cls: type["ExposureSettingsMenu"],
        v: Mapping[str, Mapping[str, Hierarchy]],
    ) -> Mapping[str, Mapping[str, Hierarchy]]:
        return settings_tools.check_unique_hierarchy(v)

    @field_validator("industries", "regions", "styles")
    @classmethod
    def check_nonempty_hierarchy(
        cls: type["ExposureSettingsMenu"],
        v: Mapping[str, Mapping[str, Hierarchy]],
    ) -> Mapping[str, Mapping[str, Hierarchy]]:
        return settings_tools.check_nonempty_hierarchy(v)

    @model_validator(mode="after")
    def check_all_codes_have_labels(self) -> "ExposureSettingsMenu":
        industry_errors = settings_tools.check_all_codes_have_labels(
            self.industries,
            self.industry_labels,
        )
        region_errors = settings_tools.check_all_codes_have_labels(
            self.regions,
            self.region_labels,
        )
        style_errors = settings_tools.check_all_codes_have_labels(
            {"styles": self.styles},
            {"styles": self.style_labels},
        )

        errors = industry_errors + region_errors + style_errors
        if errors:
            raise ValueError(os.linesep.join(errors))
        else:
            return self

    def validate_settings(self, settings: ExposureSettings) -> None:
        """
        Validates the given exposure settings against the available settings.

        Will raise an `ValueError` if settings are invalid.

        Parameters
        ----------
        settings: ExposureSettings
                  the exposure settings to validate against.
        """
        self.validate_styles(settings.styles)
        self.validate_hierarchy(self.industries, settings.industries)
        self.validate_hierarchy(self.regions, settings.regions)

    def validate_styles(self, settings: Mapping[str, list[str]] | None) -> None:
        """
        Validates the given style settings against the available settings.

        Will raise an `ValueError` if settings are invalid.

        Parameters
        ----------
        settings: Mapping[str, list[str]]
                  the style settings to validate against.
        """
        if settings is None:
            # nothing to do, default styles will be used
            return

        available_settings = self.styles
        available_labels = self.style_labels.values()

        error_messages = []
        if not settings:
            error_messages.append("Must define at least one style.")

        for style, substyles in settings.items():
            if style not in available_settings and style not in available_labels:
                error_messages.append(f"Style {style} does not exist.")
                continue

            if style in available_labels:
                style_code = next(
                    style_code
                    for style_code, style_label in self.style_labels.items()
                    if style_label == style
                )
            else:
                style_code = style

            available_substyles = available_settings[style_code]

            for substyle in substyles:
                if (
                    substyle not in available_substyles
                    and substyle not in available_labels
                ):
                    error_messages.append(f"Substyle {substyle} does not exist.")

            if len(substyles) > len(set(substyles)):
                dupes = {
                    substyle for substyle in substyles if substyles.count(substyle) > 1
                }
                error_messages.append(
                    f"Substyles {', '.join(dupes)} are duplicated for style {style}.",
                )

        if error_messages:
            raise ValueError(os.linesep.join(error_messages))

    @staticmethod
    def validate_hierarchy(
        hierarchies: Mapping[str, Mapping[str, Hierarchy]],
        settings: HierarchyLevel | HierarchyGroups,
    ) -> None:
        settings_tools.validate_hierarchy_schema(hierarchies.keys(), settings.hierarchy)

        if isinstance(settings, HierarchyLevel):
            depth = settings_tools.get_depth(hierarchies[settings.hierarchy])
            if depth < settings.level:
                raise ValueError(
                    f"Illegal level {settings.level}, maximum level is {depth}"
                )
        elif isinstance(settings, HierarchyGroups):
            existing = set(
                settings_tools.flatten(
                    hierarchies[settings.hierarchy], only_leaves=True
                )
            )
            settings_tools.check_all_leafcodes_exist(settings.groupings, existing)
            settings_tools.check_unique_hierarchy(
                {settings.hierarchy: settings.groupings}
            )

            # check all codes are used
            configured_codes = set(
                settings_tools.flatten(settings.groupings, only_leaves=True)
            )
            missing = existing - configured_codes
            if missing:
                raise ValueError(
                    f"Missing hierarchy codes for {settings.hierarchy}: {','.join(missing)}"
                )
        else:
            raise ValueError(f"unknown settings type {type(settings)}")
