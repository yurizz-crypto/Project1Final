import json
from TrackClass import Track
import os

class Playlist:
    def __init__(self, name):
        self.__name = name
        self.__tracks = []
        self.__total_duration = "00:00"

    def getName(self):
        return self.__name

    def getTotalDuration(self):
        return self.__total_duration

    def getTracks(self):
        return self.__tracks

    def countSameTitles(self, track: Track):
        """
        Checks if a track with the same title appears more than once in the playlist.

        Returns: Bool
        True if a track with the same title exists more than once, else False.
        """
        count = 0
        for i in self.__tracks:
            # Iterate through all the tracks and compare title for each track.
            if i.getTitle() == track.getTitle():
                # If titles match, increment the counter and return True if title appears more than once.
                count += 1
        return count > 1

    def addTrack(self, track):
        """
        Adds a track to the playlist if it does not exist yet and updates total duration.

        Returns:
        False (Boolean) if the track already exists else it returns the added track.
        """
        if track not in self.__tracks:
            self.__tracks += [track]
            self.updateTotalDuration()
            return track
        return False
    
    def removeTrack(self, title: str):
        """
        Removes a track from the playlist by its title through divide-and-conquer approach.

        Title of the track (string) as the parameter.
        """
        def divideAndConquer(tracks):
            """
            Helper method to recursively search for the track to remove.

            Parameter: Tracks -> list of tracks to search through

            Returns: Tuple
            A list of remaining tracks and the removed track (if there is).
            """
            if not tracks:
                # If the list is empty, it returns and empty list and None
                return [], None
            
            # If there is only one track in the list:
            if len(tracks) == 1: 
                track = tracks[0]
                # Checks if the title matched with the given title
                if track.getTitle() == title:
                    # If titles match, track will be remove else track is keep and returns None.
                    return [], track
                else:
                    return [track], None
            
            # Dividing the list into two halves.
            mid = len(tracks) // 2
            # Recursive search in the left half
            left, removed_left = divideAndConquer(tracks[:mid])
            # Recursive search in the right half
            right, removed_right = divideAndConquer(tracks[mid:])

            # Checks which half contains the removed track
            removed_track = removed_left or  removed_right
            # Combines remaining tracks and returns the removed track
            return left + right, removed_track
        
        # Divide and conquer approach to find and remove the track.
        new_tracks, removed_track = divideAndConquer(self.__tracks)

        """
        If track is removed:
            Update the playlist with the remaining tracks;
            Update the total duration of the playlist;
            Save the updated playlist to a JSON file; and
            Return the removed track.
        """
        if removed_track:
            self.__tracks = new_tracks
            self.updateTotalDuration()
            self.saveToJson()
        return removed_track
    
    def deletePlaylist(self):
        """
        Deletes the JSON file with the playlist from the disk.

        Returns: Bool
        True if file is successfully deleted, else False.
        """

        # Constructing file path
        filename = f"Data/Playlists/{self.getName()}.json"
        # Check if the file exists, if it does then it will be deleted.
        if os.path.exists(filename):
            os.remove(filename)
            return True
    
    def updateTotalDuration(self):
        """
        Updates total duration of the playlist by summing the duration of all tracks.

        Duration of each track is retrived in seconds, and the total is converted to  
        "MM:SS" format.
        """
        total_sec = 0
        track: Track
        # Iterate through all tracks in the playlist and add the duration of each track (in seconds).
        for track in self.getTracks():
            total_sec += track.getDurationInSeconds()
        # Converts total seconds to "MM:SS" format
        self.__total_duration = f"{total_sec // 60:02}:{total_sec % 60:02}"
 
    def saveToJson(self):
        """
        Saves the playlist data to a JSON file.

        The file is stored in 'Data/Playlists/' directory with the playlist name as the filename.
        """
        filename = f"Data/Playlists/{self.getName()}.json"
        with open(filename, 'w') as file:
            json.dump({
                "name": self.__name,
                "total_duration":self.__total_duration,
                "track":[track.toDict() for track in self.getTracks()]
                }, file, indent=2)

    @staticmethod
    def loadFromJson(playlistname: str):
        filename = f"Data/Playlists/{playlistname}.json"
        try:
            with open (filename, 'r') as file:
                data = json.load(file)
                playlist = Playlist(data["name"])
                playlist.__total_duration = data["total_duration"]
                for track_data in data["tracks"]:
                    track = Track.fromDict(track_data)
                    playlist.addTrack(track)
                return playlist
        except FileNotFoundError:
            print(f"File {filename}not found.")

        return None

    @staticmethod
    def displayPlaylists(playlists: list, page: int = 1, items_per_page: int = 10):
        total_pages = (len(playlists) + items_per_page - 1) // items_per_page
        if page < 1 or page > total_pages:
            return False

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        page_playlists = playlists[start_index:end_index]

        display = "List of Playlists:\n\n"
        current_index = start_index + 1
        for playlist in page_playlists:
            display += f"[{current_index}] {playlist}\n"
            current_index += 1

        display += f"\n<Page {page} of {total_pages}>\n"

        if page > 1:
            display += f"[11] Previous Page\n"
        if page < total_pages:
            display += f"[12] Next Page\n"

        return display

    @staticmethod      
    def getPlaylistName(directory = "Data/Playlists"):
        playlist_names = []
        try:
            files = os.listdir(directory)
            for file in files:
                if len(file) > 5 and file[-5:] == ".json":
                    playlist_name = file[:-5]
                    playlist_names += [playlist_name]
            return playlist_names
        except FileNotFoundError:
            print(f"Directory {directory} not found.")
        return []

    def __str__(self) -> str:
        s = f"\nPlaylist Name: {self.getName()}\nTotal Duration: {self.getTotalDuration()}\nTracks:\n"
        for track in self.__tracks:
            s += "\t" + track.__str__(True) + "\n"
        return s
