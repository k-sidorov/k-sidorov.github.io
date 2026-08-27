#!/usr/bin/env python3
"""Generate the SVG figures for the JAIR 2026 proof-length-minimization post.

Regenerates assets/img/jair2026-*.svg for the post
_posts/2026-08-27-shortest-proofs.md.

The font <defs> block (Signika Negative, subset, base64-embedded) is lifted
verbatim from assets/img/cp2026-single-task.svg so the figures match the ones
already on the site.  Run from anywhere:

    python3 bin/figures/jair2026-figures.py
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # repository root
OUT = os.path.join(ROOT, "assets", "img")

# --- palette (matches assets/img/cp2026-*.svg) -----------------------------
INDIGO = "#6366f1"
INDIGO_DK = "#4f46e5"
INDIGO_LT = "#e0e7ff"
ROSE = "#e11d48"
ROSE_LT = "#ffe4e6"
AMBER = "#d97706"
AMBER_LT = "#fef3c7"
GRAY_BG = "#f9fafb"
GRAY_LN = "#d1d5db"
GRAY_TX = "#9ca3af"
GRAY_DK = "#6b7280"
INK = "#374151"


def font_defs():
    src = open(os.path.join(ROOT, "assets", "img", "cp2026-single-task.svg")).read()
    return re.search(r"<defs>.*?</defs>", src, re.S).group(0)


DEFS = font_defs()

ARROW_DEFS = """
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"
            markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{gray}"/>
    </marker>
    <marker id="ahi" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"
            markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{indigo}"/>
    </marker>
  </defs>
