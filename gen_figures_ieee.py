# -*- coding: utf-8 -*-
"""SHine-K IEEE Access figures v3 — drawn at FINAL PRINT SIZE (figure* = 7.16 in wide)
so in-figure text is >=6.5-7 pt in print (sample-paper convention: 70-100 % of body size)."""
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
def arr(ax,x1,y1,x2,y2,lw=1.1,ls="-"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=13,
                 color=EDGE,lw=lw,ls=ls,shrinkA=1,shrinkB=1,zorder=3))
def newax(h_in,ymax):
    fig,ax=plt.subplots(figsize=(W,h_in)); ax.set_xlim(0,100); ax.set_ylim(0,ymax); ax.axis("off")
    ax.set_aspect("auto"); fig.patch.set_facecolor("white"); return fig,ax
def save(fig,name):
    fig.savefig(f"{OUT}/{name}",dpi=300,bbox_inches="tight",pad_inches=0.05); plt.close(fig)
    print(name,"ok")

# ---------- FIGURE 1: architecture (Sense -> Judge -> Act -> Connect), figure* ----------
def fig_arch():
    fig,ax=newax(2.9,100)
    stages=[("SENSE",["Vision\n(MediaPipe / YOLO)","Radar (mmWave)","Wearable (BLE)","Thermal / IoT"]),
            ("JUDGE",["Fusion (multimodal)","Risk predictor (LSTM)","REBA (33 keypoints)"]),
            ("ACT",["Nudge (haptic)","Health feedback","Task / staffing"]),
            ("CONNECT",["Emergency\n119 / e-Gen","Evacuation, roll-call","Realtime events\n(broker)"])]
    colw=22; gap=2; x0=3; y=16; H=74
    for i,(name,nodes) in enumerate(stages):
        x=x0+i*(colw+gap)
        rect(ax,x,y,colw,H,fc=GREY,lw=1.1)
        txt(ax,x+colw/2,y+H-7,name,fs=10.5,bold=True)
        top=y+H-15; bot=y+5; n=len(nodes); slot=(top-bot)/n
        for j,nd in enumerate(nodes):
            cy=top-slot*(j+0.5); bh=min(12 if "\n" in nd else 10,slot-2)
            rect(ax,x+1.2,cy-bh/2,colw-2.4,bh,fc=FILL,lw=0.9); txt(ax,x+colw/2,cy,nd,fs=7.3)
        if i<3: arr(ax,x+colw,y+H/2,x+colw+gap,y+H/2,lw=1.3)
    xL=x0; xR=x0+3*(colw+gap)+colw; yb=6.5
    ax.plot([xR,xR],[y,yb],color=EDGE,lw=1.1); ax.plot([xL,xL],[yb,y],color=EDGE,lw=1.1)
    arr(ax,xR,yb,xL,yb,lw=1.1)
    txt(ax,(xL+xR)/2,yb+3.6,"Feedback loop: personalized rest / stretch → re-measure",fs=8.2,it=True,bg="white")
    save(fig,"fig_arch.png")

