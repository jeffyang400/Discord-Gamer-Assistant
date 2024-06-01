import threading

from flask import Flask, request
from spotipy import SpotifyOAuth, Spotify


def spotify_setup(bot, spotify_id, spotify_secret, spotify_uri):
    sp_oauth = SpotifyOAuth(
        client_id=spotify_id,
        client_secret=spotify_secret,
        redirect_uri=spotify_uri,
        scope='user-library-read'
    )

    app = Flask(__name__)

    @app.route('/callback')
    def spotify_callback():
        code = request.args.get('code')
        if code:
            token_info = sp_oauth.get_access_token(code)
            if token_info:
                return "Spotify authentication is complete. You can close this window."
            else:
                return "Failed to get the access token."
        return "No code provided."

    def run_flask():
        app.run(host='0.0.0.0', port=8888)

    # Running Flask in a separate thread
    threading.Thread(target=run_flask).start()

    @bot.command(name='spotify')
    async def fetch_spotify(ctx, *, query):
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            await ctx.send(f'Please authenticate with Spotify by clicking [here]({auth_url})')
            return

        sp = Spotify(auth=token_info['access_token'])
        results = sp.search(q=query, limit=1, type='track')
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            title = track['name']
            artist = track['artists'][0]['name']
            url = track['external_urls']['spotify']
            response = f"**{title}** by **{artist}**\nListen here: {url}"
        else:
            response = "No results found for your query."

        await ctx.send(response)