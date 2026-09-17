"""
Generate 400x400 PNG illustrations for each Socioscope service,
suitable for embedding in Google Forms.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = os.path.dirname(__file__)
SIZE = 400

# ── palette ──────────────────────────────────────────────────────────────
BG       = (255, 251, 240)   # cream
GREEN    = (76,  160, 73)    # green-leaf
GREEN_D  = (39,  66,  29)    # green-forest
GREEN_L  = (229, 244, 229)   # light green
EARTH_15 = (229, 217, 193)   # border-soft
EARTH_30 = (200, 182, 138)   # border-strong
EARTH_50 = (139, 111, 71)    # text-caption
EARTH_90 = (44,  36,  22)    # text-primary
GOLD     = (212, 155, 58)    # saffron
GOLD_L   = (247, 233, 196)   # saffron-pale
CLAY     = (184, 85,  42)    # clay/alert
WHITE    = (255, 255, 255)

def new_canvas():
    img = Image.new("RGBA", (SIZE, SIZE), (*BG, 255))
    d   = ImageDraw.Draw(img)
    return img, d

def rounded_rect(d, x0, y0, x1, y1, r, fill=None, outline=None, width=2):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r,
                        fill=fill, outline=outline, width=width)

def circle(d, cx, cy, r, fill=None, outline=None, width=2):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill, outline=outline, width=width)

def line(d, pts, fill, width=2):
    d.line(pts, fill=fill, width=width)

def text_center(d, x, y, txt, fill, size=18, bold=False):
    try:
        fnt = ImageFont.truetype("arial.ttf", size)
    except:
        fnt = ImageFont.load_default()
    bbox = d.textbbox((0,0), txt, font=fnt)
    w = bbox[2] - bbox[0]
    d.text((x - w//2, y - (bbox[3]-bbox[1])//2), txt, fill=fill, font=fnt)

def label_block(d, x, y, title, subtitle, title_size=22):
    """Draw title + subtitle centred at (x,y)."""
    try:
        f_bold   = ImageFont.truetype("arialbd.ttf", title_size)
        f_normal = ImageFont.truetype("arial.ttf", 15)
    except:
        f_bold   = ImageFont.load_default()
        f_normal = f_bold
    bb = d.textbbox((0,0), title, font=f_bold)
    tw = bb[2] - bb[0]
    d.text((x - tw//2, y), title, fill=EARTH_90, font=f_bold)
    y2 = y + (bb[3]-bb[1]) + 6
    lines = subtitle.split("\n")
    for ln in lines:
        bb2 = d.textbbox((0,0), ln, font=f_normal)
        d.text((x - (bb2[2]-bb2[0])//2, y2), ln, fill=EARTH_50, font=f_normal)
        y2 += (bb2[3]-bb2[1]) + 4

def save(img, name):
    path = os.path.join(OUT, name + ".png")
    img.convert("RGB").save(path)
    print(f"  OK  {name}.png")

# ═══════════════════════════════════════════════════════════════════════
# 1. SWOT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# 4 quadrants
pads = [(30,30,196,196),(204,30,370,196),(30,204,196,370),(204,204,370,370)]
fills   = [GREEN_L, GOLD_L, GOLD_L, GREEN_L]
outlines= [GREEN,   GOLD,   GOLD,   GREEN  ]
labels  = ["S","W","O","T"]
colors  = [GREEN_D, EARTH_50, EARTH_50, GREEN_D]
descs   = ["Strengths","Weaknesses","Opportunities","Threats"]
for (x0,y0,x1,y1), f, o, lbl, c, desc in zip(pads,fills,outlines,labels,colors,descs):
    rounded_rect(d, x0,y0,x1,y1, 10, fill=f, outline=o, width=3)
    cx, cy = (x0+x1)//2, (y0+y1)//2
    try:
        fb = ImageFont.truetype("arialbd.ttf", 52)
    except:
        fb = ImageFont.load_default()
    bb = d.textbbox((0,0), lbl, font=fb)
    d.text((cx-(bb[2]-bb[0])//2, cy-40), lbl, fill=c, font=fb)
    try:
        fs = ImageFont.truetype("arial.ttf", 14)
    except:
        fs = ImageFont.load_default()
    bb2 = d.textbbox((0,0), desc, font=fs)
    d.text((cx-(bb2[2]-bb2[0])//2, cy+12), desc, fill=c, font=fs)
save(img, "swot-analysis")

# ═══════════════════════════════════════════════════════════════════════
# 2. TRANSACTION GRID
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
cx, cy = 200, 200
# Hub
circle(d, cx, cy, 45, fill=GREEN_L, outline=GREEN, width=3)
try: fb = ImageFont.truetype("arialbd.ttf", 14)
except: fb = ImageFont.load_default()
bb = d.textbbox((0,0),"Your\nInitiative", font=fb)
d.text((cx-28, cy-14),"Your", fill=GREEN_D, font=fb)
d.text((cx-30, cy+2),"Initiative", fill=GREEN_D, font=fb)
# 5 outer nodes with labels
nodes = [
    (200, 60,  "Partners"),
    (330, 120, "Funders"),
    (330, 280, "Customers"),
    (200, 340, "Suppliers"),
    (70,  200, "Community"),
]
for nx, ny, lbl in nodes:
    circle(d, nx, ny, 32, fill=WHITE, outline=EARTH_30, width=2)
    # dashed line to hub
    dx, dy = nx-cx, ny-cy
    dist = math.hypot(dx,dy)
    ux, uy = dx/dist, dy/dist
    x0, y0 = cx+ux*46, cy+uy*46
    x1, y1 = nx-ux*33, ny-uy*33
    # draw dashes
    steps = int(dist/12)
    for i in range(steps):
        t0, t1 = i/(steps), (i+0.45)/(steps)
        px0 = x0 + (x1-x0)*t0; py0 = y0 + (y1-y0)*t0
        px1 = x0 + (x1-x0)*t1; py1 = y0 + (y1-y0)*t1
        col = GREEN if i%2==0 else GOLD
        d.line([(px0,py0),(px1,py1)], fill=col, width=2)
    try: fs = ImageFont.truetype("arial.ttf", 12)
    except: fs = ImageFont.load_default()
    bb = d.textbbox((0,0), lbl, font=fs)
    d.text((nx-(bb[2]-bb[0])//2, ny-(bb[3]-bb[1])//2), lbl, fill=EARTH_90, font=fs)
save(img, "transaction-grid")

# ═══════════════════════════════════════════════════════════════════════
# 3. STAKEHOLDER MAP
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
cx, cy = 200, 200
# rings
for r, c, lbl in [(165, EARTH_15,"Peripheral"), (110, EARTH_30,"Secondary"), (60, GREEN_L,"Core")]:
    circle(d, cx, cy, r, fill=None, outline=c, width=2)
# hub
circle(d, cx, cy, 22, fill=GREEN, outline=GREEN_D, width=2)
text_center(d, cx, cy, "You", WHITE, 14)
# dots at various positions
import random; random.seed(42)
dot_configs = [
    (60,  [(cx,cy-80),(cx+55,cy-55),(cx+80,cy)], GREEN,  14),
    (120, [(cx+90,cy-80),(cx+130,cy+40),(cx-100,cy-90),(cx-110,cy+60),(cx+30,cy+130)], EARTH_50, 11),
    (160, [(cx-150,cy-20),(cx+140,cy-100),(cx+60,cy+150),(cx-80,cy+155)], EARTH_30, 9),
]
for ring_r, positions, col, dot_r in dot_configs:
    for px, py in positions:
        circle(d, px, py, dot_r, fill=col, outline=None)
        d.line([(px,py),(cx,cy)], fill=(*col,80), width=1)
save(img, "stakeholder-map")

# ═══════════════════════════════════════════════════════════════════════
# 4. BARRIERS ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Wall of bricks
brick_w, brick_h = 88, 40
rows = 4
for row in range(rows):
    offset = (row%2) * 44
    y0 = 80 + row*44
    for col in range(-1, 6):
        bx = col*brick_w + offset - 20
        if bx > 380: continue
        col_fill = EARTH_15 if row < 2 else EARTH_30
        rounded_rect(d, bx+2, y0+2, bx+brick_w-2, y0+brick_h-2, 4,
                     fill=col_fill, outline=EARTH_50, width=2)
# Gap in the wall (middle column row 1-2)
rounded_rect(d, 155,82,243,210, 0, fill=BG, outline=None)
# Arrow through gap
d.polygon([(190,110),(210,110),(220,180),(180,180)], fill=GREEN)
d.polygon([(162,155),(238,155),(200,230)], fill=GREEN)
# magnifier overlay
circle(d, 200, 300, 60, fill=None, outline=GREEN_D, width=4)
line(d, [(245,345),(285,385)], GREEN_D, 8)
# X inside
line(d, [(175,275),(225,325)], CLAY, 5)
line(d, [(225,275),(175,325)], CLAY, 5)
label_block(d, 200, 300, "", "")
save(img, "barriers-analysis")

# ═══════════════════════════════════════════════════════════════════════
# 5. WHAT WORKED ELSEWHERE MEMO
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Document
rounded_rect(d, 60,30,340,370, 12, fill=WHITE, outline=EARTH_15, width=2)
# Folded corner
d.polygon([(280,30),(340,90),(280,90)], fill=EARTH_15)
d.line([(280,30),(280,90),(340,90)], fill=EARTH_30, width=2)
# Title
try: fb = ImageFont.truetype("arialbd.ttf", 20)
except: fb = ImageFont.load_default()
d.text((85,55), "What Worked Elsewhere", fill=EARTH_90, font=fb)
d.line([(85,82),(310,82)], fill=EARTH_30, width=1)
# 3 strategy items with checkmarks
items = [
    "Strategy A — Local market access",
    "Strategy B — Community co-design",
    "Strategy C — Tiered pricing model",
]
try: fr = ImageFont.truetype("arial.ttf", 14)
except: fr = ImageFont.load_default()
for i, item in enumerate(items):
    y = 110 + i*80
    # check circle
    circle(d, 100, y+18, 18, fill=GREEN_L, outline=GREEN, width=2)
    d.line([(91,y+18),(97,y+24),(113,y+12)], fill=GREEN, width=3)
    # text lines
    d.text((130, y+10), item, fill=EARTH_90, font=fr)
    d.line([(130,y+34),(300,y+34)], fill=EARTH_15, width=1)
    d.line([(130,y+46),(280,y+46)], fill=EARTH_15, width=1)
# Star badge
star_cx, star_cy = 300, 340
circle(d, star_cx, star_cy, 28, fill=GOLD, outline=None)
# 5-point star
pts = []
for i in range(5):
    ang = math.radians(-90 + i*72)
    pts.append((star_cx + 18*math.cos(ang), star_cy + 18*math.sin(ang)))
    ang2 = math.radians(-90 + i*72 + 36)
    pts.append((star_cx + 9*math.cos(ang2), star_cy + 9*math.sin(ang2)))
d.polygon(pts, fill=WHITE)
save(img, "what-worked-memo")

# ═══════════════════════════════════════════════════════════════════════
# 6. POSITIONING BENCHMARK
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Axes
line(d, [(50,350),(50,30)], EARTH_30, 2)
line(d, [(50,350),(370,350)], EARTH_30, 2)
# Grid
for x in [130,210,290]:
    line(d, [(x,30),(x,350)], EARTH_15, 1)
for y in [110,190,270]:
    line(d, [(50,y),(370,y)], EARTH_15, 1)
# 600+ dots
random.seed(7)
for _ in range(60):
    rx = random.randint(55,365)
    ry = random.randint(35,345)
    circle(d, rx, ry, 4, fill=EARTH_30)
# Your dot — highlighted
circle(d, 230, 150, 16, fill=GREEN)
circle(d, 230, 150, 24, fill=None, outline=GREEN, width=2)
circle(d, 230, 150, 5, fill=WHITE)
# Legend
try: fs = ImageFont.truetype("arial.ttf", 12)
except: fs = ImageFont.load_default()
circle(d, 62, 38, 5, fill=EARTH_30)
d.text((72, 31), "600+ initiatives", fill=EARTH_50, font=fs)
circle(d, 62, 55, 8, fill=GREEN)
d.text((75, 48), "Your position", fill=GREEN_D, font=fs)
# Axis labels
try: fi = ImageFont.truetype("arial.ttf", 13)
except: fi = ImageFont.load_default()
d.text((55, 355), "Size / scale  →", fill=EARTH_50, font=fi)
save(img, "positioning-benchmark")

# ═══════════════════════════════════════════════════════════════════════
# 7. TRANSITION TIMELINE
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Spine
y_spine = 210
line(d, [(40, y_spine),(360, y_spine)], EARTH_30, 4)
d.polygon([(360,y_spine),(345,y_spine-8),(345,y_spine+8)], fill=EARTH_30)
# Milestones
milestones = [
    (90,  "2018", "Founded",    EARTH_50, True),
    (170, "2020", "First grant", GREEN,   True),
    (250, "2022", "Scale-up",   GREEN_D, True),
    (330, "Now",  "Strategic\npivot", GREEN, False),
]
for mx, year, label, col, above in milestones:
    # node
    circle(d, mx, y_spine, 14, fill=col, outline=WHITE, width=2)
    # connector
    if above:
        line(d, [(mx, y_spine-14),(mx, y_spine-70)], col, 2)
        box_y = y_spine - 120
    else:
        line(d, [(mx, y_spine+14),(mx, y_spine+70)], col, 2)
        box_y = y_spine + 80
    # label box
    rounded_rect(d, mx-45, box_y, mx+45, box_y+44, 6,
                 fill=GREEN_L if col==GREEN else GOLD_L,
                 outline=col, width=2)
    try: fb = ImageFont.truetype("arialbd.ttf", 12)
    except: fb = ImageFont.load_default()
    try: fs = ImageFont.truetype("arial.ttf", 11)
    except: fs = ImageFont.load_default()
    yb = d.textbbox((0,0), year, font=fb)
    d.text((mx-(yb[2]-yb[0])//2, box_y+4), year, fill=col, font=fb)
    for li, ln in enumerate(label.split("\n")):
        lb = d.textbbox((0,0), ln, font=fs)
        d.text((mx-(lb[2]-lb[0])//2, box_y+20+li*13), ln, fill=EARTH_90, font=fs)
save(img, "transition-timeline")

# ═══════════════════════════════════════════════════════════════════════
# 8. SECTOR REPORT
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Stacked pages
for offset in [(20,20),(10,10),(0,0)]:
    ox, oy = offset
    rounded_rect(d, 60+ox, 30+oy, 320+ox, 350+oy, 8,
                 fill=WHITE, outline=EARTH_15 if ox else EARTH_30, width=2)
# Folded corner on top page
d.polygon([(270,30),(320,80),(270,80)], fill=EARTH_15)
d.line([(270,30),(270,80),(320,80)], fill=EARTH_30, width=2)
# Title
try: fb = ImageFont.truetype("arialbd.ttf", 18)
except: fb = ImageFont.load_default()
d.text((80, 50), "Thematic Sector Report", fill=EARTH_90, font=fb)
d.line([(80,76),(260,76)], fill=EARTH_30, width=1)
# Bar chart
bars = [(100,180,80),(140,130,70),(180,100,60),(220,150,80),(260,120,70)]
chart_base = 290
for bx, bh, bw in bars:
    c = GREEN if bh <= 110 else GREEN_D if bh <= 130 else GREEN
    rounded_rect(d, bx, chart_base-bh, bx+bw-8, chart_base, 3, fill=c)
d.line([(85,chart_base),(305,chart_base)], fill=EARTH_50, width=1)
# "80" badge
circle(d, 285, 110, 36, fill=GREEN_D)
try: fb2 = ImageFont.truetype("arialbd.ttf", 24)
except: fb2 = ImageFont.load_default()
bb = d.textbbox((0,0), "80", font=fb2)
d.text((285-(bb[2]-bb[0])//2, 100), "80", fill=WHITE, font=fb2)
try: fs2 = ImageFont.truetype("arial.ttf", 10)
except: fs2 = ImageFont.load_default()
d.text((268, 123), "initiatives", fill=WHITE, font=fs2)
save(img, "sector-report")

# ═══════════════════════════════════════════════════════════════════════
# 9. FUNDING OPPORTUNITIES
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Coin stacks
for stack_x, n_coins, col in [(120, 3, GOLD),(200,4,GOLD),(280,2,GOLD)]:
    for i in range(n_coins):
        cy = 320 - i*22
        d.ellipse([stack_x-40, cy-8, stack_x+40, cy+8], fill=GOLD_L, outline=GOLD, width=2)
        if i == n_coins-1:
            try: fs = ImageFont.truetype("arial.ttf", 11)
            except: fs = ImageFont.load_default()
            d.text((stack_x-6, cy-7), "€", fill=GOLD, font=fs)
# Magnifying glass
mx, my, mr = 200, 155, 80
circle(d, mx, my, mr, fill=(*BG,220), outline=GREEN_D, width=5)
# Crosshair
d.line([(mx, my-mr+10),(mx, my+mr-10)], fill=(*EARTH_30,180), width=1)
d.line([(mx-mr+10, my),(mx+mr-10, my)], fill=(*EARTH_30,180), width=1)
# Euro inside magnifier
try: fb = ImageFont.truetype("arialbd.ttf", 60)
except: fb = ImageFont.load_default()
bb = d.textbbox((0,0),"€", font=fb)
d.text((mx-(bb[2]-bb[0])//2, my-36), "€", fill=GOLD, font=fb)
# Handle
d.line([(mx+mr*0.7,my+mr*0.7),(mx+mr*1.25,my+mr*1.25)], fill=GREEN_D, width=9)
# Labels
try: fs = ImageFont.truetype("arial.ttf", 12)
except: fs = ImageFont.load_default()
for lbl, x in [("EU funds", 90),("Foundations",190),("Grants",280)]:
    bb2 = d.textbbox((0,0), lbl, font=fs)
    d.text((x-(bb2[2]-bb2[0])//2, 335), lbl, fill=EARTH_50, font=fs)
save(img, "funding-opportunities")

# ═══════════════════════════════════════════════════════════════════════
# 10. NARRATIVE PORTRAIT
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Document sheet
rounded_rect(d, 40,20,360,375, 10, fill=WHITE, outline=EARTH_15, width=2)
# Folded corner
d.polygon([(300,20),(360,80),(300,80)], fill=EARTH_15)
d.line([(300,20),(300,80),(360,80)], fill=EARTH_30, width=2)
# Portrait photo box
rounded_rect(d, 55,38,160,128, 6, fill=GREEN_L, outline=GREEN, width=2)
# Person silhouette
circle(d, 108, 65, 16, fill=GREEN, outline=None)
d.ellipse([70,85,146,130], fill=GREEN, outline=None)
# Title + info lines
try: fb = ImageFont.truetype("arialbd.ttf", 18)
except: fb = ImageFont.load_default()
try: fr = ImageFont.truetype("arial.ttf", 13)
except: fr = ImageFont.load_default()
d.text((175,45), "Your Story,", fill=EARTH_90, font=fb)
d.text((175,68), "Told Well.", fill=GREEN_D, font=fb)
d.line([(175,96),(340,96)], fill=EARTH_15, width=1)
for i,t in enumerate(["Organisation","Location","Year founded","Impact"]):
    d.text((175, 105+i*16), f"— {t}", fill=EARTH_50, font=fr)
# Body text lines
for i in range(5):
    w = 270 if i < 4 else 180
    d.line([(55,155+i*18),(55+w,155+i*18)], fill=EARTH_15, width=2)
# Gold seal
sx, sy = 300, 330
circle(d, sx, sy, 38, fill=GOLD)
circle(d, sx, sy, 30, fill=GOLD_L)
pts = []
for i in range(5):
    a = math.radians(-90 + i*72)
    pts.append((sx + 22*math.cos(a), sy + 22*math.sin(a)))
    a2 = math.radians(-90 + i*72 + 36)
    pts.append((sx + 11*math.cos(a2), sy + 11*math.sin(a2)))
d.polygon(pts, fill=GOLD)
save(img, "narrative-portrait")

# ═══════════════════════════════════════════════════════════════════════
# 11. MENTION IN PUBLICATIONS
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Open book
# Left page
d.polygon([(40,60),(200,50),(200,360),(40,350)], fill=WHITE, outline=EARTH_15)
# Right page
d.polygon([(200,50),(360,60),(360,350),(200,360)], fill=WHITE, outline=EARTH_15)
# Spine
d.line([(200,50),(200,360)], fill=EARTH_30, width=3)
# Left page lines
try: fr = ImageFont.truetype("arial.ttf", 11)
except: fr = ImageFont.load_default()
for i in range(12):
    w = 130 if i%3!=2 else 90
    d.line([(60,90+i*20),(60+w,90+i*20)], fill=EARTH_15, width=2)
# Right page — highlighted mention
highlight_y = 180
rounded_rect(d, 210, highlight_y-5, 355, highlight_y+50, 4,
             fill=GREEN_L, outline=GREEN, width=2)
for i in range(12):
    w = 130 if i%3!=2 else 90
    col = GREEN if (highlight_y//20 - 3 <= i <= highlight_y//20) else EARTH_15
    width = 2 if col == EARTH_15 else 3
    d.line([(215,90+i*20),(215+w,90+i*20)], fill=col, width=width)
# Tag / bookmark on highlighted section
d.polygon([(342, highlight_y-5),(356, highlight_y-5),
           (356, highlight_y+30),(349, highlight_y+24),(342, highlight_y+30)],
          fill=GREEN)
# "Mentioned" chip
try: fs = ImageFont.truetype("arialbd.ttf", 11)
except: fs = ImageFont.load_default()
rounded_rect(d, 218, highlight_y, 290, highlight_y+20, 10, fill=GREEN, outline=None)
bb = d.textbbox((0,0),"✦ Mentioned", font=fs)
d.text((218+(72-(bb[2]-bb[0]))//2, highlight_y+4), "✦ Mentioned", fill=WHITE, font=fs)
save(img, "mention-publications")

# ═══════════════════════════════════════════════════════════════════════
# 12. CERTIFICATE / LABEL
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Outer border
rounded_rect(d, 25,25,375,375, 14, fill=WHITE, outline=GOLD, width=4)
# Inner decorative border (dashed effect via short lines)
for t in range(0,100):
    frac = t/100
    # top
    x = 45 + frac*310; y_top = 45
    if t%5<3: d.line([(x,y_top),(x+3,y_top)], fill=GOLD, width=1)
    # bottom
    y_bot = 355
    if t%5<3: d.line([(x,y_bot),(x+3,y_bot)], fill=GOLD, width=1)
    # left
    x_l = 45; y = 45 + frac*310
    if t%5<3: d.line([(x_l,y),(x_l,y+3)], fill=GOLD, width=1)
    x_r = 355
    if t%5<3: d.line([(x_r,y),(x_r,y+3)], fill=GOLD, width=1)
# Corner ornaments
for cx2, cy2 in [(50,50),(350,50),(50,350),(350,350)]:
    circle(d, cx2, cy2, 6, fill=GOLD)
# Title
try: fb = ImageFont.truetype("arialbd.ttf", 18)
except: fb = ImageFont.load_default()
try: fr = ImageFont.truetype("arial.ttf", 13)
except: fr = ImageFont.load_default()
t1 = "Food Socioscope"
bb = d.textbbox((0,0), t1, font=fb)
d.text((200-(bb[2]-bb[0])//2, 65), t1, fill=EARTH_90, font=fb)
t2 = "Contributor"
bb2 = d.textbbox((0,0), t2, font=fb)
d.text((200-(bb2[2]-bb2[0])//2, 90), t2, fill=GREEN_D, font=fb)
d.line([(80,118),(320,118)], fill=GOLD, width=1)
# Medal
mx, my = 200, 220
circle(d, mx, my, 55, fill=GOLD)
circle(d, mx, my, 45, fill=GOLD_L)
pts = []
for i in range(6):
    a = math.radians(-90 + i*60)
    pts.append((mx + 38*math.cos(a), my + 38*math.sin(a)))
    a2 = math.radians(-90 + i*60 + 30)
    pts.append((mx + 22*math.cos(a2), my + 22*math.sin(a2)))
d.polygon(pts, fill=GOLD)
# checkmark in center
d.line([(mx-18,my),(mx-5,my+15),(mx+22,my-15)], fill=WHITE, width=5)
# Ribbon tails
d.polygon([(175,275),(200,260),(225,275),(220,310),(200,298),(180,310)], fill=GREEN)
# Name line
d.line([(80,335),(320,335)], fill=EARTH_30, width=1)
try: fi = ImageFont.truetype("arial.ttf", 12)
except: fi = ImageFont.load_default()
t3 = "Awarded to: ________________________"
bb3 = d.textbbox((0,0), t3, font=fi)
d.text((200-(bb3[2]-bb3[0])//2, 345), t3, fill=EARTH_50, font=fi)
save(img, "certificate-label")

# ═══════════════════════════════════════════════════════════════════════
# 13. PEER LEARNING SESSIONS
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
cx, cy = 200, 185
r_orbit = 120
# 6 avatars in a circle
avatar_angles = [i*60 for i in range(6)]
avatar_cols = [GREEN, GREEN, GREEN_D, GREEN_D, GREEN, GREEN_D]
for ang, col in zip(avatar_angles, avatar_cols):
    rad = math.radians(ang-90)
    ax = cx + r_orbit*math.cos(rad)
    ay = cy + r_orbit*math.sin(rad)
    # Connection line
    d.line([(ax,ay),(cx,cy)], fill=(*EARTH_15,180), width=2)
    # Avatar circle
    circle(d, ax, ay, 28, fill=GREEN_L if col==GREEN else GOLD_L, outline=col, width=2)
    # Head
    circle(d, ax, ay-9, 10, fill=col, outline=None)
    # Body arc
    d.arc([ax-14,ay+1,ax+14,ay+25], start=0, end=180, fill=col, width=2)
# Central speech bubble
rounded_rect(d, cx-52, cy-35, cx+52, cy+35, 18, fill=GREEN_D, outline=None)
d.polygon([(cx-10,cy+35),(cx+10,cy+35),(cx,cy+52)], fill=GREEN_D)
try: fb = ImageFont.truetype("arialbd.ttf", 13)
except: fb = ImageFont.load_default()
d.text((cx-40, cy-28), "Peer", fill=WHITE, font=fb)
d.text((cx-43, cy-10), "Learning", fill=WHITE, font=fb)
d.text((cx-39, cy+8), "Session", fill=WHITE, font=fb)
# Bottom label
try: fr = ImageFont.truetype("arial.ttf", 13)
except: fr = ImageFont.load_default()
t = "5–6 initiatives per session"
bb = d.textbbox((0,0), t, font=fr)
d.text((200-(bb[2]-bb[0])//2, 340), t, fill=EARTH_50, font=fr)
save(img, "peer-learning")

# ═══════════════════════════════════════════════════════════════════════
# 14. WEBINAR HOSTING
# ═══════════════════════════════════════════════════════════════════════
img, d = new_canvas()
# Monitor
rounded_rect(d, 30,30,370,280, 10, fill=GREEN_D, outline=EARTH_90, width=3)
rounded_rect(d, 44,44,356,266, 6, fill=(20,50,18), outline=None)
# Main presenter tile
rounded_rect(d, 52,52,260,262, 4, fill=(40,80,35), outline=None)
# Presenter silhouette
circle(d, 156, 120, 28, fill=GREEN, outline=None)
d.ellipse([100,155,212,265], fill=GREEN, outline=None)
# LIVE badge
rounded_rect(d, 60,60,118,80, 4, fill=CLAY, outline=None)
circle(d, 70,70,5, fill=WHITE)
try: fs = ImageFont.truetype("arialbd.ttf", 11)
except: fs = ImageFont.load_default()
d.text((80,63), "LIVE", fill=WHITE, font=fs)
# Participant tiles (right column)
for i in range(3):
    ty = 58 + i*70
    rounded_rect(d, 268,ty,350,ty+60, 4, fill=(40,80,35), outline=(60,110,50), width=1)
    circle(d, 309, ty+20, 12, fill=GREEN_D, outline=None)
    d.arc([291,ty+35,327,ty+60], start=0, end=180, fill=GREEN_D, width=2)
# Screen stand
rounded_rect(d, 165,280,235,300, 4, fill=EARTH_30, outline=None)
rounded_rect(d, 120,300,280,315, 6, fill=EARTH_50, outline=None)
# Recording / play button
circle(d, 200, 355, 32, fill=GREEN)
d.polygon([(190,340),(190,370),(220,355)], fill=WHITE)
try: fr = ImageFont.truetype("arial.ttf", 12)
except: fr = ImageFont.load_default()
d.text((100, 358), "Recorded & published", fill=EARTH_50, font=fr)
save(img, "webinar-hosting")

print("\nAll 14 PNGs generated successfully!")
