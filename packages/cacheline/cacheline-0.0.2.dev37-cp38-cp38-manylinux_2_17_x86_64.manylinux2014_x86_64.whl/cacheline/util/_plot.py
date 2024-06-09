from typing import TYPE_CHECKING, List

from pydantic import BaseModel  # pylint:disable=no-name-in-module

if TYPE_CHECKING:
    from shapely.geometry import Polygon  # type:ignore


class Property(BaseModel):
    color: str


class Feature(BaseModel):
    geometries: List["Polygon"]
    properties: Property

    class Config:
        arbitrary_types_allowed = True


def plot(features: List[Feature]):
    try:
        import matplotlib.pyplot as plt  # type:ignore
    except ImportError as err:
        raise ImportError("Please install matplotlib to use this function") from err
    _, axs = plt.subplots()
    axs.set_aspect("equal", "datalim")
    for feature in features:
        for geometry in feature.geometries:
            x, y = geometry.exterior.xy
            axs.fill(x, y, feature.properties.color)
    plt.show()
