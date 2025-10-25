import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="JSONPlaceholder Analytics", layout="wide")

st.title("JSONPlaceholder Data Analytics")

# Data collect
@st.cache_data
def load_data():
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    posts = requests.get("https://jsonplaceholder.typicode.com/posts").json()
    comments = requests.get("https://jsonplaceholder.typicode.com/comments").json()
    todos = requests.get("https://jsonplaceholder.typicode.com/todos").json()
    return pd.DataFrame(users), pd.DataFrame(posts), pd.DataFrame(comments), pd.DataFrame(todos)

users_df, posts_df, comments_df, todos_df = load_data()

st.sidebar.header("Data:")
st.sidebar.write(f"Users: {len(users_df)}")
st.sidebar.write(f"Posts: {len(posts_df)}")
st.sidebar.write(f"Comments: {len(comments_df)}")
st.sidebar.write(f"TODOs: {len(todos_df)}")

# Calculations
posts_per_user = posts_df.groupby("userId").size()
comments_per_post = comments_df.groupby("postId").size()
todos_completed = todos_df.groupby("userId")["completed"].mean() * 100

avg_posts = posts_per_user.mean()
avg_comments = comments_per_post.mean()

st.subheader("Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Average number of posts per user", f"{avg_posts:.2f}")
col2.metric("Average number of comments on post", f"{avg_comments:.2f}")
col3.metric("Average % completed TODOs", f"{todos_completed.mean():.1f}%")

# Visuals
st.subheader("Number of posts per user")
fig1, ax1 = plt.subplots()
ax1.bar(posts_per_user.index, posts_per_user.values, color="skyblue")
ax1.set_xlabel("User ID")
ax1.set_ylabel("Number of posts")
st.pyplot(fig1)

st.subheader("Percents of completed TODOs")
fig2, ax2 = plt.subplots()
ax2.pie(todos_completed, labels=todos_completed.index, autopct="%1.1f%%", startangle=90)
st.pyplot(fig2)

# TOP 5 of the most commented posts :)
st.subheader("🔥 TOP % of commented posts ")
top_posts = comments_per_post.sort_values(ascending=False).head(5)
top_posts_df = posts_df[posts_df["id"].isin(top_posts.index)][["id", "title"]]
top_posts_df["Comments"] = top_posts.values
st.table(top_posts_df)
