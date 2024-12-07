import json
from TrackClass import Track

class MusicQueue:
    def __init__(self) -> None:
        self.__queue = []
        self.__orig = []
        self.__current_index = 0
        self.__total_duration = 0
        self.__repeat = False
        self.__shuffle = False
        self.__playing = False

    def addTrack(self, newTrack: Track):

        """
        Adds a new track to the end of the music queue 

        Parameters:
            newTrack (Track): The track to be added to the music queue
        """
        self.__queue += [newTrack]
        self.__orig += [newTrack]

    def nextTrack(self):

        """
        it Advances the current track index for the next track in the queue
        If the repeat mode is enabled it will wraps around to the beginning of the queue 
        If at the end of the queue and repeat is not enabled it stops the playback
        
        """
        if self.__repeat:
            self.__current_index = (self.__current_index + 1) % len(self.__queue)
        else:
            if self.__current_index + 1 < len(self.__queue):
                self.__current_index += 1
            else:
                self.__playing = False

    def previousTrack(self):

        """
        this moves the current track index to the previous track in the queue 
        if the repeat mode is enabled it wraps around to the end of the queue 
        if at the start of the queue it does nothing
        """
        if self.__repeat:
            self.__current_index = (self.__current_index - 1) % len(self.__queue)
        else:
            if self.__current_index > 0:
                self.__current_index -= 1
            else:
                return
    def updateTotalDuration(self):

        """
        Updates the total duration of the tracks in the queue
        starting from the current track index to the end of the queue
        """
        if self.__queue:
            total = 0
            for track in self.__queue[self.__current_index:]:
                total += track.getDurationInSeconds()

            self.__total_duration = total

    def shuffleQueue(self):

        """
        Shuffles the order of the tracks in the queue
        excluding the currently playing track
        The original order of the queue is saved before shuffling
        The currently playing track is placed back
        in its original position after shuffling the remaining tracks

        """
        if self.__orig:
            # Save the original order manually
            self.__orig = [track for track in self.__queue]

        # Exclude the currently playing track
        currentlyPlayingTrack = self.__queue[self.__current_index]
        remainingTracks = self.__queue[:self.__current_index] + self.__queue[self.__current_index + 1:]

        # Fisher-Yates Shuffle for the remaining tracks
        n = len(remainingTracks)
        seed = 1337
        for i in range(n - 1, 0, -1):
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            random_index = seed % (i + 1)
            # Swap elements at i and random_index
            remainingTracks[i], remainingTracks[random_index] = remainingTracks[random_index], remainingTracks[i]

        # Reconstruct the queue: Place the currently playing track back in its original position
        self.__queue = remainingTracks[:self.__current_index] + [currentlyPlayingTrack] + remainingTracks[self.__current_index:]


    def clearQueue(self):

        """
        Clears the music queue and resets all related attributes to their initial state
        
        """
        self.__queue = []
        self.__orig = []
        self.__current_index = 0
        self.__total_duration = 0
        self.__repeat = False
        self.__shuffle = False
        self.__playing = False
        self.saveState()

    def formatDuration(self, total_seconds):
        """Format duration from total seconds to 'X hr Y min Z sec' without divmod or ord
        
        Returns:
            str: A string representing the duration in the format 'X hr Y min Z sec'.

        Parameters:
            total_seconds (int): The total duration in seconds to be formatted.
        
        """
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
        
    def displayQueue(self, page=1, pageSize=10):
        self.updateTotalDuration()
        print(f"\nTotal Duration: {self.formatDuration(self.total_duration)}")
        print(f"Shuffle: {'Yes' if self.__shuffle else 'No'}")
        print(f"Repeat: {'Yes' if self.__repeat else 'No'}")
        print("\nTracks:")

        if self.queue:
            print(f"Currently Playing {'(Playing)' if self.__playing else '(Paused)'}:")
            print(f"\t{self.queue[self.__current_index].__str__(True)}\n")
            print("Next:")
        else:
            print("\nNo track is currently playing.\n")
            print("Next:")

        if self.__current_index + 1 < len(self.queue):
            startIndex = self.__current_index + 1 + (page - 1) * pageSize
            endIndex = startIndex + pageSize

            if endIndex > len(self.__queue):
                endIndex = len(self.__queue)

            for i in range(startIndex, endIndex):
                print(f"({i - self.__current_index}) {self.__queue[i].__str__(True)}")
        else:
            if not self.__repeat:
                print("No more tracks in queue.")
            else:
                print(f"(1) {self.__queue[0].__str__(True)}")

        remainingTracks = len(self.__queue) - (self.__current_index + 1)
        total_pages = (remainingTracks + pageSize - 1) // pageSize
        print(f"<Page {page} of {max(total_pages, 1)}>")


    