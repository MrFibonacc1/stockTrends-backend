import praw
import os

client_id = os.getenv('clientID')
client_secret = os.getenv('clientSecret')
user_agent = os.getenv('userAgent')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

subreddit = reddit.subreddit('wallstreetbets')

# List to store posts
posts = []

# Fetch the most recent posts (you can adjust the limit as needed)
for submission in subreddit.new(limit=1):  # Fetching fewer posts to debug
    print(f"Checking post: {submission.title} (Created UTC: {submission.created_utc})")

    post_data = {
        'title': submission.title,
        'url': submission.url,
        'upvotes': submission.score,
        'created_at': submission.created_utc,
        'comments': []  # To store comments for this post
    }

    # Fetch all comments for the submission
    submission.comments.replace_more(limit=None)  # Replace 'MoreComments' objects to get all comments
    for comment in submission.comments.list():  # Flatten the comments
        post_data['comments'].append({
            'author': comment.author.name if comment.author else 'Unknown',
            'body': comment.body,
            'score': comment.score
        })

    posts.append(post_data)

# Print out the posts and their comments
if posts:
    for post in posts:
        print(f"Title: {post['title']}")
        print(f"Upvotes: {post['upvotes']}")
        print(f"Created at (UTC): {post['created_at']}")
        print(f"URL: {post['url']}")
        print(f"Comments ({len(post['comments'])}):")
        
        for comment in post['comments']:
            print(f"\tAuthor: {comment['author']}")
            print(f"\tScore: {comment['score']}")
            print(f"\tComment: {comment['body']}\n")
else:
    print("No posts found.")
