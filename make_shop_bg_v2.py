from PIL import Image, ImageDraw
from pathlib import Path
import random
random.seed(7)
W,H=480,360
im=Image.new('RGB',(W,H),'#8f5b31');d=ImageDraw.Draw(im)
# palette
outline='#2a1b13'; wall='#4a2c1c'; wall2='#5a3521'; wood='#a86b37'; wood2='#9b6032'; seam='#7b4728'; gold='#d3a15e'; cream='#edcd90'; dark='#17191a'; green='#37613e'; green2='#2c4c33'; red='#7c2b24'; red2='#9c3b2d'; blue='#304e72';
# floor planks
for y in range(65,H,12):
    d.rectangle((6,y,W-7,y+11),fill=wood if (y//12)%2 else wood2)
    d.line((6,y,W-7,y),fill=seam,width=1)
    offset=20 if (y//12)%2 else 0
    for x in range(-20+offset,W,44): d.line((x,y,x,y+11),fill='#87502c')
    # little knots
    for _ in range(3):
        x=random.randint(15,W-15); yy=random.randint(y+3,min(y+9,H-2)); d.point((x,yy),fill='#c18349')
# top wall
d.rectangle((5,5,W-6,64),fill=wall); d.rectangle((8,8,W-9,61),fill=wall2)
for x in range(12,W-12,16): d.line((x,8,x,61),fill='#3f2519')
d.rectangle((5,61,W-6,66),fill=outline)
# outer border
d.rectangle((2,2,W-3,H-3),outline=outline,width=4); d.rectangle((6,6,W-7,H-7),outline='#6f4329',width=2)
# helpers
def sign(x,y,w,text):
    d.rectangle((x,y,x+w,y+13),fill=outline); d.rectangle((x+2,y+2,x+w-2,y+11),fill=gold)
    # fake text strokes (image has real text via CSS elsewhere too, but these add texture)

def plant(x,y):
    d.rectangle((x+6,y+13,x+13,y+19),fill=outline); d.rectangle((x+7,y+13,x+12,y+18),fill='#7b4a29')
    leaves=[(x+9,y+2,x+11,y+13),(x+2,y+6,x+10,y+10),(x+10,y+6,x+18,y+10),(x+5,y+3,x+9,y+11),(x+12,y+3,x+16,y+11)]
    for r in leaves: d.rectangle(r,fill='#2d7142')
    d.rectangle((x+9,y+7,x+11,y+12),fill='#4e9b59')

def lamp(x,y):
    d.rectangle((x+5,y+9,x+7,y+22),fill='#59371f'); d.rectangle((x+1,y+22,x+11,y+24),fill=outline)
    d.rectangle((x+1,y+2,x+11,y+9),fill=outline); d.polygon([(x+2,y+8),(x+4,y+1),(x+8,y+1),(x+10,y+8)],fill='#e0b15f')
    d.rectangle((x+4,y+4,x+8,y+8),fill='#ffe8a1')

def shelf(x,y,w,h,label,icons):
    # legs and body
    d.rectangle((x+3,y+h-2,x+6,y+h+7),fill=outline); d.rectangle((x+w-6,y+h-2,x+w-3,y+h+7),fill=outline)
    d.rectangle((x,y,x+w,y+h),fill=outline); d.rectangle((x+3,y+3,x+w-3,y+h-3),fill='#6f4125')
    d.rectangle((x+4,y+h-9,x+w-4,y+h-6),fill='#3d2518')
    d.rectangle((x+4,y+5,x+w-4,y+7),fill='#3d2518')
    sign(x+8,y-12,w-16,label)
    # object blocks
    cols=max(4,len(icons)); step=(w-14)//cols
    for i,c in enumerate(icons):
        xx=x+7+i*step
        d.rectangle((xx,y+10,xx+7,y+21),fill=outline); d.rectangle((xx+1,y+11,xx+6,y+20),fill=c)
        d.rectangle((xx+1,y+12,xx+6,y+13),fill='#efc675')
        # lower row
        if i%2==0:
            d.rectangle((xx,y+25,xx+7,y+32),fill=outline); d.rectangle((xx+1,y+26,xx+6,y+31),fill=random.choice(['#a34e3e','#596a96','#8d6e42','#477c70']))

def rug(x,y,w,h,c1,c2):
    d.rectangle((x,y,x+w,y+h),fill=outline); d.rectangle((x+3,y+3,x+w-3,y+h-3),fill=c1)
    d.rectangle((x+7,y+7,x+w-7,y+h-7),outline=c2,width=3); d.rectangle((x+12,y+12,x+w-12,y+h-12),outline='#c15a3e' if c1==red else '#61845a',width=2)
    for yy in range(y+16,y+h-10,10):
        for xx in range(x+16,x+w-10,14):
            d.rectangle((xx,yy,xx+2,yy+2),fill=c2)

def table(x,y,w,h,kind=0):
    d.rectangle((x+5,y+h-2,x+8,y+h+7),fill=outline); d.rectangle((x+w-8,y+h-2,x+w-5,y+h+7),fill=outline)
    d.rectangle((x,y,x+w,y+h),fill=outline); d.rectangle((x+3,y+3,x+w-3,y+h-3),fill='#7a4828')
    d.rectangle((x+7,y+7,x+w-7,y+h-7),fill='#9d6638')
    objs=[('#bd483a',(12,12,22,23)),('#355b87',(30,11,43,23)),('#d9ba72',(50,12,61,23)),('#5c8a5c',(68,10,80,23))]
    if kind==1: objs=[('#c7ad83',(10,8,23,22)),('#7a4b98',(31,10,43,22)),('#cc6645',(52,9,65,22)),('#8ca55d',(71,11,81,23))]
    for c,(a,b,cx,dy) in objs:
        d.rectangle((x+a,y+b,x+cx,y+dy),fill=outline); d.rectangle((x+a+1,y+b+1,x+cx-1,y+dy-1),fill=c)

def counter(x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill=outline); d.rectangle((x+3,y+3,x+w-3,y+h-3),fill='#654024')
    d.rectangle((x+5,y+7,x+w-5,y+13),fill='#825432')
    # register
    d.rectangle((x+w-28,y+6,x+w-11,y+15),fill=outline); d.rectangle((x+w-26,y+7,x+w-13,y+12),fill='#2b4a58')
    # stool / small things
    d.rectangle((x+11,y+8,x+18,y+12),fill='#c69a55'); d.rectangle((x+22,y+6,x+25,y+12),fill='#a8793e')
    sign(x+15,y+h-10,w-30,'BOT SHOP')

# left chalkboard
d.rectangle((15,17,74,61),fill=outline); d.rectangle((18,20,71,58),fill='#1e1c19')
# decorative gold dash text
for i,linew in enumerate([36,40,29,34]): d.rectangle((28,27+i*7,28+linew,28+i*7),fill='#d8ad66')
# cat
d.rectangle((29,74,54,81),fill=dark); d.rectangle((34,70,45,79),fill=dark); d.polygon([(34,70),(37,67),(39,71)],fill=dark); d.polygon([(42,70),(45,67),(47,72)],fill=dark); d.rectangle((53,77,58,79),fill=dark)
# shelves
shelf(89,30,82,38,'ODD',['#d97a2c','#8157c0','#cb4657','#e4c381','#7e9bb4'])
shelf(192,30,86,38,'HOME',['#a99a89','#c45476','#bd8f46','#e0b066','#7957a4'])
shelf(298,30,86,38,'ART',['#d35d45','#e3b76a','#4f95ca','#d75b80','#699063'])
shelf(401,30,66,38,'MISC',['#d44ea0','#4b92d0','#c18a32','#e6c56a'])
# plants wall
for p in [(76,33),(175,33),(281,33),(387,33),(456,34)]: plant(*p)
# hanging lamps
lamp(78,11); lamp(390,10)
# right sign
d.rectangle((405,152,468,213),fill=outline); d.rectangle((409,156,464,209),fill='#20201e')
for i,w in enumerate([35,43,37,47,28]): d.rectangle((421,165+i*7,421+w,166+i*7),fill='#d1a45e')
# rugs + tables
rug(111,145,151,116,red,'#58211c'); rug(281,145,116,116,green,'#203f2a')
table(137,179,98,54,0); table(307,177,77,55,1)
# lower display shelves
shelf(161,286,85,37,'VINT',['#d2b365','#855836','#55a1be','#cf5b49'])
shelf(269,286,96,37,'CURIO',['#82b5bd','#4c9ed4','#a5679e','#cc7449','#c9a15c'])
# counter/couch/corner decor
counter(18,286,112,51)
d.rectangle((374,277,459,337),fill=outline); d.rectangle((379,282,454,332),fill=blue); d.rectangle((379,282,454,297),fill='#21415f')
d.rectangle((414,258,462,282),fill=outline); d.rectangle((418,261,458,280),fill='#2f6840'); d.line((438,261,438,280),fill='#1d4a2c',width=2)
# round table couch corner
d.ellipse((396,304,444,350),fill=outline);d.ellipse((400,308,440,346),fill='#76502d'); d.rectangle((414,316,429,323),fill='#d0ac61'); d.rectangle((418,324,431,330),fill='#325b8c')
# lower lamps/plants
lamp(31,261); lamp(446,260)
for p in [(139,271),(247,272),(373,269),(452,294),(466,267),(40,244)]: plant(*p)
# little exit sign left
d.rectangle((9,195,31,246),fill=outline); d.rectangle((13,199,27,242),fill=cream); d.rectangle((18,205,21,226),fill=dark); d.rectangle((16,205,23,208),fill=dark); d.polygon([(17,234),(24,234),(20,239)],fill=dark)
# pixels / edge shading
d.rectangle((6,341,W-7,352),fill='#4e2c1d')
# upscale
im=im.resize((960,720),Image.Resampling.NEAREST)
im.save('/mnt/data/bot_shop_rework/assets/shop_bg.png')
print('wrote shop_bg v2')
