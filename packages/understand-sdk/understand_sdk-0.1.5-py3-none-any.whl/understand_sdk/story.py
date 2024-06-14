from abc import ABC
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import Field

from understand_sdk.model import BaseModel

#
#
# Story
#
#


class SlideLayout(str, Enum):
    ROW = "row"
    COLUMN = "column"


class Slide(BaseModel, ABC):
    title: Optional[str] = None


class SlideWithLayout(Slide, ABC):
    layout: Optional[SlideLayout] = None


class ChartSlide(SlideWithLayout, ABC):
    description: Optional[str] = None
    data: List[Dict[str, Union[str, float, int]]]


#
# Chart slide types attributes
#


class Attribute(BaseModel, ABC):
    field: str


class ElementAttribute(Attribute):
    role: Literal["element"] = "element"


class XAttribute(Attribute):
    role: Literal["x"] = "x"


class YAttribute(Attribute):
    role: Literal["y"] = "y"


class SizeByAttribute(Attribute):
    role: Literal["sizeBy"] = "sizeBy"


class TargetAttribute(Attribute):
    role: Literal["target"] = "target"


class VarianceAttribute(Attribute):
    role: Literal["variance"] = "variance"


class SeriesAttribute(Attribute):
    role: Literal["series"] = "series"
    from_: str = Field(..., alias="from")
    to: str


#
# Settings options
#


class Variance(str, Enum):
    ABSOLUTE = "absolute"
    RELATIVE = "relative"


class TargetFillArea(str, Enum):
    ABOVE = "above"
    BELOW = "below"
    BOTH = "both"


#
# Text slides
#


class CoverSlide(Slide):
    type: Literal["cover"] = "cover"
    title: Optional[str] = None


class HeadingSlide(Slide):
    type: Literal["heading"] = "heading"
    title: Optional[str] = None


class ParagraphSlide(SlideWithLayout):
    type: Literal["paragraph"] = "paragraph"
    description: Optional[str] = None


#
# KPI slides
#


class KpiArrow(str, Enum):
    UP = "up"
    DOWN = "down"


class KpiSentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class KpiChange(BaseModel):
    value: Optional[str] = None
    suffix: Optional[str] = Field(default=None, alias="valueSufix")  # TODO(vojta) fix typo on API
    arrow: KpiArrow
    sentiment: KpiSentiment


class KpiTarget(BaseModel):
    value: Optional[str] = None
    percentage: Optional[float] = None


class KpiInstance(BaseModel):
    measure: Optional[str] = None
    period: Optional[str] = None
    value: Optional[str] = None
    suffix: Optional[str] = Field(default=None, alias="valueSufix")  # TODO(vojta) fix typo on API
    sentiment: Optional[KpiSentiment] = None
    change: Optional[KpiChange] = None
    target: Optional[KpiTarget] = None


class KpiSlide(SlideWithLayout):
    type: Literal["kpi"] = "kpi"
    description: Optional[str] = None
    instances: List[KpiInstance]


#
# Line slide
#


class LineSlideDisplay(str, Enum):
    BASIC = "basic"
    CHANGE = "change"
    TARGET = "target"


class LineSlideSettings(BaseModel):
    variance: Optional[Variance] = None
    display: Optional[LineSlideDisplay] = LineSlideDisplay.BASIC
    targetFillArea: Optional[TargetFillArea] = None


class LineSlide(ChartSlide):
    type: Literal["line"] = "line"
    settings: Optional[LineSlideSettings] = None
    attributes: List[
        Union[
            ElementAttribute,
            YAttribute,
            TargetAttribute,
            VarianceAttribute,
        ]
    ]


#
# Bar slide
#


class BarSlideDisplay(str, Enum):
    VALUE = "value"
    BOX = "box"
    SERIES = "series"
    INTERVAL = "interval"
    TARGET = "target"


class BarSlideSeriesDisplay(str, Enum):
    CHANGE = "change"
    GROUP = "group"
    STACKED = "stacked"
    FULL_STACKED = "fullStacked"
    COMPARE = "compare"


class BarSlideSettings(BaseModel):
    variance: Optional[Variance] = None
    display: Optional[BarSlideDisplay] = BarSlideDisplay.VALUE
    series_display: Optional[BarSlideSeriesDisplay] = Field(default=None, alias="seriesDisplay")


class BarSlide(ChartSlide):
    type: Literal["bar"] = "bar"
    settings: Optional[BarSlideSettings] = None
    attributes: List[Union[ElementAttribute, XAttribute, SeriesAttribute, VarianceAttribute, TargetAttribute]]


#
# Column slide
#


class ColumnSlideDisplay(str, Enum):
    VALUE = "value"
    BOX = "box"
    SERIES = "series"
    WATERFALL = "waterfall"
    INTERVAL = "interval"
    TARGET = "target"


class ColumnSlideSeriesDisplay(str, Enum):
    CHANGE = "change"
    GROUP = "group"
    STACKED = "stacked"
    FULL_STACKED = "fullStacked"
    COMPARE = "compare"


class ColumnSlideSettings(BaseModel):
    variance: Optional[Variance] = None
    display: Optional[ColumnSlideDisplay] = ColumnSlideDisplay.VALUE
    series_display: Optional[ColumnSlideSeriesDisplay] = Field(default=None, alias="seriesDisplay")


class ColumnSlide(ChartSlide):
    type: Literal["column"] = "column"
    settings: Optional[ColumnSlideSettings] = None
    attributes: List[Union[ElementAttribute, YAttribute, SeriesAttribute, VarianceAttribute, TargetAttribute]]


#
# Dot slide
#


class DotSlideDisplay(str, Enum):
    BASIC = "basic"
    CHANGE = "change"


class DotSlideSettings(BaseModel):
    variance: Optional[Variance] = None
    display: Optional[DotSlideDisplay] = DotSlideDisplay.BASIC


class DotSlide(ChartSlide):
    type: Literal["dot"] = "dot"
    settings: Optional[DotSlideSettings] = None
    attributes: List[
        Union[
            ElementAttribute,
            YAttribute,
            SeriesAttribute,
            VarianceAttribute,
        ]
    ]


#
# Scatter slide
#


class ScatterSlide(ChartSlide):
    type: Literal["scatter"] = "scatter"
    attributes: List[Union[ElementAttribute, YAttribute, XAttribute, SeriesAttribute]]


#
# Bubble slide
#


class BubbleSlide(ChartSlide):
    type: Literal["bubble"] = "bubble"
    attributes: List[Union[ElementAttribute, YAttribute, XAttribute, SeriesAttribute, SizeByAttribute]]


#
# Story
#


class Story(BaseModel):
    title: Optional[str] = None
    slides: List[
        Union[
            CoverSlide,
            HeadingSlide,
            ParagraphSlide,
            KpiSlide,
            BubbleSlide,
            ScatterSlide,
            ColumnSlide,
            BarSlide,
            DotSlide,
            LineSlide,
        ]
    ]


class StoryWithChannels(Story):
    channels: Optional[List[str]] = None
