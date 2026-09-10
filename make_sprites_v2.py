from PIL import Image, ImageDraw
from pathlib import Path

ROOT=Path('/mnt/data/bot_shop_rework/assets')
BOTDIR=ROOT/'bots'; ITEMDIR=ROOT/'items'; DECOR=ROOT/'decor'
BOTDIR.mkdir(parents=True,exist_ok=True); ITEMDIR.mkdir(parents=True,exist_ok=True)

def up(img,scale=2,path=None):
    img=img.resize((img.width*scale,img.height*scale),Image.Resampling.NEAREST)
    if path: img.save(path)
    return img

def rect(d,xy,c): d.rectangle(xy,fill=c)
def px(d,x,y,c): d.point((x,y),fill=c)

def bot_sprite(base, accent, variant=0):
    im=Image.new('RGBA',(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    outline='#18212c'; deep='#0a1119'; visor='#08131f'; cyan='#79e9ff'; white='#dffaff'
    # ground shadow
    d.ellipse((7,27,25,30),fill=(0,0,0,70))
    # feet
    rect(d,(8,24,12,28),outline); rect(d,(20,24,24,28),outline)
    rect(d,(9,24,12,26),base); rect(d,(20,24,23,26),base)
    # arms
    rect(d,(3,13,7,20),outline); rect(d,(25,13,29,20),outline)
    rect(d,(4,14,7,18),accent); rect(d,(25,14,28,18),accent)
    # antenna / ear variants
    if variant%3==0:
        rect(d,(14,2,17,6),outline); rect(d,(15,1,16,3),accent)
    elif variant%3==1:
        rect(d,(6,6,9,10),outline); rect(d,(23,6,26,10),outline)
        rect(d,(7,6,9,8),accent); rect(d,(23,6,25,8),accent)
    else:
        rect(d,(13,3,18,6),outline); rect(d,(14,2,17,4),accent)
    # head shell
    rect(d,(7,6,24,9),outline); rect(d,(5,9,26,20),outline)
    rect(d,(7,7,22,9),accent); rect(d,(7,9,24,18),base)
    # rounded pixels
    rect(d,(5,11,6,17),outline); rect(d,(25,11,26,17),outline)
    rect(d,(7,18,24,20),outline)
    # visor
    rect(d,(8,10,23,16),visor); rect(d,(9,11,22,15),'#0d2234')
    # eye expression variants
    if variant in (3,7):
        rect(d,(11,12,13,13),cyan); rect(d,(18,12,20,13),cyan)
    elif variant in (4,8):
        rect(d,(10,12,13,14),white); rect(d,(18,12,21,14),white)
    else:
        rect(d,(10,12,13,14),cyan); rect(d,(18,12,21,14),cyan)
        px(d,11,12,white); px(d,19,12,white)
    # body
    rect(d,(8,20,23,25),outline); rect(d,(10,20,21,24),base)
    rect(d,(11,20,20,21),accent)
    # chest panel
    rect(d,(13,22,18,24),deep); rect(d,(14,22,17,22),accent)
    # highlights
    rect(d,(8,9,10,10),'#ffffff55'); px(d,9,21,'#ffffff66')
    # role-specific details
    if variant==0: # mara side sensor
        rect(d,(25,8,27,11),outline); rect(d,(25,8,26,9),accent)
    if variant==1: # otto round ears
        rect(d,(4,10,6,14),accent); rect(d,(26,10,28,14),accent)
    if variant==2: # june forehead bar
        rect(d,(10,7,20,8),'#bcefff')
    if variant==3: # felix catalog marks
        rect(d,(9,22,10,23),accent); rect(d,(21,22,22,23),accent)
    if variant==4: # dot tiny crown nub
        rect(d,(15,0,16,2),accent)
    if variant==5: # arthur side caps
        rect(d,(4,12,6,16),'#d0c09b'); rect(d,(26,12,28,16),'#d0c09b')
    if variant==6: # nell angular crest
        rect(d,(11,4,20,6),outline); rect(d,(13,3,18,5),accent)
    if variant==7: # milo antenna lights
        px(d,13,4,cyan); px(d,18,4,cyan)
    if variant==8: # iris heart-ish chest
        px(d,14,22,'#ffd0e8'); px(d,17,22,'#ffd0e8'); rect(d,(15,23,16,24),'#ffd0e8')
    if variant==9: # gus blank/simple
        rect(d,(14,23,17,23),'#d7e9ee')
    return im

bots={
 'mara':('#7e42c4','#b882ff'), 'otto':('#d66a2f','#ffb067'), 'june':('#2470d0','#6ab4ff'),
 'felix':('#476c4a','#83a76c'), 'dot':('#d5ad19','#ffe165'), 'arthur':('#77684f','#b7a47d'),
 'nell':('#d53e57','#ff7590'), 'milo':('#32a9d0','#7be5ff'), 'iris':('#e05e9a','#ff9dca'), 'gus':('#c8d8dc','#f0fbff')
}
for i,(name,(base,accent)) in enumerate(bots.items()):
    up(bot_sprite(base,accent,i),2,BOTDIR/f'{name}.png')

# ---------------- Item sprites ----------------
OUT='#3a2b22'; DK='#171a1d'; HI='#f5dfb0'; GOLD='#d6a53a'; BLUE='#3f86b8'; RED='#b94b3f'; GREEN='#5f8b68'; CREAM='#dfcfad'; PURPLE='#7d55a6'; GRAY='#9b9d98'

def item_canvas():
    return Image.new('RGBA',(24,24),(0,0,0,0))

def shadow(d,w=15):
    d.ellipse(((24-w)//2,20,(24+w)//2,22),fill=(0,0,0,65))

def save_item(name, drawfn):
    im=item_canvas(); d=ImageDraw.Draw(im); shadow(d); drawfn(d); up(im,2,ITEMDIR/f'{name}.png')

save_item('coffee_mug',lambda d:(rect(d,(6,9,15,18),OUT),rect(d,(7,8,14,17),CREAM),rect(d,(15,10,19,15),OUT),rect(d,(16,11,18,14),CREAM),rect(d,(9,9,12,9),'#fff7d8'),rect(d,(7,17,14,18),OUT)))
save_item('desk_lamp',lambda d:(rect(d,(10,8,12,18),OUT),rect(d,(11,9,11,17),GOLD),rect(d,(6,5,16,8),OUT),rect(d,(7,5,15,7),'#e9b94f'),rect(d,(7,18,16,20),OUT),rect(d,(8,18,15,19),GOLD),rect(d,(9,8,13,10),OUT)))
save_item('alarm_clock',lambda d:(rect(d,(5,8,18,18),OUT),rect(d,(6,9,17,17),GOLD),rect(d,(8,10,15,15),CREAM),rect(d,(11,10,12,14),DK),rect(d,(12,13,15,14),DK),rect(d,(6,6,9,9),OUT),rect(d,(14,6,17,9),OUT),rect(d,(7,18,8,20),OUT),rect(d,(15,18,16,20),OUT)))
save_item('motel_key',lambda d:(rect(d,(5,11,17,14),OUT),rect(d,(6,10,10,15),GOLD),rect(d,(7,11,8,12),DK),rect(d,(11,11,19,13),GOLD),rect(d,(16,13,18,15),GOLD)))
save_item('framed_photo',lambda d:(rect(d,(4,4,19,19),OUT),rect(d,(5,5,18,18),'#a86b3e'),rect(d,(7,7,16,16),'#6aa0b9'),rect(d,(8,12,15,16),'#d9c491'),rect(d,(11,8,12,11),'#f0d47e')))
save_item('bent_spoon',lambda d:(rect(d,(11,5,13,16),GRAY),rect(d,(10,4,14,8),GRAY),rect(d,(12,15,16,17),GRAY),rect(d,(15,16,17,18),GRAY),px(d,11,5,HI)))
save_item('ceramic_bird',lambda d:(rect(d,(8,10,15,16),OUT),rect(d,(9,9,15,15),BLUE),rect(d,(13,7,17,11),OUT),rect(d,(14,8,17,10),BLUE),rect(d,(17,9,19,10),GOLD),rect(d,(10,14,12,16),'#8ec6de'),px(d,15,9,DK)))
save_item('rotary_phone',lambda d:(rect(d,(5,11,18,18),OUT),rect(d,(6,12,17,17),RED),rect(d,(7,7,16,11),OUT),rect(d,(8,7,15,9),'#d86f62'),rect(d,(9,12,14,16),CREAM),rect(d,(10,13,13,15),DK)))
save_item('pocket_radio',lambda d:(rect(d,(4,8,19,18),OUT),rect(d,(5,9,18,17),'#6d6d66'),rect(d,(7,10,12,14),BLUE),rect(d,(14,10,16,12),GOLD),rect(d,(14,14,17,15),DK),rect(d,(16,5,17,9),GRAY)))
save_item('postcard',lambda d:(rect(d,(4,7,19,17),OUT),rect(d,(5,8,18,16),CREAM),rect(d,(6,9,12,15),'#6d9f7d'),rect(d,(14,9,17,11),RED),rect(d,(13,13,17,13),GRAY),rect(d,(13,15,17,15),GRAY)))
save_item('snow_globe',lambda d:(d.ellipse((6,4,18,16),fill=OUT),d.ellipse((7,5,17,15),fill='#8bd0df'),rect(d,(10,8,13,14),CREAM),rect(d,(8,16,16,19),OUT),rect(d,(9,16,15,18),'#8a5d39'),px(d,9,7,'white'),px(d,14,9,'white')))
save_item('toy_car',lambda d:(rect(d,(4,11,19,16),OUT),rect(d,(6,9,15,15),RED),rect(d,(9,8,14,10),'#6cb3d5'),rect(d,(6,16,9,18),DK),rect(d,(15,16,18,18),DK),rect(d,(5,12,7,13),'#ffd77a')))
save_item('glass_bottle',lambda d:(rect(d,(9,4,14,7),OUT),rect(d,(10,4,13,6),'#96c6af'),rect(d,(7,7,16,19),OUT),rect(d,(8,8,15,18),'#5c9c84'),rect(d,(9,9,10,16),'#aee0c9'),rect(d,(10,13,14,15),'#d5c69a')))
save_item('kitchen_timer',lambda d:(rect(d,(5,6,18,19),OUT),rect(d,(6,7,17,18),CREAM),d.ellipse((7,8,16,17),fill=OUT),d.ellipse((8,9,15,16),fill='#ece4c8'),rect(d,(11,9,12,13),RED),rect(d,(12,13,15,14),RED)))
save_item('paperback_book',lambda d:(rect(d,(5,4,18,19),OUT),rect(d,(6,5,17,18),PURPLE),rect(d,(7,6,9,17),'#d7b45e'),rect(d,(10,7,15,8),CREAM),rect(d,(10,10,14,10),CREAM)))
save_item('plastic_chair',lambda d:(rect(d,(6,5,17,13),OUT),rect(d,(7,6,16,12),BLUE),rect(d,(5,12,18,16),OUT),rect(d,(6,12,17,15),BLUE),rect(d,(7,15,9,20),OUT),rect(d,(15,15,17,20),OUT)))
save_item('cassette_tape',lambda d:(rect(d,(4,7,19,17),OUT),rect(d,(5,8,18,16),'#5f6268'),rect(d,(7,10,16,14),CREAM),d.ellipse((8,11,10,13),fill=DK),d.ellipse((14,11,16,13),fill=DK),rect(d,(9,15,15,15),DK)))
save_item('picture_frame',lambda d:(rect(d,(4,4,19,19),OUT),rect(d,(5,5,18,18),'#b58043'),rect(d,(8,8,15,15),'#2d3440')))
save_item('bus_ticket',lambda d:(rect(d,(4,8,19,16),OUT),rect(d,(5,9,18,15),'#d6bd75'),rect(d,(8,9,8,15),GRAY),rect(d,(15,9,15,15),GRAY),rect(d,(10,11,13,11),DK)))
save_item('thermos',lambda d:(rect(d,(8,4,15,19),OUT),rect(d,(9,5,14,18),'#8a9aa1'),rect(d,(9,5,14,7),'#d4d7d8'),rect(d,(10,8,11,16),'#b9c2c5')))
save_item('umbrella',lambda d:(rect(d,(11,8,12,19),GRAY),d.polygon([(4,9),(7,5),(12,3),(17,5),(20,9)],fill=OUT),d.polygon([(5,9),(8,6),(12,4),(16,6),(19,9)],fill='#d65d98'),rect(d,(12,18,15,20),GRAY)))
save_item('porcelain_dog',lambda d:(rect(d,(7,11,15,17),OUT),rect(d,(8,10,14,16),CREAM),rect(d,(13,7,18,12),OUT),rect(d,(14,8,17,11),CREAM),rect(d,(15,6,17,8),OUT),rect(d,(8,16,9,19),OUT),rect(d,(13,16,14,19),OUT),px(d,16,9,DK)))

# bubble pixel sprite
im=Image.new('RGBA',(20,16),(0,0,0,0));d=ImageDraw.Draw(im);rect(d,(2,2,17,11),'#2b211b');rect(d,(3,3,16,10),'#fffaf0');rect(d,(6,11,9,13),'#2b211b');rect(d,(7,10,10,12),'#fffaf0');rect(d,(9,4,11,5),DK);rect(d,(10,6,11,8),DK);px(d,10,9,DK);up(im,2,DECOR/'bubble_question.png')
print('generated v2 sprites')
