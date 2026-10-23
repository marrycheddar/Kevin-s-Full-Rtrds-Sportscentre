import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# ====================== CONFIG ======================
LEAGUE_ID = "1380669652224454656"
BASE = "https://api.sleeper.app/v1"
PASSWORD = "buffalo"

PERSONALITIES = {
    "Doug Flutie": "Winnie the Pooh. Famous for no-showing group events. Career bronze player. Best friend is a homeless man named Kevin.",
    "All you need is LOVE": "Conspiracy theorist. Successful fantasy player. Loves chirping. Packers fan.",
    "Justin Credible": "Known as Donner. Huge calves. Turns into Slack Jaw when intoxicated.",
    "Team Swedish Meatball": "JP. Career non-playoff manager. Loves Randy Couture and Sportchek.",
    "Run cmc": "Sean (Colossus / Donkey Kong). Balding badly. Can't name 5 NFL QBs. Degenerate gambler.",
    "JUDKINSRICECORRECTIONAL": "Todd – last year's champion who still hasn't received his trophy. Rival of One Time.",
    '"nine"': "Timmers. Likes men's butts. Wears a tie and loosens it after work. Vikings fan.",
    "Jabberwocky69": "Trav. Loves high-end sports cars and Josh Allen. Looks like Littlefinger.",
    "Pink Socks": "Mike. Acts like a grandpa. Loves the Habs. Towel-whipping champion.",
    "Raiders": "Jonesy. Barely talks. Die-hard Raiders fan. Used to get launched into sidewalks in a shopping cart.",
    "Hurts When I PPR": "Jason (Jay). Eagles fan. Platinum status but has been terrible. Loves Tootoo and hotdog costumes.",
    "One Time": "The Rat / Master Splinter. Lots of past success, terrible this year. 49ers fan. Weasel.",
}

# Random ticker facts
TICKER_FACTS = [
    "Doug Flutie is still waiting for Kevin to show up to a league event.",
    "All you need is LOVE believes the league is controlled by lizard people.",
    "Justin Credible's calves have their own Instagram.",
    "Team Swedish Meatball has never made the playoffs. Ever.",
    "Run cmc still thinks the NFL has 12 teams.",
    "JUDKINSRICECORRECTIONAL is still waiting for last year's trophy.",
    "Timmers (nine) rates every league meeting by butt quality.",
    "Jabberwocky69's car collection is worth more than the league prize pool.",
    "Pink Socks once towel-whipped three managers in one night.",
    "Jonesy (Raiders) has spoken 11 words in league chat this season.",
    "Hurts When I PPR showed up to the draft in a hotdog costume.",
    "One Time is currently in last place after years of dominance.",
    "The league still has no official commissioner. Chaos reigns.",
    "Someone once tried to trade a player for a case of beer. It almost worked.",
]

