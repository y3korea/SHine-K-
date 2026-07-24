# -*- coding: utf-8 -*-
"""SHine-K paper figures — clean academic block diagrams, 300 dpi.
   v2: overlap-free, publication quality (no line/text collisions). Set OUT to redirect output."""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon, Circle

EDGE="#1a1a1a"; FILL="#ffffff"; GREY="#eef1f6"; TXT="#000000"
OUT=os.environ.get("OUT","./figures"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":TXT,
    "axes.edgecolor":EDGE,"savefig.facecolor":"white"})

def rect(ax,x,y,w,h,fc=FILL,lw=1.0,ls="-"):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=EDGE,lw=lw,ls=ls,joinstyle="round"))
def txt(ax,x,y,s,fs=9,bold=False,it=False,ha="center",va="center",bg=None,color=TXT):
    bbox=dict(boxstyle="round,pad=0.2",fc=bg,ec="none") if bg else None
    ax.text(x,y,s,ha=ha,va=va,fontsize=fs,color=color,zorder=5,
            fontweight="bold" if bold else "normal",fontstyle="italic" if it else "normal",bbox=bbox)
def arr(ax,x1,y1,x2,y2,lw=1.1,ls="-"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=12,
                 color=EDGE,lw=lw,ls=ls,shrinkA=1,shrinkB=1,zorder=3))

def newax(w,h,ymax=100):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,100); ax.set_ylim(0,ymax); ax.axis("off")
    ax.set_aspect("auto"); fig.patch.set_facecolor("white"); return fig,ax

def save(fig,name):
    fig.savefig(f"{OUT}/{name}",dpi=300,bbox_inches="tight",pad_inches=0.06); plt.close(fig)

# ---------- Fig 1. Architecture (Sense -> Judge -> Act -> Connect) ----------
def fig1():
    fig,ax=newax(9,3.9)
    stages=[("SENSE",["Vision (MediaPipe/YOLO)","Radar (mmWave)","Wearable (BLE)","Thermal / IoT"]),
            ("JUDGE",["Fusion (multimodal)","Risk predictor (LSTM)","REBA (33 keypoints)"]),
            ("ACT",["Nudge (haptic)","Health feedback","Task / staffing"]),
            ("CONNECT",["Emergency 119/e-Gen","Evacuation, roll-call","Realtime (Supabase)"])]
    colw=22; gap=2; x0=3; y=16; H=74
    for i,(name,nodes) in enumerate(stages):
        x=x0+i*(colw+gap)
        rect(ax,x,y,colw,H,fc=GREY,lw=1.1)
        txt(ax,x+colw/2,y+H-7,name,fs=11,bold=True)
        top=y+H-15; bot=y+5; n=len(nodes); slot=(top-bot)/n
        for j,nd in enumerate(nodes):
            cy=top-slot*(j+0.5); bh=min(9,slot-2.5)
            rect(ax,x+1.5,cy-bh/2,colw-3,bh,fc=FILL,lw=0.9); txt(ax,x+colw/2,cy,nd,fs=6.8)
        if i<3: arr(ax,x+colw,y+H/2,x+colw+gap,y+H/2)
    xL=x0; xR=x0+3*(colw+gap)+colw; yb=7
    ax.plot([xR,xR],[y,yb],color=EDGE,lw=1.0); ax.plot([xL,xL],[yb,y],color=EDGE,lw=1.0)
    arr(ax,xR,yb,xL,yb)
    txt(ax,(xL+xR)/2,yb+3.0,"Feedback loop: personalized rest / stretch → re-measure",fs=7.6,it=True,bg="white")
    save(fig,"fig1_architecture.png")

# ---------- Fig 2. Web composition (modules) ----------
def fig2():
    fig,ax=newax(9,4.0)
    mods=[("(1) Landing","intro, KO/EN/ZH"),
          ("(2) Worksite Edge-AI","in-browser pose, events"),
          ("(3) Control Center","multi-site digital twin"),
          ("(4) Worker App (PWA)","check-in, evac., wearable"),
          ("(5) AI Posture (REBA)","BlazePose 33 keypoints"),
          ("(6) Site Camera","fire pixel analysis"),
          ("(7) Paper","manuscript")]
    cols=4; w=22.6; h=24; gx=2.0; gy=12; x0=2.6; y0=58
    for i,(t,s) in enumerate(mods):
        r=i//cols; c=i%cols; x=x0+c*(w+gx); y=y0-r*(h+gy)
        rect(ax,x,y,w,h,fc=FILL,lw=1.1)
        rect(ax,x,y+h-8,w,8,fc=GREY,lw=1.1)            # title band
        txt(ax,x+w/2,y+h-4,t,fs=7.6,bold=True)
        txt(ax,x+w/2,y+h/2-3,s,fs=6.9)
    save(fig,"fig2_system_overview.png")

