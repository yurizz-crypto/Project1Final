from TrackClass import Track
from AVLTree import AVLTree
from PlaylistClass import Playlist
from QueueClass import MusicQueue

musicLibrary = AVLTree()
musicLibrary.loadFromJson()
queue = MusicQueue()
queue.loadStateFromJSON()

MENUS = {
    "musicLibrary": {
        1: "Play Library",
        2: "Playlists",
        3: "Add a New Track",
        4: "View All Tracks",
        5: "Search for a Track",
        6: "Delete a Track",
        7: "Add Track to a Playlist",
        0: "Exit"
    },
    "playlists": {
        1: "Play a playlist",
        2: "Create a New Playlist",
        3: "View All Playlists",
        4: "Add Track to a Playlist",
        5: "Delete a Playlist",
        6: "Display a Playlist",
        7: "Delete a Track in Playlist",
        0: "Return"
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

def checkIfSpaceOnly(input_string: str):
    for char in input_string:
        if char != " ":
            return False
    return True

def spaceCleaner(input_string: str):
    start = 0
    while start < len(input_string) and input_string[start] == " ":
        start += 1

    end = len(input_string) - 1
    while end >= 0 and input_string[end] == " ":
        end -= 1

    trimmed = input_string[start:end + 1] if end >= start else ""

    result = ""
    in_space = False
    for char in trimmed:
        if char == " ":
            if not in_space:
                result += char
            in_space = True
        else:
            result += char
            in_space = False

    return result

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


def playPlaylist(playlistName: str, musicLibrary: AVLTree, queue: MusicQueue):
    # Check if the playlist exists
    playlist = Playlist.loadFromJson(playlistName)
    if not playlist:
        print(f"Playlist '{playlistName}' not found.")
        return

    # Clear the current queue
    queue.clearQueue()

    # Add tracks from the playlist to the queue
    print(f"Loading playlist: {playlistName}")
    for track in playlist.getTracks():
        queue.addTrack(track)

    #start playing current queue
    queue.play()

    queue.queueInterface()

def main():
    # Main loop
    while True:
        print("\n<==========Listen to Music==========>")
        showMenu("musicLibrary")
        opt = input("\nEnter choice: ")

        match opt:
            # If user choose to exit the program
            case "0":
                musicLibrary.saveToJson()
                print("Exiting Program...")
                break

            case "1":
                # Clearing current queue and sorted tracks
                queue.clearQueue()

                # Adding sorted tracks to the queue
                for track in musicLibrary.getSortedTracks():
                    queue.addTrack(track)
                
                # Start queue interface
                queue.queueInterface()

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
                        if shouldQuit(playlist_name):
                            continue

                        if playlist_name in Playlist.getPlaylists():
                            print(f"Playlist '{playlist_name}' already exists.")
                        else:
                            new_playlist = Playlist(playlist_name)
                            new_playlist.saveToJson()
                            print(f"Playlist '{playlist_name}' created successfully.")
            
            # Adding a new track to the music library
            case "3":
                while True:
                    new_track = addTrack()
                    if new_track is None:
                        # Exiting loop if user choose to cancel
                        break
                    elif new_track:
                        musicLibrary.addTrack(new_track)
                        # Successful addition of track
                        print("Track added successfully!\n")
                        # Adding another track
                        if input("Add another track? (y/n): ") == "n" or input("Add another track (y/n): ") == "N":
                            break
                        # Saving changes to music library
                        musicLibrary.saveToJson()
                    # If track is already in the library
                    else:
                        print("Track already exists.")

            # Dsiplaying music library
            case "4":
                print(musicLibrary)
            
            # Method for searching a track in music library
            case "5":
                print("\n>>> Search for a Track <<<")
                title = input("Enter Track title ('q' to cancel): ")
                if shouldQuit(title):
                    continue
                
                # Searching duplicate track
                duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
                found = musicLibrary.searchTrack(title)

                # If there is duplication:
                if len(duplicates) > 1:
                    showDuplicates(duplicates)

                # If no duplication, show track
                elif found: 
                    print(found)
                
                # If not found, notify
                else:
                    print("Track not found.\n")

            case "6":
                print("\n>>> Delete a Track <<<")
                title = input("Enter title of the track ('q' to cancel): ")
                if shouldQuit(title):
                    print("Deletion Cancelled...\n")
                    continue

                duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
                found = musicLibrary.searchTrack(title)

                if len(duplicates) > 1:
                    showDuplicates(duplicates)
                    artist_name = input("Specify track artist ('q' to cancel): ")
                    if shouldQuit(artist_name):
                        continue

                    track = musicLibrary.searchTrack(title, artist_name)
                    if track:
                        musicLibrary.removeTrack(track)
                        print("Track deleted.\n")
                        musicLibrary.saveToJson()
                    else:
                        print("Artist not found.")
                elif found:
                    musicLibrary.removeTrack(found)
                    print("Track deleted.\n")
                else:
                    print("Track not found.\n")

            case "7":
                playlist_name = input("\nEnter playlist name ('q' to cancel): ")
                if shouldQuit(playlist_name):
                    continue

                # addTrackToPlaylist(musicLibrary, playlist_name)
                # ???? 

            case _:
                print("Invalid Option.")

    if __name__ == "__main__":
        main()

                    
