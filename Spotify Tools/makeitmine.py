import spotipy
from spotipy.oauth2 import SpotifyOAuth


def initialize_spotify_client():
    """
    Initializes the Spotify client with the required scope and credentials.

    :return: Authenticated Spotify client instance.
    """
    scope = "user-library-read playlist-modify-public playlist-modify-private"
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    REDIRECT_URI = "http://localhost:8080/"

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope
    ))


def get_user_id(sp):
    """
    Retrieves the current user's Spotify ID.

    :param sp: Authenticated Spotify client instance.
    :return: Spotify user ID.
    """
    return sp.me()['id']


def get_songs(sp, playlist_id):
    """
    Retrieves all song URIs from a specified playlist.

    :param sp: Authenticated Spotify client instance.
    :param playlist_id: ID of the playlist to retrieve songs from.
    :return: List of song URIs.
    """
    try:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        return [item['track']['uri'] for item in playlist_tracks['items']]
    except Exception as e:
        print(f"Error retrieving songs: {e}")
        return []


def create_playlist(sp, user_id, playlist_name):
    """
    Creates a new playlist under the user's account.

    :param sp: Authenticated Spotify client instance.
    :param user_id: Spotify user ID.
    :param playlist_name: Name of the new playlist.
    :return: Details of the created playlist.
    """
    try:
        return sp.user_playlist_create(user=user_id, name=playlist_name)
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return None


def add_songs(sp, playlist_id, song_list):
    """
    Adds songs to a specified playlist.

    :param sp: Authenticated Spotify client instance.
    :param playlist_id: ID of the playlist to add songs to.
    :param song_list: List of song URIs.
    """
    try:
        sp.playlist_add_items(playlist_id, song_list)
        print(f"Added {len(song_list)} songs to the playlist.")
    except Exception as e:
        print(f"Error adding songs: {e}")


def main():
    sp = initialize_spotify_client()
    user_id = get_user_id(sp)

    # Get user input for playlist duplication
    source_playlist_id = input("Enter the ID of the playlist to copy: ").strip()
    new_playlist_name = input("Enter the name for the new playlist: ").strip()

    # Retrieve songs from the source playlist
    songs = get_songs(sp, source_playlist_id)
    if not songs:
        print("No songs retrieved. Exiting.")
        return

    # Create a new playlist
    created_playlist = create_playlist(sp, user_id, new_playlist_name)
    if not created_playlist:
        print("Failed to create playlist. Exiting.")
        return

    # Add songs to the new playlist
    add_songs(sp, created_playlist['id'], songs)
    print(f"Playlist '{new_playlist_name}' created and populated successfully.")


if __name__ == "__main__":
    main()
