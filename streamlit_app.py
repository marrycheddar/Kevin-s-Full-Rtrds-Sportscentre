import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ====================== CONFIG ======================
LEAGUE_ID = "1380669652224454656"
BASE = "https://api.sleeper.app/v1"

# Personality dictionary (team_name or display_name → description)
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

st.set_page_config(page_title="Full R*tards Sports Centre", page_icon="🏈", layout="wide")

st.title("🏈 Full R*tards Sports Centre")
st.caption("Weekly reports • Humorous sportscaster • Powered by Sleeper")

# ====================== DATA FETCHING ======================
@st.cache_data(ttl=300)  # refresh every 5 minutes
def get_json(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

def get_current_week():
    state = get_json(f"{BASE}/state/nfl")
    return state.get("week", 1), state.get("season", "2026")

def load_league_data():
    users = get_json(f"{BASE}/league/{LEAGUE_ID}/users")
    rosters = get_json(f"{BASE}/league/{LEAGUE_ID}/rosters")
    
    # Map owner_id → nice name
    user_map = {}
    for u in users:
        name = u.get("metadata", {}).get("team_name") or u.get("display_name") or "Unknown"
        user_map[u["user_id"]] = name.strip()
    
    # Build standings
    standings = []
    for r in rosters:
        owner = user_map.get(r.get("owner_id"), f"Roster {r['roster_id']}")
        settings = r.get("settings", {})
        standings.append({
            "Team": owner,
            "W": settings.get("wins", 0),
            "L": settings.get("losses", 0),
            "T": settings.get("ties", 0),
            "PF": round(settings.get("fpts", 0), 1),
            "PA": round(settings.get("fpts_against", 0), 1),
            "roster_id": r["roster_id"],
            "owner_id": r.get("owner_id"),
        })
    
    standings = sorted(standings, key=lambda x: (-x["W"], -x["PF"]))
    for i, s in enumerate(standings, 1):
        s["Rank"] = i
    
    return user_map, standings, rosters

week, season = get_current_week()
user_map, standings, rosters = load_league_data()

# Current week matchups
matchups_raw = get_json(f"{BASE}/league/{LEAGUE_ID}/matchups/{week}")
matchup_dict = {}
for m in matchups_raw:
    mid = m.get("matchup_id")
    if mid not in matchup_dict:
        matchup_dict[mid] = []
    matchup_dict[mid].append(m)

# ====================== SIDEBAR ======================
st.sidebar.header("League Info")
st.sidebar.write(f"**Season:** {season}")
st.sidebar.write(f"**Current Week:** {week}")
st.sidebar.write(f"**Teams:** 12")
st.sidebar.markdown("---")
st.sidebar.info("Data refreshes automatically every few minutes.")

# ====================== STANDINGS ======================
st.header("📊 Current Standings")
df = pd.DataFrame(standings)[["Rank", "Team", "W", "L", "T", "PF", "PA"]]
st.dataframe(df, use_container_width=True, hide_index=True)

# ====================== MATCHUPS ======================
st.header(f"⚔️ Week {week} Matchups")

cols = st.columns(2)
col_idx = 0
for mid, teams in sorted(matchup_dict.items()):
    if len(teams) != 2:
        continue
    t1, t2 = teams
    name1 = next((s["Team"] for s in standings if s["roster_id"] == t1["roster_id"]), "Team 1")
    name2 = next((s["Team"] for s in standings if s["roster_id"] == t2["roster_id"]), "Team 2")
    pts1 = t1.get("points") or 0
    pts2 = t2.get("points") or 0
    
    with cols[col_idx % 2]:
        st.subheader(f"{name1} vs {name2}")
        st.metric(label=name1, value=f"{pts1:.1f}")
        st.metric(label=name2, value=f"{pts2:.1f}")
        if pts1 > 0 or pts2 > 0:
            leader = name1 if pts1 > pts2 else name2
            st.caption(f"Currently leading: **{leader}**")
        st.markdown("---")
    col_idx += 1

# ====================== SPORTCASTER ======================
st.header("🎙️ The Sportscaster")
st.write("Click the button below for a colourful, personality-driven weekly recap (read out loud).")

def build_sportscaster_script():
    lines = []
    lines.append(f"Good evening ladies and gentlemen, and welcome to another wild week in the Full R*tards league!")
    lines.append(f"We are currently in week {week} of the {season} season.")
    
    # Top and bottom
    leader = standings[0]
    last = standings[-1]
    lines.append(f"Sitting pretty at the top of the standings is {leader['Team']} at {leader['W']}-{leader['L']}.")
    
    # Personality flavours
    for s in standings:
        team = s["Team"]
        personality = PERSONALITIES.get(team, "a mysterious figure")
        record = f"{s['W']}-{s['L']}"
        
        if s["Rank"] == 1:
            lines.append(f"{team} is rolling. Remember: {personality}")
        elif s["Rank"] <= 4:
            lines.append(f"{team} is in the hunt at {record}. {personality}")
        elif s["Rank"] >= 10:
            lines.append(f"Down in the dumps we find {team} at {record}. {personality} ... ouch.")
    
    lines.append("And that, my friends, is the state of the Full R*tards. Stay classy, stay unhinged, and may your waiver claims hit.")
    lines.append("This has been your sportscaster. Good night!")
    
    return " ".join(lines)

script = build_sportscaster_script()

if st.button("🔊 Play Sportscaster Recap", type="primary"):
    st.success("Playing now... (make sure your volume is up)")
    # Browser TTS via JavaScript
    st.components.v1.html(
        f"""
        <script>
            var msg = new SpeechSynthesisUtterance(`{script.replace("`", "'")}`);
            msg.rate = 0.95;
            msg.pitch = 1.1;
            window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )
    with st.expander("Read the script instead"):
        st.write(script)

st.markdown("---")
st.caption("Built for the Full R*tards • Data from Sleeper • Humour powered by your own chaos")
