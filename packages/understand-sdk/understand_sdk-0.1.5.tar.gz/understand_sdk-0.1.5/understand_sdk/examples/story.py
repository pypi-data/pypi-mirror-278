from datetime import datetime
from typing import List

from understand_sdk.story import (
    BarSlide,
    BarSlideDisplay,
    BarSlideSettings,
    BubbleSlide,
    ColumnSlide,
    ColumnSlideDisplay,
    ColumnSlideSettings,
    CoverSlide,
    DotSlide,
    ElementAttribute,
    HeadingSlide,
    KpiArrow,
    KpiChange,
    KpiInstance,
    KpiSentiment,
    KpiSlide,
    KpiTarget,
    LineSlide,
    LineSlideDisplay,
    LineSlideSettings,
    ParagraphSlide,
    ScatterSlide,
    SeriesAttribute,
    SizeByAttribute,
    Slide,
    SlideLayout,
    Story,
    StoryWithChannels,
    TargetAttribute,
    TargetFillArea,
    Variance,
    XAttribute,
    YAttribute,
)


def create_story(dt: datetime) -> Story:
    title = "Example story"
    return Story(
        title=f"{title} - {str(dt.date())}",
        slides=[
            # Cover
            CoverSlide(title=f"{title}\n{str(dt.date())}"),
            # Slide variant examples ...
            *_story_paragraph_slides(),
            *_story_kpi_slides(),
            *_story_scatter_slides(),
            *_story_bubble_slides(),
            *_story_dot_slides(),
            *_story_line_slides(),
            *_story_column_slides(),
            *_story_bar_slides(),
        ],
    )


def create_story_with_channels(dt: datetime) -> StoryWithChannels:
    title = "Example story with channel"
    return StoryWithChannels(
        title=f"{title} - {str(dt.date())}",
        channels=["general", "cashflow"],
        slides=[
            # Cover
            CoverSlide(title=f"{title}\n{str(dt.date())}"),
            # Slide variant examples ...
            *_story_paragraph_slides(),
            *_story_kpi_slides(),
            *_story_scatter_slides(),
            *_story_bubble_slides(),
            *_story_dot_slides(),
            *_story_line_slides(),
            *_story_column_slides(),
            *_story_bar_slides(),
        ],
    )


def _story_paragraph_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Paragraph examples"),
        ParagraphSlide(
            title="Custom paragraph default layout - row", description="super long\ntext with **bold** \n # bold baby"
        ),
        ParagraphSlide(
            layout=SlideLayout.COLUMN,
            title="Custom paragraph column layout",
            description="super long\ntext with **bold** \n # bold baby",
        ),
    ]


def _story_kpi_slides() -> List[Slide]:
    return [
        HeadingSlide(title="KPI examples"),
        KpiSlide(
            title="KPI row",
            description="**Markdown** description",
            instances=[
                KpiInstance(
                    measure="Metric",
                    period="Year",
                    value="$99k",
                    suffix="m",
                ),
                KpiInstance(
                    measure="Metric",
                    period="Year",
                    value="$99k",
                    suffix="m",
                    change=KpiChange(
                        value="$255k",
                        arrow=KpiArrow.UP,
                        sentiment=KpiSentiment.NEGATIVE,
                    ),
                ),
                KpiInstance(
                    measure="Metric",
                    period="Year",
                    value="$99k",
                    suffix="m",
                    sentiment=KpiSentiment.POSITIVE,
                    change=KpiChange(
                        value="$255k",
                        arrow=KpiArrow.UP,
                        sentiment=KpiSentiment.NEGATIVE,
                    ),
                ),
            ],
        ),
        KpiSlide(
            layout=SlideLayout.COLUMN,
            title="KPI column & with target",
            instances=[
                KpiInstance(
                    measure="Metric",
                    period="Year",
                    value="$99k",
                    valueSufix="m",
                ),
                KpiInstance(
                    measure="Metric",
                    period="Year",
                    value="$99k",
                    suffix="m",
                    change=KpiChange(
                        value="$255k",
                        arrow=KpiArrow.UP,
                        sentiment=KpiSentiment.NEGATIVE,
                    ),
                    target=KpiTarget(value="200", percentage=59),
                ),
            ],
        ),
    ]


def _story_scatter_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Scatter examples"),
        ScatterSlide(
            title="Scatter",
            description="**Markdown** description",
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Employees"),
                YAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_SCATTER,
        ),
        ScatterSlide(
            title="Scatter with series",
            description="**Markdown** description",
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Employees"),
                YAttribute(field="Amount"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_SCATTER,
        ),
    ]


