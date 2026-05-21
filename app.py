from __future__ import annotations
"""
FootballIQ — Complete single-file Streamlit prediction platform.
DEPLOY: Push ONLY this file + requirements.txt to GitHub.
        Add API_KEY in Streamlit Cloud → Settings → Secrets.
NO other .py files needed. No imports from local modules.
"""

import os
import requests
import streamlit as st
from datetime import datetime, timezone

# ══════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be the very first Streamlit call)
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FootballIQ — Match Predictions",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
# GLOBAL CSS + LOGO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { padding: 0.5rem 1rem 4rem; max-width: 820px; margin: auto; }

/* ── Logo banner ── */
.logo-wrap {
    display: flex; align-items: center; gap: 16px;
    padding: 1.4rem 1.6rem;
    background: linear-gradient(135deg, #0d1b3e 0%, #1a2f5e 50%, #0d1b3e 100%);
    border-radius: 20px;
    border: 1px solid rgba(59,130,246,0.35);
    box-shadow: 0 8px 32px rgba(59,130,246,0.15);
    margin-bottom: 1.5rem;
}
.logo-icon {
    width: 68px; height: 68px; border-radius: 16px;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6, #60a5fa);
    display: flex; align-items: center; justify-content: center;
    font-size: 36px; flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(59,130,246,0.4);
}
.logo-text h1 {
    margin: 0; font-size: 28px !important; font-weight: 900;
    background: linear-gradient(90deg, #60a5fa, #93c5fd, #e2e8f0);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.logo-text p { margin: 2px 0 0; font-size: 13px; color: #64748b; }
.logo-live {
    margin-left: auto; background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.4); color: #4ade80;
    font-size: 11px; font-weight: 700; padding: 4px 12px;
    border-radius: 20px; letter-spacing: 0.05em;
    display: flex; align-items: center; gap: 5px;
}
.live-dot { width:7px; height:7px; background:#4ade80;
    border-radius:50%; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* ── Cards ── */
.pred-card {
    background: rgba(17,24,39,0.9);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px; padding: 1.3rem 1.5rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: border-color .2s;
}
.pred-card:hover { border-color: rgba(59,130,246,0.3); }

.top-card {
    background: linear-gradient(135deg, #0f2444 0%, #1e3a5f 100%);
    border: 1px solid rgba(99,153,255,0.25);
    border-radius: 18px; padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 20px rgba(30,58,95,0.4);
}

/* ── Badges ── */
.warn-badge {
    background: rgba(239,68,68,0.12); color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 8px; padding: 4px 11px;
    font-size: 12px; display: inline-block; margin: 2px 2px;
}
.bet-pill {
    background: rgba(59,130,246,0.12); color: #93c5fd;
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 20px; padding: 4px 13px;
    font-size: 12px; display: inline-block; margin: 2px 2px;
}
.streak-badge {
    background: linear-gradient(90deg,#f59e0b,#ef4444);
    color: #fff; border-radius: 20px; padding: 2px 10px;
    font-size: 11px; font-weight: 700; margin-left: 6px;
}
.sec-label {
    font-size: 10px; letter-spacing: .12em;
    text-transform: uppercase; color: #475569;
    margin-bottom: 4px; margin-top: 10px;
}

/* ── Stats grid ── */
.stat-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 10px 14px; text-align: center;
}
.stat-val { font-size: 22px; font-weight: 700; color: #e2e8f0; }
.stat-lbl { font-size: 11px; color: #64748b; margin-top: 2px; }

/* ── Misc ── */
h3 { font-size: 1.05rem !important; margin: 0 0 2px !important; }
.stButton > button {
    border-radius: 12px; font-weight: 600;
    background: linear-gradient(135deg,#1d4ed8,#3b82f6);
    border: none; color: #fff;
    box-shadow: 0 4px 14px rgba(59,130,246,0.35);
}
.stButton > button:hover { opacity: .9; }
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.2rem 0 !important; }

@media (max-width: 600px) {
    .block-container { padding: 0.3rem 0.5rem 3rem; }
    .logo-wrap { padding: 1rem; gap: 10px; }
    .logo-text h1 { font-size: 20px !important; }
    .logo-icon { width:52px; height:52px; font-size:26px; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# LOGO BANNER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="logo-wrap">
  <div class="logo-icon">⚽</div>
  <div class="logo-text">
    <h1>FootballIQ</h1>
    <p>AI-powered match predictions · form analysis · safe bets</p>
  </div>
  <div class="logo-live">
    <span class="live-dot"></span> LIVE
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════
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
    "EC":  "🌍 Euro Championship",
}

# ══════════════════════════════════════════════════════════════════
# API LAYER  — all cached, no duplicate calls
# ══════════════════════════════════════════════════════════════════
def _api_key() -> str:
    try:
        return st.secrets["API_KEY"]
    except Exception:
        return os.getenv("API_KEY", "")

def _hdr() -> dict:
    return {"X-Auth-Token": _api_key()}

def _get(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=_hdr(), timeout=12)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429:
            st.warning("⏳ Rate limit hit — wait 60 s then reload.")
        elif r.status_code == 403:
            st.error("🔑 API key invalid or plan restriction.")
        elif r.status_code != 404:
            st.warning(f"API error {r.status_code}")
    except requests.Timeout:
        st.warning("⌛ Request timed out — poor connection.")
    except requests.ConnectionError:
        st.warning("📡 No internet connection.")
    except Exception as exc:
        st.warning(f"Error: {exc}")
    return None

@st.cache_data(ttl=1800, show_spinner=False)
def api_upcoming(league: str) -> list:
    d = _get(f"{BASE_URL}/competitions/{league}/matches?status=SCHEDULED")
    return d.get("matches", []) if d else []

@st.cache_data(ttl=1800, show_spinner=False)
def api_team_matches(team_id: int, limit: int = 10) -> list:
    d = _get(f"{BASE_URL}/teams/{team_id}/matches?status=FINISHED&limit={limit}")
    return d.get("matches", []) if d else []

@st.cache_data(ttl=3600, show_spinner=False)
def api_standings(league: str) -> list:
    d = _get(f"{BASE_URL}/competitions/{league}/standings")
    if not d:
        return []
    try:
        return d["standings"][0]["table"]
    except (KeyError, IndexError):
        return []

@st.cache_data(ttl=1800, show_spinner=False)
def api_h2h(match_id: int) -> list:
    d = _get(f"{BASE_URL}/matches/{match_id}/head2head?limit=5")
    return d.get("matches", []) if d else []

@st.cache_data(ttl=86400, show_spinner=False)
def api_check_key() -> bool:
    return _get(f"{BASE_URL}/competitions/PL") is not None

# ══════════════════════════════════════════════════════════════════
# UTILITIES
# ══════════════════════════════════════════════════════════════════
ICONS = {"win": "🟢", "draw": "🟡", "loss": "🔴"}

def form_strip(results: list) -> str:
    return " ".join(ICONS.get(r, "⚪") for r in results)

def conf_label(score: int) -> tuple:
    if score >= 80: return "Very High", "#22c55e"
    if score >= 60: return "High",      "#84cc16"
    if score >= 40: return "Medium",    "#f59e0b"
    return "Low", "#ef4444"

def conf_badge(score: int) -> str:
    lbl, col = conf_label(score)
    return (f'<span style="background:{col};color:#000;padding:4px 13px;'
            f'border-radius:20px;font-size:12px;font-weight:800;letter-spacing:.02em">'
            f'{lbl} {score}%</span>')

def countdown(utc: str) -> str:
    try:
        dt = datetime.fromisoformat(utc.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = dt - now
        if diff.total_seconds() < 0:
            return "Already kicked off"
        d = diff.days
        h = int(diff.total_seconds() // 3600) % 24
        if d == 0: return f"Today — in {h}h"
        if d == 1: return f"Tomorrow {dt.strftime('%H:%M')} UTC"
        return f"In {d}d {h}h — {dt.strftime('%d %b, %H:%M')} UTC"
    except Exception:
        return utc[:10] if utc else "TBD"

def ordinal(n: int) -> str:
    s = {1:"st",2:"nd",3:"rd"}.get(n%10 if n%100 not in (11,12,13) else 0,"th")
    return f"{n}{s}"

def short(name: str, n: int = 20) -> str:
    return name if len(name) <= n else name[:n-1] + "…"

def alert_text(pred: dict) -> str:
    return (f"⚽ {pred['home']} vs {pred['away']}\n"
            f"🏆 {pred['league']}\n"
            f"📊 Confidence: {pred['confidence']}% ({pred['conf_lbl']})\n"
            f"✅ Best bet: {pred['best_bet']}\n"
            f"⏰ {countdown(pred.get('date',''))}\n"
            f"💡 {pred.get('explanation','')}")

# ══════════════════════════════════════════════════════════════════
# PREDICTION ENGINE
# ══════════════════════════════════════════════════════════════════
def _vblock() -> dict:
    return {"played":0,"wins":0,"draws":0,"losses":0,"gf":0,"ga":0}

def _empty() -> dict:
    return {"played":0,"wins":0,"draws":0,"losses":0,"gf":0,"ga":0,
            "gd":0,"cs":0,"streak":0,"five":False,"avg_gf":0.0,"avg_ga":0.0,
            "form":[],"home":_vblock(),"away":_vblock()}

def analyse_form(team_id: int) -> dict:
    matches = api_team_matches(team_id, limit=10)
    if not matches:
        return _empty()
    s = _empty()
    f5: list = []
    streak = 0
    for m in matches:
        ih = m["homeTeam"]["id"] == team_id
        mg = m["score"]["fullTime"].get("home" if ih else "away") or 0
        og = m["score"]["fullTime"].get("away" if ih else "home") or 0
        w  = m["score"].get("winner","")
        if w == "HOME_TEAM":   res = "win"  if ih else "loss"
        elif w == "AWAY_TEAM": res = "loss" if ih else "win"
        elif w == "DRAW":      res = "draw"
        else:                  res = "unknown"
        s["played"]+=1; s["gf"]+=mg; s["ga"]+=og
        if res=="win":    s["wins"]+=1;   streak+=1
        elif res=="draw": s["draws"]+=1;  streak=0
        elif res=="loss": s["losses"]+=1; streak=0
        if og==0: s["cs"]+=1
        v = s["home"] if ih else s["away"]
        v["played"]+=1; v["gf"]+=mg; v["ga"]+=og
        if res=="win":    v["wins"]+=1
        elif res=="draw": v["draws"]+=1
        elif res=="loss": v["losses"]+=1
        if len(f5)<5: f5.append(res)
    s["streak"] = streak
    s["form"]   = list(reversed(f5))
    s["gd"]     = s["gf"] - s["ga"]
    s["avg_gf"] = round(s["gf"]/max(s["played"],1),2)
    s["avg_ga"] = round(s["ga"]/max(s["played"],1),2)
    s["five"]   = _five_wins(matches, team_id)
    return s

def _five_wins(matches: list, tid: int) -> bool:
    if len(matches) < 5: return False
    return all(
        (m["score"]["winner"]=="HOME_TEAM" and m["homeTeam"]["id"]==tid) or
        (m["score"]["winner"]=="AWAY_TEAM" and m["awayTeam"]["id"]==tid)
        for m in matches[:5]
    )

def get_standing(team_id: int, league: str) -> dict | None:
    for row in api_standings(league):
        if row.get("team",{}).get("id") == team_id:
            return {"pos":row.get("position"),"pts":row.get("points"),
                    "gd":row.get("goalDifference"),"played":row.get("playedGames")}
    return None

def calc_h2h(match_id: int, focus_id: int) -> dict:
    r: dict = {"played":0,"wins":0,"draws":0,"losses":0,"rows":[]}
    for m in api_h2h(match_id):
        ih = m["homeTeam"]["id"] == focus_id
        mg = m["score"]["fullTime"].get("home" if ih else "away") or 0
        og = m["score"]["fullTime"].get("away" if ih else "home") or 0
        w  = m["score"].get("winner","DRAW")
        r["played"]+=1
        if w=="DRAW":                                               res="draw"; r["draws"]+=1
        elif (w=="HOME_TEAM" and ih) or (w=="AWAY_TEAM" and not ih): res="win";  r["wins"]+=1
        else:                                                         res="loss"; r["losses"]+=1
        r["rows"].append({"date":m.get("utcDate","")[:10],
                          "home":m["homeTeam"]["name"],"away":m["awayTeam"]["name"],
                          "score":f"{m['score']['fullTime']['home']}–{m['score']['fullTime']['away']}",
                          "res":res})
    return r

def calc_confidence(hf, af, hs, as_, h2h, home_odds) -> tuple:
    sc=0; bd: dict={}
    if hf.get("five"):          sc+=30; bd["5-win streak"]=30
    ow=sum(1 for r in af.get("form",[]) if r=="win")
    if ow<=1:                   sc+=20; bd["Opponent poor form"]=20
    if hf["home"].get("wins",0)>=3: sc+=15; bd["Home advantage"]=15
    if hf.get("avg_gf",0)>=2.0: sc+=15; bd["Strong goalscoring"]=15
    if hf.get("cs",0)>=2:       sc+=10; bd["Clean sheets"]=10
    if home_odds and home_odds<=1.50: sc+=10; bd["Odds ≤ 1.50"]=10
    if h2h.get("wins",0)>=3:    sc+=5;  bd["H2H dominance"]=5
    if hs and hs.get("pos",99)<=6: sc+=5; bd["Top-6 position"]=5
    return min(sc,100), bd

def gen_bets(hf: dict, af: dict, conf: int) -> list:
    bets: list=[]
    ag = hf["avg_gf"] + af["avg_gf"]
    if conf>=70: bets.append({"t":"Match Winner","r":"High confidence from current form","c":conf})
    if ag>=2.2:  bets.append({"t":"Over 1.5 Goals","r":f"Avg {ag:.1f} goals/game combined","c":min(90,int(ag*25))})
    if ag>=3.0:  bets.append({"t":"Over 2.5 Goals","r":"Both teams score freely","c":min(85,int(ag*20))})
    if hf["cs"]<=1 and af["cs"]<=1 and ag>=2.5:
        bets.append({"t":"Both Teams To Score","r":"Neither side keeps clean sheets","c":65})
    if 45<=conf<70: bets.append({"t":"Double Chance","r":"Moderate form — wider coverage","c":conf+10})
    if conf>=55:    bets.append({"t":"Draw No Bet","r":"Protect stake on in-form team","c":conf+5})
    return sorted(bets,key=lambda x:x["c"],reverse=True)

def gen_warnings(hf: dict, af: dict) -> list:
    w: list=[]
    if af.get("five"):                       w.append("⚠️ Opponent also on 5-game win streak")
    if hf.get("avg_ga",0)>2.0:              w.append("🛡️ Shaky defence — 2+ goals conceded/game")
    if hf.get("away",{}).get("losses",0)>=3: w.append("✈️ Poor away record recently")
    if hf.get("form",[]).count("loss")>=3:   w.append("📉 3 losses in last 5 — form collapse risk")
    if hf.get("gd",0)<0:                     w.append("⚡ Negative goal difference")
    if hf.get("gf",0)<4 and hf.get("played",0)>=5: w.append("🔄 Low output — rotation risk")
    return w

def gen_explanation(hn,an,hf,af,hs,as_,h2h,conf) -> str:
    p: list=[]
    if hf.get("five"):          p.append(f"{hn} are on a 5-game winning streak")
    elif hf.get("streak",0)>=3: p.append(f"{hn} have won {hf['streak']} in a row")
    if hf.get("gf",0)>=10:     p.append(f"scoring {hf['gf']} goals in {hf.get('played',5)} games")
    al = af.get("away",{}).get("losses",0)
    if al>=3:                   p.append(f"{an} have lost {al} recent away fixtures")
    elif af.get("five"):        p.append(f"{an} are also in excellent form — caution advised")
    if hs and as_ and hs["pos"]<as_["pos"]:
        p.append(f"{hn} sit {ordinal(hs['pos'])} vs {an} in {ordinal(as_['pos'])}")
    if h2h.get("played",0)>=3: p.append(f"H2H: {hn} lead {h2h['wins']}–{h2h['losses']}")
    lbl,_=conf_label(conf); p.append(f"Confidence: {lbl.lower()} ({conf}%)")
    return (". ".join(p).capitalize()+".") if p else "Insufficient data for analysis."

def build_pred(match: dict, league: str) -> dict:
    hid=match["homeTeam"]["id"]; aid=match["awayTeam"]["id"]
    hn =match["homeTeam"]["name"]; an=match["awayTeam"]["name"]
    mid=match.get("id")
    hf=analyse_form(hid); af=analyse_form(aid)
    hs=get_standing(hid,league); as_=get_standing(aid,league)
    h2h=calc_h2h(mid,hid) if mid else {}
    odds=match.get("odds",{}).get("homeWin")
    conf,bd=calc_confidence(hf,af,hs,as_,h2h,odds)
    lbl,col=conf_label(conf)
    bets=gen_bets(hf,af,conf); warns=gen_warnings(hf,af)
    expl=gen_explanation(hn,an,hf,af,hs,as_,h2h,conf)
    return {
        "match_id":mid,"home":hn,"away":an,"home_id":hid,"away_id":aid,
        "league":league,"date":match.get("utcDate",""),
        "hf":hf,"af":af,"hs":hs,"as_":as_,"h2h":h2h,
        "confidence":conf,"conf_lbl":lbl,"conf_col":col,"bd":bd,
        "bets":bets,"warns":warns,"explanation":expl,
        "best_bet":bets[0]["t"] if bets else "Match Winner",
        "odds":odds,
        "five": hf.get("five") or af.get("five"),
        "low_odds": bool(odds and odds<=1.50),
    }

# ══════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════
def render_top_picks(preds: list):
    top3=sorted(preds,key=lambda p:p["confidence"],reverse=True)[:3]
    if not top3: return
    st.markdown("### 🏆 Today's Top 3 Picks")
    cols=st.columns(len(top3))
    medals=["🥇","🥈","🥉"]
    for i,(col,p) in enumerate(zip(cols,top3)):
        with col:
            st.markdown(f"""
            <div class="top-card">
              <div style="font-size:28px;margin-bottom:6px">{medals[i]}</div>
              <div style="font-weight:800;font-size:13px;line-height:1.4;margin-bottom:6px;color:#e2e8f0">
                {short(p['home'],16)}<br>vs {short(p['away'],16)}
              </div>
              <div style="font-size:11px;color:#475569;margin-bottom:10px">
                {p['league']} · {p['date'][:10]}
              </div>
              {conf_badge(p['confidence'])}
              <div style="font-size:12px;margin-top:8px;color:#93c5fd">✅ {p['best_bet']}</div>
            </div>""", unsafe_allow_html=True)

def render_card(pred: dict):
    hf=pred["hf"]; af=pred["af"]
    hs=pred.get("hs"); as_=pred.get("as_")
    h2h=pred.get("h2h",{})

    streak_html = '<span class="streak-badge">🔥 5W Streak</span>' if pred.get("five") else ""

    st.markdown(f"""
    <div class="pred-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
        <div>
          <h3>{pred['home']} vs {pred['away']}{streak_html}</h3>
          <div style="font-size:12px;color:#64748b;margin-top:2px">
            📅 {countdown(pred['date'])} &nbsp;·&nbsp; 🏟 {pred['league']}
          </div>
        </div>
        <div>{conf_badge(pred['confidence'])}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Form strips + standings in columns
    col_h, col_a = st.columns(2)
    with col_h:
        st.markdown('<div class="sec-label">Home form (last 5)</div>', unsafe_allow_html=True)
        st.markdown(form_strip(hf["form"]) or "—")
        if hs: st.caption(f"{ordinal(hs['pos'])} place · {hs['pts']} pts · GD {hs['gd']:+d}")
    with col_a:
        st.markdown('<div class="sec-label">Away form (last 5)</div>', unsafe_allow_html=True)
        st.markdown(form_strip(af["form"]) or "—")
        if as_: st.caption(f"{ordinal(as_['pos'])} place · {as_['pts']} pts · GD {as_['gd']:+d}")

    # Stats row
    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in [(c1,f"{hf['avg_gf']:.1f}","Home avg goals"),
                         (c2,f"{hf['cs']}","Home clean sheets"),
                         (c3,f"{af['avg_gf']:.1f}","Away avg goals"),
                         (c4,f"{af['avg_ga']:.1f}","Away conceded")]:
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-val">{val}</div>'
                        f'<div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Warnings
    if pred["warns"]:
        st.markdown(
            " ".join(f'<span class="warn-badge">{w}</span>' for w in pred["warns"]),
            unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Safe bets
    if pred["bets"]:
        st.markdown('<div class="sec-label">Safe bet options</div>', unsafe_allow_html=True)
        st.markdown(
            " ".join(f'<span class="bet-pill">✅ {b["t"]} · {b["c"]}%</span>'
                     for b in pred["bets"][:4]),
            unsafe_allow_html=True)

    # Expander — full analysis
    with st.expander("🔍 Why this prediction?"):
        st.markdown(f"**💡 Analysis:** {pred['explanation']}")
        st.divider()

        # Confidence breakdown
        st.markdown("**📊 Confidence breakdown:**")
        for factor,pts in pred["bd"].items():
            bar = int(pts/30*100)
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;margin:4px 0">'
                f'<span style="width:160px;font-size:13px;color:#94a3b8">{factor}</span>'
                f'<div style="flex:1;background:rgba(255,255,255,0.06);border-radius:6px;height:8px">'
                f'<div style="width:{bar}%;background:#3b82f6;height:100%;border-radius:6px"></div></div>'
                f'<span style="font-size:13px;color:#60a5fa;font-weight:700">+{pts}</span></div>',
                unsafe_allow_html=True)

        st.divider()

        # H2H
        if h2h.get("played",0):
            st.markdown(f"**🤝 Head-to-Head (last {h2h['played']} meetings):** "
                        f"{pred['home']} {h2h['wins']}W – {h2h['draws']}D – {h2h['losses']}L {pred['away']}")
            for row in h2h.get("rows",[]):
                icon={"win":"🟢","draw":"🟡","loss":"🔴"}.get(row["res"],"⚪")
                st.caption(f"{icon} {row['date']}  {row['home']} {row['score']} {row['away']}")
        else:
            st.caption("H2H data not available for this fixture.")

        st.divider()

        # Home/Away records
        col_hv, col_av = st.columns(2)
        with col_hv:
            h=hf["home"]
            st.markdown("**Home record**")
            st.caption(f"{h['wins']}W · {h['draws']}D · {h['losses']}L  |  GF {h['gf']} GA {h['ga']}")
        with col_av:
            a=af["away"]
            st.markdown("**Away record**")
            st.caption(f"{a['wins']}W · {a['draws']}D · {a['losses']}L  |  GF {a['gf']} GA {a['ga']}")

        st.divider()
        st.markdown("**📲 Copy for Telegram / WhatsApp:**")
        st.code(alert_text(pred), language=None)

    st.markdown("")

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Filters")
    sel_league   = st.selectbox("League", list(LEAGUES.keys()),
                                format_func=lambda k: LEAGUES[k])
    min_conf     = st.slider("Min confidence %", 0, 100, 40, 5)
    warns_only   = st.checkbox("Danger matches only", False)
    st.divider()
    st.caption("football-data.org · 30-min cache")

# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
for key, val in [("preds",[]),("league","PL"),("loaded",False)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════
# API KEY CHECK
# ══════════════════════════════════════════════════════════════════
if not api_check_key():
    st.error("🔑 API key missing or invalid.")
    st.markdown("**Streamlit Cloud:** App menu → Settings → Secrets, then add:")
    st.code('API_KEY = "your_football_data_org_key"', language="toml")
    st.markdown("**Local:** create `.streamlit/secrets.toml` with the same line.")
    st.stop()

# ══════════════════════════════════════════════════════════════════
# LOAD BUTTON
# ══════════════════════════════════════════════════════════════════
c_btn, c_info = st.columns([2,3])
with c_btn:
    load_clicked = st.button("🔄  Load fixtures", use_container_width=True)
with c_info:
    st.caption("Fixtures cached 30 min · up to 20 matches analysed per league")

need_reload = (load_clicked or not st.session_state.loaded
               or st.session_state.league != sel_league)

if load_clicked or st.session_state.loaded:
    if need_reload:
        st.session_state.league = sel_league
        with st.spinner("⚽ Fetching fixtures and analysing form…"):
            raw = api_upcoming(sel_league)
            built: list = []
            prog = st.progress(0)
            total = min(len(raw), 20)
            for i, m in enumerate(raw[:20]):
                try:
                    built.append(build_pred(m, sel_league))
                except Exception:
                    pass
                prog.progress(int((i+1)/max(total,1)*100))
            prog.empty()
        st.session_state.preds  = built
        st.session_state.loaded = True

    all_preds = st.session_state.preds

    # ── Filters ────────────────────────────────────────────────────
    filtered = [p for p in all_preds if p["confidence"] >= min_conf]
    if warns_only:
        filtered = [p for p in filtered if p["warns"]]
    sorted_preds = sorted(filtered, key=lambda p: p["confidence"], reverse=True)

    # ── Original feature: 5-win streak + low odds ──────────────────
    flagged = [p for p in sorted_preds if p["five"] and p["low_odds"]]
    if flagged:
        st.markdown("### 🚨 Original Picks — 5-Win Streak + Odds ≤ 1.50")
        for p in flagged:
            st.success(f"**{p['home']}** vs {p['away']}  |  Odds: {p['odds']}  |  {p['league']}")
        st.divider()

    # ── Summary metrics ────────────────────────────────────────────
    if sorted_preds:
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Fixtures", len(all_preds))
        m2.metric("Qualifying", len(sorted_preds))
        m3.metric("Top confidence", f"{sorted_preds[0]['confidence']}%" if sorted_preds else "—")
        m4.metric("5-Win streaks", sum(1 for p in sorted_preds if p["five"]))

        st.divider()

    # ── Top 3 picks ────────────────────────────────────────────────
    render_top_picks(sorted_preds)

    if sorted_preds:
        st.divider()
        st.markdown(f"### 📋 All Predictions ({len(sorted_preds)} matches)")
        for p in sorted_preds:
            render_card(p)
    else:
        st.info("🔍 No matches meet your filters. Lower the confidence slider or change league.")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem 2rem">
      <div style="font-size:64px;margin-bottom:1rem">⚽</div>
      <h2 style="color:#e2e8f0;margin-bottom:.5rem">Welcome to FootballIQ</h2>
      <p style="color:#64748b;font-size:15px;max-width:500px;margin:0 auto 2rem">
        Select a league from the sidebar and tap <strong>Load fixtures</strong> to see
        AI-powered predictions with confidence scoring, form analysis, and safe bet recommendations.
      </p>
    </div>
    """, unsafe_allow_html=True)

    f1,f2,f3 = st.columns(3)
    for col,icon,title,desc in [
        (f1,"📊","Form Analysis","Wins, draws, losses, goals, clean sheets from last 10 games"),
        (f2,"🔥","Confidence Score","Weighted 0–100% score with full reasoning breakdown"),
        (f3,"🎯","Safe Bets","Auto-generated bet types: Match Winner, Over 1.5, BTTS & more"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-box" style="padding:1.2rem;text-align:left">
              <div style="font-size:28px;margin-bottom:8px">{icon}</div>
              <div style="font-weight:700;font-size:14px;margin-bottom:4px;color:#e2e8f0">{title}</div>
              <div style="font-size:12px;color:#64748b;line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    f4,f5,f6 = st.columns(3)
    for col,icon,title,desc in [
        (f4,"🤝","Head-to-Head","Last 5 meetings between the teams analysed"),
        (f5,"⚡","Danger Warnings","Defence issues, poor away form, rotation risk flagged"),
        (f6,"📲","Alert Ready","One-tap copy for Telegram & WhatsApp notifications"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-box" style="padding:1.2rem;text-align:left">
              <div style="font-size:28px;margin-bottom:8px">{icon}</div>
              <div style="font-weight:700;font-size:14px;margin-bottom:4px;color:#e2e8f0">{title}</div>
              <div style="font-size:12px;color:#64748b;line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)
