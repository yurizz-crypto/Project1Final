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

def showMenu(menu: str) -> None:
    if menu in MENUS:
        for key, value in MENUS[menu].items():
            print(f"[{key}] {value}")

def should_quit(var: str) -> bool:
    return var == "q" or var == "Q"

def addTrackToPlaylist(musicLibrary: AVLTree, playlistName: str) -> None:
    playlist_obj = Playlist.loadFromJson(playlistName)
    if not playlist_obj:
        print(f"Playlist '{playlistName}' not found.")
        return

    while True:
        title = input("Enter title of the track ('q' to cancel): ")
        if should_quit(title):
            break

        duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
        found = musicLibrary.searchTrack(title)

        if len(duplicates) > 1:
            showDuplicates(duplicates)
            artist_name = input("\nSpecify track artist ('q' to cancel): ")
            if should_quit(artist_name):
                print(f"No track added to the playlist {playlistName}.")
                break

            track = musicLibrary.searchTrack(title, artist_name)
            if track:
                if track not in playlist_obj.getTracks():
                    playlist_obj.addTrack(track)
                    playlist_obj.saveToJson()
                    print(f"Track '{track.getTitle()}' by {track.getArtist()} added successfully to the playlist.")
                else:
                    print(f"Track '{track.getTitle()}' is already in the playlist {playlistName}.")
            else:
                print("Track not found. Please try again.")

        elif found:
            if found not in playlist_obj.getTracks():
                playlist_obj.addTrack(found)
                playlist_obj.saveToJson()
                print(f"{found.getTitle()} by {found.getArtist()} added successfully to the playlist.")
            else:
                print(f"Track '{found.getTitle()}' is already in the playlist {playlistName}.")
        else:
            print("Track not found. Please try again.")
        
        playlist_obj.saveToJson()

def showDuplicates(track_list: list) -> None:
    print("\nDuplicates:")
    for track in track_list:
        print(track.__str__(True))
    print(f"\n{len(track_list)} results found...")

def checkIfSpacesOnly(input_string: str):
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

def addTrack() -> Track | None | bool:
    def validateAndFormatDuration(duration):
        if ":" not in duration and len(duration) > 5 or len(duration) < 1:
            return None

        minutes = duration[:2]
        seconds = duration[2 + 1:]

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

    while True:
        print("\n<---------Add Track--------->")
        print("Instruction | 'q' to cancel adding a track")
        title = input("Enter Title: ")
        if should_quit(title):
            print("Track addition canceled.\n")
            return None
        if not title or checkIfSpacesOnly(title):
            print("Title cannot be empty. Please enter a valid title.")
            continue

        artist = input("Enter Artist: ")
        if should_quit(artist):
            print("Track addition canceled.\n")
            return None
        if not artist or checkIfSpacesOnly(artist):
            print("Artist cannot be empty. Please enter a valid artist.")
            continue

        additionalArtists = []
        while True:
            collaborators = input("Add Additional Artist(s)? (y/n): ")
            if should_quit(collaborators):
                print("Track addition canceled.\n")
                return None
            elif collaborators == "y" or collaborators == "Y":
                while True:
                    additional = input("Enter other Artist(s) ('q' to stop): ")

                    if should_quit(additional):
                        break

                    elif additional:
                        additionalArtists += [spaceCleaner(additional)]

                    elif not additional or checkIfSpacesOnly(additional):
                        print("Artist name cannot be empty.")

                break

            elif collaborators == "n" or collaborators == "N":
                break

            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        album = input("Enter Album Title: ")
        if should_quit(album):
            print("Track addition canceled.\n")
            return None
        
        if not album or checkIfSpacesOnly(album):
            print("Album cannot be empty. Please enter valid album.")

        while True:
            duration = input("Enter Duration (e.g., 1:42): ")
            if should_quit(duration):
                return None

            formattedDuration = validateAndFormatDuration(duration)
            if formattedDuration:
                break

            else:
                print("Invalid duration. Please enter in 'mm:ss' format.")

        track = Track(spaceCleaner(title), spaceCleaner(artist), spaceCleaner(album), formattedDuration, additionalArtists)
        return (track if musicLibrary.searchTrack(track.getTitle(), track.getArtist()) == None else False)

def playPlaylist(playlistName: str,musicLibrary:Track, queue: MusicQueue):
    playlist = Playlist.loadFromJson(playlistName)
    if not playlist:
        print(f"Playlist '{playlistName}' not found.")
        return

    queue.clearQueue()

    print(f"Loading playlist: {playlistName}")
    for track in playlist.getTracks():
        queue.addTrack(track)

    queue.play()
    
    queue.queueInterface()

