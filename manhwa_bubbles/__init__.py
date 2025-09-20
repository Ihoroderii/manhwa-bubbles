"""
Manhwa Bubbles - A Python library for creating manhwa-style speech bubbles and narration boxes.

This library provides functions to create various types of speech bubbles and narration
boxes commonly used in manhwa, manga, and comics.
"""

from .speech_bubbles import (
    speech_bubble, 
    draw_tail, 
    bubble_heart, 
    bubble_spiky, 
    bubble_glow, 
    bubble_scratchy
)
from .organic_overlap import (
    generate_overlapping_bubble,
)
from .extended_styles import (
    bubble_wide_soft,
    bubble_tall_narrow,
    bubble_whisper_dotted,
    bubble_shout_burst,
    bubble_shock_mini_spike,
    bubble_rage_flame,
    bubble_laugh_bouncy,
    bubble_giggle_soft,
    bubble_cry_drip,
    bubble_nervous_wobble,
    bubble_sarcastic_geometric,
    bubble_thought_cloud_chain,
    bubble_inner_monologue,
    bubble_whisper_thought,
    bubble_inverted_aura,
    bubble_dripping_horror,
    bubble_magic_glow_frame,
    bubble_arcane_glyph,
    bubble_telepathy_wave,
    bubble_ghost_translucent,
    bubble_static_electric,
    bubble_digital_system,
    bubble_radio_comms,
    bubble_robotic_panel,
    bubble_ai_card,
    bubble_impact_bang,
    bubble_sfx_capsule,
    bubble_chain_overlap_sequence,
    bubble_trailing_sequence,
    bubble_echo_layers,
    bubble_fragmented_arc,
    bubble_breath_cold,
    bubble_sleepy_slump,
    bubble_drunk_slur,
    bubble_hypnotic_spiral,
    bubble_chant_choral,
    bubble_text_only,
    bubble_bracketed_text,
    bubble_bold_plate,
    bubble_organic_overlapping_stub,
)
from .narrators import (
    narrator_plain,
    narrator_borderless, 
    narrator_dashed,
    narrator_dark,
    narrator_wavy
)

__version__ = "1.1.0"
__author__ = "Ihor Oderii"
__email__ = "ihor.oderii@gmail.com"

__all__ = [
    'speech_bubble',
    'draw_tail',
    'bubble_heart',
    'bubble_spiky', 
    'bubble_glow',
    'bubble_scratchy',
    'narrator_plain',
    'narrator_borderless',
    'narrator_dashed', 
    'narrator_dark',
    'narrator_wavy'
    ,'generate_overlapping_bubble'
    ,'bubble_wide_soft'
    ,'bubble_tall_narrow'
    ,'bubble_whisper_dotted'
    ,'bubble_shout_burst'
    ,'bubble_shock_mini_spike'
    ,'bubble_rage_flame'
    ,'bubble_laugh_bouncy'
    ,'bubble_giggle_soft'
    ,'bubble_cry_drip'
    ,'bubble_nervous_wobble'
    ,'bubble_sarcastic_geometric'
    ,'bubble_thought_cloud_chain'
    ,'bubble_inner_monologue'
    ,'bubble_whisper_thought'
    ,'bubble_inverted_aura'
    ,'bubble_dripping_horror'
    ,'bubble_magic_glow_frame'
    ,'bubble_arcane_glyph'
    ,'bubble_telepathy_wave'
    ,'bubble_ghost_translucent'
    ,'bubble_static_electric'
    ,'bubble_digital_system'
    ,'bubble_radio_comms'
    ,'bubble_robotic_panel'
    ,'bubble_ai_card'
    ,'bubble_impact_bang'
    ,'bubble_sfx_capsule'
    ,'bubble_chain_overlap_sequence'
    ,'bubble_trailing_sequence'
    ,'bubble_echo_layers'
    ,'bubble_fragmented_arc'
    ,'bubble_breath_cold'
    ,'bubble_sleepy_slump'
    ,'bubble_drunk_slur'
    ,'bubble_hypnotic_spiral'
    ,'bubble_chant_choral'
    ,'bubble_text_only'
    ,'bubble_bracketed_text'
    ,'bubble_bold_plate'
    ,'bubble_organic_overlapping_stub'
]