def _story_bubble_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Bubble examples"),
        BubbleSlide(
            title="Bubble",
            description="**Markdown** description",
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Employees"),
                SizeByAttribute(field="Size by metric"),
                YAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_BUBBLE,
        ),
        BubbleSlide(
            title="Bubble with series",
            description="**Markdown** description",
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Employees"),
                YAttribute(field="Amount"),
                SizeByAttribute(field="Size by metric"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_BUBBLE,
        ),
    ]


def _story_dot_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Dot examples"),
        DotSlide(
            title="Dot",
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        DotSlide(
            title="Dot with series",
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
    ]


def _story_line_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Line examples"),
        LineSlide(
            title="Line",
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_LINE,
        ),
        LineSlide(
            title="Line with target",
            settings=LineSlideSettings(display=LineSlideDisplay.TARGET),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                TargetAttribute(field="Target"),
            ],
            data=EXAMPLE_DATA_LINE,
        ),
        LineSlide(
            title="Line with target fill area above",
            settings=LineSlideSettings(display=LineSlideDisplay.TARGET, targetFillArea=TargetFillArea.ABOVE),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                TargetAttribute(field="Target"),
            ],
            data=EXAMPLE_DATA_LINE,
        ),
        LineSlide(
            title="Line with target absolute variance",
            settings=LineSlideSettings(display=LineSlideDisplay.TARGET, variance=Variance.ABSOLUTE),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                TargetAttribute(field="Target"),
            ],
            data=EXAMPLE_DATA_LINE,
        ),
        LineSlide(
            layout=SlideLayout.ROW,
            title="Line with row",
            description="**Markdown** description",
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_LINE,
        ),
    ]


