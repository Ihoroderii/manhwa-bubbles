"""Demonstration of extended bubble styles.
Saves a composite grid image for quick visual inspection.
"""
from PIL import Image, ImageDraw
from manhwa_bubbles import (
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

STYLES = [
    (bubble_wide_soft, "Wide Soft"),
    (bubble_tall_narrow, "Tall Narrow"),
    (bubble_whisper_dotted, "Whisper"),
    (bubble_shout_burst, "Shout"),
    (bubble_shock_mini_spike, "Shock"),
    (bubble_rage_flame, "Rage"),
    (bubble_laugh_bouncy, "Laugh"),
    (bubble_giggle_soft, "Giggle"),
    (bubble_cry_drip, "Cry"),
    (bubble_nervous_wobble, "Nervous"),
    (bubble_sarcastic_geometric, "Sarcastic"),
    (bubble_thought_cloud_chain, "Thought"),
    (bubble_inner_monologue, "Monologue"),
    (bubble_whisper_thought, "WhispThought"),
    (bubble_inverted_aura, "Inverted"),
    (bubble_dripping_horror, "Horror"),
    (bubble_magic_glow_frame, "Magic"),
    (bubble_arcane_glyph, "Glyph"),
    (bubble_telepathy_wave, "Telepathy"),
    (bubble_ghost_translucent, "Ghost"),
    (bubble_static_electric, "Static"),
    (bubble_digital_system, "Digital"),
    (bubble_radio_comms, "Radio"),
    (bubble_robotic_panel, "Robotic"),
    (bubble_ai_card, "AI Card"),
    (bubble_impact_bang, "Impact"),
    (bubble_sfx_capsule, "SFX"),
    (bubble_chain_overlap_sequence, "Chain"),
    (bubble_trailing_sequence, "Trail"),
    (bubble_echo_layers, "Echo"),
    (bubble_fragmented_arc, "Frag"),
    (bubble_breath_cold, "Breath"),
    (bubble_sleepy_slump, "Sleepy"),
    (bubble_drunk_slur, "Drunk"),
    (bubble_hypnotic_spiral, "Hypnotic"),
    (bubble_chant_choral, "Chant"),
    (bubble_text_only, "TextOnly"),
    (bubble_bracketed_text, "Bracketed"),
    (bubble_bold_plate, "Plate"),
    (bubble_organic_overlapping_stub, "OrganicStub"),
]

def main():
    cols = 6
    cell_w, cell_h = 170, 140
    pad = 20
    rows = (len(STYLES) + cols - 1)//cols
    img_w = cols*cell_w + (cols+1)*pad
    img_h = rows*cell_h + (rows+1)*pad + 40
    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)
    for idx, (fn, label) in enumerate(STYLES):
        row = idx // cols
        col = idx % cols
        x = pad + col*cell_w
        y = pad + row*cell_h
        # bubble area
        area = (x+10, y+10, cell_w-20, cell_h-40)
        try:
            if fn in (bubble_chain_overlap_sequence,):
                fn(draw, [((area[0], area[1], 60, 50), "A"), ((area[0]+30, area[1]+10, 60, 50), "B"), ((area[0]+60, area[1]+20, 60, 50), "C")])
            elif fn in (bubble_trailing_sequence,):
                fn(draw, [((area[0], area[1], 80, 60), "...") , ((area[0]+50, area[1]+10, 70, 50), ".."), ((area[0]+90, area[1]+20, 50, 40), ".")])
            else:
                fn(draw, (area[0], area[1], area[2], area[3]), label[:6])
        except Exception as e:
            draw.text((x+15,y+40), f"ERR {label}", fill="red")
        draw.text((x+8, y+cell_h-25), label, fill="black")
    img.save("extended_styles_demo.png")
    print("Saved extended_styles_demo.png")

if __name__ == "__main__":
    main()
