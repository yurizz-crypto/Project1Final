import json
from TrackClass import Track

class Playlist:
    def __init__(self, playlist_name: str):
        self.__playlist_name = playlist_name
        self.__tracks = []
        self.__total_duration = "00:00"
    
    def getPlaylistName(self):
        return self.__playlist_name
    
    def getTotalDuration(self):
        return self.__total_duration
    
    def getTracks(self):
        return self.__tracks

    class TrackLink:
        def __init__(self):
            self.__head = None
            self.__size 0

        def add(self, track):
            if self.__check_track(track.getTitle(), track.getArtist(), track.getAlbom()):

            if not self.__head:
                self.__head = track
            else:
                current = self.__head
                while current.next:
                    current = current.next
                current.next = track

            self.__size += 1
            return True
    
    def getPlaylistName(self):
        return self.__playlist_name
    
    def getTotalDuration(self):
        minutes = self.__total_duration // 60
        seconds = self.__total_duration % 60
        return f"{minutes} min {seconds} sec"
    
    def addTrack(self):
        pass

    def removeTrack(self):
        pass

    def updateTotalDuration(self):
        pass

    def __str__(self) -> str:
        pass