# ====================== PAGE SETUP ======================
st.set_page_config(
    page_title="Full R*tards Network",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern clean CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #0b0f19;
        color: #e5e7eb;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    h1 {
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        color: #f8fafc !important;
        margin-bottom: 0.25rem !important;
    }
    
    h2, h3 {
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        letter-spacing: -0.02em;
    }
    
    /* Ticker */
    .ticker-wrap {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1.75rem;
        height: 42px;
        display: flex;
        align-items: center;
    }
    
    .ticker {
        display: flex;
        white-space: nowrap;
        animation: ticker 45s linear infinite;
    }
    
    .ticker span {
        padding: 0 2.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        color: #94a3b8;
    }
    
    .ticker span::before {
        content: "•";
        color: #f59e0b;
        margin-right: 1.25rem;
    }
    
    @keyframes ticker {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    
    /* Cards */
    .card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        height: 100%;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Standings table polish */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Buttons */
    .stButton > button {
        background: #f59e0b !important;
        color: #0b0f19 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.4rem !important;
    }
    
    .stButton > button:hover {
        background: #fbbf24 !important;
    }
    
    /* Video box */
    .video-box {
        background: #111827;
        border: 1px dashed #334155;
        border-radius: 14px;
        padding: 2rem;
        text-align: center;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# ====================== PASSWORD ======================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("Full R*tards Network")
    st.write("Private league broadcast")
    pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
    if st.button("Enter"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# ====================== DATA ======================
@st.cache_data(ttl=300)
def get_json(url):
    r = requests.get(url, timeout=12)
    r.raise_for_status()
    return r.json()

def get_current_week():
    state = get_json(f"{BASE}/state/nfl")
    return state.get("week", 1), state.get("season", "2026")

def load_data():
    users = get_json(f"{BASE}/league/{LEAGUE_ID}/users")
    rosters = get_json(f"{BASE}/league/{LEAGUE_ID}/rosters")
    
    user_map = {}
    for u in users:
        name = (u.get("metadata") or {}).get("team_name") or u.get("display_name") or "Unknown"
        user_map[u["user_id"]] = name.strip()
    
    standings = []
    for r in rosters:
        owner = user_map.get(r.get("owner_id"), f"Roster {r['roster_id']}")
        s = r.get("settings", {})
        standings.append({
            "Team": owner,
            "W": s.get("wins", 0),
            "L": s.get("losses", 0),
            "T": s.get("ties", 0),
            "PF": round(s.get("fpts", 0), 1),
            "PA": round(s.get("fpts_against", 0), 1),
            "roster_id": r["roster_id"],
        })
    
    standings = sorted(standings, key=lambda x: (-x["W"], -x["PF"]))
    for i, row in enumerate(standings, 1):
        row["Rank"] = i
    return standings

week, season = get_current_week()
standings = load_data()
matchups_raw = get_json(f"{BASE}/league/{LEAGUE_ID}/matchups/{week}")

matchup_groups = {}
for m in matchups_raw:
    mid = m.get("matchup_id")
    if mid not in matchup_groups:
        matchup_groups[mid] = []
    matchup_groups[mid].append(m)

# ====================== TICKER ======================
random.shuffle(TICKER_FACTS)
ticker_content = "".join([f"<span>{fact}</span>" for fact in TICKER_FACTS * 2])

st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker">
        {ticker_content}
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.title("Full R*tards Network")
st.caption(f"Week {week}  ·  {season} Season  ·  Live from the league of chaos")

st.markdown("<br>", unsafe_allow_html=True)

# ====================== STANDINGS + POWER ======================
col1, col2 = st.columns([1.6, 1], gap="large")

with col1:
    st.subheader("Standings")
    df = pd.DataFrame(standings)[["Rank", "Team", "W", "L", "PF", "PA"]]
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn(width="small"),
            "Team": st.column_config.TextColumn(width="medium"),
            "W": st.column_config.NumberColumn(width="small"),
            "L": st.column_config.NumberColumn(width="small"),
            "PF": st.column_config.NumberColumn(format="%.1f"),
            "PA": st.column_config.NumberColumn(format="%.1f"),
        }
    )

with col2:
    st.subheader("Power Rankings")
    power = []
    for s in standings:
        score = (s["W"] * 3.2) + (s["PF"] / 95)
        power.append((s["Team"], score, s["Rank"]))
    power = sorted(power, key=lambda x: -x[1])
    
    for i, (team, score, official) in enumerate(power, 1):
        delta = official - i
        if delta > 0:
            arrow = f"<span style='color:#22c55e'>↑{delta}</span>"
        elif delta < 0:
            arrow = f"<span style='color:#ef4444'>↓{abs(delta)}</span>"
        else:
            arrow = "<span style='color:#64748b'>—</span>"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:0.45rem 0; border-bottom:1px solid #1f2937;">
            <div style="font-weight:600;">{i}. {team}</div>
            <div>{arrow}</div>
        </div>
        """, unsafe_allow_html=True)

# ====================== MATCHUPS ======================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(f"Week {week} Scoreboard")

cols = st.columns(3, gap="medium")
for idx, (mid, teams) in enumerate(sorted(matchup_groups.items())):
    if len(teams) != 2:
        continue
    t1, t2 = teams
    name1 = next((s["Team"] for s in standings if s["roster_id"] == t1["roster_id"]), "TBD")
    name2 = next((s["Team"] for s in standings if s["roster_id"] == t2["roster_id"]), "TBD")
    pts1 = t1.get("points") or 0
    pts2 = t2.get("points") or 0
    
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:0.75rem;">
                <div style="font-weight:600; font-size:0.95rem;">{name1}</div>
                <div class="metric-value" style="font-size:1.4rem;">{pts1:.1f}</div>
            </div>
            <div style="height:1px; background:#1f2937; margin:0.5rem 0;"></div>
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <div style="font-weight:600; font-size:0.95rem;">{name2}</div>
                <div class="metric-value" style="font-size:1.4rem;">{pts2:.1f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================== CHIRP ======================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Chirp of the Week")
worst = min(standings, key=lambda x: x["PF"])
st.info(f"**{worst['Team']}** currently owns the golden boot. {PERSONALITIES.get(worst['Team'], '')}")

# ====================== BROADCAST ======================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("The Broadcast")

st.markdown("Paste this week’s Ron Burgundy video link below (YouTube unlisted or direct link).")

video_url = st.text_input("Video URL", placeholder="https://youtube.com/watch?v=...", label_visibility="collapsed")

if video_url:
    st.video(video_url)
else:
    st.markdown("""
    <div class="video-box">
        No video this week yet.<br>
        Generate one with the script below and paste the link.
    </div>
    """, unsafe_allow_html=True)

def build_script():
    lines = []
    lines.append(f"Hello, I’m Ron Burgundy. This is the Full R*tards Network. Week {week} recap.")
    leader = standings[0]
    lines.append(f"At the top sits {leader['Team']} at {leader['W']}-{leader['L']}. {PERSONALITIES.get(leader['Team'], '')}")
    for s in standings[1:4]:
        lines.append(f"{s['Team']} sits at {s['W']}-{s['L']}. {PERSONALITIES.get(s['Team'], '')}")
    bottom = standings[-1]
    lines.append(f"And at the bottom we find {bottom['Team']}. {PERSONALITIES.get(bottom['Team'], '')}")
    lines.append("Stay classy, Full R*tards. This has been Ron Burgundy. Good night.")
    return " ".join(lines)

script = build_script()

with st.expander("This week’s script (copy for your video)"):
    st.write(script)

st.caption(f"Updated {datetime.now().strftime('%b %d, %Y %H:%M')}  ·  Data via Sleeper")
