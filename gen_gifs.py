# -*- coding: utf-8 -*-
"""회복 운동 가이드 GIF (스틱맨, 오프라인 생성)."""
import os, math
from PIL import Image, ImageDraw
import os
OUT=os.environ.get("OUT","./figures/recovery"); os.makedirs(OUT, exist_ok=True)
W,H=260,200; CX=W//2; BLUE=(37,99,235); INK=(20,30,55); GRID=(230,238,250)

def base(d):
    d.rectangle([0,0,W,H],fill=(247,250,255))
    for x in range(0,W,20): d.line([(x,0),(x,H)],fill=GRID)
    for y in range(0,H,20): d.line([(0,y),(W,y)],fill=GRID)

def figure(d,hip_y=150,head_dx=0,arm="down",lean=0,col=INK):
    cx=CX+lean
    head=(cx+head_dx,hip_y-78)
    d.ellipse([head[0]-13,head[1]-13,head[0]+13,head[1]+13],outline=col,width=5)
    neck=(cx,hip_y-62); d.line([(head[0],head[1]+13),neck],fill=col,width=5)
    d.line([neck,(cx,hip_y)],fill=col,width=6)              # spine
    # legs
    d.line([(cx,hip_y),(cx-20,hip_y+45)],fill=col,width=6)
    d.line([(cx,hip_y),(cx+20,hip_y+45)],fill=col,width=6)
    sh=(cx,hip_y-50)
    if arm=="up":
        d.line([sh,(cx-30,hip_y-92)],fill=BLUE,width=6); d.line([sh,(cx+30,hip_y-92)],fill=BLUE,width=6)
    elif arm=="side":
        d.line([sh,(cx-42,hip_y-50)],fill=BLUE,width=6); d.line([sh,(cx+42,hip_y-50)],fill=BLUE,width=6)
    else:
        d.line([sh,(cx-20,hip_y-18)],fill=BLUE,width=6); d.line([sh,(cx+20,hip_y-18)],fill=BLUE,width=6)

def save(frames,name,dur=140):
    frames[0].save(f"{OUT}/{name}",save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=2)
    print(name, os.path.getsize(f"{OUT}/{name}")//1024,"KB")

# 1) 스트레칭 (팔 위로 + 좌우 측면 신전)
def stretch():
    fr=[]
    seq=[("down",0),("side",0),("up",0),("up",-10),("up",0),("up",10),("up",0),("side",0)]
    for arm,lean in seq:
        im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im); base(d); figure(d,arm=arm,lean=lean)
        d.text((10,8),"Stretch",fill=BLUE); fr.append(im)
    save(fr,"stretch.gif")

# 2) 목 풀기 (머리 좌우)
def neck():
    fr=[]
    for k in [0,-10,-16,-10,0,10,16,10]:
        im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im); base(d); figure(d,head_dx=k,arm="down")
        d.text((10,8),"Neck loosen",fill=BLUE); fr.append(im)
    save(fr,"neck.gif")

# 3) 휴식/호흡 (어깨 상하 + Zzz)
def rest():
    fr=[]
    for i in range(8):
        off=int(4*math.sin(i/8*2*math.pi))
        im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im); base(d); figure(d,hip_y=150+off,arm="down")
        d.text((10,8),"Rest / breathe",fill=BLUE)
        if i%4<2: d.text((CX+30,60),"z z",fill=INK)
        fr.append(im)
    save(fr,"rest.gif",dur=200)

stretch(); neck(); rest()
