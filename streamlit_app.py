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
        background: linear-gradient(180deg, #0a0e
