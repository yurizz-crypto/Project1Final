import json
from TrackClass import Track

class MusicQueue:
    def __init__(self) -> None:
        self.queue = []
        self.orig = []
        self.current_index = 0
        self.total_duration = 0
        self.repeat = False
        self.shuffle = False
        self.playing = False

    def addTrack(self, newTrack: Track):

        """
        Adds a new track to the end of the music queue 

        Parameters:
            newTrack (Track): The track to be added to the music queue
        """
        self.queue += [newTrack]
        self.orig += [newTrack]

    def nextTrack(self):

        """
        it Advances the current track index for the next track in the queue
        If the repeat mode is enabled it will wraps around to the beginning of the queue 
        If at the end of the queue and repeat is not enabled it stops the playback
        
        """
        if self.repeat:
            self.current_index = (self.current_index + 1) % len(self.queue)
        else:
            if self.current_index + 1 < len(self.queue):
                self.current_index += 1
            else:
                self.playing = False

    def previousTrack(self):

        """
        this moves the current track index to the previous track in the queue 
        if the repeat mode is enabled it wraps around to the end of the queue 
        if at the start of the queue it does nothing
        """
        if self.repeat:
            self.current_index = (self.current_index - 1) % len(self.queue)
        else:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                return
    def updateTotalDuration(self):

        """
        Updates the total duration of the tracks in the queue
        starting from the current track index to the end of the queue
        """
        if self.queue:
            total = 0
            for track in self.queue[self.current_index:]:
                total += track.getDurationInSeconds()

            self.total_duration = total

    def shuffleQueue(self):

        """
        Shuffles the order of the tracks in the queue
        excluding the currently playing track
        The original order of the queue is saved before shuffling
        The currently playing track is placed back
        in its original position after shuffling the remaining tracks

        """
        if self.orig:
            # Save the original order manually
            self.orig = [track for track in self.queue]

        # Exclude the currently playing track
        currentlyPlayingTrack = self.queue[self.current_index]
        remainingTracks = self.queue[:self.current_index] + self.queue[self.current_index + 1:]

        # Fisher-Yates Shuffle for the remaining tracks
        n = len(remainingTracks)
        seed = 1337
        for i in range(n - 1, 0, -1):
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            random_index = seed % (i + 1)
            # Swap elements at i and random_index
            remainingTracks[i], remainingTracks[random_index] = remainingTracks[random_index], remainingTracks[i]

        # Reconstruct the queue: Place the currently playing track back in its original position
        self.queue = remainingTracks[:self.current_index] + [currentlyPlayingTrack] + remainingTracks[self.current_index:]