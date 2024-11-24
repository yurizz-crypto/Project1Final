import json
from TrackClass import Track

class Playlist:
    def __init__(self, playlist_name: str):
        self.__playlist_name = playlist_name
        self.__tracks = []
        self.__total_duration = 0
    
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