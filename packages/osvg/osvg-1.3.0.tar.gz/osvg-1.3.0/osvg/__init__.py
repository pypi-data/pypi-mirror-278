"""
Object-oriented SVG Drawing Tool
"""

from .float import (
    Const,
)
from .float_math import (
    InvertedSign,
    Cos,
    Sin,
    Cot,
    Tan,
    FunctFloat,
    Prod,
    Sum,
    Min,
    LowestAbs,
    Max,
)
from .elements.circle import Circle
from .elements.elementbase import (
    Height,
    Width,
)
from .elements.ellipse import Ellipse
from .elements.group import Group
from .elements.line import Line
from .elements.line_marker import (
    CircleMarker,
    ArrowMarker,
    LightArrowMarker,
    SkinnyArrowMarker,
)
from .elements.text import Text, TextSpan
from .elements.path import (
    Path,
    PathA,
    PathC,
    Pathc,
    PathH,
    Pathh,
    PathL,
    Pathl,
    PathM,
    Pathm,
    PathQ,
    Pathq,
    PathS,
    Paths,
    PathT,
    Patht,
    PathV,
    Pathv,
    PathZ,
)
from .elements.polyline import Polyline
from .elements.rectangle import Rectangle, SCRectangle
from .elements.svg import SVG, ViewBox
from .positions import (
    Position,
    ShiftedPosition,
    PolarShiftedPosition,
    RotatedPosition,
    Distance,
    AngleDegree,
)
from .style import (
    FillColor,
    FillOpacity,
    StrokeDashArray,
    StrokeColor,
    StrokeLineCap,
    StrokeLineJoin,
    StrokeOpacity,
    StrokeWidth,
    Style,
)

__version__ = "1.3.0"
version_info = (1, 3, 0)
