import streamlit as st
import plotly.express as px
from queries import gen_contestant_list, gen_contestant_stats, gen_contestant_hometowns, gen_average_ages, \
    gen_winners_vs_wins, gen_s16_rollercoaster, gen_win_streaks

conn = st.connection('rpdr_analysis', type='sql')

st.set_page_config(layout="wide")

st.title("RuPaul's Drag Race Stats")

main_col_1, main_col_2 = st.columns(2)
with main_col_1:
    st.header("Compare Contestants")
    st.text("Pick any 2 drag queens and view some of their stats side by side!")
    ctst_select_1, ctst_select_2 = st.columns(2)
    with ctst_select_1:
        contestant_1 = st.selectbox("Choose 1st contestant", gen_contestant_list(conn))

    with ctst_select_2:
        contestant_2 = st.selectbox("Choose 2nd contestant", gen_contestant_list(conn))

    col1, col2 = st.columns(2)
    with col1:
        contestant_1_orig_string = contestant_1
        if "'" in contestant_1:
            contestant_1 = contestant_1.replace("'", "''")
        contestant_1_df = conn.query(gen_contestant_stats(contestant_1))
        wins_1 = contestant_1_df.iloc[0]["Wins"]
        btms_1 = contestant_1_df.iloc[0]["Btms"]
        episodes_1 = contestant_1_df.iloc[0]["Episodes"]
        st.subheader(contestant_1_orig_string)
        subcol1, subcol2, subcol3 = st.columns(3)
        subcol1.metric("Wins", wins_1)
        subcol2.metric("Btms", btms_1)
        subcol3.metric("Episodes", episodes_1)

    with col2:
        contestant_2_orig_string = contestant_2
        if "'" in contestant_2:
            contestant_2 = contestant_2.replace("'", "''")
        contestant_2_df = conn.query(gen_contestant_stats(contestant_2))
        wins_2 = contestant_2_df.iloc[0]["Wins"]
        btms_2 = contestant_2_df.iloc[0]["Btms"]
        episodes_2 = contestant_2_df.iloc[0]["Episodes"]
        st.subheader(contestant_2_orig_string)
        subcol4, subcol5, subcol6 = st.columns(3)
        subcol4.metric("Wins", wins_2)
        subcol5.metric("Btms", btms_2)
        subcol6.metric("Episodes", episodes_2)

with main_col_2:

    st.header("Contestant Hometowns")
    st.text("Rupaul's Drag Race casts queens from all across the U.S.! Hover over the map to see how many come from each"
            " state!")
    hometown_df = conn.query(gen_contestant_hometowns())

    fig = px.choropleth(
        hometown_df,
        locations="state",
        locationmode="USA-states",
        color="Queens",
        color_continuous_scale="peach",
        scope="usa",
        title="Contestant Hometowns"
    )

    st.plotly_chart(fig, use_container_width=True)
st.divider()
main_col_3, main_col_4 = st.columns(2)
with main_col_3:
    st.header("Average Contestant Age Across Seasons")
    st.text("The show brings on queens of all adult ages. The oldest queen at time of competition being 52, and the"
            " youngest being 21! \nWatch how the average age of the queens changes across each season:")
    age_df = conn.query(gen_average_ages())

    age_fig = px.line(
        age_df,
        x="Season",
        y="Age",
        title = "Average Contestant Age by Season"
    )

    st.plotly_chart(age_fig, use_container_width=True)

with main_col_4:
    st.header("Winners vs. # of Challenger Wins")
    st.text("Winning challenges is a huge part of competing on Drag Race. Queens who have won the show have all won"
            " at least one challenge. But how many challenges does it take to win the season? It seems the sweet spot is"
            " 3, with some pulling it out with less wins, and a few overachievers going for 4!")
    winner_df = conn.query(gen_winners_vs_wins())

    winner_fig = px.bar(
        winner_df,
        x="Number_of_Winners",
        y="Challenge_Wins",
        orientation="h"
    )

    winner_fig.update_yaxes(dtick=1)

    st.plotly_chart(winner_fig, use_container_width=True)
st.divider()
main_col_5, main_col_6 = st.columns(2)
with main_col_5:
    st.header("Season 16 'Roller Coaster'")
    st.text("Drag Race keeps all of the queens on their toes. One week, you snatch the crown, but the next you are"
            " lip-syncing for your life! Let's call it a roller coaster when a queen wins one week, but is in the bottom"
            " the next (or vice versa!) \nSeason 16 had the most instances of queens having these 'roller coaster' weeks,"
            " see for yourself:")
    s16_r_df = conn.query(gen_s16_rollercoaster())


    st.table(s16_r_df.style
        .map(
        lambda x: f"background-color: {'lightgreen' if x == 'WIN' else 'lightpink'}",
        subset='Result')
        .map(
        lambda x: f"background-color: {'lightgreen' if x == 'WIN' else 'lightpink'}",
        subset='Prev_Ep_Result'
    )
    )
with main_col_6:
    st.header("Win Streaks")
    st.text("Sometimes these queens are on fire! Winning multiple challenges in a row is rare, and some queens have"
            " even managed to pull off 3 weeks in a row! \nBehold, the win-streak hall of fame:")
    win_streak_df = conn.query(gen_win_streaks())

    win_streak_fig = px.bar(
        win_streak_df,
        x="Season",
        y="Streak",
        orientation="v"
    )

    st.table(win_streak_df)