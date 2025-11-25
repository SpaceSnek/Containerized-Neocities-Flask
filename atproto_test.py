from atproto import Client
import credentials
client = Client()
client.login(credentials.username, credentials.password)
target_handle = 'spacesnek.shrimplybetter.me'

feed = client.app.bsky.feed.get_author_feed({'actor': target_handle, 'limit': 1})
formattedPost = []
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
        formattedPost.append((author, postText, embed))
    except KeyError:
        formattedPost = "This post has been deleted or is not displaying properly."
print(f"{formattedPost[0][0]}: \"{formattedPost[0][1]}\"\n{formattedPost[0][2]}")