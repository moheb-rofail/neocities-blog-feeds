import requests
import PyRSS2Gen
from datetime import datetime
import json

site_url = 'https://moheb-rofail.neocities.org/'
# URL of the JSON file
json_url = 'https://moheb-rofail.neocities.org/Arrays/posts.json'

# Send a GET request to the URL to fetch the JSON data
response = requests.get(json_url)
response.raise_for_status()

# Parse the JSON content
try:
    posts_data = response.json()
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    posts_data = []

# Create a list to store RSS items
rss_items = []

counter = 0;

# Iterate over each post and extract details
for post in posts_data:
    title = post
    link = post.replace(" ", "_")
    pub_date_str = posts_data[post][0]
    
    # Parse the publication date if provided
    try:
        # Parse the date into a datetime object
        date_obj = datetime.strptime(pub_date_str, "%d %b %Y")

        # Convert to the RSS format: "Wed, 02 Oct 2005 14:00:00 +0000"
        rss_date = date_obj.strftime("%a, %d %b %Y 00:00:00 +0000")
    except ValueError:
        rss_date = datetime.now()

    # Create an RSS item
    rss_item = PyRSS2Gen.RSSItem(
        title=title,
        link="https://moheb-rofail.neocities.org/post?p="+link,
        pubDate=rss_date
    )
    
    # Add the item to the list
    rss_items.append(rss_item)

    # stop when you reach the post #20
    counter += 1
    if counter == 20: break

# Create the RSS feed
rss_feed = PyRSS2Gen.RSS2(
    title="Moheb Rofail",
    link=site_url,
    description="RSS feed for Moheb Rofail",
    lastBuildDate=datetime.now(),
    items=rss_items
)

# Write the RSS feed to a file
with open('feed.xml', 'w', encoding='utf-8') as file:
    rss_feed.write_xml(file, 'utf-8')

print("RSS feed generated successfully.")
