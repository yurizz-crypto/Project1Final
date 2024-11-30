from TrackClass import Track
from PlaylistClass import Playlist
import json

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
        
        """
        Returns the height of a given node.
        
        Parameters:
            node (AVLNode): The node whose height is to be retrieved.
        
        Returns:
            int: Height of the node, or 0 if the node is None.
        """
        
        return node.getHeight() if node else 0
    
    def updateHeight(self, node: AVLNode):
        
        """
        Updates the height of a node based on its children's heights.
        
        Parameters:
            node (AVLNode): The node whose height needs updating.
        """
        
        leftHeight = self.getHeight(node.getLeft())
        rightReight = self.getHeight(node.getRight())
        
        if leftHeight >  rightReight:
            node.setHeight(leftHeight + 1)
        else:
            node.setHeight( rightReight + 1)
                   
    def getBalanceFactor(self, node: AVLNode):
        
        """
        Parameters:
            node (AVLNode): The node whose balance factor is calculated.
        
        Returns:
            int: The difference between left and right subtree heights.
        """
        
        if node:
            return self.getHeight(node.getLeft()) - self.getHeight(node.getRight())
        return 0

    def rotateRight(self, root: AVLNode):
        
        """
        Performs a right rotation on the given root node.
        
        Parameters:
            root (AVLNode): The root node to rotate.
        
        Returns:
            AVLNode: The new root after rotation.
        """
        
        rootLeft = root.getLeft()
        rootLeftRight = rootLeft.getRight()
        
        # Adjust pointers for rotation.
        rootLeft.setRight(rootLeft)
        root.setLeft(rootLeftRight)
        
        # Update heights after rotation.
        self.updateHeight(root)
        
        self.updateHeight(rootLeft)
        
        return rootLeft

    def rotateLeft(self, root: AVLNode):
        
        """
        Performs a left rotation on the given root node.
        
        Parameters:
            root (AVLNode): The root node to rotate.
        
        Returns:
            AVLNode: The new root after rotation.
        """
        
        rootRight = root.getRight()
        rootRightLeft = rootRight.getLeft()
        
        # Adjust pointers for rotation.
        rootRight.setLeft(root)
        root.setRight(rootRightLeft)
        
        # Update heights after rotation.
        self.updateHeight(root)
        self.updateHeight(rootRight)
    
    def autoRotate(self, node: AVLNode):
        
        """
        Automatically rebalances the tree at a given node.
        
        Parameters:
            node (AVLNode): The node to rebalance.
        
        Returns:
            AVLNode: The new root of the subtree after rebalancing.
        """

        balance = self.getBalanceFactor(node)
        
        # Perform rotations based on balance factor.
        if balance > 1: # Left-heavy
            if self.getBalanceFactor(node.getLeft()) >= 0: # Left-Left case
                return self.rotateRight(node)
        
            else: # Left-Right case
                node.setLeft(self.rotateLeft(node.getLeft()))
                return self.rotateRight(node)
        
        if balance < -1: # Right-heavy
            if self.getBalanceFactor(node.getRight()) <= 0: # Right-Right case
                return self.rotateLeft(node)
            
            else: # Right-Left case
                node.setRight(self.rotateRight(node.getRight()))
                return self.rotateLeft(node)
            
        return node 

    def compareTracks(self, track1: Track, track2: Track):
        
        """
        Compares two tracks for ordering in the AVL Tree.

        Parameters:
            track1 (Track): The first track to compare.
            track2 (Track): The second track to compare.

        Returns:
            bool: True if track1 is less than track2, False otherwise.
        """
        
        if track1.getTitle() != track2.getTitle():
            return track1.getTitle() < track2.getTitle()
        
        if track1.getArtist() != track2.getArtist():
            return track1.getArtist() < track2.getArtist()
        
        if track1.getAlbum() != track2.getAlbum():
            return track1.getAlbum() < track2.getAlbum()
        
        return track1.getDuration() < track2.getDuration()

    def insert(self, node: AVLNode, track: Track):
        """Inserts a track, updates node heights, 
        and balances the AVL tree."""
        if not node:
            return AVLNode(track)

        if self.compareTracks(track, node.getTrack()):
            node.setLeft(self.insert(node.getLeft(), track))
        else:
            node.setRight(self.insert(node.getRight(), track))

        self.updateHeight(node)

        return self.autoRotate(node)

    def addTrack(self, track: Track):
        
        """
        Adds a track to the AVL Tree if it doesn't already exist.
        
        Parameters:
            track (Track): The track to add.
        
        Returns:
            bool: True if the track was added, False otherwise.
        """
        
        check = self.searchTrack(track.getTitle(), track.getArtist())
        
        if check == None:
            self.__root = self.insert(self.__root, track)

        return False
    
    def delete(self, node: AVLNode, track: Track): 
        """Deletes a track from the AVL tree 
            by locating the node containing the track """
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
    
    def getMinNode(self, node: AVLNode):
        
        # Finds the node with the minimum value in the subtree.
        
        current = node
        while current.getLeft() is not None:
            current = current.getLeft()
        return current
    
    def removeTrack(self, track: Track):
        """Removes a track from the AVL tree and 
        updates all playlists by removing the track if it exists."""
        self.__root = self.delete(self.__root, track)
        
        playlists = Playlist.getPlaylists()
        for playlist_name in playlists:
            playlist = Playlist.loadFromJson(playlist_name)
            if playlist:
                removed_track = playlist.removeTrack(track.getTitle(), track.getArtist())
                if removed_track:
                    print(f"Removed '{track.getTitle()}' by {track.getArtist()} from playlist '{playlist_name}'.")

    def getDuplicates(self, node: AVLNode, title) -> list:
        """searches ang AVL tree for tracks with 
        the given title and returns a list of duplicates"""
        duplicates = []
        if node:
            duplicates += self.getDuplicates(node.getLeft(), title)

            if node.getTrack().getTitle() == title:
                duplicates += [node.getTrack()]

            duplicates += self.getDuplicates(node.getRight(), title)
        
        return duplicates
    
    def traverse(self, node: AVLNode, result: list, order: str):
        """Traverses the AVL tree in-order and appends tracks to 
        the result list."""
        if not node:
            return
        
        self.traverse(node.getLeft(), result, order)
        result += [node.getTrack()]
        self.traverse(node.getRight(), result, order)
        
    def getTotalDuration(self):
        
        """
        Calculates the total duration of all tracks in the tree.
        
        Returns:
            str: The total duration in "MM:SS" format.
        """
        
        def sumDurations(node: AVLNode):
            if not node:
                return 0
            leftDuration = sumDurations(node.getLeft())
            rightDuration = sumDurations(node.getRight())
            return node.getTrack().getDurationInSeconds() + leftDuration + rightDuration
        
        totalSeconds = sumDurations(self.getRoot())
        minutes = totalSeconds // 60
        seconds = totalSeconds % 60
        return f"{minutes:02}:{seconds:02}"

    def getSortedTracks(self) -> list:
        
        """
        Retrieves all tracks in sorted order.
        
        Returns:
            list: A list of tracks sorted by title, artist, album, and duration.
        """
        
        result = []
        self.traverse(self.__root, result, "inorder")
        return result      

    def searchTrack(self, title: str, artist: str | None = None) -> Track:
        
        """
        Searches for a specific track in the tree.
        
        Parameters:
            title (str): The title of the track to search for.
            artist (str | None): The artist of the track (optional).
        
        Returns:
            Track: The found track, or None if not found.
        """
        
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
    
    def saveToJson(self, filename="Data/tracks.json"):
        tracks = self.getSortedTracks()
        with open(filename, 'w') as file:
            json.dump([track.toDict() for track in tracks], file, indent=2)

    def loadFromJson(self, filename="Data/tracks.json"):
        """Loads tracks from a JSON file and inserts them into the AVL tree.
        handles missing file errors."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for track_data in data:
                    track = Track.fromDict(track_data)
                    self.__root = self.insert(self.__root, track)
        except FileNotFoundError:
            print(f"File {filename} not found.")

    def __str__(self) -> str:
        s = f"\n<---------All Tracks--------->\n\nTotal Duration: {self.getTotalDuration()}\n\n"
        num = 1
        for track in self.getSortedTracks():
            s += f"{num}. " + track.__str__(True) + "\n"
            num += 1
        return s