def _story_column_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Column examples"),
        ColumnSlide(
            title="Column",
            settings=ColumnSlideSettings(display=ColumnSlideDisplay.VALUE),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        ColumnSlide(
            title="Column with series change",
            settings=ColumnSlideSettings(display=ColumnSlideDisplay.SERIES),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        ColumnSlide(
            title="Column with target",
            settings=ColumnSlideSettings(display=ColumnSlideDisplay.TARGET),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                TargetAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        ColumnSlide(
            title="Column with series absolute variance",
            settings=ColumnSlideSettings(display=ColumnSlideDisplay.SERIES, variance=Variance.ABSOLUTE),
            attributes=[
                ElementAttribute(field="Company name"),
                YAttribute(field="Amount"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
    ]


def _story_bar_slides() -> List[Slide]:
    return [
        HeadingSlide(title="Bar examples"),
        BarSlide(
            title="Bar",
            settings=BarSlideSettings(display=BarSlideDisplay.VALUE),
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        BarSlide(
            title="Bar with series change",
            settings=BarSlideSettings(display=BarSlideDisplay.SERIES),
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Amount"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        BarSlide(
            title="Bar with target",
            settings=BarSlideSettings(display=BarSlideDisplay.TARGET),
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Amount"),
                TargetAttribute(field="Amount"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
        BarSlide(
            title="Bar with series absolute variance",
            settings=BarSlideSettings(display=BarSlideDisplay.SERIES, variance=Variance.ABSOLUTE),
            attributes=[
                ElementAttribute(field="Company name"),
                XAttribute(field="Amount"),
                SeriesAttribute(field="Quarter", from_="Q1", to="Q2"),
            ],
            data=EXAMPLE_DATA_GENERIC,
        ),
    ]


EXAMPLE_DATA_GENERIC = [
    {"Company name": "Blockers Mueller Inc.", "Amount": "520490.0", "Quarter": "Q2"},
    {"Company name": "Blockers Mueller Inc.", "Amount": "420490.0", "Quarter": "Q1"},
    {"Company name": "Comic Prime Inc.", "Amount": "447273.0", "Quarter": "Q2"},
    {"Company name": "Comic Prime Inc.", "Amount": "347273.0", "Quarter": "Q1"},
    {"Company name": "Cupar Times Inc.", "Amount": "345540.0", "Quarter": "Q2"},
    {"Company name": "Cupar Times Inc.", "Amount": "245540.0", "Quarter": "Q1"},
    {"Company name": "Bryson Wirral Ltd.", "Amount": "185344.0", "Quarter": "Q2"},
    {"Company name": "Necessities Caunt Co.", "Amount": "133427.0", "Quarter": "Q2"},
    {"Company name": "Maintenence Florence Co.", "Amount": "129326.0", "Quarter": "Q2"},
    {"Company name": "Herbert Geotechnical Co.", "Amount": "118896.0", "Quarter": "Q2"},
    {"Company name": "Currie Hickinbottom Ltd.", "Amount": "77750.0", "Quarter": "Q2"},
    {"Company name": "Pickering Precision Co.", "Amount": "55664.0", "Quarter": "Q2"},
    {"Company name": "Bunting Letterbox Ltd.", "Amount": "38667.0", "Quarter": "Q2"},
    {"Company name": "Stratos Pack Inc.", "Amount": "25650.0", "Quarter": "Q2"},
    {"Company name": "Wisbech Wallpaper Ltd.", "Amount": "24898.0", "Quarter": "Q2"},
    {"Company name": "Olga Biosystems Ltd.", "Amount": "18690.0", "Quarter": "Q2"},
    {"Company name": "Kingdon Denton Inc.", "Amount": "15352.0", "Quarter": "Q2"},
    {"Company name": "Sants Caledonia Inc.", "Amount": "13530.0", "Quarter": "Q2"},
    {"Company name": "Norie Wilts Co.", "Amount": "10542.0", "Quarter": "Q2"},
    {"Company name": "Suzanna Batt Inc.", "Amount": "2778.0", "Quarter": "Q2"},
    {"Company name": "Runner Driven Ltd.", "Amount": "2516.0", "Quarter": "Q2"},
    {"Company name": "Jenson Simon Inc.", "Amount": "0.0", "Quarter": "Q2"},
    {"Company name": "Hussain Subscription Co.", "Amount": "0.0", "Quarter": "Q2"},
    {"Company name": "Diane Grous Ltd.", "Amount": "0.0", "Quarter": "Q2"},
]

EXAMPLE_DATA_LINE = [
    {"Company name": "A", "Amount": "100", "Target": "100", "Variance": "100"},
    {"Company name": "B", "Amount": "200", "Target": "100", "Variance": "100"},
    {"Company name": "C", "Amount": "100", "Target": "300", "Variance": "100"},
    {"Company name": "D", "Amount": "50", "Target": "100", "Variance": "500"},
    {"Company name": "E", "Amount": "-100", "Target": "50", "Variance": "100"},
    {"Company name": "F", "Amount": "-500", "Target": "100", "Variance": "-100"},
]

EXAMPLE_DATA_BUBBLE = [
    {
        "Company name": "Blockers Mueller Inc.",
        "Amount": "520490.0",
        "Employees": 99,
        "Size by metric": 100,
        "Quarter": "Q2",
    },
    {
        "Company name": "Blockers Mueller Inc.",
        "Amount": "320490.0",
        "Employees": 59,
        "Size by metric": 10,
        "Quarter": "Q1",
    },
    {"Company name": "Comic Prime Inc.", "Amount": "447273.0", "Employees": 20, "Size by metric": 20, "Quarter": "Q2"},
    {"Company name": "Comic Prime Inc.", "Amount": "147273.0", "Employees": 90, "Size by metric": 20, "Quarter": "Q1"},
    {"Company name": "Cupar Times Inc.", "Amount": "345540.0", "Employees": 1, "Size by metric": 200, "Quarter": "Q2"},
    {
        "Company name": "Bryson Wirral Ltd.",
        "Amount": "185344.0",
        "Employees": 100,
        "Size by metric": 150,
        "Quarter": "Q2",
    },
    {
        "Company name": "Necessities Caunt Co.",
        "Amount": "133427.0",
        "Employees": 200,
        "Size by metric": 100,
        "Quarter": "Q2",
    },
]


EXAMPLE_DATA_SCATTER = [
    {"Company name": "Blockers Mueller Inc.", "Amount": "520490.0", "Employees": 99, "Quarter": "Q2"},
    {"Company name": "Blockers Mueller Inc.", "Amount": "420490.0", "Employees": 40, "Quarter": "Q1"},
    {"Company name": "Comic Prime Inc.", "Amount": "447273.0", "Employees": 20, "Quarter": "Q2"},
    {"Company name": "Cupar Times Inc.", "Amount": "345540.0", "Employees": 1, "Quarter": "Q2"},
    {"Company name": "Bryson Wirral Ltd.", "Amount": "185344.0", "Employees": 100, "Quarter": "Q2"},
    {"Company name": "Necessities Caunt Co.", "Amount": "133427.0", "Employees": 200, "Quarter": "Q2"},
]