# ---------- FIGURE 2: video-free boundary dataflow, figure* ----------
def fig_dataflow():
    fig,ax=newax(3.2,100)
    panels=[("Field\n(edge / browser)",[("Camera +\nMoveNet / YOLO",True),("Fire pixel analysis",True),("Wearable BLE — design",False)]),
            ("Relay\n(message broker)",[("Event log\n(de-identified)",True),("Pseudonymous IDs",True),("119/SMS link — design",False)]),
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
    arr(ax,gx0,ymid,gx1,ymid,lw=1.6)
    txt(ax,(gx0+gx1)/2,ymid+9.5,"17 skeleton\ncoords + events\n— NO pixels",fs=6.5,bold=True,bg="white")
    gx0=xs[1]+w; gx1=xs[2]; arr(ax,gx0,ymid,gx1,ymid,lw=1.6)
    txt(ax,(gx0+gx1)/2,ymid+6.5,"realtime push",fs=6.8,bg="white")
    rect(ax,6,8,88,21,fc=FILL,lw=1.0)
    txt(ax,50,18.5,"During continuous monitoring no pixels (raw or anonymized) leave the site — only de-identified\n"
                   "skeleton coordinates and structured events. On-demand video uses a consent-gated,\n"
                   "time-limited (60 s), audit-logged 'break-glass' gate.",fs=7.7)
    ax.plot([22,26],[3.2,3.2],color=EDGE,lw=1.6); ax.text(27.2,3.2,"implemented / validated",fontsize=7.5,va="center")
    ax.plot([57,61],[3.2,3.2],color=EDGE,lw=1.0,ls="--"); ax.text(62.2,3.2,"design target",fontsize=7.5,va="center")
    save(fig,"fig_dataflow.png")

# ---------- FIGURE 3: operational workflow, LANDSCAPE redesign, figure* ----------
def aitag(ax,x,y):
    rect(ax,x,y-1.6,4.6,3.2,fc=EDGE,lw=0)
    ax.text(x+2.3,y,"AI",ha="center",va="center",fontsize=6.8,color="white",fontweight="bold",zorder=6)
def bc(ax,cx,cy,w,h,s,ai=False,design=False,fs=7.2,tdy=0):
    rect(ax,cx-w/2,cy-h/2,w,h,fc=("#f5f7fc" if design else FILL),lw=1.0,ls=("--" if design else "-"))
    txt(ax,cx,cy+tdy,s,fs=fs,color=(DGREY if design else TXT))
    if ai: aitag(ax,cx-w/2+2.9,cy+h/2-2.1)

def fig_workflow():
    fig,ax=newax(4.6,64)
    dl=(0,(4,3))
    # legend (top strip)
    ax.plot([3,6.6],[62.4,62.4],color=EDGE,lw=1.7); ax.text(7.6,62.4,"implemented / validated",fontsize=7.4,va="center")
    ax.plot([33,36.6],[62.4,62.4],color=EDGE,lw=1.0,ls="--"); ax.text(37.6,62.4,"design target",fontsize=7.4,va="center")
    ax.add_patch(Polygon([(53.5,63.6),(55,62.4),(53.5,61.2),(52,62.4)],closed=True,fc=FILL,ec=EDGE,lw=1.0))
    ax.text(56,62.4,"decision",fontsize=7.4,va="center")
    rect(ax,66,61.1,3.4,2.6,fc=EDGE,lw=0); ax.text(67.7,62.4,"AI",ha="center",va="center",fontsize=6.2,color="white",fontweight="bold")
    ax.text(70.4,62.4,"AI step",fontsize=7.4,va="center")
    # worker (left)
    bc(ax,10,32,16,9,"Worker on the\nshop floor",fs=7.6)
    # sense column (4 stacked)
    sx=32; sw=22
    sense=[("Camera (edge AI)\nposture · fall · caught-in\nhelmet / mask / vest",True,False,52,11.5,-1.2),
           ("Wearable vitals\nHR / temp",False,True,38.5,9.5,0),
           ("Self check-in\nsleep / fatigue / pain",False,False,25.5,9.5,0),
           ("Environment IoT\ngas / noise",False,True,12.5,9.5,0)]
    for s,ai,de,cy,sh,tdy in sense:
        bc(ax,sx,cy,sw,sh,s,ai=ai,design=de,fs=6.8,tdy=tdy)
        arr(ax,18,32,sx-sw/2,cy,lw=1.0)
        arr(ax,sx+sw/2,cy,45,33,lw=1.0)
    # risk judgement (center)
    bc(ax,57,33,24,15,"Risk judgement:\nfall state machine + REBA\n(rule-based, validated)",ai=True,fs=7.1,tdy=-1.0)
    txt(ax,57,22.6,"+ open agent harness: PoC ·\ninterface-level · not evaluated",fs=6.5,it=True,color=DGREY)
    # decision diamond
    dcx,dcy=76.5,33
    ax.add_patch(Polygon([(dcx,dcy+7),(dcx+5.5,dcy),(dcx,dcy-7),(dcx-5.5,dcy)],closed=True,fc=FILL,ec=EDGE,lw=1.0,zorder=2))
    txt(ax,dcx,dcy,"Risk\ntype?",fs=7.3)
    arr(ax,69,33,dcx-5.5,33,lw=1.1)
    # right outcome column
    rx=90.5; rw=18
    bc(ax,rx,57.5,rw,8,"Acute hazard\nfall / fire / gas",fs=6.9)
    bc(ax,rx,47,rw,9.5,"Alert + evacuation\n& roll-call + 119/e-Gen\n(design)",design=True,fs=6.1)
    bc(ax,rx,38.5,rw,5.5,"Emergency resolved",fs=6.7)
    bc(ax,rx,30.5,rw,5.5,"Continue monitoring",fs=6.7)
    bc(ax,rx,22.5,rw,8,"Health / ergonomic risk\nhigh REBA / fatigue",fs=6.4)
    bc(ax,rx,12,rw,9.5,"Personalized recovery\ncoaching (rest/stretch)",ai=True,fs=6.4,tdy=-1.2)
    bc(ax,rx,2.9,rw,5.8,"Confirm done · log\nadherence (design)",fs=6.5)
    arr(ax,rx,53.5,rx,51.75,lw=1.0); arr(ax,rx,42.25,rx,41.25,lw=1.0)
    arr(ax,rx,18.5,rx,16.75,lw=1.0); arr(ax,rx,7.25,rx,5.8,lw=1.0)
    # branch connectors from diamond
    arr(ax,dcx,dcy+7,rx-rw/2,57.5,lw=1.0); txt(ax,75.5,47.5,"acute",fs=6.9,it=True,bg="white")
    arr(ax,dcx+5.5,dcy,rx-rw/2,30.5,lw=1.0,ls=dl); txt(ax,79,36.2,"normal",fs=6.9,it=True,bg="white")
    arr(ax,dcx,dcy-7,rx-rw/2,22.5,lw=1.0); txt(ax,75,18.3,"cumulative",fs=6.9,it=True,bg="white")
    # closed feedback loop: recovery chain -> back to worker (dashed, along bottom)
    ax.plot([rx-rw/2,10],[2.9,2.9],color=EDGE,lw=1.0,ls=dl)
    ax.add_patch(FancyArrowPatch((10,2.9),(10,27.5),arrowstyle="-|>",mutation_scale=13,color=EDGE,lw=1.0,ls=dl,zorder=3))
    txt(ax,55,5.4,"Closed feedback loop: re-measure & adapt",fs=7.2,it=True,bg="white")
    save(fig,"fig_workflow.png")

fig_arch(); fig_dataflow(); fig_workflow()