# ---------- Fig 3. Edge-privacy dataflow — the image-free boundary (key differentiator) ----------
def fig3():
    fig,ax=newax(9,4.2)
    # (label, implemented?) — dashed = design target
    panels=[("Field (edge / browser)",[("Camera + MoveNet / YOLO",True),("Fire pixel analysis",True),("Wearable (BLE) — design",False)]),
            ("Cloud (Supabase)",[("Realtime DB (events)",True),("Auth, pseudonymized",True),("Edge fn (119 / SMS) — design",False)]),
            ("Control center (web)",[("Multi-site monitoring",True),("Alerts / roll-call",True),("On-demand video (break-glass)",True)])]
    w=24; gap=11; x0=3; y=44; h=48
    xs=[x0+i*(w+gap) for i in range(3)]
    for i,(title,items) in enumerate(panels):
        x=xs[i]
        rect(ax,x,y,w,h,fc=GREY,lw=1.1); txt(ax,x+w/2,y+h-6,title,fs=8.4,bold=True)
        for j,(it,impl) in enumerate(items):
            cy=y+h-16-j*10.5
            rect(ax,x+1.6,cy-4,w-3.2,8,fc=FILL,lw=0.9,ls=("-" if impl else "--")); txt(ax,x+w/2,cy,it,fs=6.7)
    ymid=y+h/2
    # bold image-free boundary on Field->Cloud
    gx0=xs[0]+w; gx1=xs[1]
    arr(ax,gx0,ymid,gx1,ymid,lw=2.2)
    txt(ax,(gx0+gx1)/2,ymid+7,"17 skeleton coords\n+ events — NO pixels",fs=6.3,bold=True,bg="white")
    gx0=xs[1]+w; gx1=xs[2]; arr(ax,gx0,ymid,gx1,ymid,lw=1.2); txt(ax,(gx0+gx1)/2,ymid+6,"realtime push",fs=6.6,bg="white")
    # caption
    rect(ax,6,8,88,20,fc=FILL,lw=1.0)
    txt(ax,50,18,"During continuous monitoring no pixels (raw or anonymized) leave the site — only\n"
                 "de-identified skeleton coordinates and structured events. On-demand video uses a\n"
                 "consent-gated, time-limited (60 s), audit-logged 'break-glass' gate.",fs=7.4)
    # legend
    ax.plot([20,24],[3.5,3.5],color=EDGE,lw=1.6); ax.text(25,3.5,"implemented (see Table II)",fontsize=6.4,va="center")
    ax.plot([55,59],[3.5,3.5],color=EDGE,lw=1.0,ls="--"); ax.text(60,3.5,"design target",fontsize=6.4,va="center")
    save(fig,"fig3_dataflow.png")

# ---------- Fig 4. Closed-loop algorithm workflow (graphical abstract) ----------
def aitag(ax,cx,cy,w,h):
    rect(ax,cx-w/2,cy+h/2-3.0,7.2,3.0,fc=EDGE,lw=0)
    ax.text(cx-w/2+3.6,cy+h/2-1.5,"AI",ha="center",va="center",fontsize=6,color="white",fontweight="bold",zorder=6)
def bc(ax,cx,cy,w,h,s,ai=False,design=False,fs=7.0,ty=None):
    rect(ax,cx-w/2,cy-h/2,w,h,fc=("#f5f7fc" if design else FILL),lw=1.0,ls=("--" if design else "-"))
    txt(ax,cx,(ty if ty is not None else cy),s,fs=fs,color=("#5a5f6b" if design else TXT))
    if ai: aitag(ax,cx,cy,w,h)
def diamond(ax,cx,cy,w,h,s,ai=False,fs=7.0):
    ax.add_patch(Polygon([(cx,cy+h/2),(cx+w/2,cy),(cx,cy-h/2),(cx-w/2,cy)],closed=True,
                 fc=(GREY if ai else FILL),ec=EDGE,lw=1.0,zorder=2))
    txt(ax,cx,cy,s,fs=fs)

