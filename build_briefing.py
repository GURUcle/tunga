#!/usr/bin/env python3
"""Build the one-page Tunga sandbox briefing as a print-ready A4 PDF.

Convention: draw helpers take the BASELINE of the first line and return the
baseline for the NEXT block.
"""

import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SUP = "/System/Library/Fonts/Supplemental"
for name, fn in [
    ("Georgia", "Georgia.ttf"),
    ("Georgia-Bold", "Georgia Bold.ttf"),
    ("Georgia-Italic", "Georgia Italic.ttf"),
    ("Arial", "Arial.ttf"),
    ("Arial-Bold", "Arial Bold.ttf"),
    ("Arial-Italic", "Arial Italic.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, f"{SUP}/{fn}"))

GREEN = HexColor("#0B5D4A")
INK = HexColor("#13201B")
MUTED = HexColor("#6C7A73")
LINE = HexColor("#E5E1D7")
SAND = HexColor("#A8822A")
SANDS = HexColor("#F9F1DE")
GREENS = HexColor("#E7F2EE")

W, H = A4
ML, MR = 44, 44
CW = W - ML - MR
TOP = H - 42
BOT = 40

OUT = sys.argv[1] if len(sys.argv) > 1 else "Tunga-briefing.pdf"
# PREVIEW_SCALE=3 renders a 3x page so the result can be rasterised at print
# resolution for visual proofing (sips always rasterises at 72dpi).
SCALE = float(os.environ.get("PREVIEW_SCALE", "0") or 0)
c = canvas.Canvas(OUT, pagesize=(W * SCALE, H * SCALE) if SCALE else A4)
if SCALE:
    c.scale(SCALE, SCALE)
c.setFont("Arial", 8)   # avoid an unused base-14 Helvetica resource
c.setTitle("Tunga \u2014 Regulatory Sandbox Briefing")
c.setAuthor("Tunga")
c.setSubject("Fractional property crowdfunding for Namibia")
c.setKeywords("Namibia, NAMFISA, crowdfunding, regulatory sandbox, property, SPV")

sw = pdfmetrics.stringWidth


def wrap(text, font, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if sw(trial, font, size) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(text, x, y, w, font, size, lead, color=INK, align="left"):
    lines = wrap(text, font, size, w)
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in lines:
        if align == "right":
            c.drawRightString(x + w, y, ln)
        elif align == "center":
            c.drawCentredString(x + w / 2, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= lead
    return y


def rich(parts, x, y, w, size, lead, indent=0):
    tokens = []
    for text, font, color in parts:
        for word in text.split():
            tokens.append((word, font, color))
    lines, cur, curw = [], [], 0.0
    for word, font, color in tokens:
        ww = sw(word, font, size)
        sp = sw(" ", font, size)
        add = ww if not cur else sp + ww
        limit = w - (indent if not lines else 0)
        if curw + add <= limit or not cur:
            cur.append((word, font, color, sp if cur else 0))
            curw += add
        else:
            lines.append(cur)
            cur, curw = [(word, font, color, 0)], ww
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines):
        cx = x + (indent if i == 0 else 0)
        for word, font, color, sp in line:
            cx += sp
            c.setFont(font, size)
            c.setFillColor(color)
            c.drawString(cx, y, word)
            cx += sw(word, font, size)
        y -= lead
    return y


def tracked(text, x, y, font, size, color, track):
    c.setFont(font, size)
    c.setFillColor(color)
    cx = x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += sw(ch, font, size) + track
    return cx


def hair(y, x1=ML, x2=W - MR, color=LINE, lw=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, y, x2, y)


def section(num, title, y, gap=20):
    y -= gap
    tracked(num, ML, y, "Arial-Bold", 6.6, SAND, 0)
    tracked(title.upper(), ML + 16, y, "Arial-Bold", 7.7, INK, 0.95)
    return y - 12


def bullet(parts, x, y, w, size=8.6, lead=11.4, marker="\u2014"):
    c.setFont("Arial", size)
    c.setFillColor(SAND)
    c.drawString(x, y, marker)
    return rich(parts, x + 11, y, w - 11, size, lead)


# ── masthead ────────────────────────────────────────────────────────────
y = TOP
tracked("REGULATORY SANDBOX BRIEFING \u00b7 OCTOBER 2026", ML, y, "Arial-Bold", 6.4, GREEN, 1.45)
c.setFont("Arial-Bold", 6.0)
c.setFillColor(MUTED)
c.drawRightString(W - MR, y + 10, "LIVE PROTOTYPE")
c.setFont("Arial-Bold", 7.6)
c.setFillColor(GREEN)
c.drawRightString(W - MR, y, "gurucle.github.io/tunga")

y -= 25
c.setFont("Georgia-Bold", 27)
c.setFillColor(INK)
c.drawString(ML, y, "Tunga")

y -= 19
y = para("A crowdfunding platform for fractional property ownership in Namibia, designed to "
         "operate inside the NAMFISA Regulatory Sandbox Crowdfunding Guidelines of 28 November 2025.",
         ML, y, 380, "Georgia-Italic", 9.5, 13.0, MUTED)

y -= 7
hair(y, color=GREEN, lw=1.5)
hair(y - 2.6, color=LINE, lw=0.5)

# ── 1 ───────────────────────────────────────────────────────────────────
y = section("1", "What it is", y, gap=18)
y = para("Tunga lets a Namibian retail investor buy shares in one specific building \u2014 a "
         "separate company per property \u2014 from as little as N$5,000, receive the rent as "
         "dividends, and exit through an internal market or a sale of the asset after a 5\u20137 "
         "year hold. The prototype demonstrates the whole cycle end to end: Annexure 1 "
         "disclosure, subscription under the statutory caps, cooling-off, distribution, "
         "secondary transfer, and a regulator console reading live from the same data.",
         ML, y, CW, "Arial", 8.8, 12.0)

# ── 2 ───────────────────────────────────────────────────────────────────
y = section("2", "What it is not", y)
for lead, body in [
    ("A fund.", "No pooled vehicle, no blind pool, no discretion over investor money. One SPV per building, named on its own page."),
    ("A promise.", "No return is stated as an expectation. Every figure is a scenario with its assumptions printed beside it."),
    ("A custodian.", "Tunga has no payment path. A licensed bank holds a segregated trust account per round."),
    ("Licensed.", "This is a prototype. It is not an offer of securities, and no money moves."),
]:
    y = bullet([(lead + " ", "Arial-Bold", INK), (body, "Arial", INK)], ML, y, CW)
    y -= 3.2

# ── 3 table ─────────────────────────────────────────────────────────────
y = section("3", "Three rules that set the architecture", y)
y -= 3
w1, w2 = 96, 126
w3 = CW - w1 - w2 - 12
c1, c2 = ML, ML + w1
c3 = ML + w1 + w2
tracked("GUIDELINE", c1, y, "Arial-Bold", 6.1, MUTED, 0.7)
tracked("CONSTRAINT", c2, y, "Arial-Bold", 6.1, MUTED, 0.7)
tracked("DESIGN CONSEQUENCE", c3, y, "Arial-Bold", 6.1, MUTED, 0.7)
y -= 5
hair(y, color=INK, lw=0.8)
y -= 10

rows = [
    ("s10(3)", "N$10m per issuer, per 12 months",
     "One SPV per building. No multi-asset fund, no aggregation across properties."),
    ("s28(1)(b), s43", "Operator may not hold investor funds",
     "Licensed bank custodian, segregated trust account per round. The platform never touches cash."),
    ("s28(1)(a),(c)", "No advice, no promised returns",
     "Disclosure of costs and scenarios only. Returns are never presented as expected outcomes."),
]
TFS, TL = 7.8, 10.0
for i, (a, b, d) in enumerate(rows):
    na = len(wrap(a, "Arial-Bold", TFS, w1 - 8))
    nb = len(wrap(b, "Arial", TFS, w2 - 8))
    nd = len(wrap(d, "Arial", TFS, w3))
    n = max(na, nb, nd)
    para(a, c1, y, w1 - 8, "Arial-Bold", TFS, TL, GREEN)
    para(b, c2, y, w2 - 8, "Arial", TFS, TL, INK)
    para(d, c3, y, w3, "Arial", TFS, TL, INK)
    y -= (n - 1) * TL
    if i < len(rows) - 1:
        y -= 7.6
        hair(y)
        y -= 11.6

# ── 4 ───────────────────────────────────────────────────────────────────
y = section("4", "What the prototype actually does", y, gap=18)
for lead, body in [
    ("Investor.",
     "Seven-tab Annexure 1 disclosure including a Costs & fees tab that itemises every charge, "
     "names its recipient, and works the total cost of a N$50,000 subscription. Subscription is "
     "hard-blocked at the s11 annual limit (for retail, the lesser of 10% of net worth or "
     "N$100,000), the offering minimum, and the remaining target. Four s35 risk acknowledgements "
     "must be accepted. 48-hour s22 cooling-off with a live countdown and a working cancellation."),
    ("Issuer.",
     "Round stepper carrying every statutory step and its deadline; an Annexure 1 completeness "
     "checklist that gates publication; quarterly update composer that publishes straight to the "
     "offering page; obligations calendar including audited financials within 90 days."),
    ("Regulator.",
     "90-day s37 review clock per issuer; deadline board computed from live timestamps; investor "
     "concentration monitor against each category limit; filings log with overdue items flagged; "
     "s47 quarterly return export plus a CSV investor register."),
    ("Rulebook.",
     "Fourteen guideline sections mapped to the exact line of software where each is enforced, so "
     "a reviewer can test the claim rather than accept it."),
]:
    y = bullet([(lead + " ", "Arial-Bold", INK), (body, "Arial", INK)], ML, y, CW)
    y -= 3.2

# ── 5 fee callout ───────────────────────────────────────────────────────
y = section("5", "What it costs the investor", y, gap=18)
y -= 2
box_top = y + 8.5
inner = "On a N$50,000 subscription in the N$9.5m Khomasdal round, total fees over the term come to "
body_parts = [
    ("N$16,781 \u2014 33.6% of the money invested. ", "Arial-Bold", INK),
    ("N$4,368 one-off, N$10,307 of management, N$2,105 on disposal, plus a 20% promote on "
     "profit above an 8% preferred return. Every line is itemised on the offering page, with the "
     "recipient named.", "Arial", INK),
]
ty = y
ty = rich([(inner, "Arial", INK)] + body_parts, ML + 10, ty, CW - 20, 8.5, 11.4)
box_bot = ty + 3.5
c.setFillColor(SANDS)
c.rect(ML, box_bot, CW, box_top - box_bot, stroke=0, fill=1)
# redraw text over the fill
rich([(inner, "Arial", INK)] + body_parts, ML + 10, y, CW - 20, 8.5, 11.4)
y = box_bot - 2

# ── 6 / 7 two columns ───────────────────────────────────────────────────
y = section("6", "Gaps before a single real dollar", y, gap=18)
colw = CW * 0.46
gx = ML + colw + 24
tracked("7", gx, y + 12, "Arial-Bold", 6.6, SAND, 0)
tracked("IN PARALLEL, AND GATING EVERYTHING", gx + 16, y + 12, "Arial-Bold", 7.7, INK, 0.95)

left_items = [
    "Server-side storage, authentication, role permissions",
    "KYC / AML with sanctions and PEP screening",
    "Custodian bank API and daily reconciliation",
    "Authoritative share registry and cap table",
    "Subscription agreements and e-signature",
    "Secondary trading facility (s30)",
    "Tamper-evident audit trail, 7-year retention",
    "Hosting, backups, monitoring, penetration test",
]
ly = y
for item in left_items:
    c.setFont("Arial", 8.1)
    c.setFillColor(SAND)
    c.drawString(ML, ly, "\u00b7")
    c.setFillColor(INK)
    c.drawString(ML + 7, ly, item)
    ly -= 10.4

right_items = [
    "Sandbox admission",
    "Custodian agreement with a Bank of Namibia-licensed bank",
    "Fit-and-proper packs for directors and key persons",
    "Platform rules and a written s7(f) conflict-of-interest policy",
]
box_w = W - MR - gx
rlines = [len(wrap(it, "Arial", 7.9, box_w - 24)) for it in right_items]
box_h = sum(n * 10.0 for n in rlines) + 14
c.setFillColor(GREENS)
c.rect(gx, y - box_h + 3, box_w, box_h, stroke=0, fill=1)
ry = y - 5
for it, n in zip(right_items, rlines):
    c.setFont("Arial", 7.9)
    c.setFillColor(GREEN)
    c.drawString(gx + 8, ry, "\u2014")
    ry = rich([(it, "Arial", INK)], gx + 18, ry, box_w - 24, 7.9, 10.0) - 1.4

# ── footer ──────────────────────────────────────────────────────────────
content_end = min(ly, ry)
fy = BOT + 12
assert content_end > fy + 18, f"content collides with pinned footer: {content_end:.1f} vs {fy + 18:.1f}"
hair(fy + 9)
c.setFont("Arial", 6.1)
c.setFillColor(MUTED)
c.drawString(ML, fy,
             "Prototype only \u00b7 illustrative data \u00b7 capital at risk \u00b7 not an offer of "
             "securities \u00b7 not licensed by NAMFISA \u00b7 nothing here is investment advice")
c.setFont("Arial-Bold", 6.1)
c.setFillColor(GREEN)
c.drawRightString(W - MR, fy, "gurucle.github.io/tunga")

print(f"footer baseline = {fy:.1f}   bottom margin = {BOT}   slack = {fy - BOT:.1f}pt")
assert fy > BOT, f"OVERFLOW by {BOT - fy:.1f}pt"

c.showPage()
c.save()
print("wrote", OUT)
