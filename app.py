from __future__ import annotations
"""
FootballIQ Premium — Single-file Streamlit prediction platform.
DEPLOY: Push ONLY this file + requirements.txt to GitHub.
Add API_KEY in Streamlit Cloud → Settings → Secrets.
Zero local imports. Cannot break on any OS.
"""
import os, requests, streamlit as st
from datetime import datetime, timezone
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────
# 0. PAGE CONFIG  (MUST be first Streamlit call)
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FootballIQ — AI Predictions",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# 1. CSS — Premium dark football theme, fully mobile-responsive
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,600;0,700;0,900;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}
.block-container {
    padding: 0 1rem 5rem !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}

/* ── HERO LOGO ───────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg,#040c1e 0%,#0a1628 40%,#071122 100%);
    border: 1px solid rgba(59,130,246,.25);
    border-radius: 22px;
    padding: 1.6rem 1.8rem;
    margin: .6rem 0 1.4rem;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 0 60px rgba(59,130,246,.08), 0 8px 32px rgba(0,0,0,.5);
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -40%; right: -10%;
    width: 280px; height: 280px; border-radius: 50%;
    background: radial-gradient(circle,rgba(59,130,246,.12) 0%,transparent 70%);
    pointer-events: none;
}
.hero-icon {
    width: 72px; height: 72px; border-radius: 18px; flex-shrink: 0;
    background: linear-gradient(145deg,#1d4ed8,#3b82f6);
    display: flex; align-items: center; justify-content: center;
    font-size: 38px;
    box-shadow: 0 6px 20px rgba(59,130,246,.45);
}
.hero-text h1 {
    font-size: 26px !important; font-weight: 900 !important;
    background: linear-gradient(90deg,#60a5fa,#93c5fd,#e2e8f0);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -.5px; margin: 0 !important;
}
.hero-text p { font-size: 13px; color: #475569; margin-top: 4px; }
.hero-live {
    margin-left: auto; display: flex; align-items: center; gap: 6px;
    background: rgba(34,197,94,.1); border: 1px solid rgba(34,197,94,.3);
    color: #4ade80; font-size: 11px; font-weight: 700; letter-spacing: .06em;
    padding: 5px 13px; border-radius: 20px;
}
.live-dot {
    width: 7px; height: 7px; background: #4ade80; border-radius: 50%;
    animation: blink 1.5s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }

/* ── SECTION HEADERS ─────────────────────────────────────── */
.sec-hdr {
    display: flex; align-items: center; gap: 10px;
    font-size: 15px; font-weight: 700; color: #e2e8f0;
    margin: 1.6rem 0 .8rem; letter-spacing: -.1px;
}
.sec-hdr::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg,rgba(255,255,255,.07),transparent);
}

