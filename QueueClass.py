import json
from TrackClass import Track

class Node:
    def __init__(self,track = None):
        self.track = track
        self.next = None
        self.prev = None

class PreviousTrackStack:
    def __init__(self, filename="Data/previous_tracks.json"):
        self.stack = []
        self.filename = filename

    def push(self, track: Track):
        """Push a track onto the stack."""
        if track not in self.stack:
            self.stack += [track]

    def pop(self):
        """Pop a track from the stack."""
        if not self.stack:
            return None
        
        track = self.stack[-1]
        self.stack = self.stack[:-1]

        return track

    def peek(self):
        """Peek at the top of the stack without removing it."""
        return self.stack[-1] if self.stack else None

class MusicQueue:
    def __init__(self):
        self.__head = None  # The first track in the queue (linked list)
        self.tail = None  # The last track in the queue (linked list)
        self.__currentTrackNode = None  # Pointer to the currently playing track
        self.__shuffle = False
        self.__repeat = True
        self.__playing = False  # Whether the track is currently playing
        self.__totalDuration = 0  # Total duration of all tracks in the queue
        self.previousTracks = PreviousTrackStack()
        
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
        """Enable or disable shuffle and update the queue accordingly."""
        if self.__shuffle == newShuffle:
            return  # No change if shuffle state is the same

        self.__shuffle = newShuffle

        if self.__shuffle:
            # Shuffle the queue
            self.shuffleQueue()
        else:
            # Restore the original order
            self.__head = None
            self.__tail = None
            self.__totalDuration = 0

            for track in self.__originalOrder:
                self.addTrackWithoutDuration(track)  # Rebuild the queue
                self.__totalDuration += track.getDurationInSeconds()

            print("Queue restored to the original order.")
    def setRepeat(self, newRepeat):
        self.__repeat = newRepeat
    def setPlay(self, newPlay):
        self.__playing = newPlay

    def clearQueue(self):
        """Clear the current queue and reset the state."""
        self.__head = None
        self.__tail = None
        self.__currentTrackNode = None
        self.previousTracks = PreviousTrackStack()
        self.__playing = False
        self.__totalDuration = 0
        self.saveQueueToJson()
        print("Queue has been cleared.")


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
    
    def _iterateQueue(self):
        """Helper to iterate over the queue nodes."""
        current = self.__head
        while current:
            yield current
            current = current.next
    # Add a track to the queue
    def addTrack(self, track: Track):
        """Add a track to the queue."""
        new_node = Node(track)
        if not self.__head:
            self.__head = new_node
            self.__tail = new_node
        else:
            self.__tail.next = new_node
            new_node.prev = self.__tail
            self.__tail = new_node
        self.__totalDuration += track.getDurationInSeconds()
        self.saveQueueToJson()

        
    def addPlaylist(self, playlist):
        for track in playlist:
            self.addTrack(track)

    def play(self):
        """Start playing the queue."""
        if not self.__head:
            print("No tracks in the queue.")
            return
        if not self.__currentTrackNode:
            self.__currentTrackNode = self.__head
        self.__playing = True
        print(f"Now Playing: {self.__currentTrackNode.track.getTitle()}")

    # Pause Currently Playing track
    def pause(self):
        if self.__playing:
            self.__playing = False
            print(f"Paused: {self.__currentTrackNode.track}")

    
    # Get the tail (last track)
    def Tail(self, head:Node):
        """Find the tail node of the linked list."""
        if not head:
            return None
        current = head
        while current.next:
            current = current.next
        return current

    # Shuffle the queue (optional)
    def shuffleQueue(self):
        """Shuffle the queue without losing the current track and correctly update the total duration."""
        if not self.__head or not self.__head.next:
            print("Queue is too small to shuffle.")
            return

        # Collect all nodes into a list
        nodes = []
        current = self.__head
        while current:
            nodes.append(current)
            current = current.next

        # Shuffle the list of nodes
        n = len(nodes)
        for i in range(n - 1, 0, -1):
            j = self.randomIndex(0, i)
            nodes[i], nodes[j] = nodes[j], nodes[i]

        self.__head = nodes[0]
        self.__tail = nodes[-1]

        for i in range(len(nodes)):
            nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
            nodes[i].prev = nodes[i - 1] if i - 1 >= 0 else None

        self.__totalDuration = 0
        current = self.__head
        while current:
            self.__totalDuration += current.track.getDurationInSeconds()
            current = current.next

        print("Queue shuffled successfully!")


    def randomIndex(self, start, end):
        """Generate a random index between start and end (inclusive)."""
        if not hasattr(self, "randomSeed"):
            self.randomSeed = 123456789

        modulus = 233280
        multiplier = 9301
        increment = 49297

        self.randomSeed = (self.randomSeed * multiplier + increment) % modulus

        return start + (self.randomSeed % (end - start + 1))



    def addTrackWithoutDuration(self, track: Track):
        """Add a track to the queue without updating the total duration."""
        if not track:
            print("Invalid track. Skipping addition.")
            return

        new_node = Node(track)
        if not self.__head:
            self.__head = new_node
            self.__tail = new_node
        else:
            self.__tail.next = new_node
            new_node.prev = self.__tail
            self.__tail = new_node

        # Update __originalOrder manually
        temp = [None] * (len(self.__originalOrder) + 1)
        for i in range(len(self.__originalOrder)):
            temp[i] = self.__originalOrder[i]
        temp[len(self.__originalOrder)] = track
        self.__originalOrder = temp
    # Play the next track
    def nextTrack(self):
        """Move to the next track in the queue and remove the finished track if repeat is OFF."""
        if not self.__currentTrackNode:
            print("No tracks in the queue.")
            return

        if not self.__repeat:
            # Save the current track to the previous stack
            self.previousTracks.push(self.__currentTrackNode.track)

            # Handle track removal
            current_track = self.__currentTrackNode
            next_node = current_track.next
            prev_node = current_track.prev

            # Subtract the duration of the current track from the total duration
            self.__totalDuration -= current_track.track.getDurationInSeconds()

            # Remove the current track from the queue
            if prev_node:
                prev_node.next = next_node
            if next_node:
                next_node.prev = prev_node

            if current_track == self.__head:
                self.__head = next_node
            if current_track == self.__tail:
                self.__tail = prev_node 

            # Move to the next track or stop playback if no tracks left
            self.__currentTrackNode = next_node
            if self.__currentTrackNode:
                print(f"Next track: {self.__currentTrackNode.track.getTitle()}")
            else:
                self.__playing = False
                print("No more tracks left in the queue.")
        else:
            # If repeat is ON, just move to the next track (no removal or pushing to the stack)
            if self.__currentTrackNode.next:
                self.__currentTrackNode = self.__currentTrackNode.next
                print(f"Repeat is enabled. Now playing: {self.__currentTrackNode.track.getTitle()}")
            else:
                self.__currentTrackNode = self.__head
                print(f"Repeat is enabled. Returning to the first track: {self.__currentTrackNode.track.getTitle()}")

        # Save the updated queue state
        self.saveQueueToJson()
        
    def previousTrack(self):
        """Move to the previous track in the queue, considering repeat behavior."""
        if self.__repeat:
            # Repeat is ON: Move to the previous track without modifying the queue or stack
            if self.__currentTrackNode.prev:
                self.__currentTrackNode = self.__currentTrackNode.prev
                print(f"Repeat is enabled. Now playing: {self.__currentTrackNode.track.getTitle()}")
            else:
                # If we're at the first track, move to the last track
                self.__currentTrackNode = self.__tail
                print(f"Repeat is enabled. Returning to the last track: {self.__currentTrackNode.track.getTitle()}")
        else:
            # If repeat is OFF, we can use the stack and modify the queue
            if self.previousTracks.peek():
                previous_track = self.previousTracks.pop()

                # Insert track back into the queue
                new_node = Node(previous_track)

                if self.__currentTrackNode:
                    new_node.next = self.__currentTrackNode
                    new_node.prev = self.__currentTrackNode.prev
                    if self.__currentTrackNode.prev:
                        self.__currentTrackNode.prev.next = new_node
                    self.__currentTrackNode.prev = new_node

                    if self.__currentTrackNode == self.__head:
                        self.__head = new_node
                else:
                    self.__head = new_node
                    self.__tail = new_node

                self.__currentTrackNode = new_node
                print(f"Now playing: {self.__currentTrackNode.track.getTitle()}")

                # Add the duration of the previous track to the total duration
                self.__totalDuration += previous_track.getDurationInSeconds()

            elif self.__repeat and self.__tail:
                self.__currentTrackNode = self.__tail
                print(f"Repeat is enabled. Returning to the last track: {self.__currentTrackNode.track.getTitle()}")

            else:
                print("No previous tracks available.")

        # Save the queue state
        self.previousTracks.saveToJson()
        self.saveQueueToJson()
            
    def getQueueInfo(self):
        totalDurationStr = self.formatDuration(self.__totalDuration)
        print(f"\nTotal Duration: {totalDurationStr}")
        print(f"Shuffled: {'Yes' if self.__shuffle else 'No'}")
        print(f"Repeat: {'Yes' if self.__repeat else 'No'}\n")
    

    def displayQueue(self, page=1, pageSize=10):
        """Display the queue with a formatted layout."""
        current = self.__head
        startIndex = (page - 1) * pageSize
        count = 0

        self.getQueueInfo()
        print("Tracks:")

        if self.__currentTrackNode:
            playing_status = "(Playing)" if self.getPlay() else "(Paused)"
            print(f"Currently Playing {playing_status}:\n")
            print(f"\n{self.__currentTrackNode.track.__str__(True)}\n")
            print("Next:\n")
        else:
            print("\nNo track is currently playing.\n")
            print("Next:\n")

        while current:
            if startIndex > 0:
                startIndex -= 1
                current = current.next
                continue

            if count < pageSize:
                track = current.track
                print(f"({count + 1}) {track.__str__(True)}")
                count += 1
            else:
                break
            current = current.next

        total_pages = self.getTotalPages(pageSize)
        print(f"<Page {page} of {total_pages}>")
        
    def getTotalPages(self, pageSize=10):
        length = 0
        current = self.__head
        while current:
            length += 1
            current = current.next
        return (length + pageSize - 1) // pageSize
    
    def saveQueueToJson(self):
        """Save the queue state to a JSON file."""
        queue_list = [node.track.toDict() for node in self._iterateQueue()]

        state = {
            "queue": queue_list,
            "currentTrackIndex": self.getIndexOfNode(self.__currentTrackNode),
            "shuffle": self.__shuffle,
            "repeat": self.__repeat,
        }

        try:
            with open("Data/queue.json", "w") as file:
                json.dump(state, file, indent=4)
        except Exception as e:
            print(f"Error saving queue: {e}")
            
    def getIndexOfNode(self, node: Node):
        """Return the index of a given node in the queue."""
        current = self.__head
        index = 0
        while current:
            if current == node:
                return index
            current = current.next
            index += 1
        return -1
    
    def loadStateFromJSON(self):
        pass
    
    def queueInterface(self):
        self.loadStateFromJSON()
        if not isinstance(self.previousTracks, PreviousTrackStack):
            print("Reinitializing previousTracks as PreviousTrackStack.")
            self.previousTracks = PreviousTrackStack()
        self.previousTracks.loadFromJson()

        while True:
            self.displayQueue()
            print("\nOptions:")
            print("[1] Play")
            print("[2] Pause")
            print("[3] Next")
            print("[4] Previous")
            print("[5] Turn off Repeat" if self.getRepeat() else "[5] Turn on Repeat")
            print("[6] Turn off Shuffle" if self.getShuffled() else "[6] Turn on Shuffle")
            print("[7] Clear Queue")
            print("[0] Exit")
            choice = input("Enter your choice: ")

            if choice == "0":
                self.saveQueueToJson()
                self.previousTracks.saveToJson()
                print("Exiting queue interface.")
                break
            elif choice == "1":
                self.play()
            elif choice == "2":
                self.pause()
            elif choice == "3":
                self.nextTrack()
                if not self.getPlay():
                    self.setPlay(True)
            elif choice == "4":
                self.previousTrack()
            elif choice == "5":
                self.setRepeat(not self.getRepeat())
            elif choice == "6":
                self.setShuffled(not self.getShuffled())
            elif choice == "7":
                self.clearQueue()
            else:
                print("Invalid choice. Try again.")


MusicQueue().queueInterface()