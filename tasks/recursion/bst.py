from typing import Any, Optional


class TreeNode:
    def __init__(self, data) -> None:
        self.data = data
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None
    
    def search(self, target: Any) -> Optional['TreeNode']:
        if self.data == target:
            return self
        elif self.data < target:
            if self.right:
                return self.right.search(target)
            return None
        else:
            if self.left:
                return self.left.search(target)
            return None
    
    def insert(self, data: Any):
        if not self.search(data):
            if data < self.data:
                if self.left:
                    self.left.insert(data)
                else:
                    self.left = TreeNode(data)
            else:
                if self.right:
                    self.right.insert(data)
                else:
                    self.right = TreeNode(data)
    
    def printTree(self):
        if self.right:
            self.right.printTree()
        print(self.data)
        if self.left:
            self.left.printTree()
    
    def printSideways(self, indent=0):
        if self.right:
            self.right.printSideways(indent+1)
        print(f"{"    "*indent}{self.data}")
        if self.left:
            self.left.printSideways(indent+1)
    

root = TreeNode(13)
node7 = TreeNode(7)
node15 = TreeNode(15)
node3 = TreeNode(3)
node8 = TreeNode(8)
node14 = TreeNode(14)
node19 = TreeNode(19)
node18 = TreeNode(18)

root.left = node7
root.right = node15

node7.left = node3
node7.right = node8

node15.left = node14
node15.right = node19

node19.left = node18

print(root.search(14).data)
root.printTree()
print("=====")
root.printSideways()