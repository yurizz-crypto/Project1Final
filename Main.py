from TrackClass import Track
from AVLTree import AVLTree
from PlaylistClass import Playlist
from QueueClass import MusicQueue

musicLibrary = AVLTree()
musicLibrary.loadFromJson()
queue = MusicQueue()
queue.loadState()

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
    """
    Displays the menu options for the specified menu.

    Parameters:
        menu (str): The name of the menu to display

    """
    if menu in MENUS:
        keys = list(MENUS[menu])
        for i in range(len(keys)):
            print("[" + str(keys[i]) + "] " + MENUS[menu][keys[i]])
    else:
        print("Menu not found.")

def should_quit(var: str) -> bool:
    """
    Checks if the input variable indicates a request to quit.

    Parameters:
        var (str): The input variable to check.

    Returns:
        bool: True if the input is 'q' or 'Q', otherwise False.
    """
    return var == "q" or var == "Q"

def addTrackToPlaylist(musicLibrary: AVLTree, playlistName: str) -> None:
    """
    Adds a track to the specified playlist.

    Parameters:
        musicLibrary (AVLTree): The music library containing tracks.
        playlistName (str): The name of the playlist to which the track will be added.
    """
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
    """
    Displays a list of duplicate tracks.

    Parameters:
        track_list (list): A list of duplicate track objects.

    """
    print("\nDuplicates:")
    for track in track_list:
        print(track.__str__(True))
    print(f"\n{len(track_list)} results found...")

def checkIfSpacesOnly(input_string: str):
    """
    Checks if the input string contains only spaces.

    Parameters:
        input_string (str): The string to check.

    Returns:
        bool: True if the string contains only spaces, otherwise False.
    """
    for char in input_string:
        if char != " ":
            return False
    return True