def fig4():
    fig,ax=newax(9.2,11.6)
    dl=(0,(4,3))
    # --- legend: validated(solid) vs design-target(dashed) + decision + AI ---
    ax.plot([6,10],[97.9,97.9],color=EDGE,lw=1.7); ax.text(11,97.9,"implemented (see Table II)",fontsize=6.5,va="center")
    ax.plot([40,44],[97.9,97.9],color=EDGE,lw=1.0,ls="--"); ax.text(45,97.9,"design target",fontsize=6.5,va="center")
    ax.add_patch(Polygon([(63.5,99.2),(65,97.9),(63.5,96.6),(62,97.9)],closed=True,fc=FILL,ec=EDGE,lw=1.0))
    ax.text(66.5,97.9,"decision",fontsize=6.5,va="center")
    rect(ax,80,96.6,3,2.8,fc=EDGE,lw=0); ax.text(80+1.5,98,"AI",ha="center",va="center",fontsize=5.2,color="white",fontweight="bold")
    ax.text(84.5,97.9,"AI step",fontsize=6.5,va="center")
    # 1 worker
    bc(ax,50,90,30,5.5,"Worker on the shop floor")
    # 2 SENSE inputs (camera + self-check = implemented; wearable + environment = design target)
    sy=80; sx=[14,38,62,86]
    bc(ax,sx[0],sy,21.5,10,"Camera (edge AI)\nposture · fall\nhelmet / mask / vest",ai=True,fs=5.7,ty=79.2)
    bc(ax,sx[1],sy,21,10,"Wearable vitals\nHR / temp",design=True,fs=6.2)
    bc(ax,sx[2],sy,21,10,"Self check-in\nsleep / fatigue / pain",fs=6.2)
    bc(ax,sx[3],sy,21,10,"Environment IoT\ngas / noise",design=True,fs=6.2)
    for x in sx: arr(ax,50,87.25,x,sy+5.0)
    # 3 risk judgement — validated rule-based core + honest PoC note
    bc(ax,50,65,52,11,"Risk judgement: fall state machine (benchmark-validated) + posture index (rule-based)",ai=True,fs=6.6,ty=66.7)
    txt(ax,50,62.6,"+ open agent harness (Sense→Judge→Act→Connect): PoC · interface-level · not evaluated",fs=5.7,it=True,color="#6a6f7b")
    for x in sx: arr(ax,x,sy-5.0,50,70.5)
    # 4 decision
    diamond(ax,50,52,27,12,"Risk type?",fs=8); arr(ax,50,59.5,50,58)
    # left: acute hazard -> emergency
    bc(ax,18,40,30,9,"Acute hazard\nfall / fire / gas / asphyxia",fs=6.5)
    arr(ax,37,52,18,44.5); txt(ax,27,49,"acute",fs=6.5,it=True,bg="white")
    bc(ax,18,25,30,9,"Alert + evacuation & roll-call\n+ 119 / e-Gen (design target)",design=True,fs=6.4)
    arr(ax,18,35.5,18,29.5)
    bc(ax,18,12,30,6,"Emergency resolved",fs=6.6); arr(ax,18,20.5,18,15)
    # right: health/ergonomic risk -> recovery loop
    bc(ax,80,40,30,9,"Health / ergonomic risk\nhigh posture index / fatigue",fs=6.5)
    arr(ax,63,52,80,44.5); txt(ax,72.5,49,"cumulative",fs=6.5,it=True,bg="white")
    bc(ax,80,25,32,10,"Personalized recovery coaching\nrest / stretch (animated guide)",ai=True,fs=6.5)
    arr(ax,80,35.5,80,30)
    bc(ax,80,12,32,7,"Worker performs → confirm done\nlog adherence (design)",fs=6.4); arr(ax,80,20,80,15.5)
    # center: normal -> continue
    arr(ax,50,46,50,36,ls=dl); txt(ax,53.5,41,"normal",fs=6.5,it=True,bg="white")
    bc(ax,50,33,22,6,"Continue monitoring",fs=6.5)
    # closed feedback loop (dashed) up the clear right margin, back into the worker box
    ax.plot([80,80],[8.5,4.5],color=EDGE,lw=1.0,ls=dl)
    ax.plot([80,98],[4.5,4.5],color=EDGE,lw=1.0,ls=dl)
    ax.plot([98,98],[4.5,90],color=EDGE,lw=1.0,ls=dl)
    ax.add_patch(FancyArrowPatch((98,90),(65.5,90),arrowstyle="-|>",mutation_scale=12,color=EDGE,lw=1.0,ls=dl,zorder=3))
    txt(ax,42,1.6,"Closed feedback loop: re-measure & adapt",fs=7.0,it=True)
    save(fig,"fig4_workflow.png")

fig1(); fig2(); fig3(); fig4()
for f in ["fig1_architecture.png","fig2_system_overview.png","fig3_dataflow.png","fig4_workflow.png"]:
    print(f, os.path.getsize(f"{OUT}/{f}")//1024,"KB")
