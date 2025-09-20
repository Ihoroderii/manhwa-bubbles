"""Render every available bubble style into individual PNGs plus a composite sheet.

This covers:
- Core Pillow-based styles from speech_bubbles.py
- Extended styles from extended_styles.py
- Organic overlapping Cairo variant (if pycairo installed)

Outputs:
  build_bubbles/<style_name>.png
  build_bubbles/all_bubbles_sheet.png
"""
import os, math
from PIL import Image, ImageDraw
from manhwa_bubbles import (
    speech_bubble,
    bubble_heart,
    bubble_spiky,
    bubble_glow,
    bubble_scratchy,
    narrator_plain,
    narrator_borderless,
    narrator_dashed,
    narrator_dark,
    narrator_wavy,
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

# Optional Cairo variant
try:
    from manhwa_bubbles import generate_overlapping_bubble
    HAS_CAIRO = True
except Exception:
    HAS_CAIRO = False

OUT_DIR = "build_bubbles"
os.makedirs(OUT_DIR, exist_ok=True)

# (function, label, mode)
# mode: 'single' -> call with (draw, (x,y,w,h), text)
#       'chain'  -> special list input
STYLES = [
    (lambda d,xy,t: speech_bubble(d, xy, t, 'oval'), 'oval'),
    (lambda d,xy,t: speech_bubble(d, xy, t, 'rect'), 'rect'),
    (lambda d,xy,t: speech_bubble(d, xy, t, 'cloud'), 'cloud'),
    (lambda d,xy,t: speech_bubble(d, xy, t, 'jagged'), 'jagged'),
    (lambda d,xy,t: speech_bubble(d, xy, t, 'wavy'), 'wavy'),
    (lambda d,xy,t: speech_bubble(d, xy, t, 'black'), 'black'),
    (lambda d,xy,t: bubble_heart(d, xy, t), 'heart'),
    (lambda d,xy,t: bubble_spiky(d, xy, t), 'spiky'),
    (lambda d,xy,t: bubble_glow(d, xy, t), 'glow'),
    (lambda d,xy,t: bubble_scratchy(d, xy, t), 'scratchy'),
    (bubble_wide_soft, 'wide_soft'),
    (bubble_tall_narrow, 'tall_narrow'),
    (bubble_whisper_dotted, 'whisper_dotted'),
    (bubble_shout_burst, 'shout_burst'),
    (bubble_shock_mini_spike, 'shock_spike'),
    (bubble_rage_flame, 'rage_flame'),
    (bubble_laugh_bouncy, 'laugh_bouncy'),
    (bubble_giggle_soft, 'giggle_soft'),
    (bubble_cry_drip, 'cry_drip'),
    (bubble_nervous_wobble, 'nervous_wobble'),
    (bubble_sarcastic_geometric, 'sarcastic'),
    (bubble_thought_cloud_chain, 'thought_cloud_chain'),
    (bubble_inner_monologue, 'inner_monologue'),
    (bubble_whisper_thought, 'whisper_thought'),
    (bubble_inverted_aura, 'inverted_aura'),
    (bubble_dripping_horror, 'dripping_horror'),
    (bubble_magic_glow_frame, 'magic_glow_frame'),
    (bubble_arcane_glyph, 'arcane_glyph'),
    (bubble_telepathy_wave, 'telepathy_wave'),
    (bubble_ghost_translucent, 'ghost_translucent'),
    (bubble_static_electric, 'static_electric'),
    (bubble_digital_system, 'digital_system'),
    (bubble_radio_comms, 'radio_comms'),
    (bubble_robotic_panel, 'robotic_panel'),
    (bubble_ai_card, 'ai_card'),
    (bubble_impact_bang, 'impact_bang'),
    (bubble_sfx_capsule, 'sfx_capsule'),
    # special multi
    (bubble_chain_overlap_sequence, 'chain_overlap'),
    (bubble_trailing_sequence, 'trailing_sequence'),
    (bubble_echo_layers, 'echo_layers'),
    (bubble_fragmented_arc, 'fragmented_arc'),
    (bubble_breath_cold, 'breath_cold'),
    (bubble_sleepy_slump, 'sleepy_slump'),
    (bubble_drunk_slur, 'drunk_slur'),
    (bubble_hypnotic_spiral, 'hypnotic_spiral'),
    (bubble_chant_choral, 'chant_choral'),
    (bubble_text_only, 'text_only'),
    (bubble_bracketed_text, 'bracketed_text'),
    (bubble_bold_plate, 'bold_plate'),
    (bubble_organic_overlapping_stub, 'organic_overlap_stub'),
]

if HAS_CAIRO:
    STYLES.append((None, 'cairo_organic_minimal'))
    STYLES.append((None, 'cairo_laugh_minimal'))

HEIGHT = 160
WIDTH = 200

results = []

for fn, label in STYLES:
    img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(img)
    if fn is None and 'cairo' in label:
        # Use cairo renderer then paste
        from manhwa_bubbles import generate_overlapping_bubble
        style = 'organic'
        if 'laugh' in label:
            style = 'laugh'
        surface, ctx = generate_overlapping_bubble(160, 110, style=style, show_full_ovals=False)
        # Export to bytes and load via Pillow
        import io
        buf = io.BytesIO()
        surface.write_to_png(buf)
        buf.seek(0)
        cimg = Image.open(buf).convert('RGBA')
        # center
        offx = (WIDTH - cimg.width)//2
        offy = (HEIGHT - cimg.height)//2
        img.paste(cimg, (offx, offy), cimg)
    elif fn in (bubble_chain_overlap_sequence,):
        fn(draw, [((20,30,80,60), 'A'), ((50,40,80,60),'B'), ((80,50,80,60),'C')])
    elif fn in (bubble_trailing_sequence,):
        fn(draw, [((40,35,90,70),'...'), ((95,50,70,55),'..'), ((135,60,50,40),'.')])
    else:
        fn(draw, (20,25,160,100), label[:6])
    out_path = os.path.join(OUT_DIR, f"{label}.png")
    img.save(out_path)
    results.append(out_path)
    print("Saved", out_path)

# Composite sheet -------------------------------------------------
cols = 8
cell_w, cell_h = 220, 190
rows = math.ceil(len(results)/cols)
sheet = Image.new('RGB', (cols*cell_w, rows*cell_h), 'white')
for idx, path in enumerate(results):
    r = idx//cols
    c = idx%cols
    im = Image.open(path)
    sheet.paste(im, (c*cell_w + (cell_w-im.width)//2, r*cell_h + 10))
    # label text
    d = ImageDraw.Draw(sheet)
    lbl = os.path.basename(path).replace('.png','')
    d.text((c*cell_w+10, r*cell_h+cell_h-25), lbl, fill='black')

sheet_out = os.path.join(OUT_DIR, 'all_bubbles_sheet.png')
sheet.save(sheet_out)
print('Saved composite sheet ->', sheet_out)
