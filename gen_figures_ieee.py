# -*- coding: utf-8 -*-
"""SHine-K IEEE Access diagram figures - FINAL v7 (2026-07-23)
fig_arch / fig_dataflow / fig_workflow. Local: python3 gen_figures_ieee.py -> ./figures
Colab: run gen_figures_colab.ipynb (auto-mounts Drive, saves into project figures/)
fig_workflow v6 (variant H): right-column chain gaps widened to 2.3 units so
each chain arrow has shaft+head+clearance (was 1.0-1.75: head-only stubs that
touched borders); tip-to-border gap unified at G=0.7 for all arrows; all arrowheads unified at MS=4.5 (half of v4) with a
uniform G=0.5-unit tip-to-border gap; the four sense->judgement arrows land on
fanned endpoints (y=38.5/35.0/31.0/27.5) so heads no longer pile on one point.
Layout: worker 13.5/gap 2, sense 15.5 (camera 4-line), judgement 20 @5.4pt
(floor: measured line width 17.9 units), diamond half-width 8 ("Risk type?" one
line, centered normal), diamond-column gap 4, Continue monitoring y=32.
"""

import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon

EDGE="#1a1a1a"; FILL="#ffffff"; GREY="#eef1f6"; TXT="#000000"; DGREY="#5a5f6b"
OUT=os.environ.get("OUT","./figures"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":TXT,
    "axes.edgecolor":EDGE,"savefig.facecolor":"white"})
W=7.16  # IEEE Access \textwidth in inches

def rect(ax,x,y,w,h,fc=FILL,lw=1.0,ls="-"):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=EDGE,lw=lw,ls=ls,joinstyle="round"))
def txt(ax,x,y,s,fs=8,bold=False,it=False,ha="center",va="center",bg=None,color=TXT):
    bbox=dict(boxstyle="round,pad=0.22",fc=bg,ec="none") if bg else None
    ax.text(x,y,s,ha=ha,va=va,fontsize=fs,color=color,zorder=5,
            fontweight="bold" if bold else "normal",fontstyle="italic" if it else "normal",bbox=bbox)
def arr(ax,x1,y1,x2,y2,lw=1.1,ls="-",ms=13):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=ms,
                 color=EDGE,lw=lw,ls=ls,shrinkA=1,shrinkB=1,zorder=3))
def newax(h_in,ymax):
    fig,ax=plt.subplots(figsize=(W,h_in)); ax.set_xlim(0,100); ax.set_ylim(0,ymax); ax.axis("off")
    ax.set_aspect("auto"); fig.patch.set_facecolor("white"); return fig,ax
def save(fig,name):
    fig.savefig(f"{OUT}/{name}",dpi=300,bbox_inches="tight",pad_inches=0.05); plt.close(fig)
    print(name,"ok")


MS=4.5   # workflow arrowhead size (half of previous)
G=0.7    # uniform arrowhead-to-border gap (data units)

