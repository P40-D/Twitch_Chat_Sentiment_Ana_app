import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('Final_Pestily_Chat.csv')

df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
df.set_index('Datetime', inplace=True)

# Calculate the Positive, Negative, and Neutral Comment Counts
sentiment_counts = df.groupby([pd.Grouper(freq='5T'), 'Sentiment_Label']).size().unstack(fill_value=0)
sentiment_counts['Not Neutral'] = sentiment_counts['POSITIVE'] + sentiment_counts['NEGATIVE']

def show_dashboard():
    # Intro
    st.title("Twitch Chat Sentiment Analysis")
    st.subheader("About the Streamer & Video")
    st.write(
        "This video is from the Twitch stream of [Pestily](https://www.twitch.tv/pestily), a popular content creator who streams games like Escape from Tarkov. "
    )
    st.write(
        "In this video, Pestily plays Zero Sievert, a top-down extraction shooter where the stakes are high. "
        "If his character dies, he will lose all progress and must start the game over from the beginning."
    )
    st.write(
        "You can watch the full video on [Twitch here](https://www.twitch.tv/videos/2305090004)."
    )

    st.subheader("Chat Sentiment Analysis")
    st.write(
        "Sentiment analysis was performed on the chat thread from this video using Hugging Face's ""cardiffnlp/twitter-roberta-base-sentiment"" model. "
        "The user is invited to explore the visualizations below showing the quantity of comments and their positivity."
    )

    # pie chart for sentiment distribution
    sentiment_summary = {
        'Positive': sentiment_counts['POSITIVE'].sum(),
        'Negative': sentiment_counts['NEGATIVE'].sum(),
        'Neutral': sentiment_counts['NEUTRAL'].sum()
    }

    fig_pie = go.Figure(data=[go.Pie(
        labels=list(sentiment_summary.keys()),
        values=list(sentiment_summary.values()),
        hole=0.3,
        marker=dict(colors=['green', 'red', 'blue'])
    )])

    fig_pie.update_layout(
        title="Sentiment Distribution of Comments",
        title_font_size=20,
    )

    st.plotly_chart(fig_pie)

    # Not Neutral and Neutral Comment Counts Over Time
    fig1 = go.Figure()

    fig1.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['Not Neutral'], 
                         name='Sentimental Comment Count', 
                         marker=dict(color='orange', opacity=0.8)))
    fig1.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['NEUTRAL'], 
                         name='Neutral Comment Count', 
                         marker=dict(color='blue', opacity=0.8)))

    fig1.update_layout(
        title={
            'text': "Neutral & Sentimental Comment Counts Over Time",
            'font': {'size': 30}
        },
        xaxis=dict(
            title="Time",
            tickformat="%H:%M:%S",
            tickangle=45,
            dtick=3600000,
        ),
        yaxis=dict(
            title="Comment Count"
        ),
        barmode='stack',
        legend=dict(
            x=0.01, y=0.99
        ),
    )

    # Positive and Negative Comment Counts Over Time
    fig2 = go.Figure()

    fig2.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['POSITIVE'], 
                         name='Positive Comment Count', 
                         marker=dict(color='green', opacity=0.8)))
    fig2.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['NEGATIVE'], 
                         name='Negative Comment Count', 
                         marker=dict(color='red', opacity=0.8)))

    fig2.update_layout(
        title={
            'text': "Positive & Negative Comment Counts Over Time",
            'font': {'size': 30}
        },
        xaxis=dict(
            title="Time",
            tickformat="%H:%M:%S",
            tickangle=45,
            dtick=3600000,
        ),
        yaxis=dict(
            title="Comment Count"
        ),
        barmode='stack',
        legend=dict(
            x=0.01, y=0.99),
    )

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)