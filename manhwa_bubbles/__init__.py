"""
Manhwa Bubbles - A Python library for creating manhwa-style speech bubbles and narration boxes.

This library provides functions to create various types of speech bubbles and narration
boxes commonly used in manhwa, manga, and comics.
"""

from .speech_bubbles import speech_bubble, draw_tail
from .narrators import (
    narrator_plain,
    narrator_borderless, 
    narrator_dashed,
    narrator_dark,
    narrator_wavy
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    'speech_bubble',
    'draw_tail',
    'narrator_plain',
    'narrator_borderless',
    'narrator_dashed', 
    'narrator_dark',
    'narrator_wavy'
]