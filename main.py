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
tickers = {'tsmc':0, "nvda":0}
comments = []
information = {}

def parseInfo(comments):
    global information
    for comment in comments:
        for word in comment.split():
            word = word.lower().strip()
            # print(word)
            if word in tickers:
                information[word] = information.get(word,0) + 1



def subredditInfo(subredditName):
    subreddit = reddit.subreddit(subredditName)

    # List to store posts
    posts = []

    # Fetch the most recent posts (you can adjust the limit as needed)
    for submission in subreddit.new(limit=19):  # Fetching fewer posts to debug
        print(f"Checking post: {submission.title} (Created UTC: {submission.created_utc})")
        comments.append(submission.title)

        # post_data = {
        #     'title': submission.title,
        #     'url': submission.url,
        #     'upvotes': submission.score,
        #     'created_at': submission.created_utc,
        #     'comments': []  # To store comments for this post
        # }

        # Fetch all comments for the submission
        submission.comments.replace_more(limit=None)  # Replace 'MoreComments' objects to get all comments
        for comment in submission.comments.list():  # Flatten the comments
            # print(comment)
            comments.append(comment.body)
            # parseInfo(comment.body)
            # post_data['comments'].append({
            #     'author': comment.author.name if comment.author else 'Unknown',
            #     'body': comment.body,
            #     'score': comment.score
            # })

        # posts.append(post_data)

# Print out the posts and their comments
# if posts:
#     for post in posts:
#         print(f"Title: {post['title']}")
#         print(f"Upvotes: {post['upvotes']}")
#         print(f"Created at (UTC): {post['created_at']}")
#         print(f"URL: {post['url']}")
#         print(f"Comments ({len(post['comments'])}):")
        
#         for comment in post['comments']:
#             print(f"\tAuthor: {comment['author']}")
#             print(f"\tScore: {comment['score']}")
#             print(f"\tComment: {comment['body']}\n")
# else:
#     print("No posts found.")

# Loads keywords from tickers.txt
# def loadTickers(file_path):
#     global tickers
#     with open(file_path, 'r') as file:
#         words = [line.strip() for line in file if line.strip()]
#         tickers =  {keyword: 0 for keyword in words}
#     return



subredditInfo('wallstreetbets')
# loadTickers("tickers.txt")
# print(tickers)
# print(comments)
print("next point")
parseInfo(comments)
print(information)