def fig_arch():
    fig,ax=newax(2.9,100)
    # (label, is_design): design/PoC nodes are dashed + light-filled to match
    # Figs. 2-3 and the Working/PoC/Design staging of Table II (honest staging).
    stages=[("SENSE",[("Vision: pose / PPE / fire",False),("Wearable vitals (BLE)",True),
                      ("Radar (mmWave)",True),("Environment IoT",True)]),
            ("JUDGE",[("Fall state machine",False),("Posture index (2-cue)",False),
                      ("Agent harness",True)]),
            ("ACT",[("Risk alerts + log",False),("Ergonomic feedback",False),
                    ("Recovery coaching",True)]),
            ("CONNECT",[("Control twin\n(multi-site)",False),("Realtime events\n(broker)",False),
                        ("119 / e-Gen\ndispatch",True)])]
    colw=22; gap=2; x0=3; y=16; H=74
    # legend (top band): solid = implemented/validated, dashed = design target
    ax.plot([x0,x0+3.4],[95.5,95.5],color=EDGE,lw=1.3)
    txt(ax,x0+4.2,95.5,"implemented (see Table II)",fs=8.0,ha="left")
    ax.plot([54,57.4],[95.5,95.5],color=EDGE,lw=1.1,ls=(0,(4,3)))
    txt(ax,58.2,95.5,"design target",fs=8.0,ha="left")
    for i,(name,nodes) in enumerate(stages):
        x=x0+i*(colw+gap)
        rect(ax,x,y,colw,H,fc=GREY,lw=1.1)
        txt(ax,x+colw/2,y+H-7,name,fs=10.5,bold=True)
        top=y+H-15; bot=y+5; n=len(nodes); slot=(top-bot)/n
        for j,(nd,des) in enumerate(nodes):
            cy=top-slot*(j+0.5); bh=min(12 if "\n" in nd else 10,slot-2)
            rect(ax,x+0.8,cy-bh/2,colw-1.6,bh,fc=("#f5f7fc" if des else FILL),lw=0.9,ls=("--" if des else "-"))
            txt(ax,x+colw/2,cy,nd,fs=7.0,color=(DGREY if des else TXT))
        if i<3: arr(ax,x+colw,y+H/2,x+colw+gap-G,y+H/2,lw=1.1,ms=4.5)   # 촉 4.5·간격 G 통일
    # 피드백 루프: CONNECT 하변 중앙 → 하단 레일(점선) → SENSE 하변으로 상향 진입(촉은 하변-G)
    dl=(0,(4,3)); y_rail=8.0
    xS=x0+colw/2; xC=x0+3*(colw+gap)+colw/2
    ax.plot([xC,xC],[y,y_rail],color=EDGE,lw=1.1,ls=dl)
    ax.plot([xC,xS],[y_rail,y_rail],color=EDGE,lw=1.1,ls=dl)
    ax.add_patch(FancyArrowPatch((xS,y_rail),(xS,y-G),arrowstyle="-|>",mutation_scale=4.5,
                 color=EDGE,lw=1.1,ls=dl,shrinkA=0,shrinkB=0,zorder=3))
    txt(ax,(xS+xC)/2,y_rail+3.8,"Feedback loop: personalized rest / stretch → re-measure",fs=8.2,it=True,bg="white")
    save(fig,"fig_arch.png")

# ---------- FIGURE 2: video-free boundary dataflow, figure* ----------
def fig_dataflow():
    fig,ax=newax(3.2,100)
    panels=[("Field\n(edge / browser)",[("Camera +\nMoveNet / YOLO",True),("Fire pixel analysis",True),("Wearable BLE\n(design)",False)]),
            ("Relay\n(message broker)",[("Event log\n(de-identified)",True),("Pseudonymous IDs",True),("119/SMS link\n(design)",False)]),
            ("Control center\n(web)",[("Multi-site monitoring",True),("Alerts / roll-call",True),("On-demand video\n(break-glass)",True)])]
    w=21; gap=15.5; x0=3; y=40; h=54
    xs=[x0+i*(w+gap) for i in range(3)]
    for i,(title,items) in enumerate(panels):
        x=xs[i]
        rect(ax,x,y,w,h,fc=GREY,lw=1.1)
        txt(ax,x+w/2,y+h-(8 if "\n" in title else 6),title,fs=7.8,bold=True)
        for j,(it,impl) in enumerate(items):
            cy=y+h-20-j*12
            bh=10.5 if "\n" in it else 8.5
            rect(ax,x+1.2,cy-bh/2,w-2.4,bh,fc=FILL,lw=0.9,ls=("-" if impl else "--"))
            txt(ax,x+w/2,cy,it,fs=6.7)
    ymid=y+h/2-4
    gx0=xs[0]+w; gx1=xs[1]
    arr(ax,gx0,ymid,gx1-G,ymid,lw=1.6)
    txt(ax,(gx0+gx1)/2,ymid+9.5,"17 skeleton\ncoords + events\n— NO pixels",fs=6.1,bold=True,bg="white")
    gx0=xs[1]+w; gx1=xs[2]; arr(ax,gx0,ymid,gx1-G,ymid,lw=1.6)
    txt(ax,(gx0+gx1)/2,ymid+6.5,"realtime push",fs=6.8,bg="white")
    rect(ax,6,10,88,17,fc=FILL,lw=1.0)
    ax.text(9,18.5,"During continuous monitoring no pixels (raw or anonymized) leave the site —\n"
                   "only de-identified skeleton coordinates and structured events. On-demand video\n"
                   "uses a consent-gated, time-limited (60 s), audit-logged 'break-glass' gate.",
            ha="left",va="center",ma="left",fontsize=7.2,color=TXT,zorder=5,linespacing=1.55)
    ax.plot([22,26],[3.2,3.2],color=EDGE,lw=1.6); ax.text(27.2,3.2,"implemented (see Table II)",fontsize=7.5,va="center")
    ax.plot([57,61],[3.2,3.2],color=EDGE,lw=1.0,ls="--"); ax.text(62.2,3.2,"design target",fontsize=7.5,va="center")
    save(fig,"fig_dataflow.png")

