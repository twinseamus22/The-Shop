from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random, math

ROOT=Path('/mnt/data/bot_shop_pixel/assets')
(ROOT/'bots').mkdir(parents=True, exist_ok=True)
(ROOT/'items').mkdir(parents=True, exist_ok=True)
(ROOT/'decor').mkdir(parents=True, exist_ok=True)

# ---------- helpers ----------
def pxrect(d, xy, fill, outline=None, w=1):
    d.rectangle(xy, fill=fill, outline=outline, width=w)

def save_scaled(img, path, scale=1):
    if scale!=1:
        img=img.resize((img.width*scale,img.height*scale), Image.Resampling.NEAREST)
    img.save(path)

def noise_rect(d, box, base, amount=10, seed=0):
    random.seed(seed)
    x0,y0,x1,y1=box
    for _ in range(120):
        x=random.randint(x0,x1-1); y=random.randint(y0,y1-1)
        delta=random.randint(-amount,amount)
        c=tuple(max(0,min(255,v+delta)) for v in base)
        d.point((x,y), fill=c)

# ---------- shop background ----------
W,H=960,720
img=Image.new('RGB',(W,H),'#0a1320')
d=ImageDraw.Draw(img)

# Outer frame
pxrect(d,(8,8,952,706),'#2a2019','#0d0a08',3)
pxrect(d,(14,14,946,700),'#5c3a24','#28190f',2)

# floor
floor=(167,111,59)
pxrect(d,(20,120,940,680),floor)
# floor boards
for y in range(120,681,24):
    d.line((20,y,940,y), fill='#8d572f', width=2)
for row,y in enumerate(range(120,681,24)):
    offset=0 if row%2==0 else 48
    for x in range(20-offset,941,96):
        d.line((x,y,x,y+24), fill='#955e34', width=1)
# highlights/noise
random.seed(2)
for _ in range(500):
    x=random.randint(22,938); y=random.randint(122,678)
    d.point((x,y), fill=random.choice(['#b77b45','#9b6337','#c1844a']))

# top wall
pxrect(d,(20,20,940,120),'#52321f','#26170f',2)
for x in range(20,941,18): d.line((x,20,x,120), fill='#3f281a')
for y in range(20,121,18): d.line((20,y,940,y), fill='#614029')
# baseboard
pxrect(d,(20,112,940,122),'#362116','#1e120b',1)

# rugs
def rug(box, base, border, inner):
    x0,y0,x1,y1=box
    pxrect(d,box,border,'#3a1e17',2)
    pxrect(d,(x0+8,y0+8,x1-8,y1-8),base)
    pxrect(d,(x0+18,y0+18,x1-18,y1-18),inner)
    # pixel motifs
    for x in range(x0+24,x1-20,18):
        for y in range(y0+24,y1-20,18):
            if (x+y)//18%2==0:
                pxrect(d,(x,y,x+5,y+5),border)

rug((220,280,520,520),'#7a2d25','#4a221d','#9a3b2e')
rug((560,280,790,520),'#2f5537','#1f3b28','#3d6a45')
rug((660,548,905,675),'#263d61','#17283f','#38527d')
rug((40,560,220,675),'#7f3025','#4c211a','#9b3b2e')

