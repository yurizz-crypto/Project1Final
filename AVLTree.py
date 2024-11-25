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