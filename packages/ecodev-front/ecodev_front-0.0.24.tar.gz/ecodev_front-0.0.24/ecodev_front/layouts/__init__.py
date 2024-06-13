"""
Module containing all base (app) and page layouts
"""

from ecodev_front.layouts.app_layout import dash_base_layout
from ecodev_front.layouts.page_helpers import generic_page
from ecodev_front.layouts.page_layouts import simple_layout
from ecodev_front.layouts.page_layouts import page_left_aside
from ecodev_front.layouts.page_layouts import page_right_aside
from ecodev_front.layouts.page_layouts import page_left_right_asides


__all__ = ['dash_base_layout', 'generic_page', 'simple_layout', 
           'page_left_aside', 'page_right_aside', 'page_left_right_asides']