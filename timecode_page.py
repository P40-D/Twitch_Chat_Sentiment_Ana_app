import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

# Load CSV
df = pd.read_csv('Final_Pestily_Chat.csv')

# Process Datetime
df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
df.set_index('Datetime', inplace=True)

def show_timecode_page():
    st.title("Choose a Timecode!")
    st.subheader("Timecode Event Examples")
    st.write(
        "**02:00:40** - death of Pestily's in-game character"
    )
    st.write(
        "**02:45:00** - Pestily engages with chat about a game he dislikes"
    )
    st.write(
        "**04:42:00** - death of Pestily's in-game character"
    )
    st.write(
        "**06:27:40** - death of Pestily's in-game character"
    )
    st.write(
        "*Use the dialog below to generate a link to the video at any time you like. Find out what happened that made the comments spike!*"
    )

    # Input box for timecode
    timecode_input = st.text_input(
        "Enter a timecode in HH:MM:SS format (e.g., 01:30:45):", 
        "",
        max_chars=8
    )

    # Convert timecode to seconds
    def convert_timecode_to_seconds(timecode: str):
        try:
            hours, minutes, seconds = map(int, timecode.split(":"))
            total_seconds = hours * 3600 + minutes * 60 + seconds - 5
            return total_seconds
        except ValueError:
            return None

    # word cloud function
    def generate_wordcloud(timecode):
        total_seconds = convert_timecode_to_seconds(timecode)
        if total_seconds is not None:
            start_time = pd.to_datetime(df.index[0]) + pd.Timedelta(seconds=total_seconds)
            end_time = start_time + pd.Timedelta(minutes=1)
            
            # Filter comments
            minute_comments = df[(df.index >= start_time) & (df.index < end_time)]
            text = ' '.join(minute_comments['Message'].dropna())
            
            if text:
                wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

                # Convert word cloud to an image
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')

                # BytesIO object
                buf = BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)

                # Display
                st.image(buf)

            else:
                st.warning("No comments found for this timecode.")
        else:
            st.error("Please enter a valid timecode in HH:MM:SS format.")
            
    # Generate Twitch link and display word cloud
    if timecode_input:
        total_seconds = convert_timecode_to_seconds(timecode_input)
        if total_seconds is not None:
            twitch_video_url = f"https://www.twitch.tv/videos/2305090004?t={total_seconds}s"
            st.write(f"Here is the link to the Twitch video at {timecode_input}: [Twitch Video](https://www.twitch.tv/videos/2305090004?t={total_seconds}s)")

            st.subheader("Top words used at timecode minute")
            generate_wordcloud(timecode_input)
        else:
            st.error("Please enter a valid timecode in HH:MM:SS format.")

    # Plot Total Comment Count
    total_comment_counts = df.resample('1T').size()

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=total_comment_counts.index, y=total_comment_counts, 
                        name='Total Comment Count', 
                        marker=dict(color='purple', opacity=0.6)))

    # Layout
    fig3.update_layout(
        title={
            'text': "Total Comment Count Every Minute",
            'font': {'size': 35}
        },
        xaxis=dict(
            title="Time",
            tickformat="%H:%M:%S",
            tickangle=45,
        ),
        yaxis=dict(
            title="Comment Count"
        )
    )

    st.plotly_chart(fig3)
