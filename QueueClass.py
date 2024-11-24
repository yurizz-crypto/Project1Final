import json
from TrackClass import Track
from PlaylistClass import Playlist

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

    
    # Add a track to the queue
    def addTrack(self):
        pass

    # Remove a track from the queue
    def removeTrack(self):
        pass
    
    # Get the tail (last track)
    def getTail(self):
        pass

    # Shuffle the queue (optional)
    def shuffleQueue(self):
        pass

    # Play the next track
    def playNextTrack(self):
        pass
