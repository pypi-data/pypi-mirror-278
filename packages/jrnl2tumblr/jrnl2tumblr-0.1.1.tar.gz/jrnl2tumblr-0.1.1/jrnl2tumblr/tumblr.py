import pytumblr

def create_tumblr_client(consumer_key, consumer_secret, oauth_token, oauth_secret):
    client = pytumblr.TumblrRestClient(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret
    )
    return client

def post_entries_to_tumblr(entries, client, blog_name):
    for entry in entries:
        title = entry.get('title', 'No Title')
        body = entry['body']
        tags = entry.get('tags', [])

        client.create_text(
            blog_name,
            state="published",
            title=title,
            body=body,
            tags=tags
        )
        print(f"Published entry: {title}")
