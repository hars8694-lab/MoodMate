import streamlit as st
from src import emotion, responder, safety, journal

st.set_page_config(page_title="MoodMate", page_icon=":sun_behind_cloud:")
journal.init_db()
chat_tab, mood_tab = st.tabs(["Chat", "My mood"])

with chat_tab:
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_msg := st.chat_input("What's on your mind?"):
        st.chat_message("user").write(user_msg)
        st.session_state.history.append({"role": "user", "content": user_msg})

        if crisis := safety.check(user_msg):
            reply = crisis
        else:
            emotions = emotion.detect_emotions(user_msg)
            journal.log(user_msg, emotions)
            reply = responder.generate_reply(st.session_state.history, emotions)

        st.chat_message("assistant").write(reply)
        st.session_state.history.append({"role": "assistant", "content": reply})

    st.caption(
        "MoodMate is a companion app, not a substitute for "
        "professional mental-health care."
    )

with mood_tab:
    df = journal.load_history_df()

    if df.empty:
        st.info("Chat a little first - your mood trends will appear here.")
    else:
        import pandas as pd
        import plotly.express as px

        df["day"] = pd.to_datetime(df["ts"]).dt.date
        df["top_emotion"] = df["emotions"].apply(
            lambda e: max(e, key=e.get) if e else "neutral"
        )
        counts = df.groupby(["day", "top_emotion"]).size().reset_index(name="count")
        fig = px.bar(
            counts,
            x="day",
            y="count",
            color="top_emotion",
            title="Your emotional landscape over time",
        )
        st.plotly_chart(fig, use_container_width=True)