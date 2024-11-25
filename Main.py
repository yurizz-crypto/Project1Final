from TrackClass import Track
from AVLTree import AVLTree
from PlaylistClass import Playlist
from QueueClass import MusicQueue

musicLibrary = AVLTree()
musicLibrary.load_from_json()
playlist = Playlist
queue = MusicQueue()

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

def showDuplicates(track_list: list):
    print("\nDuplicates:")
    num = 0
    for track in track_list:
        print(track.__str__(True))
        num += 1

    print(f"\n{num} results found...")

def shouldQuit(var: str) -> bool:
        return (True if var == "q" or var == "Q" else False)

def addTrack():
    def validateAndFormatDuration(duration):
        if ":" not in duration and len(duration) > 5 or len(duration) < 1:
            return None

        colon_index = -1
        for i in range(len(duration)):
            if duration[i] == ":":
                colon_index = i
                break

        minutes = duration[:colon_index]
        seconds = duration[colon_index + 1:]

        for char in minutes:
            if not ('0' <= char <= '9'):
                return None

        for char in seconds:
            if not ('0' <= char <= '9'):
                return None

        minutes_value = 0
        for i in range(len(minutes)):
            minutes_value = minutes_value * 10 + (int(minutes[i]))

        seconds_value = 0
        for i in range(len(seconds)):
            seconds_value = seconds_value * 10 + (int(seconds[i]))

        if minutes_value < 0 or seconds_value < 0 or seconds_value > 59:
            return None

        formatted_minutes = str(minutes_value)
        formatted_seconds = str(seconds_value)

        if len(formatted_minutes) == 1:
            formatted_minutes = "0" + formatted_minutes

        if len(formatted_seconds) == 1:
            formatted_seconds = "0" + formatted_seconds

        return formatted_minutes + ":" + formatted_seconds

def main():
    # Diri mag Start para sa UI
    pass