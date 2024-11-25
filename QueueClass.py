import json
from TrackClass import Track
from PlaylistClass import Playlist
import AVLTree

class Node:
    def __init__(self,track = None):
        self.track = track
        self.next = None
        self.prev = None

class MusicQueue:
    def __init__(self):
        self.__head = None  # The first track in the queue (linked list)
        self.tail = None  # The last track in the queue (linked list)
        self.__currentTrackNode = None  # Pointer to the currently playing track
        self.__shuffle = False
        self.__repeat = True
        self.__playing = False  # Whether the track is currently playing
        self.__totalDuration = 0  # Total duration of all tracks in the queue
        self.avlTree = AVLTree.AVLTree()

    # Accessor methods
    def getQueue(self):
        return self.__head
    def getCurrentTrackNode(self):
        return self.__currentTrackNode
    def getShuffled(self):
       return self.__shuffle
    def getRepeat(self):
        return self.__repeat
    def getPlay(self):
        return self.__playing
    def getTotalDuration(self):
        return self.__totalDuration

    
    # Mutator methods
    def setQueue(self, newQueue):
        self.head = newQueue
        self.tail = self.Tail(newQueue)
    def setCurrentTrackNode(self, newTrackNode):
        self.__currentTrackNode = newTrackNode
    def setShuffled(self, newShuffle):
        self.__shuffle = newShuffle
        if self.__shuffle:
            self.shuffleQueue()
    def setRepeat(self, newRepeat):
        self.__repeat = newRepeat
    def setPlay(self, newPlay):
        self.__playing = newPlay


    # load to json
    def loadToJS(self):
        with open("playlist.json", "r") as file:
            return json.load(file)

    def convertToSeconds(self, timeStr):
        """Convert a time string (MM:SS) to total seconds without any built-in functions."""
        colon_index = 0
        for i in range(len(timeStr)):
            if timeStr[i] == ":":
                colon_index = i
                break

        minutes_str = timeStr[:colon_index]
        seconds_str = timeStr[colon_index + 1:]

        def toInt(num_str):
            digits = "0123456789"
            value = 0
            for char in num_str:
                for i in range(len(digits)):
                    if char == digits[i]:
                        value = value * 10 + i
                        break
            return value

        minutes = toInt(minutes_str)
        seconds = toInt(seconds_str)

        return minutes * 60 + seconds

    def formatDuration(self, total_seconds):
        """Format duration from total seconds to 'X hr Y min Z sec' without divmod or ord."""
        minutes = 0
        while total_seconds >= 60:
            total_seconds -= 60
            minutes += 1

        seconds = total_seconds
        hours = 0
        while minutes >= 60:
            minutes -= 60
            hours += 1

        if hours > 0:
            return f"{hours} hr {minutes} min {seconds} sec"
        else:
            return f"{minutes} min {seconds} sec"
        
    # Add a track to the queue
    def addTrack(self, track):
        """Add a track to the queue."""
        new_node = Node(track)
        if self.__head is None:
            self.__head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            
        self.__totalDuration += self.convertToSeconds(track.getDuration())

        
    def addPlaylist(self, playlist):
        for track in playlist:
            self.addTrack(track)

    # Remove a track from the queue
    def play(self):
        if not self.__head:
            print("No tracks in the queue.")
            return
        
        if not self.__currentTrackNode:
            self.__currentTrackNode = self.__head
        
        self.__playing = True
        print(f"Now Playing: {self.__currentTrackNode.track}")

    
    # Get the tail (last track)
    def getTail(self):
        pass

    # Shuffle the queue (optional)
    def shuffleQueue(self):
        pass

    # Play the next track
    def playNextTrack(self):
        pass
