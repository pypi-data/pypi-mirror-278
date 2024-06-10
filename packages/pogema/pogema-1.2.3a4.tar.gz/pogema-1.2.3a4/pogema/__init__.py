from gymnasium import register
from pogema.grid_config import GridConfig
from pogema.integrations.make_pogema import pogema_v0
from pogema.svg_animation.animation_wrapper import AnimationMonitor, AnimationConfig
from pogema.a_star_policy import AStarAgent, BatchAStarAgent

from pogema.grid_config import Easy8x8, Normal8x8, Hard8x8, ExtraHard8x8
from pogema.grid_config import Easy16x16, Normal16x16, Hard16x16, ExtraHard16x16
from pogema.grid_config import Easy32x32, Normal32x32, Hard32x32, ExtraHard32x32
from pogema.grid_config import Easy64x64, Normal64x64, Hard64x64, ExtraHard64x64

__version__ = '1.2.3a4'


__all__ = [
    'GridConfig',
    'pogema_v0',
    'AStarAgent', 'BatchAStarAgent',
    "AnimationMonitor", "AnimationConfig",

    'Easy8x8', 'Normal8x8', 'Hard8x8', 'ExtraHard8x8',
    'Easy16x16', 'Normal16x16', 'Hard16x16', 'ExtraHard16x16',
    'Easy32x32', 'Normal32x32', 'Hard32x32', 'ExtraHard32x32',
    'Easy64x64', 'Normal64x64', 'Hard64x64', 'ExtraHard64x64',
]

register(
    id="Pogema-v0",
    entry_point="pogema.integrations.make_pogema:make_single_agent_gym",
)
