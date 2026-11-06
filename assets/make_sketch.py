"""Generate assets/team.svg, the pen sketch of the devs roles around a table.

Run: python3 assets/make_sketch.py assets/team.svg
The random seed is fixed, so the same code gives the same drawing.
"""
import math, random, sys

random.seed(7)
W, H = 1360, 470
TABLE_Y = 352          # table top front edge
out = []

def P(*a): out.append("".join(a))

def wob(v, s=1.2): return v + random.uniform(-s, s)

def sketch_circle(cx, cy, r, sw=2.2, fill="none"):
    # Irregular circle that slightly overshoots its start, like a pen stroke.
    n = 14
    start = random.uniform(0, 2 * math.pi)
    pts = []
    for i in range(n + 3):
        a = start + i * 2 * math.pi / n
        rr = r * random.uniform(0.95, 1.05)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        c1 = (p0[0] + (p1[0] - (pts[i - 2][0] if i > 1 else p0[0])) / 6, p0[1] + (p1[1] - (pts[i - 2][1] if i > 1 else p0[1])) / 6)
        c2 = (p1[0] - (p2[0] - p0[0]) / 6, p1[1] - (p2[1] - p0[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}"
    P(f'<path d="{d}" fill="{fill}" stroke-width="{sw}"/>')

def line(d, sw=2.2, twice=True):
    P(f'<path d="{d}" stroke-width="{sw}"/>')
    if twice:  # a second, lighter pass makes it read as a pen sketch
        P(f'<path d="{d}" stroke-width="{sw*0.5:.1f}" opacity="0.45" transform="translate({wob(0,1.4):.1f} {wob(0,1.4):.1f})"/>')

def text(x, y, s, size=17, anchor="middle", weight="normal", fill="#111", extra=""):
    # No attribute may repeat: GitHub shows an SVG as a standalone image, and a
    # duplicate attribute makes the whole file invalid XML there.
    P(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" stroke="none" fill="{fill}" {extra}>{s}</text>')

def bubble(x, y, w, h, tail_x, tail_y, msg):
    # Rounded box with a tail pointing at the speaker.
    r = 14
    l, t, rgt, b = x - w / 2, y - h / 2, x + w / 2, y + h / 2
    tx = max(l + 22, min(rgt - 22, tail_x))
    d = (f"M{l+r},{t} H{rgt-r} Q{rgt},{t} {rgt},{t+r} V{b-r} Q{rgt},{b} {rgt-r},{b} "
         f"H{tx+9} L{tail_x},{tail_y} L{tx-5},{b} H{l+r} Q{l},{b} {l},{b-r} V{t+r} Q{l},{t} {l+r},{t} Z")
    P(f'<path d="{d}" fill="#fff" stroke-width="2"/>')
    P(f'<path d="{d}" fill="none" stroke-width="1" opacity="0.4" transform="translate(1.5 1)"/>')
    text(x, y + 6, msg, 15)

def face(x, hy, glasses=False, brows=None, mouth="smile"):
    if glasses:
        sketch_circle(x - 9, hy - 2, 6.5, 1.8)
        sketch_circle(x + 9, hy - 2, 6.5, 1.8)
        line(f"M{x-2.5},{hy-2} H{x+2.5}", 1.6, False)
    P(f'<circle cx="{x-9}" cy="{hy-2}" r="2.1" fill="#111" stroke="none"/>')
    P(f'<circle cx="{x+9}" cy="{hy-2}" r="2.1" fill="#111" stroke="none"/>')
    if brows == "raised":   # one brow up: doubt
        line(f"M{x-15},{hy-12} L{x-4},{hy-11}", 1.8, False)
        line(f"M{x+4},{hy-15} Q{x+10},{hy-19} {x+16},{hy-14}", 1.8, False)
    elif brows == "focus":
        line(f"M{x-15},{hy-13} L{x-4},{hy-10}", 1.8, False)
        line(f"M{x+4},{hy-10} L{x+15},{hy-13}", 1.8, False)
    if mouth == "smile":
        line(f"M{x-7},{hy+10} Q{x},{hy+16} {x+7},{hy+10}", 1.8, False)
    elif mouth == "flat":
        line(f"M{x-6},{hy+12} H{x+6}", 1.8, False)
    elif mouth == "open":
        sketch_circle(x, hy + 12, 3.5, 1.6)
    elif mouth == "hmm":
        line(f"M{x-6},{hy+13} Q{x},{hy+10} {x+7},{hy+12}", 1.8, False)

def seated(x, hair="short", arms="table", **f):
    hy = 228   # head centre
    # torso (the table hides the lower half)
    line(f"M{x-40},{TABLE_Y} C{x-42},{hy+60} {x-30},{hy+38} {x},{hy+34} C{x+30},{hy+38} {x+42},{hy+60} {x+40},{TABLE_Y}")
    line(f"M{x-6},{hy+27} L{x},{hy+36} L{x+6},{hy+27}", 1.6, False)  # collar
    sketch_circle(x, hy, 27, 2.4, "#fff")
    if hair == "short":
        line(f"M{x-26},{hy-6} C{x-24},{hy-34} {x+24},{hy-34} {x+26},{hy-6} M{x-18},{hy-20} q8,6 18,-2 q8,6 16,0")
    elif hair == "curly":
        for i in range(-3, 4):
            sketch_circle(x + i * 8, hy - 25 + abs(i) * 2.5, 6.5, 1.8, "#fff")
    elif hair == "bun":
        line(f"M{x-26},{hy-4} C{x-26},{hy-34} {x+26},{hy-34} {x+26},{hy-4}")
        sketch_circle(x, hy - 34, 9, 2, "#fff")
    elif hair == "cap":
        line(f"M{x-27},{hy-8} C{x-26},{hy-36} {x+26},{hy-36} {x+27},{hy-8} Z M{x+20},{hy-10} L{x+44},{hy-6}")
    elif hair == "bald":
        line(f"M{x-27},{hy+2} q-4,-8 0,-14 M{x+27},{hy+2} q4,-8 0,-14", 1.8)
    elif hair == "long":
        line(f"M{x-27},{hy+20} C{x-34},{hy-36} {x+34},{hy-36} {x+27},{hy+20} M{x-12},{hy-22} q10,10 26,2")
    elif hair == "spiky":
        line(f"M{x-24},{hy-10} l4,-18 l7,10 l5,-16 l7,13 l6,-15 l5,14 l6,-12 l4,18")
    face(x, hy, **f)
    if arms == "table":
        line(f"M{x-34},{hy+70} Q{x-36},{TABLE_Y-12} {x-18},{TABLE_Y-6} M{x+34},{hy+70} Q{x+36},{TABLE_Y-12} {x+18},{TABLE_Y-6}")
    elif arms == "crossed":
        line(f"M{x-34},{hy+66} Q{x-10},{hy+92} {x+26},{hy+80} M{x+34},{hy+66} Q{x+10},{hy+96} {x-26},{hy+86}")
    elif arms == "raise":   # one hand up, gesturing
        line(f"M{x+34},{hy+62} Q{x+58},{hy+50} {x+56},{hy+18}")
        sketch_circle(x + 56, hy + 10, 8, 2, "#fff")
        line(f"M{x-34},{hy+70} Q{x-36},{TABLE_Y-12} {x-18},{TABLE_Y-6}")
    elif arms == "point":   # pointing at the papers on the table
        line(f"M{x+34},{hy+66} Q{x+46},{hy+100} {x+64},{TABLE_Y-8}")
        line(f"M{x-34},{hy+70} Q{x-36},{TABLE_Y-12} {x-18},{TABLE_Y-6}")
    elif arms == "chin":    # hand on chin, thinking
        line(f"M{x+34},{hy+66} Q{x+30},{hy+52} {x+12},{hy+36}")
        sketch_circle(x + 10, hy + 32, 7, 2, "#fff")
        line(f"M{x-34},{hy+70} Q{x-36},{TABLE_Y-12} {x-18},{TABLE_Y-6}")

def standing(x, y_feet):
    # Step back stands on a small step, hands behind back, looking over the table.
    hy = y_feet - 190
    line(f"M{x-18},{y_feet} L{x-8},{hy+110} M{x+18},{y_feet} L{x+8},{hy+110}")  # legs
    line(f"M{x-30},{y_feet} h12 M{x+18},{y_feet} h12", 2.6)                       # shoes
    line(f"M{x-30},{hy+112} C{x-34},{hy+60} {x-26},{hy+38} {x},{hy+34} C{x+26},{hy+38} {x+34},{hy+60} {x+30},{hy+112} Z")
    line(f"M{x-30},{hy+50} Q{x-40},{hy+80} {x-22},{hy+100} M{x+30},{hy+50} Q{x+40},{hy+80} {x+22},{hy+100}")
    sketch_circle(x, hy, 25, 2.4, "#fff")
    line(f"M{x-25},{hy-4} C{x-24},{hy-30} {x+24},{hy-30} {x+25},{hy-4} M{x-22},{hy-8} q4,-10 14,-12")
    # binoculars hanging on a strap
    line(f"M{x-12},{hy+30} L{x-6},{hy+62} M{x+12},{hy+30} L{x+6},{hy+62}", 1.4, False)
    sketch_circle(x - 7, hy + 70, 7, 1.8, "#fff")
    sketch_circle(x + 7, hy + 70, 7, 1.8, "#fff")
    face(x, hy, brows="focus", mouth="hmm")

P(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  'aria-label="Pen sketch: the devs roles sit around a table and discuss a plan; step back watches from a step">')
P('<defs><filter id="pen" x="-5%" y="-5%" width="110%" height="110%">'
  '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/>'
  '<feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></defs>')
# White card: black lines need a light background on GitHub's dark theme too.
P(f'<rect width="{W}" height="{H}" rx="20" fill="#fff"/>')
P('<g transform="translate(0 -62)" filter="url(#pen)" fill="none" stroke="#111" stroke-linecap="round" stroke-linejoin="round" '
  'font-family="\'Segoe Print\', \'Bradley Hand\', \'Chalkboard SE\', \'Comic Sans MS\', \'Comic Neue\', cursive">')

xs = [100 + 140 * i for i in range(8)]
roles = [
    ("brainstorm",  dict(hair="curly", arms="raise", mouth="open")),
    ("plan",        dict(hair="bun", arms="point", glasses=True)),
    ("implement",   dict(hair="cap", arms="table", mouth="smile")),
    ("neutral",     dict(hair="short", arms="table", glasses=True, mouth="flat")),
    ("skeptic",     dict(hair="bald", arms="crossed", brows="raised", mouth="hmm")),
    ("security",    dict(hair="spiky", arms="table", brows="focus", mouth="flat")),
    ("performance", dict(hair="short", arms="chin", mouth="flat")),
    ("ux",          dict(hair="long", arms="table", mouth="smile")),
]
for x, (name, kw) in zip(xs, roles):
    seated(x, **kw)

# step back: on a small step to the right, a little apart from the table
SX, STEP_Y = 1250, 404
line(f"M{SX-52},{STEP_Y} H{SX+52} V{STEP_Y+44} H{SX-52} Z M{SX-52},{STEP_Y+14} H{SX+52}")
standing(SX, STEP_Y)

# table
R = xs[-1] + 62
line(f"M40,{TABLE_Y} H{R} M30,{TABLE_Y+22} H{R+10} M40,{TABLE_Y} L30,{TABLE_Y+22} M{R},{TABLE_Y} L{R+10},{TABLE_Y+22}")
line(f"M70,{TABLE_Y+22} V{TABLE_Y+120} M{R-30},{TABLE_Y+22} V{TABLE_Y+120}", 2.6)
# things on the table: plan.md papers, the implementer's laptop, mugs
line(f"M268,{TABLE_Y-2} l24,-16 l58,0 l-20,16 Z M286,{TABLE_Y-8} h30 M294,{TABLE_Y-13} h26", 1.8)
text(310, TABLE_Y + 16, "plan.md", 13)
line(f"M352,{TABLE_Y-2} h68 l-4,-4 h-60 Z M360,{TABLE_Y-6} l10,-34 h44 l-6,34", 1.8)
line(f"M566,{TABLE_Y-2} v-16 h16 v16 Z M582,{TABLE_Y-14} q8,0 0,9", 1.8)
line(f"M890,{TABLE_Y-2} v-16 h16 v16 Z M906,{TABLE_Y-14} q8,0 0,9", 1.8)

# name labels under the table edge
for x, (name, _) in zip(xs, roles):
    text(x, TABLE_Y + 50, name, 17, weight="bold")
text(SX, STEP_Y + 72, "step back", 17, weight="bold")

# one row of speech bubbles; short lines so they fit the 140px spacing
says = ["What if...?", "Plan is ready.", "Tests pass.", "Line 42 says...",
        "Do we need it?", "Who can call it?", "At what load?", "Is it clear?"]
for x, msg in zip(xs, says):
    w = 7.3 * len(msg) + 22
    bubble(x, 130, w, 40, x + 4, 188, msg)
bubble(SX, 148, 150, 40, SX + 4, 186, "Is it worth it?")

P('</g>')
text(W - 20, H - 14, "devs", 14, anchor="end", fill="#888", extra='font-family="ui-monospace, Menlo, Consolas, monospace"')
P('</svg>')
open(sys.argv[1], "w").write("\n".join(out))
