from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum

# Enum classes for DefaultNodeAppearance and NodeOutlineColor
class DefaultNodeAppearance(Enum):
    Default = 'Default'
    Outlined = 'Outlined'
    Hidden = 'Hidden'
    InFront = 'InFront'
    Ghosted = 'Ghosted'

@dataclass
class Color:
    r: float
    g: float
    b: float

@dataclass
class NodeAppearance:
    """
    Data class to represent the appearance of a node.
    """
    color: Optional[Color|str] = None
    visible: Optional[bool] = None
    render_in_front: Optional[bool] = None
    render_ghosted: Optional[bool] = None
    outline_color: Optional[Color|str] = None
    prioritized_for_loading_hint: Optional[int] = None
    

@dataclass
class StyledNodeCollection:
    filter_criteria: Dict[str, Any]
    node_appearance: NodeAppearance

@dataclass
class ClippingPlane:
    normal: Tuple[float, float, float]
    distance: float

@dataclass
class RevealConfig:
    clipping_planes: List[ClippingPlane] = field(default_factory=list)
    selected_asset_ids: List[int] = field(default_factory=list)
    default_node_appearance: DefaultNodeAppearance = DefaultNodeAppearance.Default
    styled_node_collections: List[StyledNodeCollection] = field(default_factory=list)
    height: int = 500