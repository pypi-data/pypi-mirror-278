"""
Sfmrect package for rectification functionality using Structure from Motion (SfM).

This package provides tools for various image processing and rectification tasks.
"""

# Import necessary components for easy access
from .sfmrect import (
    blackout_by_bgmatting_mask,
    blackout_vertical_by_mask,
    convert_disp_to_depth_png16,
    fast_tanh2,
    horizontal_teeth_mask_ratio,
    run_sfm_rectification
)

# Define what should be accessible directly from the package
__all__ = [
    'blackout_by_bgmatting_mask',
    'blackout_vertical_by_mask',
    'convert_disp_to_depth_png16',
    'fast_tanh2',
    'horizontal_teeth_mask_ratio',
    'run_sfm_rectification'
]

# Add version information
__version__ = '0.1.0'
__author__ = 'TamilSelvan'
__email__ = 'tamilselvan82485@gmail.com'

# Package-level initialization code (if any)
# For example, setting up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Sfmrect package initialized.")
