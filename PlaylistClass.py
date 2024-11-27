import json
from TrackClass import Track
import os

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
    
    def countSameTitle(self, track: Track):
        count = 0
        for i in self.__tracks:
            if i.getTitle() == track.getTitle():
                count += 1
            return count > 1
    
    def addTrack(self, track):
        if track not in self.__tracks:
            self.__tracks += [track]
            self.update_total_duration()
            self.save_to_json()
            return track
        return False
    
    def removeTrack(self, title: str, artist: str):
        def divideAndConquer(tracks):
            if not tracks:
                return [], None
            
            if len(tracks) == 1:
                track = tracks[0]
                if track.getTitle() == title and track.getArtist() == artist:
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
    
    def deletePlaylist(self):
        filename = f"Fata/Playlists/{self.getName()}.json"
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return True
        except Exception as e:
            print(f"An error occurred while deleting the playlists: {e}")
        return False
    
    def updateTotalDuration(self):
        total_sec = 0
        track: Track
        for track in self.getTracks():
            minutes = int(track.getDuration()[:2])
            seconds = int(track.getDuration()[3:])
            total_sec += (minutes * 60) + seconds
        self.__total_duration = f"{total_sec // 60:02}:{total_sec % 60:02}"
            
class TrackLink:
        def __init__(self):
            self.__head = None
            self.__size = 0

        def add(self, track):
            if self.__check_track(track.getTitle(), track.getArtist(), track.getAlbum()):

                if not self.__head:
                    self.__head = track
                else:
                    current = self.__head
                    while current.next:
                        current = current.next
                    current.next = track

            self.__size += 1
            return True

        def __check_track(self, title, artist, album):
            current = self.__head
            while current:
                if current.getTitle()== title and current.getArtist() == artist and current.getAlbum() == album:
                    return False
                current = current.next
            return False

        def  remove(self, title):
            if not self.__head:
                return False

            if  self.__head.getTitle() == title:
                self.__head = self.__head.next
                self.__size -= 1
                return True

        current = self.__head
        while current.next:
            if current.next.getTitle() == title:
                current.next = current.next.next
                self.__size -= 1
                return True
            current = current.next
        return False

        def __str__(self):
            result = " "
            current = self.__head
            while current:
                result += str(current) + "\n"
                current = current.next
            return result.strip()

        def get_head(self):
            return self.__head
            
        
        
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
