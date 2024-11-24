class Track:
    def __init__(self, title: str, main_artist: str, album: str, duration: str, additional_artists: list | None = None):
        self.__title = self.validateInput(title, "Title")
        self.__artist = self.validateInput(main_artist, "Artist")
        self.__album = self.validateInput(album, "Album")
        self.__duration = duration
        self.__additional_artists = additional_artists or []

    def getTitle(self): return self.__title
    def getArtist(self): return self.__artist
    def getAlbum(self): return self.__album
    def getDuration(self): return self.__duration
    def getAdditionalArtists(self): return self.__additional_artists

    def validateInput(self, value: str, field_name: str) -> str:
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        return value
    
    def toDict(self):
        return {
            "title": self.__title,
            "main_artist": self.__artist,
            "additional_artists": self.__additional_artists,
            "album": self.__album,
            "duration": self.__duration
        }