""".format(gray=GRAY_TX, indigo=INDIGO_DK)


def svg(name, w, h, body, extra_defs=True):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f"font-family=\"'Signika Negative', sans-serif\">\n"
        + DEFS
        + (ARROW_DEFS if extra_defs else "")
        + body
        + "\n</svg>\n"
    )
    path = os.path.join(OUT, name)
    open(path, "w").write(doc)
    print(f"wrote {path} ({len(doc)/1024:.0f} KB)")


# --- clause rendering ------------------------------------------------------
# A clause is a string like "x-y z" -- a literal prefixed with '-' is negated
# and gets an overbar (matching the paper's compact notation).


def parse(clause):
    lits, i = [], 0
    while i < len(clause):
        if clause[i] == "-":
            lits.append((clause[i + 1], True))
            i += 2
        else:
            lits.append((clause[i], False))
            i += 1
    return lits


def clause_text(cx, cy, clause, size=15, fill=INK, weight="600", adv=None):
    """Centered clause label with drawn overbars over negated literals."""
    if clause == "0":  # the empty clause
        return (
            f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">&#8869;</text>'
        )
    lits = parse(clause)
    adv = adv if adv is not None else size * 0.60
    total = len(lits) * adv
    x0 = cx - total / 2
    out = []
    for k, (ch, neg) in enumerate(lits):
        lx = x0 + adv * (k + 0.5)
        out.append(
            f'<text x="{lx:.1f}" y="{cy}" text-anchor="middle" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{ch}</text>'
        )
        if neg:
            # the bar covers the glyph, so it scales with the font size rather
            # than with the advance -- widening the spacing must not widen it
            bar_y = cy - size * 0.78
            bar_half = size * 0.216
            out.append(
                f'<line x1="{lx - bar_half:.1f}" y1="{bar_y:.1f}" '
                f'x2="{lx + bar_half:.1f}" y2="{bar_y:.1f}" '
                f'stroke="{fill}" stroke-width="1.3" stroke-linecap="round"/>'
            )
    return "".join(out)


def chip(cx, cy, clause, w=54, h=30, fill=INDIGO_LT, stroke=INDIGO,
         text=INDIGO_DK, size=15, dash=None, opacity=1.0, adv=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (
        f'<g{o}><rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h}" '
        f'rx="6" fill="{fill}" stroke="{stroke}"{d}/>'
        + clause_text(cx, cy + size * 0.35, clause, size=size, fill=text, adv=adv)
        + "</g>"
    )


def literal_x(cx, n_lits, k, adv):
    """x of the k-th literal of an n-literal clause centered on cx."""
    return cx - n_lits * adv / 2 + adv * (k + 0.5)


def label(x, y, s, size=13, fill=GRAY_DK, anchor="middle", weight="400"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{s}</text>'
    )


def arrow(x1, y1, x2, y2, color=GRAY_TX, marker="ah", width=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"{d}/>'
    )


# ===========================================================================
# Figure 1 -- the resolution rule
# ===========================================================================
def fig_rule():
    b = []
    b.append(label(200, 20, "two clauses you already have", 13, GRAY_TX))
    # premises; the literals are spaced a little wider than the default here, so
    # that the pivot box around x clears the overbar of the neighbouring y
    padv, pbox = 15, 12
    b.append(chip(110, 46, "x-y", w=64, h=32, adv=padv))
    b.append(chip(290, 46, "-x", w=64, h=32, adv=padv))
    # highlight the pivot literals; the box is kept narrower than the advance so
    # that it clears the overbar of the literal next to it
    for cx, n_lits, k in ((110, 2, 0), (290, 1, 0)):
        bx = literal_x(cx, n_lits, k, padv) - pbox / 2
        b.append(f'<rect x="{bx:.1f}" y="32" width="{pbox}" height="28" rx="4" '
                 f'fill="none" stroke="{ROSE}" stroke-width="1.6"/>')
    b.append(arrow(110, 62, 176, 106, INDIGO_DK, "ahi"))
    b.append(arrow(290, 62, 224, 106, INDIGO_DK, "ahi"))
    b.append(chip(200, 124, "-y", w=64, h=32, fill="#ffffff"))
    b.append(label(200, 162,
                   "x is the pivot: the variable the two clauses disagree on", 12, ROSE))
    b.append(label(200, 182, "it cancels, and everything else survives", 12, GRAY_DK))
    svg("jair2026-resolution.svg", 400, 196, "\n".join(b))


# ===========================================================================
# Figure 2 -- a complete proof as a DAG
# ===========================================================================
def fig_dag():
    b = []
    axioms = [("x-y", 78), ("-x", 200), ("y", 322)]
    for cl, x in axioms:
        b.append(chip(x, 34, cl, w=62, h=32, fill=GRAY_BG, stroke=GRAY_LN, text=INK))
    b.append(label(200, 12, "the formula: three clauses that cannot all be true", 12, GRAY_TX))
    b.append(arrow(78, 50, 133, 92, INDIGO_DK, "ahi"))
    b.append(arrow(200, 50, 155, 92, INDIGO_DK, "ahi"))
    b.append(chip(144, 110, "-y", w=62, h=32))
    b.append(arrow(144, 126, 190, 168, INDIGO_DK, "ahi"))
    b.append(arrow(322, 50, 214, 168, INDIGO_DK, "ahi"))
    b.append(chip(200, 186, "0", w=62, h=32, fill=ROSE_LT, stroke=ROSE, text=ROSE))
    b.append(label(246, 182, "the empty clause:", 11, ROSE, anchor="start"))
    b.append(label(246, 197, "no literal is left", 11, ROSE, anchor="start"))
    b.append(label(246, 212, "that could be true", 11, ROSE, anchor="start"))
    b.append(label(200, 232, "5 clauses in total, so this proof has length 5", 13, GRAY_DK))
    svg("jair2026-proof-dag.svg", 400, 248, "\n".join(b))


# ===========================================================================
# Figure 3 -- trimming versus rebuilding
# ===========================================================================
def fig_trim_vs_rebuild():
    b = []
    panel_w = 296

    def node(x, y, r=9, fill=INDIGO_LT, stroke=INDIGO, dash=None, op=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op != 1.0 else ""
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="1.5"{d}{o}/>')

    def edge(x1, y1, x2, y2, color=INDIGO, op=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op != 1.0 else ""
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                f'stroke-width="1.4"{d}{o}/>')

    # ---- left panel: a solver proof, with dead branches trimmed away
    b.append(f'<rect x="8" y="34" width="{panel_w}" height="196" rx="10" '
             f'fill="none" stroke="{GRAY_LN}"/>')
    b.append(label(8 + panel_w / 2, 22, "Trimming: drop the steps you never used", 13, INK, weight="600"))

    live = {"a": (60, 66), "b": (110, 66), "c": (160, 66), "d": (210, 66),
            "e": (85, 120), "f": (185, 120), "g": (135, 172)}
    dead = {"p": (255, 66), "q": (255, 120), "r": (232, 172)}
    for (x, y) in dead.values():
        b.append(node(x, y, fill="#ffffff", stroke=GRAY_TX, dash="3 3", op=0.75))
    b.append(edge(255, 75, 255, 111, GRAY_TX, 0.75, "3 3"))
    b.append(edge(210, 75, 249, 112, GRAY_TX, 0.75, "3 3"))
    b.append(edge(255, 129, 236, 163, GRAY_TX, 0.75, "3 3"))
    b.append(f'<line x1="222" y1="52" x2="278" y2="190" stroke="{ROSE}" '
             f'stroke-width="2" opacity="0.55"/>')
    b.append(label(268, 205, "trimmed", 11, ROSE))

    for (x, y) in live.values():
        b.append(node(x, y))
    for (x1, y1, x2, y2) in [(60, 75, 82, 111), (110, 75, 88, 111),
                             (160, 75, 182, 111), (210, 75, 188, 111),
                             (85, 129, 130, 163), (185, 129, 140, 163)]:
        b.append(edge(x1, y1, x2, y2))
    b.append(f'<circle cx="135" cy="172" r="9" fill="{ROSE_LT}" stroke="{ROSE}" stroke-width="1.5"/>')
    b.append(label(8 + panel_w / 2, 220,
                   "same reasoning, fewer steps written down", 12, GRAY_DK))

    # ---- right panel: a different, shorter derivation
    x0 = 336
    b.append(f'<rect x="{x0}" y="34" width="{panel_w}" height="196" rx="10" '
             f'fill="none" stroke="{GRAY_LN}"/>')
    b.append(label(x0 + panel_w / 2, 22, "Minimizing: think different", 13, INK, weight="600"))
    new = {"a": (x0 + 70, 66), "b": (x0 + 140, 66), "c": (x0 + 210, 66),
           "d": (x0 + 105, 120), "e": (x0 + 148, 172)}
    for (x, y) in new.values():
        b.append(node(x, y))
    for (x1, y1, x2, y2) in [(x0 + 70, 75, x0 + 100, 111),
                             (x0 + 140, 75, x0 + 110, 111),
                             (x0 + 105, 129, x0 + 142, 163),
                             (x0 + 210, 75, x0 + 155, 163)]:
        b.append(edge(x1, y1, x2, y2))
    b.append(f'<circle cx="{x0 + 148}" cy="172" r="9" fill="{ROSE_LT}" '
             f'stroke="{ROSE}" stroke-width="1.5"/>')
    b.append(label(x0 + panel_w / 2, 220,
                   "an entirely different chain of derivations", 12, GRAY_DK))
    svg("jair2026-trim-vs-rebuild.svg", 640, 244, "\n".join(b))


# ===========================================================================
# Figure 4 -- the layer list
# ===========================================================================
def fig_layers():
    layers = [
        ("L0", ["y-t", "xyzt", "-xy", "y-z", "-z-t", "-x-t", "x-y"]),
        ("L1", ["-xz", "yzt"]),
        ("L2", ["-xt", "yt"]),
        ("L3", ["y", "-x"]),
        ("L4", ["-y"]),
        ("L5", ["0"]),
    ]
    b = []
    top, band_h, gap = 40, 40, 8
    chip_w, chip_gap = 56, 8
    left = 74
    b.append(label(280, 20, "every clause sits in the earliest layer that can produce it",
                   13, INK, weight="600"))
    for i, (name, clauses) in enumerate(layers):
        cy = top + i * (band_h + gap) + band_h / 2
        n = len(clauses)
        width = n * chip_w + (n - 1) * chip_gap
        b.append(f'<rect x="{left - 12}" y="{cy - band_h / 2}" width="{width + 24}" '
                 f'height="{band_h}" rx="10" fill="{GRAY_BG}" stroke="{GRAY_LN}"/>')
        sub = f'<tspan font-size="10" dy="3">{name[1]}</tspan>'
        b.append(f'<text x="{left - 26}" y="{cy + 5}" text-anchor="end" font-size="14" '
                 f'fill="{GRAY_DK}" font-weight="600">L{sub}</text>')
        for k, cl in enumerate(clauses):
            cx = left + chip_w / 2 + k * (chip_w + chip_gap)
            if cl == "0":
                b.append(chip(cx, cy, cl, w=chip_w, h=30, fill=ROSE_LT,
                              stroke=ROSE, text=ROSE))
            elif i == 0:
                b.append(chip(cx, cy, cl, w=chip_w, h=30, fill="#ffffff",
                              stroke=GRAY_LN, text=INK))
            else:
                b.append(chip(cx, cy, cl, w=chip_w, h=30))
    b.append(label(left - 40, top + 6 * (band_h + gap) + 18,
                   "L&#8320; holds the axioms; each later layer is built out of the ones before it",
                   12, GRAY_TX, anchor="start"))

    # the take-it-or-leave-it callout
    cx_ghost = left + chip_w / 2 + 2 * (chip_w + chip_gap)
    cy_ghost = top + 2 * (band_h + gap) + band_h / 2
    b.append(chip(cx_ghost, cy_ghost, "-xz", w=chip_w, h=30, fill="#ffffff",
                  stroke=ROSE, text=ROSE, dash="4 3", opacity=0.95))
    b.append(f'<line x1="{cx_ghost - 20}" y1="{cy_ghost - 11}" '
             f'x2="{cx_ghost + 20}" y2="{cy_ghost + 11}" stroke="{ROSE}" stroke-width="1.6"/>')
    b.append(arrow(cx_ghost + 40, cy_ghost, cx_ghost + 92, cy_ghost, ROSE, "ah"))
    b.append(label(cx_ghost + 100, cy_ghost - 4,
                   "not allowed: this clause already", 12, ROSE, anchor="start"))
    b.append(label(cx_ghost + 100, cy_ghost + 12,
                   "follows from the axioms alone", 12, ROSE, anchor="start"))
    svg("jair2026-layers.svg", 560, 356, "\n".join(b))


# ===========================================================================
# Figure 5 -- the branching scheme
# ===========================================================================
def fig_branching():
    b = []
    b.append(label(280, 20, "one candidate at a time, in a fixed order", 13, INK, weight="600"))
    # root
    b.append(f'<rect x="170" y="34" width="220" height="46" rx="10" '
             f'fill="{GRAY_BG}" stroke="{GRAY_LN}"/>')
    b.append(label(280, 52, "candidates for the next layer", 11, GRAY_TX))
    for k, cl in enumerate(["-y", "xt", "yz"]):
        b.append(chip(212 + k * 68, 66, cl, w=54, h=22, fill="#ffffff",
                      stroke=INDIGO, size=13))
    kids = [
        (78, "derive", ["-y"], []),
        (232, "derive", ["xt"], ["-y"]),
        (386, "derive", ["yz"], ["-y", "xt"]),
        (540, "close the layer", [], ["-y", "xt", "yz"]),
    ]
    for x, cap, taken, skipped in kids:
        b.append(arrow(280, 82, x, 122, GRAY_TX, "ah"))
        b.append(f'<rect x="{x - 68}" y="126" width="136" height="94" rx="10" '
                 f'fill="#ffffff" stroke="{GRAY_LN}"/>')
        b.append(label(x, 145, cap, 11, GRAY_DK, weight="600"))
        if taken:
            b.append(chip(x, 166, taken[0], w=52, h=24, size=14))
        else:
            b.append(label(x, 171, "nothing new", 13, GRAY_TX))
        if skipped:
            b.append(label(x, 194, "give up for good on:", 10, GRAY_TX))
            cw, cg = 26, 6
            total = len(skipped) * cw + (len(skipped) - 1) * cg
            for k, cl in enumerate(skipped):
                b.append(chip(x - total / 2 + cw / 2 + k * (cw + cg), 206, cl,
                              w=cw, h=18, size=11, fill="#ffffff",
                              stroke=GRAY_LN, text=GRAY_TX))
        else:
            b.append(label(x, 200, "nothing given up yet", 10, GRAY_TX))
    b.append(label(300, 242,
                   "the branches are disjoint, and together they cover every proof",
                   12, GRAY_DK))
    svg("jair2026-branching.svg", 620, 258, "\n".join(b))


# ===========================================================================
# Figure 6 -- the model-covering lower bound
# ===========================================================================
def fig_counting():
    b = []
    b.append(label(240, 20, "how few clauses could possibly do the job?", 13, INK, weight="600"))
    bar_x, bar_y, bar_w, bar_h = 40, 46, 384, 34
    seg = bar_w / 8
    b.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" '
             f'fill="{GRAY_BG}" stroke="{GRAY_LN}"/>')
    for k in range(8):
        x = bar_x + k * seg
        filled = k < 5
        b.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{seg:.1f}" height="{bar_h}" '
                 f'fill="{INDIGO_LT if filled else "#ffffff"}" stroke="{INDIGO if filled else GRAY_LN}" '
                 f'{"" if filled else "stroke-dasharray=\'4 3\'"}/>')
        b.append(label(x + seg / 2, bar_y + 22, "1/8", 12,
                       INDIGO_DK if filled else GRAY_TX))
    b.append(label(bar_x, bar_y - 8, "every possible assignment to the variables",
                   12, GRAY_TX, anchor="start"))
    b.append(label(232, bar_y + bar_h + 20,
                   "each three-literal clause rules out one eighth of them &#8230;",
                   12, GRAY_DK))
    b.append(label(232, bar_y + bar_h + 38,
                   "&#8230; and for a contradiction, the bar has to be covered completely",
                   12, GRAY_DK))
    b.append(f'<rect x="40" y="140" width="384" height="40" rx="10" '
             f'fill="{AMBER_LT}" stroke="{AMBER}"/>')
    b.append(label(232, 165,
                   "so no unsatisfiable set of 3-clauses has fewer than 8 of them",
                   13, "#92400e", weight="600"))
    svg("jair2026-counting.svg", 464, 194, "\n".join(b))


if __name__ == "__main__":
    fig_rule()
    fig_dag()
    fig_trim_vs_rebuild()
    fig_layers()
    fig_branching()
    fig_counting()
