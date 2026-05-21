from __future__ import annotations
"""
FootballIQ Premium v3 — Single-file Streamlit platform.
DEPLOY: Push ONLY this file + requirements.txt to GitHub.
        Add API_KEY in Streamlit Cloud → Settings → Secrets.
Zero local imports. No module errors. Ever.
"""

import os, requests, streamlit as st
from datetime import datetime, timezone

# ╔══════════════════════════════════════════════════════════════╗
# ║  0.  PAGE CONFIG  — must be very first Streamlit call       ║
# ╚══════════════════════════════════════════════════════════════╝
st.set_page_config(
    page_title="FootballIQ — AI Predictions",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ╔══════════════════════════════════════════════════════════════╗
# ║  1.  PREMIUM CSS                                            ║
# ╚══════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* ── Layout ─────────────────────────────────────────────── */
.block-container {
    padding: 0 1rem 6rem !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* ── HERO BANNER ─────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg,#03080f 0%,#071020 50%,#03080f 100%);
    border: 1px solid rgba(59,130,246,.2);
    border-radius: 24px;
    padding: 1.8rem 2rem;
    margin: .6rem 0 1.6rem;
    display: flex; align-items: center; gap: 20px;
    box-shadow: 0 0 80px rgba(59,130,246,.07), 0 12px 40px rgba(0,0,0,.6);
    position: relative; overflow: hidden;
}
.hero::before {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse 60% 80% at 80% 50%,rgba(59,130,246,.08),transparent);
    pointer-events:none;
}
.hero-ball {
    width:78px; height:78px; border-radius:20px; flex-shrink:0;
    background: linear-gradient(145deg,#1a3a6b,#2563eb,#3b82f6);
    display:flex; align-items:center; justify-content:center;
    font-size:42px; line-height:1;
    box-shadow: 0 8px 28px rgba(37,99,235,.5);
}
.hero-title { font-size:30px; font-weight:900; letter-spacing:-.8px;
    background:linear-gradient(90deg,#60a5fa 0%,#93c5fd 50%,#dbeafe 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-sub { font-size:13px; color:#475569; margin-top:5px; }
.hero-live {
    margin-left:auto; flex-shrink:0;
    display:flex; align-items:center; gap:7px;
    background:rgba(34,197,94,.08); border:1px solid rgba(34,197,94,.25);
    color:#4ade80; font-size:11px; font-weight:700; letter-spacing:.08em;
    padding:6px 14px; border-radius:20px;
}
.ldot { width:7px; height:7px; background:#22c55e; border-radius:50%;
    box-shadow:0 0 6px #22c55e; animation:blink 1.6s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.25;transform:scale(.7)} }

/* ── SECTION TITLE ──────────────────────────────────────── */
.stitle {
    font-size:14px; font-weight:700; color:#94a3b8;
    letter-spacing:.06em; text-transform:uppercase;
    display:flex; align-items:center; gap:10px;
    margin: 1.4rem 0 .9rem;
}
.stitle::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg,rgba(148,163,184,.2),transparent);
}

/* ── METRICS ROW ────────────────────────────────────────── */
.metrics {
    display:grid; grid-template-columns:repeat(4,1fr); gap:10px;
    margin-bottom:1rem;
}
.mbox {
    background:rgba(255,255,255,.025);
    border:1px solid rgba(255,255,255,.06);
    border-radius:16px; padding:1rem 1.1rem; text-align:center;
}
.mval { font-size:26px; font-weight:900; color:#f1f5f9; }
.mlbl { font-size:11px; color:#64748b; margin-top:3px; }
.msub { font-size:10px; color:#475569; margin-top:2px; }

/* ── HIGHLIGHTS STRIP ───────────────────────────────────── */
.hl-strip {
    display:grid; grid-template-columns:repeat(3,1fr); gap:10px;
    margin-bottom:.8rem;
}
.hl {
    border-radius:16px; padding:1rem 1.1rem;
    background:rgba(255,255,255,.025);
    border:1px solid rgba(255,255,255,.06);
}
.hl.hot  { background:rgba(239,68,68,.06);  border-color:rgba(239,68,68,.2); }
.hl.cold { background:rgba(99,102,241,.06); border-color:rgba(99,102,241,.2); }
.hl.botd { background:rgba(251,191,36,.06); border-color:rgba(251,191,36,.2); }
.hl-lbl { font-size:10px; font-weight:700; letter-spacing:.08em;
    text-transform:uppercase; color:#64748b; margin-bottom:6px; }
.hl.hot  .hl-lbl { color:#f87171; }
.hl.cold .hl-lbl { color:#818cf8; }
.hl.botd .hl-lbl { color:#fbbf24; }
.hl-name { font-size:14px; font-weight:700; color:#e2e8f0; }
.hl-sub  { font-size:12px; color:#64748b; margin-top:3px; }

/* ── TOP-3 GRID ─────────────────────────────────────────── */
.top3 {
    display:grid; grid-template-columns:repeat(3,1fr); gap:10px;
    margin-bottom:1rem;
}
.t3card {
    background:linear-gradient(155deg,#0b1e3d,#102848);
    border:1px solid rgba(59,130,246,.2);
    border-radius:20px; padding:1.2rem 1.1rem;
    position:relative; overflow:hidden;
    box-shadow:0 6px 24px rgba(0,0,0,.4);
}
.t3card::after {
    content:''; position:absolute; bottom:-24px; right:-24px;
    width:90px; height:90px; border-radius:50%;
    background:radial-gradient(circle,rgba(59,130,246,.12),transparent);
    pointer-events:none;
}
.t3medal { font-size:28px; margin-bottom:8px; }
.t3teams { font-size:12px; font-weight:700; color:#e2e8f0;
    line-height:1.5; margin-bottom:5px; }
.t3meta  { font-size:10px; color:#475569; margin-bottom:10px; }
.t3bet   { font-size:11px; color:#93c5fd; margin-top:7px; }

/* ── PREDICTION CARD ────────────────────────────────────── */
.pcard {
    background:rgba(12,20,35,.95);
    border:1px solid rgba(255,255,255,.07);
    border-radius:22px; padding:1.4rem 1.5rem;
    margin-bottom:1.1rem;
    box-shadow:0 4px 28px rgba(0,0,0,.45);
    transition:border-color .3s, box-shadow .3s;
}
.pcard:hover { border-color:rgba(59,130,246,.28); box-shadow:0 8px 36px rgba(0,0,0,.5); }
.pcard.flagged { border-color:rgba(251,191,36,.35); box-shadow:0 4px 24px rgba(251,191,36,.08); }

.phdr { display:flex; justify-content:space-between; align-items:flex-start;
    gap:12px; margin-bottom:12px; }
.pvs  { font-size:17px; font-weight:800; color:#f1f5f9; line-height:1.35; }
.pvs-mid { color:#475569; font-weight:500; }
.ptag {
    display:inline-block; margin-left:8px; vertical-align:middle;
    background:linear-gradient(90deg,#b45309,#dc2626);
    color:#fff; font-size:9px; font-weight:800; letter-spacing:.06em;
    padding:2px 9px; border-radius:20px; text-transform:uppercase;
}
.pmeta { font-size:11px; color:#475569; margin-top:3px; }

/* ── FORM DOTS ──────────────────────────────────────────── */
.frow { display:flex; align-items:center; gap:8px; margin:5px 0; }
.flbl { font-size:11px; color:#475569; width:90px; flex-shrink:0;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.fdots { display:flex; gap:5px; }
.fd {
    width:20px; height:20px; border-radius:50%;
    font-size:9px; font-weight:700;
    display:flex; align-items:center; justify-content:center;
    flex-shrink:0; letter-spacing:0;
}
.fd.W { background:#16a34a; color:#fff; box-shadow:0 2px 6px rgba(22,163,74,.4); }
.fd.D { background:#a16207; color:#fff; box-shadow:0 2px 6px rgba(161,98,7,.3); }
.fd.L { background:#b91c1c; color:#fff; box-shadow:0 2px 6px rgba(185,28,28,.4); }
.fd.N { background:rgba(255,255,255,.07); color:#475569; }

/* ── CONFIDENCE METER ───────────────────────────────────── */
.cmeter { margin:12px 0 8px; }
.cmeter-hdr { display:flex; justify-content:space-between;
    align-items:center; margin-bottom:5px; }
.cmeter-lbl { font-size:12px; color:#64748b; }
.ctrack { width:100%; height:7px; background:rgba(255,255,255,.06);
    border-radius:6px; overflow:hidden; }
.cfill  { height:100%; border-radius:6px; }

/* ── CONFIDENCE BADGE ───────────────────────────────────── */
.cbadge {
    display:inline-flex; align-items:center; gap:5px;
    padding:4px 13px; border-radius:20px;
    font-size:11px; font-weight:800; letter-spacing:.04em;
}
.cb-vh { background:#052e16; color:#4ade80; border:1px solid #166534; }
.cb-hi { background:#1a2e05; color:#a3e635; border:1px solid #4d7c0f; }
.cb-md { background:#431407; color:#fb923c; border:1px solid #c2410c; }
.cb-lo { background:#450a0a; color:#f87171; border:1px solid #991b1b; }

/* ── STAT BOXES ─────────────────────────────────────────── */
.srow { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:10px 0; }
.sbox {
    background:rgba(255,255,255,.025);
    border:1px solid rgba(255,255,255,.055);
    border-radius:14px; padding:10px 8px; text-align:center;
}
.sv { font-size:20px; font-weight:800; color:#e2e8f0; }
.sl { font-size:10px; color:#64748b; margin-top:3px; line-height:1.3; }

/* ── PILLS ──────────────────────────────────────────────── */
.pills { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; }
.pill {
    display:inline-flex; align-items:center; gap:4px;
    font-size:11px; font-weight:600;
    padding:4px 12px; border-radius:20px;
}
.p-bet  { background:rgba(59,130,246,.13); color:#93c5fd;
    border:1px solid rgba(59,130,246,.22); }
.p-safe { background:rgba(34,197,94,.1);  color:#4ade80;
    border:1px solid rgba(34,197,94,.2); }
.p-warn { background:rgba(239,68,68,.1);  color:#fca5a5;
    border:1px solid rgba(239,68,68,.2); }
.p-hot  { background:rgba(251,146,60,.1); color:#fdba74;
    border:1px solid rgba(251,146,60,.2); }

/* ── FLAGGED BANNER ─────────────────────────────────────── */
.fbanner {
    display:flex; align-items:center; gap:10px;
    background:linear-gradient(90deg,rgba(251,191,36,.1),rgba(239,68,68,.08));
    border:1px solid rgba(251,191,36,.28);
    border-radius:14px; padding:.8rem 1.1rem; margin-bottom:.8rem;
    font-size:13px; color:#fde68a; font-weight:600;
}

/* ── WHY BOX ────────────────────────────────────────────── */
.why {
    background:rgba(255,255,255,.02);
    border-left:3px solid #3b82f6;
    border-radius:0 12px 12px 0;
    padding:.9rem 1.1rem; margin:8px 0;
    font-size:13px; color:#94a3b8;
    line-height:1.75; font-style:italic;
}
.bdr { display:flex; align-items:center; gap:10px; margin:5px 0; }
.bdr-l { font-size:12px; color:#64748b; flex:0 0 175px; }
.bdr-t { flex:1; height:6px; background:rgba(255,255,255,.05);
    border-radius:4px; overflow:hidden; }
.bdr-f { height:100%; border-radius:4px;
    background:linear-gradient(90deg,#1d4ed8,#3b82f6); }
.bdr-p { font-size:12px; color:#60a5fa; font-weight:700;
    flex:0 0 30px; text-align:right; }

/* ── DANGER MATCHES ─────────────────────────────────────── */
.danger-card {
    background:rgba(239,68,68,.05);
    border:1px solid rgba(239,68,68,.2);
    border-radius:16px; padding:.9rem 1.1rem; margin-bottom:.7rem;
    display:flex; justify-content:space-between; align-items:center; gap:8px;
}
.danger-match { font-size:13px; font-weight:700; color:#e2e8f0; }
.danger-why   { font-size:11px; color:#f87171; margin-top:3px; }

/* ── LOAD BUTTON ────────────────────────────────────────── */
.stButton > button {
    background:linear-gradient(135deg,#1d4ed8,#2563eb,#3b82f6) !important;
    color:#fff !important; border:none !important;
    border-radius:14px !important; font-weight:700 !important;
    font-size:15px !important; padding:.75rem 1.6rem !important;
    width:100% !important;
    box-shadow:0 4px 20px rgba(37,99,235,.4) !important;
}
.stButton > button:hover { opacity:.87 !important; }

/* ── HR DIVIDER ─────────────────────────────────────────── */
.hd { border:none; border-top:1px solid rgba(255,255,255,.06); margin:.9rem 0; }

/* ── EMPTY / WELCOME ────────────────────────────────────── */
.welcome { text-align:center; padding:2.5rem 1rem 1.5rem; }
.welcome .emoji { font-size:60px; margin-bottom:1rem; }
.welcome h2 { font-size:22px; color:#f1f5f9; margin-bottom:.5rem; }
.welcome p  { font-size:14px; color:#64748b; max-width:420px; margin:0 auto 1.5rem; }
.feat-grid  { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:.8rem 0; }
.fcard {
    background:rgba(255,255,255,.025);
    border:1px solid rgba(255,255,255,.06);
    border-radius:16px; padding:1.1rem;
}
.fcard-icon  { font-size:26px; margin-bottom:7px; }
.fcard-title { font-size:13px; font-weight:700; color:#e2e8f0; margin-bottom:4px; }
.fcard-desc  { font-size:11px; color:#64748b; line-height:1.55; }

/* ── EXPANDER ───────────────────────────────────────────── */
details { border:1px solid rgba(255,255,255,.07) !important;
    border-radius:14px !important; overflow:hidden; }
details summary { padding:.7rem 1rem !important; font-weight:600 !important;
    color:#93c5fd !important; cursor:pointer; }

/* ── KEY ERROR ──────────────────────────────────────────── */
.key-err {
    background:rgba(239,68,68,.07); border:1px solid rgba(239,68,68,.2);
    border-radius:16px; padding:1.4rem 1.6rem; text-align:center;
}

/* ════════════ MOBILE ════════════════════════════════════ */
@media (max-width:660px) {
    .block-container { padding:0 .5rem 5rem !important; }
    .hero { padding:1.1rem; gap:12px; }
    .hero-ball { width:56px; height:56px; font-size:30px; border-radius:14px; }
    .hero-title { font-size:20px; }
    .hero-live  { display:none; }
    .metrics    { grid-template-columns:repeat(2,1fr); }
    .hl-strip   { grid-template-columns:1fr; }
    .top3       { grid-template-columns:1fr; }
    .srow       { grid-template-columns:repeat(2,1fr); }
    .feat-grid  { grid-template-columns:repeat(2,1fr); }
    .bdr-l      { flex:0 0 120px; font-size:11px; }
    .pvs        { font-size:14px; }
}
@media (max-width:380px) {
    .feat-grid { grid-template-columns:1fr; }
    .metrics   { grid-template-columns:1fr 1fr; }
}
</style>
""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  2.  CONSTANTS                                              ║
# ╚══════════════════════════════════════════════════════════════╝
BASE = "https://api.football-data.org/v4"
MAX  = 20

LEAGUES = {
    "PL":  "🏴 Premier League",
    "PD":  "🇪🇸 La Liga",
    "BL1": "🇩🇪 Bundesliga",
    "SA":  "🇮🇹 Serie A",
    "FL1": "🇫🇷 Ligue 1",
    "CL":  "🌍 Champions League",
    "ELC": "🏴 Championship",
    "WC":  "🌍 World Cup",
    "EC":  "🌍 Euros",
}

# ╔══════════════════════════════════════════════════════════════╗
# ║  3.  API LAYER                                              ║
# ╚══════════════════════════════════════════════════════════════╝
def _key():
    try:    return st.secrets["API_KEY"]
    except: return os.getenv("API_KEY","")

def _h(): return {"X-Auth-Token":_key()}

def _get(url):
    try:
        r = requests.get(url,headers=_h(),timeout=12)
        if r.status_code==200:   return r.json()
        if r.status_code==429:   st.warning("⏳ Rate limit — wait 60 s.")
        elif r.status_code==403: st.error("🔑 API key invalid / plan restriction.")
        elif r.status_code!=404: st.warning(f"API {r.status_code}")
    except requests.Timeout:         st.warning("⌛ Timed out.")
    except requests.ConnectionError: st.warning("📡 No connection.")
    except Exception as e:           st.warning(f"Error: {e}")
    return None

@st.cache_data(ttl=1800,show_spinner=False)
def api_fixtures(lg): return (_get(f"{BASE}/competitions/{lg}/matches?status=SCHEDULED") or {}).get("matches",[])

@st.cache_data(ttl=1800,show_spinner=False)
def api_tm(tid,n=10): return (_get(f"{BASE}/teams/{tid}/matches?status=FINISHED&limit={n}") or {}).get("matches",[])

@st.cache_data(ttl=3600,show_spinner=False)
def api_table(lg):
    d=_get(f"{BASE}/competitions/{lg}/standings")
    try:    return (d or {})["standings"][0]["table"]
    except: return []

@st.cache_data(ttl=1800,show_spinner=False)
def api_h2h(mid): return (_get(f"{BASE}/matches/{mid}/head2head?limit=5") or {}).get("matches",[])

@st.cache_data(ttl=86400,show_spinner=False)
def api_ok(): return _get(f"{BASE}/competitions/PL") is not None

# ╔══════════════════════════════════════════════════════════════╗
# ║  4.  UTILITIES                                              ║
# ╚══════════════════════════════════════════════════════════════╝
def trunc(s,n=20): return s if len(s)<=n else s[:n-1]+"…"

def ordinal(n):
    sfx={1:"st",2:"nd",3:"rd"}.get(n%10 if n%100 not in (11,12,13) else 0,"th")
    return f"{n}{sfx}"

def cd(utc):
    try:
        dt=datetime.fromisoformat(utc.replace("Z","+00:00"))
        now=datetime.now(timezone.utc); df=dt-now
        if df.total_seconds()<0: return "Kicked off"
        d,h=df.days,int(df.total_seconds()//3600)%24
        if d==0: return f"Today · in {h}h"
        if d==1: return f"Tomorrow {dt.strftime('%H:%M')} UTC"
        return f"In {d}d {h}h · {dt.strftime('%d %b')}"
    except: return utc[:10] if utc else "TBD"

def cmeta(sc):
    """(label, bar_color, badge_class)"""
    if sc>=78: return "Very High","#22c55e","cb-vh"
    if sc>=58: return "High",     "#84cc16","cb-hi"
    if sc>=38: return "Medium",   "#f59e0b","cb-md"
    return "Low","#ef4444","cb-lo"

def badge(sc):
    l,_,c=cmeta(sc)
    return f'<span class="cbadge {c}">{l} · {sc}%</span>'

def meter(sc):
    _,col,_=cmeta(sc)
    return (f'<div class="cmeter">'
            f'<div class="cmeter-hdr">'
            f'<span class="cmeter-lbl">Prediction confidence</span>'
            f'{badge(sc)}'
            f'</div>'
            f'<div class="ctrack"><div class="cfill" style="width:{sc}%;background:{col}"></div></div>'
            f'</div>')

def form_dots(results,label):
    dots=""
    for r in results:
        c={"win":"W","draw":"D","loss":"L"}.get(r,"N")
        dots+=f'<div class="fd {c}">{c}</div>'
    for _ in range(5-len(results)):
        dots+='<div class="fd N">·</div>'
    return (f'<div class="frow">'
            f'<span class="flbl">{label}</span>'
            f'<div class="fdots">{dots}</div>'
            f'</div>')

def alert(p):
    return (f"⚽ {p['home']} vs {p['away']}\n"
            f"🏆 {p['league']}\n"
            f"📊 Confidence: {p['conf']}% ({p['lbl']})\n"
            f"✅ Best bet: {p['best_bet']}\n"
            f"⏰ {cd(p.get('date',''))}\n"
            f"💡 {p.get('expl','')}")

# ╔══════════════════════════════════════════════════════════════╗
# ║  5.  PREDICTION ENGINE                                      ║
# ╚══════════════════════════════════════════════════════════════╝

# ── 5a. Form analysis ─────────────────────────────────────────
def _vb(): return {"p":0,"w":0,"d":0,"l":0,"gf":0,"ga":0}

def _ef():
    return {"p":0,"w":0,"d":0,"l":0,"gf":0,"ga":0,"gd":0,
            "cs":0,"streak":0,"five":False,"agf":0.,"aga":0.,
            "form":[],"home":_vb(),"away":_vb()}

def form(tid):
    ms=api_tm(tid,10)
    if not ms: return _ef()
    s=_ef(); f5=[]; sk=0
    for m in ms:
        ih=m["homeTeam"]["id"]==tid
        mg=m["score"]["fullTime"].get("home" if ih else "away") or 0
        og=m["score"]["fullTime"].get("away" if ih else "home") or 0
        w =m["score"].get("winner","")
        if   w=="HOME_TEAM": res="win"  if ih else "loss"
        elif w=="AWAY_TEAM": res="loss" if ih else "win"
        elif w=="DRAW":      res="draw"
        else:                res="unknown"
        s["p"]+=1; s["gf"]+=mg; s["ga"]+=og
        if res=="win":    s["w"]+=1; sk+=1
        elif res=="draw": s["d"]+=1; sk=0
        elif res=="loss": s["l"]+=1; sk=0
        if og==0: s["cs"]+=1
        v=s["home"] if ih else s["away"]
        v["p"]+=1; v["gf"]+=mg; v["ga"]+=og
        if res=="win":    v["w"]+=1
        elif res=="draw": v["d"]+=1
        elif res=="loss": v["l"]+=1
        if len(f5)<5: f5.append(res)
    s["streak"]=sk; s["form"]=list(reversed(f5))
    s["gd"]=s["gf"]-s["ga"]
    s["agf"]=round(s["gf"]/max(s["p"],1),2)
    s["aga"]=round(s["ga"]/max(s["p"],1),2)
    s["five"]=_5w(ms,tid)
    return s

def _5w(ms,tid):
    if len(ms)<5: return False
    return all(
        (m["score"]["winner"]=="HOME_TEAM" and m["homeTeam"]["id"]==tid) or
        (m["score"]["winner"]=="AWAY_TEAM" and m["awayTeam"]["id"]==tid)
        for m in ms[:5])

# ── 5b. Standing ──────────────────────────────────────────────
def standing(tid,lg):
    for r in api_table(lg):
        if r.get("team",{}).get("id")==tid:
            return {"pos":r.get("position"),"pts":r.get("points"),
                    "gd":r.get("goalDifference"),"pl":r.get("playedGames")}
    return None

# ── 5c. H2H ───────────────────────────────────────────────────
def h2h(mid,fid):
    out={"p":0,"w":0,"d":0,"l":0,"rows":[]}
    for m in api_h2h(mid):
        ih=m["homeTeam"]["id"]==fid
        w =m["score"].get("winner","DRAW")
        out["p"]+=1
        if w=="DRAW":                                                res="draw";out["d"]+=1
        elif (w=="HOME_TEAM" and ih) or (w=="AWAY_TEAM" and not ih):res="win"; out["w"]+=1
        else:                                                        res="loss";out["l"]+=1
        out["rows"].append({
            "date":m.get("utcDate","")[:10],
            "home":m["homeTeam"]["name"],"away":m["awayTeam"]["name"],
            "score":f"{m['score']['fullTime']['home']}–{m['score']['fullTime']['away']}",
            "res":res})
    return out

# ── 5d. Confidence scoring (9 factors, max 100) ───────────────
def confidence(hf,af,hs,as_,hh,odds):
    sc=0; bd={}

    # Streak (max 25)
    if hf.get("five"):                          sc+=25;bd["5-game winning streak"]=25
    elif hf.get("streak",0)>=3:
        pt=8+(hf["streak"]-3)*3                 ;sc+=pt;bd[f"{hf['streak']}-game win streak"]=pt

    # Opponent away weakness (max 20)
    aw=af.get("away",{}); awr=aw.get("w",0)/max(aw.get("p",1),1)
    if   awr<=.20 and aw.get("p",0)>=3: sc+=20;bd["Opponent terrible away form"]=20
    elif awr<=.35 and aw.get("p",0)>=3: sc+=12;bd["Opponent weak away record"]=12

    # Home form strength (max 15)
    hw=hf.get("home",{}); hwr=hw.get("w",0)/max(hw.get("p",1),1)
    if   hwr>=.75 and hw.get("p",0)>=3: sc+=15;bd["Dominant home form (75%+ WR)"]=15
    elif hwr>=.55 and hw.get("p",0)>=3: sc+=9; bd["Good home record"]=9

    # Goalscoring output (max 15)
    if   hf.get("agf",0)>=2.8: sc+=15;bd["Elite attack (2.8+ goals/g)"]=15
    elif hf.get("agf",0)>=2.0: sc+=9; bd["Strong goalscoring form"]=9
    elif hf.get("agf",0)>=1.4: sc+=4; bd["Decent attack"]=4

    # Defensive solidity (max 10)
    if   hf.get("cs",0)>=4: sc+=10;bd["Excellent defence (4+ clean sheets)"]=10
    elif hf.get("cs",0)>=2: sc+=6; bd["Solid defence (2+ clean sheets)"]=6
    elif hf.get("cs",0)>=1: sc+=2; bd["Some defensive solidity"]=2

    # H2H dominance (max 10)
    if   hh.get("w",0)>=4 and hh.get("p",0)>=4: sc+=10;bd["H2H dominance"]=10
    elif hh.get("w",0)>=3 and hh.get("p",0)>=3: sc+=6; bd["H2H advantage"]=6
    elif hh.get("w",0)>=2 and hh.get("p",0)>=3: sc+=3; bd["Slight H2H edge"]=3

    # League position gap (max 8)
    if hs and as_:
        gap=as_.get("pos",20)-hs.get("pos",20)
        if   gap>=10: sc+=8;bd["Huge league position gap"]=8
        elif gap>=6:  sc+=5;bd["Large position advantage"]=5
        elif gap>=3:  sc+=2;bd["Position advantage"]=2

    # Odds signal (max 8)
    if   odds and odds<=1.25: sc+=8;bd["Very short odds (≤1.25)"]=8
    elif odds and odds<=1.50: sc+=5;bd["Low odds (≤1.50)"]=5
    elif odds and odds<=1.75: sc+=2;bd["Moderate odds (≤1.75)"]=2

    # Opponent poor form (max 9)
    owr=af.get("w",0)/max(af.get("p",1),1)
    if   owr<=.15: sc+=9;bd["Opponent in crisis form"]=9
    elif owr<=.30: sc+=5;bd["Opponent struggling"]=5

    return min(sc,100), bd

# ── 5e. Safe bets ─────────────────────────────────────────────
def bets(hf,af,conf):
    out=[]; ag=hf["agf"]+af["agf"]
    if conf>=68: out.append({"t":"Match Winner",      "c":conf,            "safe":True})
    if ag>=2.4:  out.append({"t":"Over 1.5 Goals",   "c":min(93,int(ag*23)),"safe":True})
    if ag>=3.2:  out.append({"t":"Over 2.5 Goals",   "c":min(88,int(ag*19)),"safe":ag>=3.6})
    if hf["cs"]<=1 and af["cs"]<=1 and ag>=2.8:
                 out.append({"t":"Both Teams Score",  "c":67,              "safe":False})
    if 42<=conf<68: out.append({"t":"Double Chance",  "c":conf+14,         "safe":True})
    if conf>=52:    out.append({"t":"Draw No Bet",    "c":conf+7,          "safe":True})
    return sorted(out,key=lambda x:x["c"],reverse=True)

# ── 5f. Danger warnings ───────────────────────────────────────
def warns(hf,af):
    w=[]
    if af.get("five"):                             w.append("Opponent on 5-win streak ⚠️")
    if hf.get("aga",0)>2.2:                       w.append("Defence conceding 2+ per game")
    if hf.get("away",{}).get("l",0)>=3:           w.append("Poor away record")
    if hf.get("form",[]).count("loss")>=3:        w.append("3 losses in last 5")
    if hf.get("gd",0)<-4:                         w.append("Poor goal difference")
    if hf.get("gf",0)<4 and hf.get("p",0)>=5:    w.append("Low scoring — rotation risk")
    if hf.get("cs",0)==0 and hf.get("p",0)>=5:   w.append("Zero clean sheets recently")
    return w

# ── 5g. AI Explanation ────────────────────────────────────────
def explain(hn,an,hf,af,hs,as_,hh,conf):
    p=[]
    if hf.get("five"):           p.append(f"{hn} have won their last 5 matches consecutively")
    elif hf.get("streak",0)>=3: p.append(f"{hn} are on a {hf['streak']}-match winning run")
    if hf.get("gf",0)>=10:     p.append(f"scoring {hf['gf']} goals in {hf.get('p',5)} games")
    if hf.get("agf",0)>=2.0:   p.append(f"averaging {hf['agf']:.1f} goals per game")
    if hf.get("cs",0)>=2:      p.append(f"with {hf['cs']} clean sheets in that run")
    al=af.get("away",{}).get("l",0)
    if al>=3: p.append(f"while {an} have lost {al} of their last away fixtures")
    elif af.get("five"): p.append(f"though {an} are also in strong form — treat with caution")
    if af.get("aga",0)>2.0: p.append(f"{an} have conceded {af['aga']:.1f} goals per game away")
    if hs and as_ and hs["pos"]<as_["pos"]:
        p.append(f"{hn} sit {ordinal(hs['pos'])} vs {an} in {ordinal(as_['pos'])} place")
    if hh.get("p",0)>=3:
        p.append(f"H2H record favours {hn} {hh['w']}–{hh['l']} in {hh['p']} meetings")
    l,_,_=cmeta(conf); p.append(f"giving overall {l.lower()} confidence")
    return (". ".join(p).capitalize()+".") if p else "Insufficient data for detailed analysis."

# ── 5h. Master prediction builder ─────────────────────────────
def predict(match,lg):
    hid=match["homeTeam"]["id"]; aid=match["awayTeam"]["id"]
    hn =match["homeTeam"]["name"]; an=match["awayTeam"]["name"]
    mid=match.get("id")
    hf=form(hid); af=form(aid)
    hs=standing(hid,lg); as_=standing(aid,lg)
    hh=h2h(mid,hid) if mid else {}
    odds=match.get("odds",{}).get("homeWin")
    conf,bd=confidence(hf,af,hs,as_,hh,odds)
    lbl,col,bcls=cmeta(conf)
    bb=bets(hf,af,conf); ww=warns(hf,af)
    ex=explain(hn,an,hf,af,hs,as_,hh,conf)
    return dict(
        mid=mid,home=hn,away=an,hid=hid,aid=aid,
        league=lg,date=match.get("utcDate",""),
        hf=hf,af=af,hs=hs,as_=as_,hh=hh,
        conf=conf,lbl=lbl,col=col,bcls=bcls,bd=bd,
        bets=bb,warns=ww,expl=ex,
        best_bet=bb[0]["t"] if bb else "Match Winner",
        odds=odds,
        five=hf.get("five") or af.get("five"),
        low_odds=bool(odds and odds<=1.50),
        flagged=bool((hf.get("five") or af.get("five")) and odds and odds<=1.50),
    )

# ╔══════════════════════════════════════════════════════════════╗
# ║  6.  UI COMPONENTS                                          ║
# ╚══════════════════════════════════════════════════════════════╝

def ui_hero():
    st.markdown("""
    <div class="hero">
      <div class="hero-ball">⚽</div>
      <div>
        <div class="hero-title">FootballIQ</div>
        <div class="hero-sub">AI-powered predictions · form analysis · safe bets · danger alerts</div>
      </div>
      <div class="hero-live"><span class="ldot"></span>LIVE</div>
    </div>""",unsafe_allow_html=True)

def ui_metrics(all_p,filt):
    hi=max((p["conf"] for p in filt),default=0)
    streaks=sum(1 for p in filt if p.get("five"))
    flagged=sum(1 for p in filt if p.get("flagged"))
    st.markdown(f"""
    <div class="metrics">
      <div class="mbox"><div class="mval">{len(all_p)}</div><div class="mlbl">Fixtures</div></div>
      <div class="mbox"><div class="mval">{len(filt)}</div><div class="mlbl">Qualifying</div><div class="msub">above min conf</div></div>
      <div class="mbox"><div class="mval">{hi}%</div><div class="mlbl">Peak confidence</div></div>
      <div class="mbox"><div class="mval">{streaks}</div><div class="mlbl">Win streaks</div><div class="msub">{flagged} flagged</div></div>
    </div>""",unsafe_allow_html=True)

def ui_highlights(preds):
    if not preds: return
    hot =max(preds,key=lambda p:p["hf"].get("agf",0),default=None)
    cold=max(preds,key=lambda p:p["af"].get("l",0),  default=None)
    byc =sorted(preds,key=lambda p:p["conf"],reverse=True)
    botd=next((p for p in byc if any(b.get("safe") for b in p["bets"])),byc[0] if byc else None)
    st.markdown('<div class="stitle">⚡ Quick Insights</div>',unsafe_allow_html=True)
    st.markdown('<div class="hl-strip">',unsafe_allow_html=True)
    if hot:
        st.markdown(f'<div class="hl hot"><div class="hl-lbl">🔥 Hot Team</div>'
                    f'<div class="hl-name">{trunc(hot["home"],18)}</div>'
                    f'<div class="hl-sub">{hot["hf"]["agf"]:.1f} goals/game avg</div></div>',
                    unsafe_allow_html=True)
    if cold:
        st.markdown(f'<div class="hl cold"><div class="hl-lbl">🧊 Struggling</div>'
                    f'<div class="hl-name">{trunc(cold["away"],18)}</div>'
                    f'<div class="hl-sub">{cold["af"]["l"]} recent losses</div></div>',
                    unsafe_allow_html=True)
    if botd:
        sb=next((b["t"] for b in botd["bets"] if b.get("safe")),botd["best_bet"])
        st.markdown(f'<div class="hl botd"><div class="hl-lbl">🎯 Bet of the Day</div>'
                    f'<div class="hl-name">{trunc(botd["home"],14)} vs {trunc(botd["away"],14)}</div>'
                    f'<div class="hl-sub">✅ {sb} · {botd["conf"]}% conf</div></div>',
                    unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def ui_top3(preds):
    top3=sorted(preds,key=lambda p:p["conf"],reverse=True)[:3]
    if not top3: return
    st.markdown('<div class="stitle">🏆 Top 3 Safest Picks</div>',unsafe_allow_html=True)
    st.markdown('<div class="top3">',unsafe_allow_html=True)
    for i,p in enumerate(top3):
        safe=next((b["t"] for b in p["bets"] if b.get("safe")),p["best_bet"])
        st.markdown(f"""
        <div class="t3card">
          <div class="t3medal">{['🥇','🥈','🥉'][i]}</div>
          <div class="t3teams">{trunc(p['home'],16)}<br>
            <span style="color:#475569;font-weight:400">vs</span> {trunc(p['away'],16)}</div>
          <div class="t3meta">{p['league']} · {p['date'][:10]}</div>
          {badge(p['conf'])}
          <div class="t3bet">✅ {safe}</div>
        </div>""",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def ui_danger_section(preds):
    dangerous=[p for p in preds if len(p["warns"])>=2]
    if not dangerous: return
    st.markdown('<div class="stitle">⚠️ Dangerous Matches — Avoid or Reduce Stake</div>',
                unsafe_allow_html=True)
    for p in dangerous[:3]:
        st.markdown(f"""
        <div class="danger-card">
          <div>
            <div class="danger-match">⚽ {trunc(p['home'],20)} vs {trunc(p['away'],20)}</div>
            <div class="danger-why">{' · '.join(p['warns'][:2])}</div>
          </div>
          {badge(p['conf'])}
        </div>""",unsafe_allow_html=True)

def ui_card(p):
    hf=p["hf"]; af=p["af"]
    hs=p.get("hs"); as_=p.get("as_"); hh=p.get("hh",{})

    # Flagged original-pick banner
    if p.get("flagged"):
        st.markdown(f"""
        <div class="fbanner">
          ⭐ <strong>Original Pick:</strong> 5-Win Streak + Odds ≤ 1.50
          &nbsp;—&nbsp; {p['home']} vs {p['away']}
          &nbsp;|&nbsp; Odds: {p['odds']}
        </div>""",unsafe_allow_html=True)

    stag='<span class="ptag">🔥 5W STREAK</span>' if p.get("five") else ""
    cls ="pcard flagged" if p.get("flagged") else "pcard"

    # Card shell + header + form dots + meter
    st.markdown(f"""
    <div class="{cls}">
      <div class="phdr">
        <div>
          <div class="pvs">{p['home']} <span class="pvs-mid">vs</span> {p['away']}{stag}</div>
          <div class="pmeta">📅 {cd(p['date'])} &nbsp;·&nbsp; {p['league']}
            {'&nbsp;·&nbsp; Odds: '+str(p['odds']) if p['odds'] else ''}</div>
        </div>
        {badge(p['conf'])}
      </div>
      {form_dots(hf.get("form",[]), trunc(p['home'],13)+" (H)")}
      {form_dots(af.get("form",[]), trunc(p['away'],13)+" (A)")}
      {meter(p['conf'])}
    </div>""",unsafe_allow_html=True)

    # Stat boxes
    c1,c2,c3,c4=st.columns(4)
    for col,val,lbl in [
        (c1,f"{hf['agf']:.1f}","Home goals/g"),
        (c2,str(hf['cs']),    "Clean sheets"),
        (c3,f"{af['agf']:.1f}","Away goals/g"),
        (c4,f"{af['aga']:.1f}","Away conceded"),
    ]:
        col.markdown(f'<div class="sbox"><div class="sv">{val}</div>'
                     f'<div class="sl">{lbl}</div></div>',unsafe_allow_html=True)

    # Standing captions
    parts=[]
    if hs:  parts.append(f"{trunc(p['home'],14)}: {ordinal(hs['pos'])} · {hs['pts']}pts")
    if as_: parts.append(f"{trunc(p['away'],14)}: {ordinal(as_['pos'])} · {as_['pts']}pts")
    if parts: st.caption("  ·  ".join(parts))

    # Warning pills
    if p["warns"]:
        wh=" ".join(f'<span class="pill p-warn">⚠️ {w}</span>' for w in p["warns"])
        st.markdown(f'<div class="pills">{wh}</div>',unsafe_allow_html=True)

    # Safe bet pills
    if p["bets"]:
        st.markdown('<div style="font-size:10px;color:#475569;text-transform:uppercase;'
                    'letter-spacing:.07em;margin:6px 0 3px">Safe Bets</div>',
                    unsafe_allow_html=True)
        bh=" ".join(
            f'<span class="pill {"p-safe" if b.get("safe") else "p-bet"}">✅ {b["t"]} · {b["c"]}%</span>'
            for b in p["bets"][:4])
        st.markdown(f'<div class="pills">{bh}</div>',unsafe_allow_html=True)

    # WHY THIS PREDICTION — expander
    with st.expander("🔍  Why this prediction?"):
        st.markdown(f'<div class="why">{p["expl"]}</div>',unsafe_allow_html=True)

        # Confidence factor breakdown
        st.markdown("**📊 Confidence factors:**")
        for factor,pts in p["bd"].items():
            pct=int(pts/25*100)
            st.markdown(f"""
            <div class="bdr">
              <span class="bdr-l">{factor}</span>
              <div class="bdr-t"><div class="bdr-f" style="width:{pct}%"></div></div>
              <span class="bdr-p">+{pts}</span>
            </div>""",unsafe_allow_html=True)

        st.markdown('<hr class="hd">',unsafe_allow_html=True)

        # H2H block
        if hh.get("p",0):
            st.markdown(f"**🤝 Head-to-Head (last {hh['p']} meetings):**  "
                        f"{p['home']} **{hh['w']}W** – {hh['d']}D – {hh['l']}L {p['away']}")
            for row in hh.get("rows",[]):
                ic={"win":"🟢","draw":"🟡","loss":"🔴"}.get(row["res"],"⚪")
                st.caption(f"{ic} {row['date']}  {row['home']} {row['score']} {row['away']}")
        else:
            st.caption("No H2H data available for this fixture.")

        st.markdown('<hr class="hd">',unsafe_allow_html=True)

        # Venue records
        ch,ca=st.columns(2)
        with ch:
            h=hf["home"]
            st.markdown("**🏠 Home record**")
            st.caption(f"{h['w']}W · {h['d']}D · {h['l']}L  |  GF {h['gf']}  GA {h['ga']}")
        with ca:
            a=af["away"]
            st.markdown("**✈️ Away record**")
            st.caption(f"{a['w']}W · {a['d']}D · {a['l']}L  |  GF {a['gf']}  GA {a['ga']}")

        st.markdown('<hr class="hd">',unsafe_allow_html=True)
        st.markdown("**📲 Copy for Telegram / WhatsApp:**")
        st.code(alert(p),language=None)

    st.markdown("<div style='height:2px'></div>",unsafe_allow_html=True)

def ui_welcome():
    st.markdown("""
    <div class="welcome">
      <div class="emoji">⚽</div>
      <h2>Welcome to FootballIQ</h2>
      <p>Select a league from the sidebar and tap <strong>Load Fixtures</strong>
         to receive AI-powered predictions with confidence scoring,
         form analysis, safe bets, and detailed reasoning.</p>
    </div>""",unsafe_allow_html=True)

    feats=[
        ("📊","Advanced Form Analysis","Wins, draws, losses, goals & clean sheets from last 10 games per team"),
        ("🔥","Confidence Scoring","9-factor weighted 0–100% engine with full breakdown per match"),
        ("🎯","Safe Bet Generator","Match Winner, Over 1.5, BTTS, Double Chance auto-recommended"),
        ("🤝","Head-to-Head","Last 5 meetings analysed and weighted into prediction score"),
        ("⚡","Danger Warnings","Defence issues, poor away form & rotation risk auto-flagged"),
        ("📲","Alert Ready","Copy predictions for Telegram & WhatsApp in one click"),
    ]
    st.markdown('<div class="feat-grid">',unsafe_allow_html=True)
    for icon,title,desc in feats:
        st.markdown(f"""
        <div class="fcard">
          <div class="fcard-icon">{icon}</div>
          <div class="fcard-title">{title}</div>
          <div class="fcard-desc">{desc}</div>
        </div>""",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  7.  SIDEBAR                                                ║
# ╚══════════════════════════════════════════════════════════════╝
with st.sidebar:
    st.markdown("## ⚙️ Filters")
    sel_lg       = st.selectbox("League",list(LEAGUES.keys()),format_func=lambda k:LEAGUES[k])
    min_conf     = st.slider("Min confidence %",0,100,40,5)
    warns_only   = st.checkbox("⚠️ Danger matches only",  False)
    streaks_only = st.checkbox("🔥 5-win streak only",    False)
    flagged_only = st.checkbox("⭐ Flagged picks only",   False)
    st.divider()
    st.caption("⚡ API data cached 30 min\nPowered by football-data.org")

# ╔══════════════════════════════════════════════════════════════╗
# ║  8.  SESSION STATE INIT                                     ║
# ╚══════════════════════════════════════════════════════════════╝
for k,v in [("preds",[]),("league","PL"),("loaded",False)]:
    if k not in st.session_state: st.session_state[k]=v

# ╔══════════════════════════════════════════════════════════════╗
# ║  9.  MAIN RENDER                                            ║
# ╚══════════════════════════════════════════════════════════════╝
ui_hero()

# ── API key guard ─────────────────────────────────────────────
if not api_ok():
    st.markdown("""
    <div class="key-err">
      <h3>🔑 API Key Required</h3>
      <p style="color:#64748b;font-size:13px;margin:.5rem 0 1rem">
        This app needs a free football-data.org API key to load match data.</p>
    </div>""",unsafe_allow_html=True)
    st.markdown("**On Streamlit Cloud:** App menu (⋮) → Settings → Secrets → add:")
    st.code('API_KEY = "your_key_here"',language="toml")
    st.markdown("**Local dev:** create `.streamlit/secrets.toml` with the same line.")
    st.stop()

# ── Load button row ───────────────────────────────────────────
cb,ci=st.columns([2,3])
with cb: go=st.button("🔄  Load Fixtures",use_container_width=True)
with ci: st.caption(f"Up to {MAX} fixtures · 30-min cache · {LEAGUES.get(sel_lg,'')}")

# ── Fetch + build predictions ─────────────────────────────────
need = go or not st.session_state.loaded or st.session_state.league!=sel_lg

if go or st.session_state.loaded:
    if need:
        st.session_state.league=sel_lg
        with st.spinner("⚽ Fetching fixtures and building predictions…"):
            raw=api_fixtures(sel_lg)
            built=[]
            total=min(len(raw),MAX)
            bar=st.progress(0,text="Analysing matches…")
            for i,m in enumerate(raw[:MAX]):
                try: built.append(predict(m,sel_lg))
                except Exception: pass
                bar.progress(int((i+1)/max(total,1)*100),text=f"Analysing {i+1}/{total}…")
            bar.empty()
        st.session_state.preds=built
        st.session_state.loaded=True

    all_p=st.session_state.preds

    # ── Apply filters ─────────────────────────────────────────
    filt=[p for p in all_p if p["conf"]>=min_conf]
    if warns_only:   filt=[p for p in filt if p["warns"]]
    if streaks_only: filt=[p for p in filt if p.get("five")]
    if flagged_only: filt=[p for p in filt if p.get("flagged")]
    srt=sorted(filt,key=lambda p:p["conf"],reverse=True)

    # ── Dashboard render ──────────────────────────────────────
    ui_metrics(all_p,srt)
    st.markdown('<hr class="hd">',unsafe_allow_html=True)

    if srt:
        ui_highlights(srt)
        st.markdown('<hr class="hd">',unsafe_allow_html=True)
        ui_top3(srt)
        st.markdown('<hr class="hd">',unsafe_allow_html=True)
        ui_danger_section(srt)

    # ── All predictions ───────────────────────────────────────
    if srt:
        st.markdown(f'<div class="stitle">📋 All Predictions · {len(srt)} matches</div>',
                    unsafe_allow_html=True)
        for p in srt:
            ui_card(p)
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem">
          <div style="font-size:52px;margin-bottom:1rem">🔍</div>
          <h3 style="color:#e2e8f0">No matches found</h3>
          <p style="color:#64748b;font-size:13px;margin-top:.5rem">
            Try lowering the confidence threshold or clearing filters.</p>
        </div>""",unsafe_allow_html=True)
else:
    ui_welcome()