/* ── TOP-PICK CARDS ──────────────────────────────────────── */
.top-picks-grid {
    display: grid; grid-template-columns: repeat(3,1fr); gap: 10px;
    margin-bottom: 1rem;
}
.tp-card {
    background: linear-gradient(155deg,#0d1f42,#122955);
    border: 1px solid rgba(59,130,246,.22);
    border-radius: 18px; padding: 1.1rem 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,.4);
    position: relative; overflow: hidden;
}
.tp-card::after {
    content:''; position:absolute; bottom:-20px; right:-20px;
    width:80px; height:80px; border-radius:50%;
    background:radial-gradient(circle,rgba(59,130,246,.1),transparent);
}
.tp-medal { font-size: 26px; margin-bottom: 6px; }
.tp-teams { font-weight: 700; font-size: 12px; color: #e2e8f0; line-height: 1.5; margin-bottom: 6px; }
.tp-meta  { font-size: 10px; color: #475569; margin-bottom: 10px; }
.tp-bet   { font-size: 11px; color: #93c5fd; margin-top: 6px; }

/* ── HIGHLIGHT STRIP CARDS ───────────────────────────────── */
.hl-row { display:flex; gap:8px; margin-bottom:1rem; flex-wrap:wrap; }
.hl-card {
    flex:1; min-width:140px;
    background:rgba(255,255,255,.03);
    border:1px solid rgba(255,255,255,.07);
    border-radius:14px; padding:.9rem 1rem;
}
.hl-card.hot  { border-color:rgba(239,68,68,.25);  background:rgba(239,68,68,.06); }
.hl-card.cold { border-color:rgba(99,102,241,.25); background:rgba(99,102,241,.06); }
.hl-card.botd { border-color:rgba(251,191,36,.3);  background:rgba(251,191,36,.07); }
.hl-title { font-size:11px; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
            color:#64748b; margin-bottom:6px; }
.hl-card.hot  .hl-title { color:#f87171; }
.hl-card.cold .hl-title { color:#818cf8; }
.hl-card.botd .hl-title { color:#fbbf24; }
.hl-team  { font-size:14px; font-weight:700; color:#e2e8f0; margin-bottom:2px; }
.hl-sub   { font-size:12px; color:#64748b; }

/* ── MAIN PREDICTION CARD ────────────────────────────────── */
.pred-card {
    background: rgba(15,23,42,.95);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px; padding: 1.3rem 1.4rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 2px 20px rgba(0,0,0,.4);
    transition: border-color .25s;
}
.pred-card:hover { border-color: rgba(59,130,246,.3); }
.pred-card.flagged { border-color: rgba(251,191,36,.35); }

.match-header {
    display: flex; justify-content: space-between;
    align-items: flex-start; gap: 10px; margin-bottom: 10px;
}
.match-vs { font-size: 16px; font-weight: 800; color: #f1f5f9; line-height: 1.3; }
.match-vs span { color: #475569; font-weight: 400; }
.streak-tag {
    display: inline-block;
    background: linear-gradient(90deg,#f59e0b,#ef4444);
    color: #fff; font-size: 10px; font-weight: 800;
    padding: 2px 9px; border-radius: 20px; letter-spacing: .04em;
    vertical-align: middle; margin-left: 6px;
}
.match-meta { font-size: 11px; color: #475569; margin-top: 2px; }

/* ── FORM STRIP ──────────────────────────────────────────── */
.form-row { display:flex; align-items:center; gap:8px; margin:6px 0; }
.form-lbl { font-size:11px; color:#64748b; width:80px; flex-shrink:0; }
.form-dots { display:flex; gap:4px; }
.fd { width:18px; height:18px; border-radius:50%; font-size:10px;
      display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.fd.W { background:#16a34a; color:#fff; }
.fd.D { background:#ca8a04; color:#fff; }
.fd.L { background:#dc2626; color:#fff; }
.fd.N { background:rgba(255,255,255,.1); color:#64748b; }

/* ── CONFIDENCE METER ────────────────────────────────────── */
.conf-wrap { margin: 10px 0; }
.conf-bar-track {
    width:100%; height:8px; background:rgba(255,255,255,.07);
    border-radius:6px; overflow:hidden; margin-top:4px;
}
.conf-bar-fill { height:100%; border-radius:6px; transition:width .5s ease; }

.badge {
    display:inline-block; padding:3px 12px; border-radius:20px;
    font-size:11px; font-weight:800; letter-spacing:.04em;
}
.badge-vhigh { background:#14532d; color:#4ade80; border:1px solid #16a34a; }
.badge-high  { background:#1a2e05; color:#a3e635; border:1px solid #65a30d; }
.badge-med   { background:#431407; color:#fb923c; border:1px solid #ea580c; }
.badge-low   { background:#450a0a; color:#f87171; border:1px solid #dc2626; }

/* ── STAT BOXES ──────────────────────────────────────────── */
.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:10px 0; }
.stat-box {
    background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.06);
    border-radius:12px; padding:8px 10px; text-align:center;
}
.stat-val { font-size:20px; font-weight:700; color:#e2e8f0; }
.stat-lbl { font-size:10px; color:#64748b; margin-top:2px; }

/* ── BET PILLS ───────────────────────────────────────────── */
.pills-row { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; }
.pill {
    font-size:11px; font-weight:600; padding:4px 12px; border-radius:20px;
    display:inline-flex; align-items:center; gap:4px;
}
.pill-bet  { background:rgba(59,130,246,.15);  color:#93c5fd; border:1px solid rgba(59,130,246,.25); }
.pill-warn { background:rgba(239,68,68,.12);   color:#fca5a5; border:1px solid rgba(239,68,68,.2); }
.pill-hot  { background:rgba(251,146,60,.12);  color:#fdba74; border:1px solid rgba(251,146,60,.2); }
.pill-safe { background:rgba(34,197,94,.1);    color:#4ade80; border:1px solid rgba(34,197,94,.2); }

/* ── EXPANDER CONTENT ────────────────────────────────────── */
.why-box {
    background:rgba(255,255,255,.02); border-radius:14px;
    padding:1rem 1.1rem; margin:4px 0;
}
.why-quote {
    font-size:14px; color:#94a3b8; line-height:1.7;
    border-left:3px solid #3b82f6; padding-left:12px;
    font-style:italic; margin-bottom:12px;
}
.breakdown-row {
    display:flex; align-items:center; gap:10px; margin:5px 0;
}
.bdr-lbl  { font-size:12px; color:#64748b; flex:0 0 160px; }
.bdr-bar  { flex:1; height:6px; background:rgba(255,255,255,.06); border-radius:4px; overflow:hidden; }
.bdr-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,#1d4ed8,#3b82f6); }
.bdr-pts  { font-size:12px; color:#60a5fa; font-weight:700; flex:0 0 32px; text-align:right; }

/* ── METRIC SUMMARY ROW ──────────────────────────────────── */
.metrics-row { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:1rem 0; }
.metric-box {
    background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.06);
    border-radius:14px; padding:1rem; text-align:center;
}
.metric-val { font-size:28px; font-weight:900; color:#e2e8f0; }
.metric-lbl { font-size:11px; color:#64748b; margin-top:4px; }
.metric-sub { font-size:10px; color:#475569; margin-top:2px; }

/* ── LOAD BUTTON ─────────────────────────────────────────── */
.stButton > button {
    background:linear-gradient(135deg,#1d4ed8,#3b82f6) !important;
    color:#fff !important; border:none !important; border-radius:14px !important;
    font-weight:700 !important; font-size:15px !important;
    padding:.7rem 1.4rem !important; width:100% !important;
    box-shadow:0 4px 18px rgba(59,130,246,.35) !important;
    transition:opacity .2s !important;
}
.stButton > button:hover { opacity:.88 !important; }

/* ── DANGER / FLAGGED banner ─────────────────────────────── */
.danger-banner {
    background:linear-gradient(90deg,rgba(251,191,36,.12),rgba(239,68,68,.1));
    border:1px solid rgba(251,191,36,.3); border-radius:14px;
    padding:.9rem 1.1rem; margin-bottom:.8rem;
    font-size:13px; color:#fde68a;
}

/* ── EMPTY STATE ─────────────────────────────────────────── */
.empty-state { text-align:center; padding:4rem 1rem; }
.empty-state .emoji { font-size:56px; margin-bottom:1rem; }
.empty-state h3 { font-size:18px; color:#e2e8f0; margin-bottom:.5rem; }
.empty-state p  { font-size:13px; color:#64748b; max-width:380px; margin:0 auto; }

/* ── WELCOME SCREEN ──────────────────────────────────────── */
.feat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:1rem 0; }
.feat-card {
    background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
    border-radius:16px; padding:1.1rem;
}
.feat-icon { font-size:28px; margin-bottom:8px; }
.feat-title { font-size:13px; font-weight:700; color:#e2e8f0; margin-bottom:4px; }
.feat-desc  { font-size:11px; color:#64748b; line-height:1.5; }

/* ── MOBILE RESPONSIVE ───────────────────────────────────── */
@media (max-width:640px) {
    .block-container { padding:0 .5rem 5rem !important; }
    .hero { padding:1rem; gap:10px; }
    .hero-icon { width:52px; height:52px; font-size:26px; border-radius:14px; }
    .hero-text h1 { font-size:19px !important; }
    .hero-live { display:none; }
    .top-picks-grid { grid-template-columns:1fr; }
    .stat-row { grid-template-columns:repeat(2,1fr); }
    .metrics-row { grid-template-columns:repeat(2,1fr); }
    .feat-grid { grid-template-columns:1fr 1fr; }
    .match-vs { font-size:14px; }
    .bdr-lbl { flex:0 0 120px; font-size:11px; }
}
@media (max-width:380px) {
    .feat-grid { grid-template-columns:1fr; }
    .hl-row { flex-direction:column; }
}

/* ── MISC ────────────────────────────────────────────────── */
hr.fiq { border:none; border-top:1px solid rgba(255,255,255,.06); margin:1rem 0; }
.st-expander { border:1px solid rgba(255,255,255,.07) !important; border-radius:14px !important; }
details summary { font-weight:600 !important; color:#93c5fd !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# 2. CONSTANTS
# ─────────────────────────────────────────────────────────────────
BASE_URL = "https://api.football-data.org/v4"

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

MAX_MATCHES = 20   # cap per league to stay fast on free tier

# ─────────────────────────────────────────────────────────────────
# 3. API LAYER
# ─────────────────────────────────────────────────────────────────
def _key() -> str:
    try:    return st.secrets["API_KEY"]
    except: return os.getenv("API_KEY", "")

def _hdr() -> dict:
    return {"X-Auth-Token": _key()}

def _get(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=_hdr(), timeout=12)
        if r.status_code == 200: return r.json()
        if r.status_code == 429: st.warning("⏳ Rate limit — wait 60 s and reload.")
        elif r.status_code == 403: st.error("🔑 Invalid API key or plan restriction.")
        elif r.status_code != 404: st.warning(f"API {r.status_code}")
    except requests.Timeout:         st.warning("⌛ Request timed out.")
    except requests.ConnectionError: st.warning("📡 No connection.")
    except Exception as e:           st.warning(f"Error: {e}")
    return None

@st.cache_data(ttl=1800, show_spinner=False)
def api_upcoming(league: str) -> list:
    d = _get(f"{BASE_URL}/competitions/{league}/matches?status=SCHEDULED")
    return (d or {}).get("matches", [])

@st.cache_data(ttl=1800, show_spinner=False)
def api_team_matches(tid: int, n: int = 10) -> list:
    d = _get(f"{BASE_URL}/teams/{tid}/matches?status=FINISHED&limit={n}")
    return (d or {}).get("matches", [])

@st.cache_data(ttl=3600, show_spinner=False)
def api_standings(league: str) -> list:
    d = _get(f"{BASE_URL}/competitions/{league}/standings")
    if not d: return []
    try:    return d["standings"][0]["table"]
    except: return []

@st.cache_data(ttl=1800, show_spinner=False)
def api_h2h(mid: int) -> list:
    d = _get(f"{BASE_URL}/matches/{mid}/head2head?limit=5")
    return (d or {}).get("matches", [])

@st.cache_data(ttl=86400, show_spinner=False)
def api_check() -> bool:
    return _get(f"{BASE_URL}/competitions/PL") is not None

def fetch_odds_fallback(mid: int) -> dict:
    """Stub — swap for The Odds API / SportMonks when plan upgrades."""
    return {}

# ─────────────────────────────────────────────────────────────────
# 4. UTILITIES
# ─────────────────────────────────────────────────────────────────
def _vb() -> dict:
    return {"p":0,"w":0,"d":0,"l":0,"gf":0,"ga":0}

def _empty_form() -> dict:
    return {"p":0,"w":0,"d":0,"l":0,"gf":0,"ga":0,"gd":0,
            "cs":0,"streak":0,"five":False,"agf":0.,"aga":0.,
            "form":[],"home":_vb(),"away":_vb()}

def short(s: str, n: int = 20) -> str:
    return s if len(s) <= n else s[:n-1]+"…"

def ordinal(n: int) -> str:
    sfx = {1:"st",2:"nd",3:"rd"}.get(n%10 if n%100 not in (11,12,13) else 0,"th")
    return f"{n}{sfx}"

def countdown(utc: str) -> str:
    try:
        dt  = datetime.fromisoformat(utc.replace("Z","+00:00"))
        now = datetime.now(timezone.utc)
        df  = dt - now
        if df.total_seconds() < 0: return "Kicked off"
        d,h = df.days, int(df.total_seconds()//3600)%24
        if d == 0: return f"Today · in {h}h"
        if d == 1: return f"Tomorrow {dt.strftime('%H:%M')} UTC"
        return f"In {d}d {h}h · {dt.strftime('%d %b')}"
    except: return utc[:10] if utc else "TBD"

def conf_meta(score: int) -> tuple:
    """Returns (label, bar_color, badge_class)."""
    if score >= 78: return "Very High", "#22c55e", "badge-vhigh"
    if score >= 58: return "High",      "#84cc16", "badge-high"
    if score >= 38: return "Medium",    "#f59e0b", "badge-med"
    return "Low", "#ef4444", "badge-low"

def form_html(results: list, label: str) -> str:
    dots = ""
    for r in results:
        cls = {"win":"W","draw":"D","loss":"L"}.get(r,"N")
        letter = cls
        dots += f'<div class="fd {cls}">{letter}</div>'
    # pad to 5
    for _ in range(5 - len(results)):
        dots += '<div class="fd N">·</div>'
    return (f'<div class="form-row">'
            f'<span class="form-lbl">{label}</span>'
            f'<div class="form-dots">{dots}</div>'
            f'</div>')

def badge_html(score: int) -> str:
    lbl, _, cls = conf_meta(score)
    return f'<span class="badge {cls}">{lbl} · {score}%</span>'

def conf_bar(score: int) -> str:
    _, color, _ = conf_meta(score)
    return (f'<div class="conf-wrap">'
            f'<div class="conf-bar-track">'
            f'<div class="conf-bar-fill" style="width:{score}%;background:{color}"></div>'
            f'</div></div>')

def alert_text(p: dict) -> str:
    return (f"⚽ {p['home']} vs {p['away']}\n"
            f"🏆 {p['league']}\n"
            f"📊 Confidence: {p['conf']}% ({p['conf_lbl']})\n"
            f"✅ Best bet: {p['best_bet']}\n"
            f"⏰ {countdown(p.get('date',''))}\n"
            f"💡 {p.get('expl','')}")

# ─────────────────────────────────────────────────────────────────
# 5. PREDICTION ENGINE
# ─────────────────────────────────────────────────────────────────
def analyse_form(tid: int) -> dict:
    """Full form stats from last 10 finished matches."""
    ms = api_team_matches(tid, 10)
    if not ms: return _empty_form()
    s = _empty_form()
    f5: list = []; streak = 0
    for m in ms:
        ih  = m["homeTeam"]["id"] == tid
        mg  = m["score"]["fullTime"].get("home" if ih else "away") or 0
        og  = m["score"]["fullTime"].get("away" if ih else "home") or 0
        win = m["score"].get("winner","")
        if   win == "HOME_TEAM": res = "win"  if ih else "loss"
        elif win == "AWAY_TEAM": res = "loss" if ih else "win"
        elif win == "DRAW":      res = "draw"
        else:                    res = "unknown"
        s["p"]+=1; s["gf"]+=mg; s["ga"]+=og
        if res=="win":    s["w"]+=1; streak+=1
        elif res=="draw": s["d"]+=1; streak=0
        elif res=="loss": s["l"]+=1; streak=0
        if og==0: s["cs"]+=1
        v = s["home"] if ih else s["away"]
        v["p"]+=1; v["gf"]+=mg; v["ga"]+=og
        if res=="win":    v["w"]+=1
        elif res=="draw": v["d"]+=1
        elif res=="loss": v["l"]+=1
        if len(f5)<5: f5.append(res)
    s["streak"] = streak
    s["form"]   = list(reversed(f5))
    s["gd"]     = s["gf"] - s["ga"]
    s["agf"]    = round(s["gf"]/max(s["p"],1),2)
    s["aga"]    = round(s["ga"]/max(s["p"],1),2)
    s["five"]   = _five(ms, tid)
    return s

def _five(ms: list, tid: int) -> bool:
    if len(ms)<5: return False
    return all(
        (m["score"]["winner"]=="HOME_TEAM" and m["homeTeam"]["id"]==tid) or
        (m["score"]["winner"]=="AWAY_TEAM" and m["awayTeam"]["id"]==tid)
        for m in ms[:5])

def standing(tid: int, league: str) -> dict | None:
    for r in api_standings(league):
        if r.get("team",{}).get("id")==tid:
            return {"pos":r.get("position"),"pts":r.get("points"),
                    "gd":r.get("goalDifference"),"played":r.get("playedGames")}
    return None

def h2h_stats(mid: int, fid: int) -> dict:
    r: dict = {"p":0,"w":0,"d":0,"l":0,"rows":[]}
    for m in api_h2h(mid):
        ih = m["homeTeam"]["id"] == fid
        win= m["score"].get("winner","DRAW")
        r["p"]+=1
        if win=="DRAW": res="draw"; r["d"]+=1
        elif (win=="HOME_TEAM" and ih) or (win=="AWAY_TEAM" and not ih): res="win"; r["w"]+=1
        else: res="loss"; r["l"]+=1
        r["rows"].append({"date":m.get("utcDate","")[:10],
                          "home":m["homeTeam"]["name"],"away":m["awayTeam"]["name"],
                          "score":f"{m['score']['fullTime']['home']}–{m['score']['fullTime']['away']}",
                          "res":res})
    return r

def calc_conf(hf,af,hs,as_,h2h,odds) -> tuple:
    """
    Multi-factor weighted confidence score (0–100).
    Returns (score, breakdown_dict).
    """
    sc=0; bd: dict={}

    # ── Win streak (max +25) ──────────────────────────────────
    if hf.get("five"):
        sc+=25; bd["5-game win streak"]=25
    elif hf.get("streak",0)>=3:
        pts=15; sc+=pts; bd[f"{hf['streak']}-game win streak"]=pts

    # ── Opponent poor away form (max +20) ────────────────────
    a_away = af.get("away",{})
    a_away_wr = a_away.get("w",0)/max(a_away.get("p",1),1)
    if a_away_wr <= .2 and a_away.get("p",0)>=3:
        sc+=20; bd["Opponent poor away form"]=20
    elif a_away_wr <= .35 and a_away.get("p",0)>=3:
        sc+=12; bd["Opponent weak away record"]=12

    # ── Strong home form (max +15) ───────────────────────────
    h_home = hf.get("home",{})
    h_home_wr = h_home.get("w",0)/max(h_home.get("p",1),1)
    if h_home_wr >= .7 and h_home.get("p",0)>=3:
        sc+=15; bd["Dominant home form"]=15
    elif h_home_wr >= .5:
        sc+=8;  bd["Good home record"]=8

    # ── Goalscoring strength (max +15) ───────────────────────
    if hf.get("agf",0) >= 2.5:
        sc+=15; bd["Prolific attack (2.5+ goals/g)"]=15
    elif hf.get("agf",0) >= 1.8:
        sc+=9;  bd["Good goalscoring form"]=9

    # ── Defensive solidity / clean sheets (max +10) ──────────
    if hf.get("cs",0) >= 3:
        sc+=10; bd["Strong defence (3+ clean sheets)"]=10
    elif hf.get("cs",0) >= 1:
        sc+=5;  bd["Some clean sheets"]=5

    # ── H2H dominance (max +10) ──────────────────────────────
    if h2h.get("w",0) >= 3 and h2h.get("p",0)>=3:
        sc+=10; bd["H2H dominance"]=10
    elif h2h.get("w",0) >= 2 and h2h.get("p",0)>=3:
        sc+=5;  bd["Slight H2H edge"]=5

    # ── League position gap (max +8) ─────────────────────────
    if hs and as_:
        gap = as_.get("pos",20) - hs.get("pos",20)
        if gap >= 8:   sc+=8; bd["Large league position gap"]=8
        elif gap >= 4: sc+=4; bd["League position advantage"]=4

    # ── Low odds signal (max +7) ─────────────────────────────
    if odds and odds <= 1.30:
        sc+=7; bd["Very low odds (≤1.30)"]=7
    elif odds and odds <= 1.50:
        sc+=5; bd["Low odds (≤1.50)"]=5

    # ── Opponent in poor overall form ────────────────────────
    opp_wr = af.get("w",0)/max(af.get("p",1),1)
    if opp_wr <= .2:
        sc+=10; bd["Opponent in very poor form"]=10
    elif opp_wr <= .35:
        sc+=5;  bd["Opponent struggling"]=5

    # ── Goal difference bonus ─────────────────────────────────
    if hf.get("gd",0) >= 8:
        sc+=5; bd["Excellent goal difference"]=5

    return min(sc,100), bd

def gen_bets(hf: dict, af: dict, conf: int) -> list:
    """Generate safe bet recommendations sorted by confidence."""
    bets: list=[]
    ag = hf["agf"]+af["agf"]
    if conf>=70: bets.append({"t":"Match Winner","c":conf,"safe":True})
    if ag>=2.5:  bets.append({"t":"Over 1.5 Goals","c":min(92,int(ag*24)),"safe":True})
    if ag>=3.2:  bets.append({"t":"Over 2.5 Goals","c":min(88,int(ag*19)),"safe":ag>=3.5})
    if hf["cs"]<=1 and af["cs"]<=1 and ag>=2.8:
        bets.append({"t":"Both Teams Score","c":68,"safe":False})
    if 42<=conf<70: bets.append({"t":"Double Chance","c":conf+12,"safe":True})
    if conf>=55:    bets.append({"t":"Draw No Bet","c":conf+6,"safe":True})
    return sorted(bets,key=lambda x:x["c"],reverse=True)

def gen_warns(hf: dict, af: dict) -> list:
    w: list=[]
    if af.get("five"):                         w.append("Opponent on 5-win streak")
    if hf.get("aga",0)>2.2:                   w.append("Shaky defence — 2+ conceded/g")
    if hf.get("away",{}).get("l",0)>=3:       w.append("Poor away record")
    if hf.get("form",[]).count("loss")>=3:    w.append("3 losses in last 5 — collapse risk")
    if hf.get("gd",0)<-3:                     w.append("Negative goal difference")
    if hf.get("gf",0)<4 and hf.get("p",0)>=5: w.append("Low output — rotation risk")
    if hf.get("cs",0)==0 and hf.get("p",0)>=5: w.append("Zero clean sheets recently")
    return w

def gen_expl(hn,an,hf,af,hs,as_,h2h,conf) -> str:
    """Template-driven intelligent explanation."""
    p: list=[]
    if hf.get("five"):
        p.append(f"{hn} have won their last 5 matches consecutively")
    elif hf.get("streak",0)>=3:
        p.append(f"{hn} are on a {hf['streak']}-game winning run")
    if hf.get("gf",0)>=10:
        p.append(f"scoring {hf['gf']} goals in their last {hf.get('p',5)} games")
    if hf.get("agf",0)>=2.0:
        p.append(f"averaging {hf['agf']:.1f} goals per game")
    if hf.get("cs",0)>=2:
        p.append(f"keeping {hf['cs']} clean sheets")
    al=af.get("away",{}).get("l",0)
    if al>=3:
        p.append(f"while {an} have lost {al} of their last away fixtures")
    elif af.get("five"):
        p.append(f"though {an} are also in excellent form — exercise caution")
    if hs and as_ and hs["pos"]<as_["pos"]:
        p.append(f"{hn} sit {ordinal(hs['pos'])} vs {an} in {ordinal(as_['pos'])} place")
    if h2h.get("p",0)>=3:
        p.append(f"H2H history favours {hn} {h2h['w']}–{h2h['l']}")
    lbl,_,_=conf_meta(conf); p.append(f"giving {lbl.lower()} confidence overall")
    return (". ".join(p).capitalize()+".") if p else "Insufficient historical data for detailed analysis."

def build_pred(match: dict, league: str) -> dict:
    """Build the complete prediction object for one fixture."""
    hid=match["homeTeam"]["id"]; aid=match["awayTeam"]["id"]
    hn =match["homeTeam"]["name"]; an=match["awayTeam"]["name"]
    mid=match.get("id")
    hf=analyse_form(hid); af=analyse_form(aid)
    hs=standing(hid,league); as_=standing(aid,league)
    h2h=h2h_stats(mid,hid) if mid else {}
    odds=match.get("odds",{}).get("homeWin")
    conf,bd=calc_conf(hf,af,hs,as_,h2h,odds)
    lbl,col,bcls=conf_meta(conf)
    bets=gen_bets(hf,af,conf); warns=gen_warns(hf,af)
    expl=gen_expl(hn,an,hf,af,hs,as_,h2h,conf)
    return dict(
        mid=mid,home=hn,away=an,hid=hid,aid=aid,
        league=league,date=match.get("utcDate",""),
        hf=hf,af=af,hs=hs,as_=as_,h2h=h2h,
        conf=conf,conf_lbl=lbl,conf_col=col,conf_bcls=bcls,bd=bd,
        bets=bets,warns=warns,expl=expl,
        best_bet=bets[0]["t"] if bets else "Match Winner",
        odds=odds,
        five=hf.get("five") or af.get("five"),
        low_odds=bool(odds and odds<=1.50),
        flagged=bool((hf.get("five") or af.get("five")) and odds and odds<=1.50),
    )

# ─────────────────────────────────────────────────────────────────
# 6. UI COMPONENTS
# ─────────────────────────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero">
      <div class="hero-icon">⚽</div>
      <div class="hero-text">
        <h1>FootballIQ</h1>
        <p>AI-powered predictions · form analysis · safe bets · danger alerts</p>
      </div>
      <div class="hero-live"><span class="live-dot"></span>LIVE</div>
    </div>""", unsafe_allow_html=True)

def render_highlights(preds: list):
    if not preds: return
    by_conf = sorted(preds, key=lambda p:p["conf"], reverse=True)
    # Hot team = home team with highest avg goals
    hot = max(preds, key=lambda p:p["hf"].get("agf",0), default=None)
    # Cold team = away team with most recent losses
    cold= max(preds, key=lambda p:p["af"].get("l",0), default=None)
    # Bet of the day = highest confidence with a "safe" bet
    botd= next((p for p in by_conf if any(b.get("safe") for b in p["bets"])), by_conf[0] if by_conf else None)

    st.markdown('<div class="hl-row">', unsafe_allow_html=True)
    if hot:
        st.markdown(f"""
        <div class="hl-card hot">
          <div class="hl-title">🔥 Hot Team</div>
          <div class="hl-team">{short(hot['home'],18)}</div>
          <div class="hl-sub">{hot['hf']['agf']:.1f} goals/game avg</div>
        </div>""", unsafe_allow_html=True)
    if cold:
        st.markdown(f"""
        <div class="hl-card cold">
          <div class="hl-title">🧊 Cold Team</div>
          <div class="hl-team">{short(cold['away'],18)}</div>
          <div class="hl-sub">{cold['af']['l']} recent losses</div>
        </div>""", unsafe_allow_html=True)
    if botd:
        safe_bet = next((b["t"] for b in botd["bets"] if b.get("safe")), botd["best_bet"])
        st.markdown(f"""
        <div class="hl-card botd">
          <div class="hl-title">🎯 Bet of the Day</div>
          <div class="hl-team">{short(botd['home'],16)} vs {short(botd['away'],16)}</div>
          <div class="hl-sub">✅ {safe_bet} · {botd['conf']}% conf</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_top_picks(preds: list):
    top3 = sorted(preds, key=lambda p:p["conf"], reverse=True)[:3]
    if not top3: return
    st.markdown('<div class="sec-hdr">🏆 Top 3 Safest Picks</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-picks-grid">', unsafe_allow_html=True)
    medals=["🥇","🥈","🥉"]
    for i,p in enumerate(top3):
        safe = next((b["t"] for b in p["bets"] if b.get("safe")), p["best_bet"])
        _,col,bcls=conf_meta(p["conf"])
        st.markdown(f"""
        <div class="tp-card">
          <div class="tp-medal">{medals[i]}</div>
          <div class="tp-teams">{short(p['home'],17)}<br><span style="color:#475569;font-weight:400">vs</span> {short(p['away'],17)}</div>
          <div class="tp-meta">{p['league']} · {p['date'][:10]}</div>
          {badge_html(p['conf'])}
          <div class="tp-bet">✅ {safe}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_metrics(all_preds: list, filtered: list):
    hi = max((p["conf"] for p in filtered), default=0)
    streaks = sum(1 for p in filtered if p.get("five"))
    flagged = sum(1 for p in filtered if p.get("flagged"))
    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-box">
        <div class="metric-val">{len(all_preds)}</div>
        <div class="metric-lbl">Fixtures loaded</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{len(filtered)}</div>
        <div class="metric-lbl">Qualifying</div>
        <div class="metric-sub">above min confidence</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{hi}%</div>
        <div class="metric-lbl">Top confidence</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{streaks}</div>
        <div class="metric-lbl">Win streaks</div>
        <div class="metric-sub">{flagged} flagged picks</div>
      </div>
    </div>""", unsafe_allow_html=True)

def render_card(p: dict):
    hf=p["hf"]; af=p["af"]
    hs=p.get("hs"); as_=p.get("as_")
    h2h=p.get("h2h",{})
    _,bar_col,_=conf_meta(p["conf"])

    streak_tag = '<span class="streak-tag">🔥 5-WIN STREAK</span>' if p.get("five") else ""
    card_cls   = "pred-card flagged" if p.get("flagged") else "pred-card"

    # Flagged banner
    if p.get("flagged"):
        st.markdown(f"""
        <div class="danger-banner">
          ⭐ <strong>Original Pick:</strong> 5-Win Streak + Odds ≤ 1.50
          — {p['home']} vs {p['away']} | Odds: {p['odds']}
        </div>""", unsafe_allow_html=True)

    # Card header
    st.markdown(f"""
    <div class="{card_cls}">
      <div class="match-header">
        <div>
          <div class="match-vs">{p['home']} <span>vs</span> {p['away']}{streak_tag}</div>
          <div class="match-meta">📅 {countdown(p['date'])} &nbsp;·&nbsp; 🏟 {p['league']}</div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          {badge_html(p['conf'])}<br>
          <span style="font-size:10px;color:#475569;margin-top:4px;display:block">
            {'Odds '+str(p['odds']) if p['odds'] else 'Odds N/A'}
          </span>
        </div>
      </div>

      {form_html(hf.get("form",[]), p['home'][:14]+"(H)")}
      {form_html(af.get("form",[]), p['away'][:14]+"(A)")}
      {conf_bar(p['conf'])}
    </div>""", unsafe_allow_html=True)

    # Stats row (outside card div — inside st container)
    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in [
        (c1, f"{hf['agf']:.1f}", "Home goals/g"),
        (c2, f"{hf['cs']}",      "Clean sheets"),
        (c3, f"{af['agf']:.1f}", "Away goals/g"),
        (c4, f"{af['aga']:.1f}", "Away conceded"),
    ]:
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-val">{val}</div>'
                        f'<div class="stat-lbl">{lbl}</div></div>',
                        unsafe_allow_html=True)

    # Standings caption
    if hs or as_:
        parts=[]
        if hs:  parts.append(f"{short(p['home'],14)}: {ordinal(hs['pos'])} · {hs['pts']}pts")
        if as_: parts.append(f"{short(p['away'],14)}: {ordinal(as_['pos'])} · {as_['pts']}pts")
        st.caption("  ·  ".join(parts))

    # Warnings
    if p["warns"]:
        w_html=" ".join(f'<span class="pill pill-warn">⚠️ {w}</span>' for w in p["warns"])
        st.markdown(f'<div class="pills-row">{w_html}</div>', unsafe_allow_html=True)

    # Safe bets
    if p["bets"]:
        b_html=" ".join(
            f'<span class="pill {"pill-safe" if b.get("safe") else "pill-bet"}">✅ {b["t"]} · {b["c"]}%</span>'
            for b in p["bets"][:4])
        st.markdown(f'<div class="sec-label" style="font-size:10px;color:#475569;margin:6px 0 3px;text-transform:uppercase;letter-spacing:.06em">Safe Bets</div>'
                    f'<div class="pills-row">{b_html}</div>',
                    unsafe_allow_html=True)

    # Why this prediction — expander
    with st.expander("🔍 Why this prediction?"):
        st.markdown(f"""
        <div class="why-box">
          <div class="why-quote">{p['expl']}</div>
        </div>""", unsafe_allow_html=True)

        # Confidence breakdown bars
        st.markdown("**📊 Confidence factors:**")
        for factor,pts in p["bd"].items():
            pct = int(pts/30*100)
            st.markdown(f"""
            <div class="breakdown-row">
              <span class="bdr-lbl">{factor}</span>
              <div class="bdr-bar"><div class="bdr-fill" style="width:{pct}%"></div></div>
              <span class="bdr-pts">+{pts}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="fiq">', unsafe_allow_html=True)

        # H2H
        if h2h.get("p",0):
            st.markdown(f"**🤝 H2H (last {h2h['p']}):** "
                        f"{p['home']} {h2h['w']}W – {h2h['d']}D – {h2h['l']}L {p['away']}")
            for row in h2h.get("rows",[]):
                icon={"win":"🟢","draw":"🟡","loss":"🔴"}.get(row["res"],"⚪")
                st.caption(f"{icon} {row['date']}  {row['home']} {row['score']} {row['away']}")
        else:
            st.caption("No H2H data available for this fixture.")

        st.markdown('<hr class="fiq">', unsafe_allow_html=True)

        # Venue records
        c_h,c_a=st.columns(2)
        with c_h:
            h=hf["home"]
            st.markdown("**🏠 Home record**")
            st.caption(f"{h['w']}W {h['d']}D {h['l']}L · GF {h['gf']} GA {h['ga']}")
        with c_a:
            a=af["away"]
            st.markdown("**✈️ Away record**")
            st.caption(f"{a['w']}W {a['d']}D {a['l']}L · GF {a['gf']} GA {a['ga']}")

        st.markdown('<hr class="fiq">', unsafe_allow_html=True)
        st.markdown("**📲 Copy for Telegram / WhatsApp:**")
        st.code(alert_text(p), language=None)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

def render_welcome():
    st.markdown("""
    <div class="empty-state" style="padding:2rem 0 1rem">
      <div class="emoji">⚽</div>
      <h3>Welcome to FootballIQ</h3>
      <p>Select a league from the sidebar and tap Load fixtures to get AI-powered predictions.</p>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="feat-grid">', unsafe_allow_html=True)
    feats = [
        ("📊","Advanced Form","Wins, draws, losses, goals & clean sheets from last 10 games"),
        ("🔥","Confidence Score","Weighted 0–100% with 9 scoring factors and full breakdown"),
        ("🎯","Safe Bets","Match Winner, Over 1.5, BTTS, Double Chance auto-generated"),
        ("🤝","Head-to-Head","Last 5 meetings analysed and weighted into the score"),
        ("⚡","Danger Warnings","Defence issues, away form, rotation risk auto-detected"),
        ("📲","Alert Ready","One-tap copy for Telegram & WhatsApp notifications"),
    ]
    for icon,title,desc in feats:
        st.markdown(f"""
        <div class="feat-card">
          <div class="feat-icon">{icon}</div>
          <div class="feat-title">{title}</div>
          <div class="feat-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# 7. SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Filters")
    sel_league   = st.selectbox("League", list(LEAGUES.keys()),
                                format_func=lambda k:LEAGUES[k])
    min_conf     = st.slider("Min confidence %", 0, 100, 40, 5)
    warns_only   = st.checkbox("⚠️ Danger matches only", False)
    streaks_only = st.checkbox("🔥 5-Win streak only",   False)
    st.divider()
    st.caption("⚡ Data cached 30 min\n\nPowered by football-data.org")

# ─────────────────────────────────────────────────────────────────
# 8. SESSION STATE
# ─────────────────────────────────────────────────────────────────
for k,v in [("preds",[]),("league","PL"),("loaded",False)]:
    if k not in st.session_state: st.session_state[k]=v

# ─────────────────────────────────────────────────────────────────
# 9. MAIN RENDER
# ─────────────────────────────────────────────────────────────────
render_hero()

# ── API key gate ──────────────────────────────────────────────────
if not api_check():
    st.error("🔑 API key missing or invalid.")
    st.markdown("**Streamlit Cloud:** App menu → Settings → Secrets, add:")
    st.code('API_KEY = "your_football_data_org_key"', language="toml")
    st.markdown("**Local dev:** `.streamlit/secrets.toml` with the same line.")
    st.stop()

# ── Load button ───────────────────────────────────────────────────
cb,ci = st.columns([2,3])
with cb:
    go = st.button("🔄  Load Fixtures", use_container_width=True)
with ci:
    st.caption(f"Up to {MAX_MATCHES} fixtures · 30-min cache · {LEAGUES.get(sel_league,'')}")

need = go or not st.session_state.loaded or st.session_state.league!=sel_league

if go or st.session_state.loaded:
    if need:
        st.session_state.league=sel_league
        with st.spinner("⚽ Fetching fixtures and building predictions…"):
            raw=api_upcoming(sel_league)
            built: list=[]
            prog=st.progress(0, text="Analysing teams…")
            total=min(len(raw),MAX_MATCHES)
            for i,m in enumerate(raw[:MAX_MATCHES]):
                try: built.append(build_pred(m,sel_league))
                except Exception: pass
                prog.progress(int((i+1)/max(total,1)*100),
                              text=f"Analysing {i+1}/{total}…")
            prog.empty()
        st.session_state.preds=built
        st.session_state.loaded=True

    all_p=st.session_state.preds

    # ── Filters ───────────────────────────────────────────────
    filt=[p for p in all_p if p["conf"]>=min_conf]
    if warns_only:   filt=[p for p in filt if p["warns"]]
    if streaks_only: filt=[p for p in filt if p.get("five")]
    srt=sorted(filt,key=lambda p:p["conf"],reverse=True)

    # ── Metrics ───────────────────────────────────────────────
    render_metrics(all_p, srt)
    st.markdown('<hr class="fiq">', unsafe_allow_html=True)

    # ── Highlights strip ──────────────────────────────────────
    if srt:
        render_highlights(srt)
        st.markdown('<hr class="fiq">', unsafe_allow_html=True)

    # ── Top 3 picks ───────────────────────────────────────────
    render_top_picks(srt)

    if srt:
        st.markdown('<hr class="fiq">', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-hdr">📋 All Predictions ({len(srt)})</div>',
                    unsafe_allow_html=True)
        for p in srt:
            render_card(p)
    else:
        st.markdown("""
        <div class="empty-state">
          <div class="emoji">🔍</div>
          <h3>No matches found</h3>
          <p>Try lowering the confidence threshold or removing filters in the sidebar.</p>
        </div>""", unsafe_allow_html=True)
else:
    render_welcome()