# shelf drawer
shelf_labels=[]
def shelf(x,y,w,h,label):
    # shadow
    pxrect(d,(x+6,y+6,x+w+6,y+h+6),'#2a1a11')
    pxrect(d,(x,y,x+w,y+h),'#5b351f','#2a180f',3)
    pxrect(d,(x+6,y+8,x+w-6,y+h-10),'#7d4a29','#3d2416',2)
    # shelves
    for sy in (y+34, y+62):
        if sy<y+h-8: pxrect(d,(x+5,sy,x+w-5,sy+5),'#3f2617')
    # sign backing
    sw=max(72,min(w-18, len(label)*10+24))
    sx=x+(w-sw)//2
    pxrect(d,(sx,y-22,sx+sw,y+2),'#d2a05f','#54341f',3)
    shelf_labels.append((label,sx+sw//2,y-10))

shelf(170,58,160,82,'ODDITIES')
shelf(380,58,160,82,'HOUSEWARES')
shelf(590,58,160,82,'ART & PRINTS')
shelf(795,58,125,82,'MISC')
shelf(320,565,165,92,'VINTAGE')
shelf(535,565,190,92,'CURIOS')

# fill shelves with tiny pixels / objects
shelf_icons=[(195,85,'#dd8b34'),(225,84,'#6957a8'),(255,85,'#c4454f'),(285,84,'#d9d1bc'),
             (405,85,'#77706a'),(435,85,'#b34f76'),(465,84,'#e3d7a4'),(495,86,'#c88941'),
             (612,82,'#d66c44'),(646,81,'#e0b05f'),(680,84,'#6b9fc7'),(714,84,'#c35456'),
             (815,84,'#bf4b87'),(845,82,'#4b85bd'),(876,84,'#d1a33f'),
             (345,596,'#d2b463'),(377,595,'#7b4b2a'),(409,595,'#5b99af'),(445,596,'#c65a4b'),
             (565,596,'#b0c0c4'),(600,594,'#5b88a4'),(635,595,'#9f5c84'),(671,596,'#c77746')]
for x,y,c in shelf_icons:
    pxrect(d,(x,y,x+16,y+20),c,'#2b1a12',2)
    pxrect(d,(x+4,y+4,x+12,y+8),'#f1d59a')

# center display tables
def table(x,y,w,h):
    pxrect(d,(x+6,y+6,x+w+6,y+h+6),'#3b2416')
    pxrect(d,(x,y,x+w,y+h),'#6a3f22','#2f1c12',3)
    pxrect(d,(x+8,y+8,x+w-8,y+h-8),'#8e5a2e','#4a2b18',2)
    # legs
    for lx in (x+8,x+w-14):
        pxrect(d,(lx,y+h,lx+8,y+h+18),'#3e2517')

table(270,350,200,110)
table(610,350,150,110)
# table objects
for x,y,c in [(305,375,'#b83e31'),(347,374,'#365f9d'),(390,375,'#e0be77'),(430,374,'#65884c'),
              (637,375,'#ccb48c'),(675,373,'#8f5ea9'),(712,375,'#cc6646')]:
    pxrect(d,(x,y,x+24,y+28),c,'#362015',2)

# counter
pxrect(d,(38,560,255,650),'#57331e','#29190f',3)
pxrect(d,(48,572,245,632),'#6d4224','#3a2315',2)
pxrect(d,(72,630,220,655),'#d3a464','#55331f',3)
# stool / register
pxrect(d,(188,575,220,592),'#1d2d3a','#0b1117',2)
pxrect(d,(195,592,212,609),'#31465a','#0b1117',2)
# couch
pxrect(d,(815,505,922,555),'#2c5a3a','#16331f',3)
pxrect(d,(820,510,870,548),'#356d46')
pxrect(d,(873,510,917,548),'#356d46')
# lamp
for x,y in [(75,520),(892,470)]:
    pxrect(d,(x,y,x+6,y+35),'#5f4027')
    pxrect(d,(x-10,y-12,x+16,y+8),'#f0c55e','#6d4424',2)
# plants
for x,y in [(130,90),(355,94),(557,94),(925,92),(105,250),(885,250),(285,550),(750,540),(920,575)]:
    pxrect(d,(x-6,y+12,x+8,y+28),'#7a4b28','#3b2416',1)
    for dx,dy in [(-8,2),(0,0),(8,2),(-4,-7),(5,-8)]:
        pxrect(d,(x+dx-5,y+dy-5,x+dx+5,y+dy+5),random.choice(['#2d6d3b','#3f824a','#4a944f']))
# cat
pxrect(d,(72,165,108,183),'#24282a','#131516',1)
pxrect(d,(62,170,76,184),'#24282a')
pxrect(d,(66,164,73,170),'#24282a')
pxrect(d,(72,164,78,170),'#24282a')
pxrect(d,(99,175,117,179),'#24282a')
pxrect(d,(67,174,70,177),'#e2d4b4')
# signs
pxrect(d,(40,58,137,135),'#1f1b18','#4f321f',3)
pxrect(d,(825,290,928,395),'#1d1b19','#4d3020',3)

# fonts: default small bitmap-ish
font=None
try:
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',14)
    font_small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',12)
except:
    font=ImageFont.load_default(); font_small=font

# shelf labels
for label,cx,cy in shelf_labels:
    bbox=d.textbbox((0,0),label,font=font)
    tw=bbox[2]-bbox[0]; th=bbox[3]-bbox[1]
    d.text((cx-tw/2,cy-th/2-1),label,fill='#24160d',font=font)
# sign text
def center_text(box, lines, fill='#efc983'):
    x0,y0,x1,y1=box
    yy=y0+10
    for line in lines:
        bbox=d.textbbox((0,0),line,font=font_small)
        tw=bbox[2]-bbox[0]
        d.text(((x0+x1-tw)/2,yy),line,fill=fill,font=font_small)
        yy+=18
center_text((40,58,137,135),['WELCOME','CURIOUS','MINDS'])
center_text((825,290,928,395),['GOOD','OBJECTS','BETTER','COMPANY',':)'])
# counter sign
bbox=d.textbbox((0,0),'THE BOT SHOP',font=font_small); tw=bbox[2]-bbox[0]
d.text((146-tw/2,637),'THE BOT SHOP',fill='#2c1a0e',font=font_small)

save_scaled(img, ROOT/'shop_bg.png')

# ---------- bot sprites ----------
bots={
 'mara':'#a857d6','otto':'#e77a35','june':'#3c8be8','felix':'#5f8a51','dot':'#e0bb29',
 'arthur':'#98825f','nell':'#e84c62','milo':'#62cce4','iris':'#ef71a8','gus':'#d8e7eb'}
for name,color in bots.items():
    im=Image.new('RGBA',(32,32),(0,0,0,0)); dr=ImageDraw.Draw(im)
    # shadow
    dr.rectangle((8,27,24,29), fill=(0,0,0,90))
    # antenna / ears
    dr.rectangle((5,7,9,12), fill='#1a2027'); dr.rectangle((23,7,27,12), fill='#1a2027')
    dr.rectangle((6,6,8,9), fill=color); dr.rectangle((24,6,26,9), fill=color)
    # body
    dr.rectangle((6,10,26,25), fill='#121820')
    dr.rectangle((8,8,24,24), fill=color)
    dr.rectangle((6,12,8,20), fill=color); dr.rectangle((24,12,26,20), fill=color)
    # face screen
    dr.rectangle((9,11,23,17), fill='#08101a')
    dr.rectangle((11,13,13,14), fill='#8ff5ff'); dr.rectangle((19,13,21,14), fill='#8ff5ff')
    # belly highlight
    dr.rectangle((11,20,21,22), fill='#e4edf0')
    # legs
    dr.rectangle((9,24,13,27), fill='#141a20'); dr.rectangle((19,24,23,27), fill='#141a20')
    # pixel accents unique-ish
    if name in ('mara','iris','nell'):
        dr.rectangle((14,5,18,8), fill=color)
    if name=='gus':
        dr.rectangle((10,18,22,20), fill='#c8dce3')
    save_scaled(im, ROOT/'bots'/f'{name}.png', 2)

# ---------- item sprites ----------
# simple 16x16 sprites
item_defs={
'coffee_mug':('mug','#d9d2bd'), 'desk_lamp':('lamp','#e0b55e'), 'alarm_clock':('clock','#d7bf6b'),
'motel_key':('key','#d0a63f'), 'framed_photo':('frame','#5f86a8'), 'bent_spoon':('spoon','#aeb8bd'),
'ceramic_bird':('bird','#6fa4bf'), 'rotary_phone':('phone','#b63e34'), 'pocket_radio':('radio','#4e6678'),
'postcard':('postcard','#e8d0a6'), 'snow_globe':('globe','#69b7d6'), 'toy_car':('car','#cf493a'),
'glass_bottle':('bottle','#6fa58a'), 'kitchen_timer':('timer','#d7b166'), 'paperback_book':('book','#7b4fa1'),
'plastic_chair':('chair','#4c86bd'), 'cassette_tape':('cassette','#4c4e55'), 'picture_frame':('frame','#a67843'),
'bus_ticket':('ticket','#d9c27d'), 'thermos':('thermos','#7794a1'), 'umbrella':('umbrella','#d8638f'), 'porcelain_dog':('dog','#d5ccb8')}

def draw_item(kind,color):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); dr=ImageDraw.Draw(im)
    dark='#2b231d'; light='#f2dfaa'
    if kind=='mug':
        dr.rectangle((3,5,10,12),fill=color,outline=dark); dr.rectangle((10,7,13,10),outline=color,width=2)
    elif kind=='lamp':
        dr.rectangle((7,6,8,13),fill=dark); dr.rectangle((4,4,11,7),fill=color,outline=dark); dr.rectangle((5,13,10,14),fill=dark)
    elif kind=='clock':
        dr.rectangle((3,4,12,12),fill=color,outline=dark); dr.rectangle((7,6,8,10),fill=dark); dr.rectangle((7,8,10,9),fill=dark)
    elif kind=='key':
        dr.ellipse((2,3,7,8),outline=color,width=2); dr.rectangle((6,5,13,7),fill=color); dr.rectangle((10,7,12,9),fill=color)
    elif kind=='frame':
        dr.rectangle((2,2,13,13),fill=color,outline=dark); dr.rectangle((4,4,11,11),fill='#d8a45e')
    elif kind=='spoon':
        dr.ellipse((5,2,10,7),fill=color,outline=dark); dr.rectangle((7,7,8,14),fill=color)
    elif kind=='bird':
        dr.rectangle((4,7,11,11),fill=color,outline=dark); dr.rectangle((8,4,12,8),fill=color,outline=dark); dr.point((10,6),fill='#111')
    elif kind=='phone':
        dr.rectangle((3,7,12,12),fill=color,outline=dark); dr.arc((5,4,10,9),0,360,fill=light,width=2)
    elif kind=='radio':
        dr.rectangle((2,5,13,12),fill=color,outline=dark); dr.rectangle((4,7,7,10),fill='#1a2228'); dr.rectangle((9,7,11,8),fill=light)
    elif kind=='postcard':
        dr.rectangle((2,4,13,11),fill=color,outline=dark); dr.line((8,4,8,11),fill='#7a6a54')
    elif kind=='globe':
        dr.ellipse((4,2,11,9),fill=color,outline=dark); dr.rectangle((6,9,9,12),fill='#8c5c32'); dr.rectangle((4,12,11,13),fill='#8c5c32')
    elif kind=='car':
        dr.rectangle((3,7,12,11),fill=color,outline=dark); dr.rectangle((5,5,10,8),fill=color,outline=dark); dr.point((5,12),fill='#111'); dr.point((10,12),fill='#111')
    elif kind=='bottle':
        dr.rectangle((6,2,9,5),fill=color,outline=dark); dr.rectangle((4,5,11,13),fill=color,outline=dark)
    elif kind=='timer':
        dr.rectangle((4,4,11,12),fill=color,outline=dark); dr.ellipse((5,5,10,10),outline=dark)
    elif kind=='book':
        dr.rectangle((3,3,12,13),fill=color,outline=dark); dr.line((5,3,5,13),fill=light)
    elif kind=='chair':
        dr.rectangle((4,3,11,8),fill=color,outline=dark); dr.rectangle((4,8,11,10),fill=color); dr.rectangle((5,10,6,14),fill=dark); dr.rectangle((10,10,11,14),fill=dark)
    elif kind=='cassette':
        dr.rectangle((2,5,13,11),fill=color,outline=dark); dr.ellipse((4,7,6,9),outline=light); dr.ellipse((9,7,11,9),outline=light)
    elif kind=='ticket':
        dr.rectangle((2,5,13,10),fill=color,outline=dark); dr.line((8,5,8,10),fill='#876')
    elif kind=='thermos':
        dr.rectangle((5,3,10,13),fill=color,outline=dark); dr.rectangle((4,2,11,4),fill='#d2d7d9',outline=dark)
    elif kind=='umbrella':
        dr.pieslice((2,2,13,10),180,360,fill=color,outline=dark); dr.line((8,7,8,13),fill=dark,width=1); dr.arc((6,10,10,14),0,180,fill=dark)
    elif kind=='dog':
        dr.rectangle((5,6,11,12),fill=color,outline=dark); dr.rectangle((7,3,11,7),fill=color,outline=dark); dr.point((10,5),fill='#111')
    return im

for fname,(kind,color) in item_defs.items():
    save_scaled(draw_item(kind,color), ROOT/'items'/f'{fname}.png', 3)

# marker icon for inspect thought
im=Image.new('RGBA',(20,20),(0,0,0,0)); dr=ImageDraw.Draw(im)
dr.rectangle((2,2,17,14),fill='white',outline='#251d18',width=2); dr.polygon([(7,14),(10,18),(11,14)],fill='white'); dr.text((6,2),'?',fill='#111',font=font_small)
save_scaled(im, ROOT/'decor'/'bubble_question.png',2)

print('assets created')
