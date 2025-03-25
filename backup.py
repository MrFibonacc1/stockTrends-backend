import praw
import os
import time
from datetime import datetime, timezone
from prawcore.exceptions import TooManyRequests

# Set up Reddit API credentials
client_id = os.getenv('clientID')
client_secret = os.getenv('clientSecret')
user_agent = os.getenv('userAgent')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

information = {}
alias_map = {}
variation_map = set()  # To efficiently check if a word is a valid variation


def load_tickers(file_path):
    """
    Load tickers from file and create alias and variation maps.
    """
    global alias_map, variation_map
    try:
        with open(file_path, 'r') as file:
            for line in file:
                variations = [word.strip().lower() for word in line.split(',') if word.strip()]
                if variations:
                    canonical = variations[0]  # First word is the canonical name
                    alias_map[canonical] = variations
                    
                    # Add all variations to the reverse lookup map
                    for var in variations:
                        variation_map.add(var)

        print("Alias Map:", alias_map)           # Debug print
        print("Valid Variations:", variation_map)  # Debug print

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error loading tickers: {e}")


def parse_info(comments):
    """
    Count occurrences of tickers (and their variations) only.
    """
    global information
    for comment in comments:
        for word in comment.split():
            word = word.lower().strip(",.!?()[]{}\"'")  # Clean punctuation
            
            # Only count words that are in the variation map
            if word in variation_map:
                # Map to canonical name
                for canonical, variations in alias_map.items():
                    if word in variations:
                        if canonical in information:
                            information[canonical] += 1
                        else:
                            information[canonical] = 1
                        break


def fetch_recent_posts(subreddit_name, time_threshold=10800):
    """
    Fetch subreddit posts from the last hour using Unix timestamps.
    """
    subreddit = reddit.subreddit(subreddit_name)
    comments = []

    current_time = int(time.time())  # Current Unix timestamp
    found_recent = False

    for submission in subreddit.new(limit=100):  # Increase limit to get more recent posts
        post_time = int(submission.created_utc)

        # Check if the post is within the last hour
        if current_time - post_time <= time_threshold:
            found_recent = True
            print(f"Processing post: {submission.title} (Unix Time: {post_time})")

            try:
                submission.comments.replace_more(limit=0)
                comments.extend([comment.body for comment in submission.comments.list()])
                time.sleep(1)  # Delay to avoid hitting rate limits

            except TooManyRequests:
                print("Rate limit exceeded. Pausing for 10 seconds...")
                time.sleep(10)
            except Exception as e:
                print(f"Error processing post '{submission.title}': {e}")
        else:
            # Stop processing if the post is older than 1 hour
            break

    if not found_recent:
        print("\nNo posts found from the last hour.")
        return []

    return comments


# ✅ Load tickers and create alias/variation maps
load_tickers("tickers.txt")

# ✅ Fetch and process recent subreddit posts
all_comments = fetch_recent_posts('wallstreetbets')

if all_comments:
    parse_info(all_comments)

# ✅ Display results
if information:
    print("\nTicker Information:")
    for ticker, count in information.items():
        print(f"{ticker}: {count}")
else:
    print("\nNo matching tickers found in recent posts.")
