import argparse
import json
import openai
import os
import spotipy
from dotenv import load_dotenv


def login_spotify(client_id, client_secret):

    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://localhost:9999',
            scope="playlist-modify-private"
        )
    )

    return sp


def create_playlist(SpotifyClient, name):
    cuurent_user_id = SpotifyClient.current_user()["id"]
    new_playlist = SpotifyClient.user_playlist_create(
        cuurent_user_id,
        public=False,
        name=name
    )

    return new_playlist


def add_to_playlist(SpotifyClient, playlist_id, tracks_ids):
    current_user_id = SpotifyClient.current_user()["id"]

    SpotifyClient.user_playlist_add_tracks(
        current_user_id,
        playlist_id,
        tracks_ids
    )


def search_song(SpotifyClient, title):
    results = SpotifyClient.search(q=title, type="track", limit=1)
    return results["tracks"]["items"][0]["id"]


def get_playlist(prompt, num_of_songs):

    def parse_result(result):
        try:
            start = result.index("[")
            string = result[start:]
            return json.loads(string)
        except Exception as e:
            print(e)

    messages = [
        {
            "role": "system",
            "content": """You are a helpful playlist generating assitant.
            You should generate a list of songs and their artists according to a text prompt.
            You should return only a JSON array where each element follows this format: {"song": <song_title>, "artist": <artist_name>}."""
        },
        {
            "role": "user",
            "content": "Generate a playlist with 10 songs based on this prompt: top 10 bilboard pop songs 2020"
        },
        {
            "role": "system",
            "content": """
            [
                {"song": "Blinding Lights", "artist": "The Weeknd"}        
                {"song": "Circles", "artist": "Post Malone"}
                {"song": "The Box", "artist": "Roddy Ricch"}
                {"song": "Don't Start Now", "artist": "Dua Lipa"}
                {"song": "Adore You", "artist": "Harry Styles"}
                {"song": "Everything I Wanted", "artist": "Billie Eilish"} 
                {"song": "Life Is Good", "artist": "Future ft. Drake"}     
                {"song": "Intentions", "artist": "Justin Bieber ft. Quavo"}
                {"song": "Someone You Loved", "artist": "Lewis Capaldi"}   
                {"song": "Say So", "artist": "Doja Cat"}
            ]
            """
        },
        {
            "role": "user",
            "content": "Generate a playlist with 5 songs based on this prompt: instrumental"
        },
        {
            "role": "system",
            "content": """
            [
                {"song": "Comptine d'un autre ete, L'apres-midi", "artist": "Yann Tiersen"},
                {"song": "Clair de Lune", "artist": "Claude Debussy"},
                {"song": "The Four Seasons - Concerto No. 4 in F Minor, RV 297, 'Winter' - II. Largo", "artist": "Antonio Vivaldi"},
                {"song": "Moonlight Sonata, 1st Movement", "artist": "Ludwig van Beethoven"},
                {"song": "Rhapsody on a Theme of Paganini, Op. 43: 18. Variation XVIII", "artist": "Sergei Rachmaninoff"}
            ]
            """
        },
        {
            "role": "user",
            "content": f"Generate a playlist with {num_of_songs} songs based on this prompt: {prompt}"
        }
    ]

    res = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=500
    )

    return (parse_result(res["choices"][0]["message"]["content"]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Simple command line playlist utility."
    )

    parser.add_argument("--prompt", type=str, help="Prompt to generate the playlist")
    parser.add_argument("--name", type=str, help="Name of the playlist")
    parser.add_argument("--size", type=int, help="Number of songs to include", default=10)

    args = parser.parse_args()

    # load .env data
    load_dotenv()

    # get spotify data
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # get openai data
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # log into spotify
    curr_user = login_spotify(client_id, client_secret)
    assert curr_user is not None

    # prompt
    songs = get_playlist(args.prompt, args.size)

    # empty list to store tracks' ids
    tracks_ids = list()

    if songs is not None:
        for song in songs:
            query = f"{song['song']}, {song['artist']}"
            id = search_song(curr_user, query)
            if id:
                tracks_ids.append(id)

    new_playlist = create_playlist(curr_user, args.name)
    new_playlist_id = (new_playlist["id"])

    # add tracks to playlist
    add_to_playlist(curr_user, new_playlist_id, tracks_ids)

    print("Playlist created!")