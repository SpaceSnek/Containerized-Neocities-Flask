from atproto import Client
import credentials
client = Client()
client.login(credentials.username, credentials.password)
target_handle = 'spacesnek.shrimplybetter.me'

feed = client.app.bsky.feed.get_author_feed({'actor': target_handle, 'limit': 1})
for post_view in feed['feed']:
    try:
        record = post_view.post.record
        embed = post_view.post.embed
        try:
            embed = embed.images[0].thumb
        except:
            embed = ""
            pass
        author = post_view.post.author.handle
        postText = record.text
        postTime = record.created_at
        formattedPost = (author, postText, embed, postTime)
    except KeyError:
        formattedPost = "This post has been deleted or is not displaying properly."
    print(formattedPost[0])
    print(formattedPost[1])