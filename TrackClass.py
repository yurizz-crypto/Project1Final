class Track:
    def __init__(self, title: str, main_artist: str, album: str, duration: str, additional_artists: list | None = None):
        """
        Initializes a Track object with the provided attributes.
        """
        self.__title = title
        self.__artist = main_artist
        self.__album = album
        self.__duration = duration
        self.__additional_artists = additional_artists or []

    # Getter Methods
    def getTitle(self): return self.__title
    def getArtist(self): return self.__artist
    def getAlbum(self): return self.__album
    def getDuration(self): return self.__duration
    def getAdditionalArtists(self): return self.__additional_artists

    def getDurationInSeconds(self) -> int:
        """
        Converts the object's duration "MM:SS" format to total seconds, by spliting the __duration
        string by locating the colon (:) and extracts the minutes and seconds, converts them to integers,
        and calculates the total duration in seconds.
        
        Returns:
            int: The total duration in seconds.
        """
        colon_index = -1
        index = 0

        for char in self.__duration:
            if char == ':':
                colon_index = index
                break
            index += 1

        minutes = int(self.__duration[:colon_index])
        seconds = int(self.__duration[colon_index + 1:])

        return minutes * 60 + seconds

    def toDict(self) -> dict:
        """
        Converts the object into a dictionary representation for storing purposes(JSON).

        Returns:
            dic: Containing the following keys and their corresponding values.
        """
        return {
            "title": self.__title,
            "artist": self.__artist,
            "additional_artists": self.__additional_artists,
            "album": self.__album,
            "duration": self.__duration
        }

    @staticmethod
    def fromDict(data: dict):
        """
        Create a Track object from a dictionary representation especially from a JSON file.
        
        Parameters:
            data (dict): A dictionary conataining keys corresponding to the Track attributes.

        Returns:
            Track (object): Initialized with the data from the dictionary.
        """
        return Track(
            data["title"],
            data["artist"],
            data["album"],
            data["duration"],
            data.get("additional_artists", [])
        )

    def __str__(self, compact: bool = False) -> str:
        """
        String representation of the object Track.
        
        Parameters:
            compact (boolean): To check on how the Track should be display, for 1 line only
            or in detail.
        
        Returns:
            Compact (True): A concise string in the format "Title - Artist (Duration).
            Detailed (Compact: False): Returns a detailed string of a Track.
        """
        additional_artists = "None"
        if self.__additional_artists:
            additional_artists = ""
            index = 0
            for artist in self.__additional_artists:
                if index > 0:
                    additional_artists += ","
                additional_artists += artist
                index += 1

        if compact:
            return f"{self.getTitle()} - {self.getArtist()} ({self.getDuration()})"
        else:
            return (f"\nTitle: {self.getTitle()}\nArtist: {self.getArtist()}\nAlbum: {self.getAlbum()}\n"
                    f"Duration: {self.getDuration()}\nAdditional Artists: {additional_artists}\n")