import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ====================== CONFIG ======================
LEAGUE_ID = "1380669652224454656"
BASE = "https://api.sleeper.app/v1"
PASSWORD = "buffalo"

PERSONALITIES = {
    "Doug Flutie": "Winnie the Pooh. Famous for no-showing group events and being a career bronze-level fantasy player. Best friend is a homeless man named Kevin.",
    "All you need is LOVE": "Conspiracy theorist, successful fantasy player, loves chirping everyone, and is a Packers fan. (That's you!)",
    "Justin Credible": "Known as Donner. Huge calves. When intoxicated turns into Slack Jaw – a walking hazard.",
    "Team Swedish Meatball": "JP. Career non-playoff manager. Loves Randy Couture and Sportchek.",
    "Run cmc": "Sean, aka Colossus / Donkey Kong. Balding badly. Can't name 5 NFL quarterbacks. Degenerate gambler.",
    "JUDKINSRICECORRECTIONAL": "Todd – last year's champion who still hasn't received his trophy. Big rival of One Time.",
    '"nine"': "Timmers. Likes to see men's butts. Wears a tie and loosens it after a hard day's work. Vikings fan.",
    "Jabberwocky69": "Trav. Loves high-end sports cars and Josh Allen. Looks like Littlefinger from Game of Thrones.",
    "Pink Socks": "Mike. Acts like a grandpa. Loves the Habs. Reigning towel-whipping champion.",
    "Raiders": "Jonesy. Barely talks to the rest of the league. Die-hard Raiders fan. Used to get pushed around in a shopping cart into sidewalks.",
    "Hurts When I PPR": "Jason (Jay). Eagles fan. Has platinum status but has been terrible since joining. Loves dressing up in Tootoos and hotdog costumes.",
    "One Time": "Aka The Rat / Master Splinter. Has had a lot of success but is terrible this year. 49ers fan. Weasel.",
}

# ====================== PAGE SETUP ======================
st.set_page_config(
    page_title="Full R*tards Network",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS – sports broadcast look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0e17 0%, #111827 100%);
        color: #e5e7eb;
    }
    h1, h2, h3 {
        color: #fbbf24 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    .stMetric {
        background: #1f2937;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 16px;
    }
    .broadcast-card {
        background: #1f2937;
        border: 1px solid #374151;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .ticker {
        background: #b91c1c;
        color: white;
        padding: 8px 16px;
        font-weight: 700;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
    }
    div[data-testid="stSidebar"] {
        background: #111827;
    }
</style>
""", unsafe_allow_html=True)

# ====================== PASSWORD ======================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🏈 Full R*tards Network")
    st.write("Private league broadcast. Enter the password to continue.")
    pwd = st.text_input("Password", type="password")
    if st.button("Enter the Network"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password. Try again.")
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
    return user_map, standings

week, season = get_current_week()
user_map, standings = load_data()
matchups_raw = get_json(f"{BASE}/league/{LEAGUE_ID}/matchups/{week}")

# Group matchups
matchup_groups = {}
for m in matchups_raw:
    mid = m.get("matchup_id")
    if mid not in matchup_groups:
        matchup_groups[mid] = []
    matchup_groups[mid].append(m)

# ====================== HEADER ======================
st.markdown(f"""
<div class="ticker">
    FULL R*TARDS NETWORK • WEEK {week} • {season} SEASON • LIVE FROM THE LEAGUE OF CHAOS
</div>
""", unsafe_allow_html=True)

st.title("Full R*tards Network")
st.caption("The only place where Winnie the Pooh, Master Splinter, and Slack Jaw share a league.")

# ====================== STANDINGS + POWER RANKINGS ======================
col1, col2 = st.columns([1.4, 1])

with col1:
    st.header("📊 Official Standings")
    df = pd.DataFrame(standings)[["Rank", "Team", "W", "L", "PF", "PA"]]
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.header("🔥 Power Rankings")
    # Simple power ranking: 60% record + 40% points
    power = []
    for s in standings:
        score = (s["W"] * 3) + (s["PF"] / 100)
        power.append((s["Team"], score, s["Rank"]))
    power = sorted(power, key=lambda x: -x[1])
    
    for i, (team, score, official_rank) in enumerate(power, 1):
        arrow = "↑" if i < official_rank else ("↓" if i > official_rank else "–")
        st.markdown(f"**{i}. {team}** {arrow}")

# ====================== MATCHUPS ======================
st.header(f"⚔️ Week {week} Scoreboard")

cols = st.columns(3)
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
        <div class="broadcast-card">
            <h4 style="margin:0;color:#fbbf24;">{name1}</h4>
            <h2 style="margin:4px 0;">{pts1:.1f}</h2>
            <p style="margin:0;opacity:0.7;">vs</p>
            <h4 style="margin:0;color:#fbbf24;">{name2}</h4>
            <h2 style="margin:4px 0;">{pts2:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)

# ====================== CHIRP OF THE WEEK ======================
st.header("🗣️ Chirp of the Week")
# Simple logic: lowest points or worst record gets roasted
worst = min(standings, key=lambda x: x["PF"])
chirp = f"This week’s golden boot goes to **{worst['Team']}**. {PERSONALITIES.get(worst['Team'], '')} The league is watching."
st.info(chirp)

# ====================== SPORTCASTER / VIDEO SECTION ======================
st.header("🎙️ The Ron Burgundy Broadcast")

st.markdown("""
**Weekly Video Broadcast**  
Once scores are final, generate a Ron Burgundy-style video using the script below and paste the video link here.
""")

# Placeholder for the weekly video
video_url = st.text_input("Paste this week’s video URL (YouTube, Vimeo, or direct .mp4 link)", 
                          placeholder="https://...")

if video_url:
    st.video(video_url)
else:
    st.warning("No video uploaded yet this week. Generate one using the script below and paste the link.")

# Detailed humorous script
def build_script():
    lines = []
    lines.append(f"Hello, I’m Ron Burgundy, and this is the Full R*tards Network. You’re watching the Week {week} recap.")
    lines.append("Stay classy, San Diego… I mean, Ottawa.")
    
    leader = standings[0]
    lines.append(f"Sitting atop the mountain is {leader['Team']} at {leader['W']}-{leader['L']}. {PERSONALITIES.get(leader['Team'], '')}")
    
    # Highlight a few more
    for s in standings[1:4]:
        lines.append(f"{s['Team']} is right there at {s['W']}-{s['L']}. {PERSONALITIES.get(s['Team'], '')}")
    
    bottom = standings[-1]
    lines.append(f"And down in the basement we find {bottom['Team']}. {PERSONALITIES.get(bottom['Team'], '')} Brutal.")
    
    lines.append("That’s the state of the league this week. May your waivers hit and your friends show up. Good night, and stay classy.")
    return " ".join(lines)

script = build_script()

with st.expander("📜 This Week’s Full Script (copy this for your video)"):
    st.write(script)
    st.code(script, language=None)

st.caption("Tip: Copy the script → go to a free AI talking-head tool (HeyGen free plan works) → generate a Ron Burgundy style video → upload to YouTube/Vimeo (unlisted) → paste the link above.")

# ====================== FOOTER ======================
st.markdown("---")
st.caption(f"Full R*tards Network • Data from Sleeper • Updated {datetime.now().strftime('%Y-%m-%d %H:%M')}")
