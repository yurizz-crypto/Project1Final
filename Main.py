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
        6 : "Delete a Track",
        7 : "Add Track to a Playlist"
        0 : "Exit:
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

def should_quit(var: str) -> bool:
    return var == "q" or var == "Q"

def addTrackToPlaylist(musicLibrary: AVLTree, playlist_name: str) -> None:
    if playlist_name not in Playlist.getPlaylists():
        print(f"Playlist "{playlist_name}" not found." )
        return
        
    while True:
          title = input("Enter title of the track ('q' to cancel): ")
        if should_quit(title):
            print(f"No track added to the playlist {playlist_name}.\n")
            break

        duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
        found = musicLibrary.searchTrack(title)

        if len(duplicates) > 1:
            showDuplicates(duplicates)
            artist_name = input("\nSpecify track artist ('q' to cancel): ")
            if should_quit(artist_name):
                print(f"No track added to the playlist {playlist_name}.")
                break

            track = musicLibrary.searchTrack(title, artist_name)
            if track:
                playlist_obj = Playlist(playlist_name)
                playlist_obj.addTrack(track)
                playlist_obj.saveToJson()
                print("Track added successfully to the playlist.")
                break

        elif found:
            playlist_obj = Playlist(playlist_name)
            playlist_obj.addTrack(found)
            playlist_obj.saveToJson()
            print("Track added successfully to the playlist.")
            break

        else:
            print("Track not found. Please try again.")
                
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
    while True:
        print("\n<==========Listen to Music==========>")
        showMenu("musicLibrary")
        opt = input("\nEnter choice: ")

        match opt:
            case "0":
                musicLibrary.saveToJson()
                print("Exiting Program...")
                break

            #case "1"

            case "2":
                # The Diplay this if the input is 2
                # 1: "Play a playlist",
                # 2: "Create a New Playlist",
                # 3: "View All Playlists",
                # 4: "Add Track to a Playlist",
                # 5: "Delete a Playlist",
                # 6: "Display a Playlist",
                # 7: "Delete a Track in Playlist",
                # 8: "Return"
                while True:
                    print("\n<---------Playlists--------->")
                    showMenu("playlists")
                    opt = input("\nEnter choice: ")

                    if opt == "0":
                        break

                    elif opt == "1":
                        pass

                    elif opt == "2":  # Create a New Playlist
                        playlist_name = input("Enter new playlist name ('q' to cancel): ")
                        if should_quit(playlist_name):
                            continue

                        if playlist_name in Playlist.getPlaylists():
                            print(f"Playlist '{playlist_name}' already exists.")
                        else:
                            new_playlist = Playlist(playlist_name)
                            new_playlist.saveToJson()
                            print(f"Playlist '{playlist_name}' created successfully.")

            case "2":
                while True:
                    print("\n<--------Playlists-------->")
                    showMenu("playlists")
                    opt = input("\nEnter choice: ")

                    if opt == "1":
                        pass

                    elif opt == "2":
                        playlist_name = input("Enter new playlist name('q' to cancel): ")
                        if should_quit(playlist_name):
                            continue'

                        if playlist_name in Playlist.getPlaylist():
                            print(f"Playlist '{playlist_name}' already exists.")
                        else:
                            new_playlist = Playlist(spaceCleaner(playlist_name))
                            new_playlist.saveToJson()
                            print(f"Playlist '{playlist_name}' created successfully.")

                    elif opt =="3":
                        playlist_names = Playlist.getPlaylists()
                        if not playlist_names:
                            print("No playlists available.:)

                        else:
                            current_page = 1
                            while True:
                                print(Playlist.displayPlaylists(playlist_names, current_page))
                                user_input = input("Enter option ('0' to Exit): ")
                                if user_input == "0":
                                    break
                                elif user_input == "11":
                                    if current_page > 1:
                                        current_page -= 1
                                elif user_input == "12":
                                    if current_page < (len(playlist_names) + 6) // 7:
                                        curent_page += 1
                                else:
                                    print("Invalid input. Please try again.")
            
            case "3":
                while True:
                    new_track = addTrack()
                    if new_track is None:
                        break
                    elif new_track:
                        musicLibrary.addTrack(new_track)
                        print("Track added successfully!\n")
                        if input("Add another track? (y/n): ") == "n" or input("Add another track (y/): ") == "N":
                            break
                        musicLibrary.saveToJson()
                    else: 
                        print("Track already exists.")

            case "4":
                print(musicLibrary)
            
            case "5":
                print("\n>>> Search for a Track <<<")
                title = input("Enter Track title ('q' to cancel): ")
                if should_quit(title):
                    continue

                duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
                found = musicLibrary.searchTrack(title)

                if len(duplicates) > 1:
                    showDuplicates(duplicates)
                elif found: 
                    print(found)
                else:
                    print("Track not found.\n")