def main():
    while True:
        print("\n<==========Listen to Music==========>")
        showMenu("musicLibrary")
        opt = input("\nEnter choice: ")

        match opt:
            case "0":
                musicLibrary.saveToJson()
                print("Exiting program. Goodbye!")
                break
            
            case "1":
                queue.clearQueue()

                for track in musicLibrary.getSortedTracks():
                    queue.addTrack(track)
                
                queue.saveState()
                queue.play()
                queue.queueInterface()

            case "2":
                while True:
                    print("\n<---------Playlists--------->")
                    showMenu("playlists")
                    opt = input("\nEnter choice: ")

                    if opt == "0":
                        break

                    elif opt == "1":
                        playlistName = input("Enter the playlist name to play ('q' to cancel): ")
                        if should_quit(playlistName):
                            continue
                        playPlaylist(playlistName, musicLibrary, queue)

                    elif opt == "2":
                        playlistName = input("Enter new playlist name ('q' to cancel): ")
                        if should_quit(playlistName):
                            continue

                        if playlistName in Playlist.getPlaylistName():
                            print(f"Playlist '{playlistName}' already exists.")
                        else:
                            new_playlist = Playlist(spaceCleaner(playlistName))
                            new_playlist.saveToJson()
                            print(f"Playlist '{playlistName}' created successfully.")

                    elif opt == "3":
                        playlist_names = Playlist.getPlaylistName()
                        if not playlist_names:
                            print("No playlists available.")

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
                                        current_page += 1
                                else:
                                    print("Invalid input. Please try again.")

                    elif opt == "4":
                        while True:
                            playlistName = input("Enter playlist name ('q' to cancel): ")
                            if should_quit(playlistName):
                                break

                            if playlistName not in Playlist.getPlaylistName():
                                print(f'Playlist "{playlistName}" not found.')
                                continue
                            else:
                                addTrackToPlaylist(musicLibrary, playlistName)
                                Playlist(playlistName).saveToJson()
                                break
                            
                    elif opt == "5":
                        playlistName = input("Enter playlist name to delete ('q' to cancel): ")
                        if should_quit(playlistName):
                            continue

                        if playlistName in Playlist.getPlaylistName():
                            Playlist(playlistName).deletePlaylist()
                            print(f"Playlist '{playlistName}' deleted successfully.")
                        else:
                            print(f"Playlist '{playlistName}' not found.")

                    elif opt == "6":
                        playlistName = input("Enter playlist name to display ('q' to cancel): ")
                        if should_quit(playlistName):
                            continue

                        if playlistName in Playlist.getPlaylistName():
                            print(Playlist.loadFromJson(playlistName))

                        else:
                            print(f"Playlist '{playlistName}' not found.")

                    elif opt == "7":
                        while True:
                            playlistName = input("Enter playlist name ('q' to cancel): ")
                            if should_quit(playlistName):
                                break

                            if playlistName not in Playlist.getPlaylistName():
                                print(f"Playlist '{playlistName}' not found. Please check the name and try again.")
                                continue

                            playlist = Playlist.loadFromJson(playlistName)
                            if playlist:
                                track_title = input("Enter title of the track: ")
                                
                                deleted = playlist.removeTrack(track_title)
                                if deleted != None:
                                    print("Track deleted...\n")
                                    break

                                else:
                                    print("Track not found in {}.\n".format(playlistName))
                            
            case "3":
                while True:
                    new_track = addTrack()
                    if new_track is None:
                        break
                    elif new_track:
                        musicLibrary.addTrack(new_track)
                        print("Track added successfully...\n")
                        if input("Add another track? (y/n): ") == "n" or input("Add another track (y/): ") == "N":
                            break

                    else:
                        print("Track already exists...")
                
                musicLibrary.saveToJson()

            case "4":
                print(musicLibrary)
            
            case "5":
                print("\n>>> Search for a Track <<<")
                title = input("Enter title of the track ('q' to cancel): ")
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

            case "6":
                print("\n>>> Delete a Track <<<")
                title = input("Enter title of the track ('q' to cancel): ")
                if should_quit(title):
                    print("Deletion Cancelled...\n")
                    continue

                duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
                found = musicLibrary.searchTrack(title)

                if len(duplicates) > 1:
                    showDuplicates(duplicates)
                    artist_name = input("Specify track artist ('q' to cancel): ")
                    if should_quit(artist_name):
                        continue

                    track = musicLibrary.searchTrack(title, artist_name)
                    if track:
                        print(f"Track {track.getTitle()} by {track.getArtist()} deleted.\n")
                        musicLibrary.removeTrack(track)
                        musicLibrary.saveToJson()
                    else:
                        print("Artist not found.")
                elif found:
                    musicLibrary.removeTrack(found)
                    print("Track deleted.\n")
                else:
                    print("Track not found.\n")

            case "7":
                playlistName = input("\nEnter playlist name ('q' to cancel): ")
                if should_quit(playlistName):
                    continue

                addTrackToPlaylist(musicLibrary, playlistName)
            
            case _:
                print("Invalid Option.")

if __name__ == "__main__":
    main()