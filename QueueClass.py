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

    def play(self):
        if not self.__head:
            print("No tracks in the queue.")
            return
        
        if not self.__currentTrackNode:
            self.__currentTrackNode = self.__head
        
        self.__playing = True
        print(f"Now Playing: {self.__currentTrackNode.track}")

    # Pause Currently Playing track
    def pause(self):
        if self.__playing:
            self.__playing = False
            print(f"Paused: {self.__currentTrackNode.track}")

    
    # Get the tail (last track)
    def Tail(self, head):
        """Find the tail node of the linked list."""
        if not head:
            return None
        current = head
        while current.next:
            current = current.next
        return current

    # Shuffle the queue (optional)
    def shuffleQueue(self):
        if self.__head is None:
            return  # No tracks to shuffle

        # Convert linked list to array
        tracks = []
        current = self.__head
        while current is not None:
            tracks.append(current.track)
            current = current.next

        # Shuffle the array using a simple algorithm (Fisher-Yates)
        n = len(tracks)
        for i in range(n - 1, 0, -1):
            j = self.getRandomIndex(i + 1)  # Get a random index from 0 to i
            tracks[i], tracks[j] = tracks[j], tracks[i]  # Swap

        # Rebuild the linked list from the shuffled array
        self.__head = None
        self.tail = None
        for track in tracks:
            self.addTrack(track)



    def getRandomIndex(self, max_value):
        """ Get a random index from 0 to max_value also ensuring their are new sets of shuffled queues every now and then """
        # Simple linear congruential generator (LCG) for demonstration
        seed = 123456789  # Example seed
        a = 1664525
        c = 1013904223
        m = 2**32

        # Generate a pseudo-random number
        seed = (a * seed + c) % m
        return seed % max_value
 

    # Play the next track
    def nextTrack(self):
        if not self.__currentTrackNode:
            print("No tracks in the queue.")
            return

        # current_track = self.__currentTrackNode.track

        if self.__repeat:
            self.__currentTrackNode = self.__currentTrackNode.next or self.__head
            print(f"Repeat is enabled. Playing next track: {self.__currentTrackNode.track}")
            return

        next_node = self.__currentTrackNode.next
        if self.__currentTrackNode == self.__head:
            self.__head = next_node
            if self.__head:
                self.__head.prev = None
        else: 
            if self.__currentTrackNode.prev:
                self.__currentTrackNode.prev.next = next_node
            if next_node:
                next_node.prev = self.__currentTrackNode.prev

        self.__currentTrackNode = next_node

        if self.__currentTrackNode:
            print(f"Next track: {self.__currentTrackNode.track}")
        else:
            print("No more tracks left.")
            self.__playing = False

    def previousTrack(self):
        if not self.__currentTrackNode:
            print("No tracks in the queue.")
            return

        # current_track = self.__currentTrackNode.track

        if self.__repeat:
            self.__currentTrackNode = self.__currentTrackNode.prev or self.tail
            print(f"Repeat is enabled. Playing previous track: {self.__currentTrackNode.track}")
            return

        if self.__currentTrackNode.prev:
            self.__currentTrackNode = self.__currentTrackNode.prev
            print(f"Previous track: {self.__currentTrackNode.track}")
        else:
            print("No previous tracks. Staying on the current track.")
    
    def addTrackToQueue(self, track):
        """Helper method to add a track to the queue."""
        new_node = Node(track)
        if self.__head is None:
            self.__head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
    

