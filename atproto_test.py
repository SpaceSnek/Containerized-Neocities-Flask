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
        postText = record.text
        embed = post_view.post.embed
        print(embed)
        if hasattr(embed, 'images') and embed.images:
            embed = embed.images[0].thumb
        elif hasattr(embed, 'thumbnail') and embed.thumbnail:
            embed = embed.thumbnail
            postText = postText + " [Video thumbail, find video on bsky]"
        else:
            embed = ""
        author = post_view.post.author.handle
        formattedPost.append((author, postText, embed))
        print(post_view.post.embed)
    except KeyError:
        formattedPost = "This post has been deleted or is not displaying properly."
print(f"{formattedPost[0][0]}: \"{formattedPost[0][1]}\"\n{formattedPost[0][2]}")