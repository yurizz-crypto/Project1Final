from TrackClass import Track
from PlaylistClass import Playlist

class AVLNode:
    def __init__(self, track: Track):
        self.__track = track
        self.__left = None
        self.__right = None
        self.__height = 1
    
    def getTrack(self):
        return self.__track

    def getLeft(self):
        return self.__left

    def getRight(self):
        return self.__right

    def setLeft(self, left):
        self.__left = left

    def setRight(self, right):
        self.__right = right

    def getHeight(self):
        return self.__height

    def setHeight(self, height):
        self.__height = height

class AVLTree:
    def __init__(self):
        self.__root = None
        
    def getRoot(self):
        return self.__root
    
    def getHeight(self, node: AVLNode):
        return node.getHeight() if node else 0
    
    def updateHeight(self, node: AVLNode):
        leftHeight = self.getHeight(node.getLeft())
        rightHeight = self.getHeight(node.getRight())
        
        if leftHeight > rightHeight:
            node.setHeight(leftHeight + 1)
        else:
            node.setHeight(rightHeight + 1)
                   
    def getBalanceFactor(self, node: AVLNode):
        if node:
            return self.get_height(node.getLeft()) - self.get_height(node.getRight())
        return 0

    def rotateRight(self, root: AVLNode):
        rootLeft = root.getLeft()
        rootLeftRight = rootLeft.getRight()
        
        rootLeft.setRight(rootLeft)
        root.setLeft(rootLeftRight)
        
        self.updateHeight(root)
        self.updateHeight(rootLeft)
        
        return rootLeft

    def rotateLeft(self, root: AVLNode):
        rootRight = root.getRight()
        rootRightLeft = rootRight.getLeft()
        
        rootRight.setLeft(root)
        root.setRight(rootRightLeft)
        
        self.updateHeight(root)
        self.updateHeight(rootRight)
    
    def autoRotate(self, node: AVLNode):
        balance = self.get_balance_factor(node)
        
        if balance > 1: 
            if self.getBalanceFactor(node.getLeft()) >= 0:
                return self.rotateRight(node)
        
            else:
                node.setLeft(self.rotateLeft(node.getLeft()))
                return self.rotateRight(node)
        
        if balance < -1:
            if self.get_balance_factor(node.getRight()) <= 0:
                return self.rotateLeft(node)
            
            else:
                node.setRight(self.rotateRight(node.getRight()))
                return self.rotateLeft(node)
            
        return node

    def compareTracks(self, track1: Track, track2: Track):
        if track1.getTitle() != track2.getTitle():
            return track1.getTitle() < track2.getTitle()
        
        if track1.getArtist() != track2.getArtist():
            return track1.getArtist() < track2.getArtist()
        
        if track1.getAlbum() != track2.getAlbum():
            return track1.getAlbum() < track2.getAlbum()
        
        return track1.getDuration() < track2.getDuration()

    def insert(self, node: AVLNode, track: Track):
        if not node:
            return AVLNode(track)

        if self.compareTracks(track, node.getTrack()):
            node.setLeft(self.insert(node.getLeft(), track))
        else:
            node.setRight(self.insert(node.getRight(), track))

        self.updateHeight(node)

        return self.autoRotate(node)

    def addTrack(self):
        check = self.searchTrack(track.getTitle(), track.getArtist())
        
        if check == None:
            self.__root = self.insert(self.__root, track)

        return False
    
    def delete(self, node: AVLNode, track: Track):
        if not node:
            return node

        if self.compareTracks(track, node.getTrack()):
            node.setLeft(self.delete(node.getLeft(), track))
        elif self.compareTracks(node.getTrack(), track):
            node.setRight(self.delete(node.getRight(), track))
        else:
            if not node.getLeft():
                return node.getRight()
            elif not node.getRight():
                return node.getLeft()

            min_node = self.getMinNode(node.getRight())
            node.getTrack().__dict__.update(min_node.getTrack().__dict__)
            node.setRight(self.delete(node.getRight(), min_node.getTrack()))

        self.updateHeight(node)

        return self.autoRotate(node)

    def removeTrack(self, track: Track):
        self.__root = self.delete(self.__root, track)
        
        playlists = Playlist.getPlaylists()
        for playlist_name in playlists:
            playlist = Playlist.loadFromJson(playlist_name)
            if playlist:
                removed_track = playlist.removeTrack(track.getTitle(), track.getArtist())
                if removed_track:
                    print(f"Removed '{track.getTitle()}' by {track.getArtist()} from playlist '{playlist_name}'.")

    def sort(self):
        pass

    def getDuplicates(self, node: AVLNode, title) -> list:
        duplicates = []
        if node:
            duplicates += self.getDuplicates(node.getLeft(), title)

            if node.getTrack().getTitle() == title:
                duplicates += [node.getTrack()]

            duplicates += self.getDuplicates(node.getRight(), title)
        
        return duplicates
    

    def shuffle(self, node: AVLNode, result: list):
        pass
    
    def traverse(self, node: AVLNode, result: list, order: str):
        if not node:
            return
        
        self.traverse(node.getLeft(), result, order)
        result += [node.getTrack()]
        self.traverse(node.getRight(), result, order)

        if order == "shuffle":
            n = len(result)
            for i in range(n - 1, 0, -1):
                seed = (i * 53 + 23) % 256
                j = (seed * 41 + 29) % i + 1
                result[i], result[j] = result[j], result[i]
        
    def getTotalDuration(self):
        def sum_durations(node: AVLNode):
            if not node:
                return 0
            left_duration = sum_durations(node.getLeft())
            right_duration = sum_durations(node.getRight())
            return node.getTrack().getDurationInSeconds() + left_duration + right_duration
        
        total_Seconds = sum_durations

    def getSortedTracks(self) -> list:
        result = []
        
    
    def getShuffledTracks(self) -> list:
        result = []

    def searchTrack(self, title: str, artist: str | None = None) -> Track:
        current = self._root
        while current:
            track = current.getTrack()
            if title == track.getTitle() and (artist is None or artist == track.getArtist()):
                return track
            if title < track.getTitle():
                current = current.getLeft()
            else:
                current = current.getRight()
        return None
        

    # Methods for Storing and Loading using Json

    def __str__(self) -> str:
        pass