def spaceCleaner(input_string: str):
    """
    Cleans the input string by trimming leading and trailing spaces and reducing multiple spaces to a single space.

    Parameters:
        input_string (str): The string to clean.

    Returns:
        str: The cleaned string.
    """

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
    """
    Prompts the user to add a new track to the music library.

    Returns:
        Track, None , bool: Returns a Track object if added successfully, None if canceled, or False if the track already exists.
    """
    def validateAndFormatDuration(duration):
        """
        Parameters:
            duration (str): A string representing the duration in "mm:ss" format.
        Returns:
            str or None: Returns a formatted duration string if valid; otherwise, returns None

        This method validates the input duration string to ensure it follows the "mm:ss" 
        format checking for a single colon valid numeric values, and appropriate ranges 
        (minutes >= 0, seconds between 0-59). It returns the formatted duration as a two-digit string or 
        None if the input is invalid
        """

         # Check for exactly one ':' in the input
        colon_count = 0
        colon_index = -1
        length = 0

        # Manually find the length of the input and locate the ':'
        for char in duration:
            length += 1
            if char == ':':
                colon_count += 1
                colon_index = length - 1

        if colon_count != 1 or length > 5 or length < 4:
            return None

        # Separate minutes and seconds manually
        minutes = ""
        seconds = ""

        for i in range(length):
            if i < colon_index:
                minutes += duration[i]
            elif i > colon_index:
                seconds += duration[i]

        # Validate that minutes and seconds contain only digits
        valid_digits = "0123456789"

        for char in minutes:
            is_valid = False
            for digit in valid_digits:
                if char == digit:
                    is_valid = True
                    break
            if not is_valid:
                return None

        for char in seconds:
            is_valid = False
            for digit in valid_digits:
                if char == digit:
                    is_valid = True
                    break
            if not is_valid:
                return None

        # Convert minutes to an integer manually
        minutes_value = 0
        for char in minutes:
            for i in range(10):  # Loop through 0-9 to find the numeric value
                if char == valid_digits[i]:
                    minutes_value = minutes_value * 10 + i
                    break

        # Convert seconds to an integer manually
        seconds_value = 0
        for char in seconds:
            for i in range(10):  # Loop through 0-9 to find the numeric value
                if char == valid_digits[i]:
                    seconds_value = seconds_value * 10 + i
                    break

        # Check for valid range of minutes and seconds
        if minutes_value < 0 or seconds_value < 0 or seconds_value > 59:
            return None

        # Format minutes and seconds manually to ensure two digits
        formatted_minutes = ""
        formatted_seconds = ""

        if minutes_value < 10:
            formatted_minutes += "0"
        if minutes_value >= 10:
            formatted_minutes += valid_digits[minutes_value // 10]
        formatted_minutes += valid_digits[minutes_value % 10]

        if seconds_value < 10:
            formatted_seconds += "0"
        if seconds_value >= 10:
            formatted_seconds += valid_digits[seconds_value // 10]
        formatted_seconds += valid_digits[seconds_value % 10]

        # Return the formatted duration
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

    queue.checkAndLoadState(source="Playlist", playlist_name=playlistName)
    if queue.isQueueEmpty():
        for track in playlist.getTracks():
            queue.addTrack(track)
        queue.saveState(source="Playlist", playlist_name=playlistName)

    queue.play()
    queue.queueInterface()
    queue.saveState(source="Playlist", playlist_name=playlistName)


def main():
    """
    Menu interface for managing and interacting with a music library, including tracks and playlists.
        Managing tracks (add, search, delete);
        Playing tracks/playlists;
        Managing playlists (create, add/remove tracks, display, delete);
        Persistent data storage in JSON format

    """
    while True:
        print("\n<==========Listen to Music==========>")
        showMenu("musicLibrary")
        opt = input("\nEnter choice: ")

        match opt:
            case "0":
            # Exit Program
                musicLibrary.saveToJson()
                print("Exiting program. Goodbye!")
                break
            
            case "1":
                queue.checkAndLoadState(source="Library")
                if queue.isQueueEmpty():
                    for track in musicLibrary.getSortedTracks():
                        queue.addTrack(track)
                        queue.saveState()

                queue.play()
                queue.queueInterface()
                queue.saveState()

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
                # Adds new track
                while True:
                    new_track = addTrack()
                    if new_track is None:
                        break
                    elif new_track:
                        # Add track to library
                        musicLibrary.addTrack(new_track)
                        print("Track added successfully...\n")
                        if input("Add another track? (y/n): ") == "n" or input("Add another track (y/): ") == "N":
                            break

                    else:
                        print("Track already exists...")
                
                # Save updated library
                musicLibrary.saveToJson()

            case "4":
                # Display all tracks in the music library.
                print(musicLibrary)
            
            case "5":
                # Search for a track
                print("\n>>> Search for a Track <<<")
                title = input("Enter title of the track ('q' to cancel): ")
                if should_quit(title):
                    continue   

                duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
                found = musicLibrary.searchTrack(title)

                if len(duplicates) > 1:
                    # Handle duplicate tracks
                    showDuplicates(duplicates)
                elif found:
                    print(found)
                else:
                    print("Track not found.\n")

            case "6":       # Prompt user to enter the title of the track to delete
                print("\n>>> Delete a Track <<<")
                title = input("Enter title of the track ('q' to cancel): ")
                if should_quit(title):   # Check if the user wants to cancel the operation
                    print("Deletion Cancelled...\n")
                    continue   # Exit the current loop and return to the main menu

                
                # Retrieve duplicates of the track in the music library
                
                duplicates = musicLibrary.getDuplicates(musicLibrary.getRoot(), title)
                found = musicLibrary.searchTrack(title)

                # If there are multiple duplicates, ask for the artist's name to identify the correct track
                if len(duplicates) > 1:
                    showDuplicates(duplicates)
                    artist_name = input("Specify track artist ('q' to cancel): ")
                    if should_quit(artist_name):   # If the user cancels, move to the next loop
                        continue

                    # Search for the track by both title and artist
                    track = musicLibrary.searchTrack(title, artist_name)
                    if track:
                        print(f"Track {track.getTitle()} by {track.getArtist()} deleted.\n")
                        musicLibrary.removeTrack(track) # Delete the track from the library
                        musicLibrary.saveToJson() # Save the updated library to a JSON file
                    else:
                        print("Artist not found.") 
                elif found:                       # If there's no duplication, simply delete the track found by title
                    musicLibrary.removeTrack(found)
                    print("Track deleted.\n")
                else:                             # If no track is found with the specified artist
                    print("Track not found.\n") 

            case "7":                     # Prompt the user to enter the playlist name where they want to add a track
                playlistName = input("\nEnter playlist name ('q' to cancel): ")
                if should_quit(playlistName):
                    continue

                # Add the track to the specified playlist
                addTrackToPlaylist(musicLibrary, playlistName)
            
            case _:
                print("Invalid Option.")

if __name__ == "__main__":
    main()
