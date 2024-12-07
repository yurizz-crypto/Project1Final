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
    
    # Divide and Conquer approach to remove track in the playlist by title
    def removeTrack(self, title: str):
        def divideAndConquer(tracks):
            if not tracks:
                return [], None
            
            if len(tracks) == 1:
                track = tracks[0]
                if track.getTitle() == title:
                    return [], track
                else:
                    return [track], None
            
            mid = len(tracks) // 2
            left, removed_left = divideAndConquer(tracks[:mid])
            right, removed_right = divideAndConquer(tracks[mid:])

            removed_track = removed_left or  removed_right
            return left + right, removed_track
        
        new_tracks, removed_track = divideAndConquer(self.__tracks)

        if removed_track:
            self.__tracks = new_tracks
            self.updateTotalDuration()
            self.saveToJson()
        return removed_track
    
    # Deleting playlist JSON file from the disk
    def deletePlaylist(self):
        filename = f"Data/Playlists/{self.getName()}.json"
        if os.path.exists(filename):
            os.remove(filename)
            return True
    
    # Total Duration of playlist
    def updateTotalDuration(self):
        total_sec = 0
        track: Track
        for track in self.getTracks():
            total_sec += track.getDurationInSeconds()
        self.__total_duration = f"{total_sec // 60:02}:{total_sec % 60:02}"
 
    def saveToJson(self):
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
