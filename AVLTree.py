from TrackClass import Track

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

    # Getters
    def getRoot(self):
        return self.__root
    
    def getHeight(self, node: AVLNode):
        return node.getHeight() if node else 0
    
    def updateHeight(self, node: AVLNode):
        leftHeight = self.getHeight(node.getLeft())
        rightHeight = self.getHeight(node.getRight())
               

    def getBalanceFactor(self):
        pass

    def rotateRight(self):
        pass

    def rotateLeft(self):
        pass
    
    def autoRotate(self):
        pass

    def compareTracks(self):
        pass

    def insert(self):
        pass

    def addTrack(self):
        pass

    def delete():
        pass

    def removeTrack():
        pass

    def sort(self):
        pass

    def getDuplicates(self):
        pass

    def shuffle(self, node: AVLNode, result: list):
        pass

    def getSortedTracks(self):
        pass
    
    def getShuffledTracks(self):
        pass

    def searchTrack(self):
        pass

    # Methods for Storing and Loading using Json

    def __str__(self) -> str:
        pass