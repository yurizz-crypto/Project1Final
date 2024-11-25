from TrackClass import Track
from AVLTree import AVLTree
from PlaylistClass import Playlist
from QueueClass import MusicQueue

MENUS = {
    "main": {
        1 : "Library",
        2 : "Playlists",
        3 : "Queue",
        4 : "Now Playing",
        5 : "Exit"
    },
    "musicLibrary": {
        1 : "Add a New Track",
        2 : "View All Tracks",
        3 : "Search for a Track",
        4 : "Delete a Track",
        5 : "Return to Main Menu",
    },
    "playlists": {
        1 : "Create a New Playlist",
        2 : "View All Playlist",
        3 : "Add Tracks to a Playlist",
        4 : "Delete a Playlist",
        5 : "Display a Playlist",
        6 : "Return to Main Menu"
    },
    "queue" : {
        1 : "Play",
        2 : "Next",
        3 : "Previous",
        4 : "Shuffle",
        5 : "Repeat",
        6 : "Clear Queue",
        7 : "Exit"
    }   
}

def showMenu(menu: str) -> str:
    if menu in MENUS:
        keys = list(MENUS[menu])
        for i in range(len(keys)):
            print("[{}]".format(str(keys[i])) + " " + MENUS[menu][keys[i]])
    else:
        print("Menu not found.")

def shouldQuit(var: str) -> bool:
        return (True if var == "q" or var == "Q" else False)

def main():
    musicLibrary = AVLTree()
    musicLibrary.load_from_json()
    playlist = Playlist
    queue = MusicQueue()
    # Diri mag Start para sa UI