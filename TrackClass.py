class Track:
    def __init__(self, title: str, main_artist: str, album: str, duration: str, additional_artists: list | None = None):
        self.__title = title
        self.__artist = main_artist
        self.__album = album
        self.__duration = duration
        self.__additional_artists = additional_artists or []

    def getTitle(self): return self.__title
    def getArtist(self): return self.__artist
    def getAlbum(self): return self.__album
    def getDuration(self): return self.__duration
    def getAdditionalArtists(self): return self.__additional_artists

    def getDurationInSeconds(self) -> int:
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
        return {
            "title": self.__title,
            "artist": self.__artist,
            "additional_artists": self.__additional_artists,
            "album": self.__album,
            "duration": self.__duration
        }

    @staticmethod
    def fromDict(data: dict):
        return Track(
            data["title"],
            data["artist"],
            data["album"],
            data["duration"],
            data.get("additional_artists", [])
        )

    def __str__(self, compact: bool = False) -> str:
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