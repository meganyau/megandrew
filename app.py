
from datetime import datetime
import pandas as pd
import streamlit as st
import time

st.set_page_config(page_title="Megandrew Wrapped", layout="wide")
st.markdown(
    """
    <style>
        /* Responsive layout for all screen sizes */
        html, body, .stApp {
            background-color: #9DC183;
            margin: 0;
            padding: 0;
            font-size: 16px;
        }

        @media only screen and (max-width: 600px) {
            .stApp {
                padding: 10px;
                font-size: 14px;
            }
            h1, h2, h3 {
                font-size: 20px !important;
            }
        }

        .bubble {
            padding: 10px 14px;
            border-radius: 18px;
            margin: 6px 0;
            max-width: 90%;
            word-wrap: break-word;
            display: inline-block;
        }

        .left {
            background-color: #e5e5ea;
            color: black;
            text-align: left;
        }

        .right {
            background-color: #007aff;
            color: white;
            text-align: right;
            float: right;
        }

        .clearfix {
            clear: both;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Show balloons on page load
st.balloons()

# Optional: pause briefly so it displays before everything else renders
time.sleep(1)


# === Load Data ===
df = pd.read_csv('messagess.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp', 'text'])
df = df[~df['text'].str.contains(r'loved\s+["“”]', case=False, na=False)]  # remove quotes after loved


# === Keyword Summary Function ===
def wrapped_keyword_summary(df, keywords):
    # first_date = df['timestamp'].min().strftime("%b %d, %Y")
    # last_date = df['timestamp'].max().strftime("%b %d, %Y")
    # st.markdown(f"📆 **Messages from {first_date} to {last_date}**")
    # st.markdown(f"📬 **Total messages: {len(df)}**")
    # st.markdown("---")

    for word in keywords:
        mask = df['text'].str.contains(word, case=False, na=False)
        matching_df = df[mask].copy()
        count_total = len(matching_df)
        count_andrew = len(matching_df[matching_df['from_me'] == 0])
        count_megan = len(matching_df[matching_df['from_me'] == 1])

        st.markdown(f"### 🔑 '{word}' appeared in {count_total} messages")
        st.markdown(f"- Andrew sent it **{count_andrew}** times")
        st.markdown(f"- Megan sent it **{count_megan}** times")

        if count_total > 0:
            first_row = matching_df.sort_values('timestamp').iloc[0]
            first_date = first_row['timestamp'].strftime("%b %d, %Y")
            first_sender = "Andrew" if first_row['from_me'] == 0 else "Megan"
            first_msg = first_row['text']
            st.markdown(f"   - First sent on: **{first_date}** by **{first_sender}**")
            st.markdown(f"      **{first_msg}**")

            matching_df['day'] = pd.to_datetime(matching_df['timestamp']).dt.date
            most_day = matching_df['day'].value_counts().idxmax()
            most_day_count = matching_df['day'].value_counts().max()
            most_day_fmt = most_day.strftime("%b %d, %Y")

        
            st.markdown(f"- Most used on **{most_day_fmt}** with **{most_day_count}** messages")

            st.markdown("#### 👤 Messages Andrew sent:")
            for msg in matching_df[matching_df['from_me'] == 0]['text'].head(5):
                st.markdown(
                    f"<div style='background-color:#e5e5ea; color:black; padding:8px 12px; border-radius:16px; "
                    f"display:inline-block; margin:5px 0; max-width:80%; text-align:left;'>"
                    f"{msg}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("#### 🧍 Messages Megan sent:")
            for msg in matching_df[matching_df['from_me'] == 1]['text'].head(5):
                st.markdown(
                    f"<div style='background-color:#007aff; color:white; padding:8px 12px; border-radius:16px; "
                    f"display:inline-block; margin:5px 0; max-width:80%; text-align:right; float:right;'>"
                    f"{msg}</div><div style='clear:both;'></div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")

# === Birthday Message Pull ===
def birthday_message_block(df):
    birthday_msgs = df.loc[324:329]
    st.markdown("Here’s what Megan wished you last birthday!!!")

    for _, row in birthday_msgs.iterrows():
        bubble_style = {
            0: "background-color:#e5e5ea; text-align:left; color:black;",    # Andrew
            1: "background-color:#007aff; color:white; text-align:right; float:right;"    # Megan
        }[row['from_me']]

        bubble_html = f"""
        <div style="{bubble_style} padding:10px; border-radius:18px; margin:5px 0; max-width:80%; display:inline-block;">
            {row['text']}
        </div>
        <div style="clear:both;"></div>
        """
        st.markdown(bubble_html, unsafe_allow_html=True)
        
        
# === Streamlit Page Setup ===

st.markdown(
    """
    <style>
        body {
            background-color: #9DC183;  /* pastel green */
        }
        .stApp {
            background-color: #9DC183;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center;'>
        <span style="white-space: nowrap;">💌 Megandrew Messages Wrapped 💌</span>
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("### HAPPY 22ND BIRTHDAY ANDREW WHOOOO")
st.markdown("---")

first_date = df['timestamp'].min().strftime("%b %d, %Y")
last_date = df['timestamp'].max().strftime("%b %d, %Y")
total_msgs = len(df)

st.markdown("""
<div style='font-size:20px; line-height:1.6;'>
Happy birthday to stinker Andrew, <br>
this also means one whole year of texting! 🎉 <br><br>
So I collected our chat history, did some data cleaning (as I do best), <br>
and ran some data analysis on our messages 💻📊
</div>
""", unsafe_allow_html=True)

first_date = df['timestamp'].min().strftime("%b %d, %Y")
last_date = df['timestamp'].max().strftime("%b %d, %Y")
total_msgs = len(df)

st.markdown(f"""
<div style='font-size:20px; line-height:1.6;'>
I collected messages starting from:  

📆 <strong>Messages from {first_date} to {last_date}</strong>  
  
We sent a total of:  
📬 <strong>Total messages: {total_msgs}</strong>
</div>
""", unsafe_allow_html=True)





st.markdown("---")

# === Show Birthday Block ===
birthday_message_block(df)

st.markdown("---")

# === Show Keyword Summary ===
keywords = ['i love you', 'stinker', 'poop', 'my boy', 'it true', 'drewbert']
wrapped_keyword_summary(df, keywords)

# === Allow user to input custom keyword ===
st.markdown("### Now you try!!:")
user_keyword = st.text_input("Type a word or phrase below and press Enter:")

if user_keyword:
    st.markdown("---")
    st.markdown(f"## Analysis for: '{user_keyword}'")
    wrapped_keyword_summary(df, [user_keyword])