# ---------- FIGURE 3: operational workflow, LANDSCAPE redesign, figure* ----------
def aitag(ax,x,y):
    rect(ax,x,y,3.2,2.4,fc=EDGE,lw=0)
    ax.text(x+1.6,y+1.2,"AI",ha="center",va="center",fontsize=5.6,color="white",fontweight="bold",zorder=6)
def bc(ax,cx,cy,w,h,s,ai=False,design=False,fs=7.2,tdy=0):
    rect(ax,cx-w/2,cy-h/2,w,h,fc=("#f5f7fc" if design else FILL),lw=1.0,ls=("--" if design else "-"))
    txt(ax,cx,cy+tdy,s,fs=fs,color=(DGREY if design else TXT))
    if ai: aitag(ax,cx-w/2+1.2,cy+h/2-3.6)

def warr(ax,x1,y1,x2,y2,lw=1.0,ls="-"):
    """workflow 전용: 촉 MS(소형)·수축 0 — 촉 끝이 지정 좌표(테두리-G)에 정확히 위치"""
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=MS,
                 color=EDGE,lw=lw,ls=ls,shrinkA=0,shrinkB=0,zorder=3))

def fig_workflow():
    fig,ax=newax(4.6,64)
    dl=(0,(4,3))
    # ---- 레이아웃 상수 (F안 확정치) ----
    ww,wgap,sw,jw,dhw,dgap = 13.5,2.0,15.5,20.0,8.0,4.0
    wx=2+ww/2; wr=2+ww
    sx=wr+wgap+sw/2; sright=sx+sw/2; sleft=sx-sw/2
    jx=sright+2.0+jw/2; jleft=jx-jw/2; jright=jx+jw/2
    dcx=jright+2.0+dhw; dcy=33
    rxl=dcx+dhw+dgap; rw=min(25.0,99.5-rxl); rx=rxl+rw/2
    cm_y=32.0
    # ---- 범례 ----
    ax.plot([3,6.6],[62.4,62.4],color=EDGE,lw=1.7); ax.text(7.6,62.4,"implemented (see Table II)",fontsize=6.4,va="center")
    ax.plot([33,36.6],[62.4,62.4],color=EDGE,lw=1.0,ls="--"); ax.text(37.6,62.4,"design target",fontsize=6.4,va="center")
    ax.add_patch(Polygon([(53.5,63.6),(55,62.4),(53.5,61.2),(52,62.4)],closed=True,fc=FILL,ec=EDGE,lw=1.0))
    ax.text(56,62.4,"decision",fontsize=6.4,va="center")
    rect(ax,66,61.2,3.2,2.4,fc=EDGE,lw=0); ax.text(67.6,62.4,"AI",ha="center",va="center",fontsize=5.6,color="white",fontweight="bold")
    ax.text(70.4,62.4,"AI step",fontsize=6.4,va="center")
    # ---- 워커 ----
    bc(ax,wx,32,ww,9,"Worker on the\nshop floor",fs=6.4)
    # ---- 센서 열 + 분산 수렴 ----
    sense=[("Camera (edge AI)\nposture · fall\nhelmet / mask / vest",True,False,52,11.5,-1.2,38.5),
           ("Wearable vitals\nHR / temp",False,True,38.5,9.5,0,35.0),
           ("Self check-in\nsleep / fatigue / pain",False,False,25.5,9.5,0,31.0),
           ("Environment IoT\ngas / noise",False,True,12.5,9.5,0,27.5)]
    for s,ai,de,cy,sh,tdy,jy in sense:
        bc(ax,sx,cy,sw,sh,s,ai=ai,design=de,fs=5.5,tdy=tdy)
        warr(ax,wr,32,sleft-G,cy)                    # 워커 → 센서 (좌변-G)
        warr(ax,sright,cy,jleft-G,jy)                # 센서 → 판정 (좌변-G, 세로 분산 종점)
    # ---- 판정 ----
    bc(ax,jx,33,jw,15,"Risk judgement:\nfall state machine\n(benchmark-validated) +\nposture index (rule-based)",ai=True,fs=5.0,tdy=-1.0)
    txt(ax,jx,22.6,"+ open agent harness: PoC ·\ninterface-level · not evaluated",fs=5.4,it=True,color=DGREY)
    # ---- 마름모 ----
    ax.add_patch(Polygon([(dcx,dcy+7),(dcx+dhw,dcy),(dcx,dcy-7),(dcx-dhw,dcy)],closed=True,fc=FILL,ec=EDGE,lw=1.0,zorder=2))
    txt(ax,dcx,dcy,"Risk type?",fs=6.4); txt(ax,dcx,36.3,"normal",fs=5.8,it=True,bg="white")
    warr(ax,jright,33,dcx-dhw-G,33)
    # ---- 우측 결과 열 ----
    # 사슬 구간 틈 2.3(화살표: 몸통+촉+간격), 그룹 사이 1.3 / Continue=32(마름모 정렬)
    yA,yAl,yE,yH,yP,yC = 59.65,48.6,38.8,23.95,12.9,2.95
    bc(ax,rx,yA,rw,8,"Acute hazard\nfall / fire / gas",fs=6.4)
    bc(ax,rx,yAl,rw,9.5,"Alert + evacuation\n& roll-call + 119/e-Gen\n(design)",design=True,fs=5.9)
    bc(ax,rx,yE,rw,5.5,"Emergency resolved",fs=6.4)
    bc(ax,rx,cm_y,rw,5.5,"Continue monitoring",fs=6.4)
    bc(ax,rx,yH,rw,8,"Health / ergonomic risk\nhigh posture index / fatigue",fs=5.9)
    bc(ax,rx,yP,rw,9.5,"Personalized recovery\ncoaching (rest/stretch)",ai=True,design=True,fs=5.9,tdy=-1.1)
    bc(ax,rx,yC,rw,5.8,"Confirm done · log\nadherence (design)",design=True,fs=5.9)
    warr(ax,rx,yA-4.0,rx,yAl+4.75+G)   # Acute 하변(55.65) → Alert 상변(53.35)+G
    warr(ax,rx,yAl-4.75,rx,yE+2.75+G)  # Alert 하변(43.85) → Emergency 상변(41.55)+G
    warr(ax,rx,yH-4.0,rx,yP+4.75+G)    # Health 하변(19.95) → Personalized 상변(17.65)+G
    warr(ax,rx,yP-4.75,rx,yC+2.9+G)    # Personalized 하변(8.15) → Confirm 상변(5.85)+G
    # ---- 분기 (촉은 좌변-G에서 정지) ----
    warr(ax,dcx,dcy+7,rxl-G,yA)
    txt(ax,(dcx+rxl)/2-3.2,(dcy+7+yA)/2+0.4,"acute",fs=5.8,it=True,bg="white")
    warr(ax,dcx+dhw,dcy,rxl-G,cm_y,ls=dl)
    warr(ax,dcx,dcy-7,rxl-G,yH)
    txt(ax,(dcx+rxl)/2-1.2,(dcy-7+yH)/2-1.8,"cumulative",fs=5.8,it=True,bg="white")
    # ---- 피드백 루프 (워커 하변, 촉은 하변-G 아래에서 정지) ----
    ax.plot([rxl,wx],[yC,yC],color=EDGE,lw=1.0,ls=dl)
    ax.add_patch(FancyArrowPatch((wx,yC),(wx,27.5-G),arrowstyle="-|>",mutation_scale=MS,
                 color=EDGE,lw=1.0,ls=dl,shrinkA=0,shrinkB=0,zorder=3))
    txt(ax,52,5.4,"Closed feedback loop: re-measure & adapt",fs=6.2,it=True,bg="white")
    save(fig,"fig_workflow.png")

if __name__ == "__main__":
    fig_arch(); fig_dataflow(); fig_workflow()
    print("figures written to", OUT)
