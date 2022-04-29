import colorama
from colorama import Fore
colorama.init(autoreset=True)


class Node:
    def __init__(self, key, parent):
        self.key = key
        self.color = "red"
        self.parent = parent
        self.left_child = None
        self.right_child = None
        self.size = 1


# to display the tree in ascending order
def inorder_traversal(node):
    if node is not None:
        inorder_traversal(node.left_child)
        print(node.key, "\t", "<===\t", node.color, "\tsize =", node.size)
        inorder_traversal(node.right_child)


# left rotate needed in fixing after insertion
def left_rotate(root, x):
    y = x.right_child

    # sizes handling
    temp = y.size
    y.size = x.size
    if y.left_child is not None:
        x.size = x.size - temp + y.left_child.size
    else:
        x.size = x.size - temp

    x.right_child = y.left_child
    if y.left_child is not None:
        y.left_child.parent = x
    y.parent = x.parent
    if x.parent is None:
        root = y
    else:
        if x == x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y

    y.left_child = x
    x.parent = y
    return root


# right rotate needed in fixing after insertion
def right_rotate(root, y):
    x = y.left_child

    # sizes handling
    temp = x.size
    x.size = y.size
    if x.right_child is not None:
        y.size = y.size - temp + x.right_child.size
    else:
        y.size = y.size - temp

    y.left_child = x.right_child
    if x.right_child is not None:
        x.right_child.parent = y
    x.parent = y.parent

    if y.parent is None:
        root = x
    else:
        if y == y.parent.right_child:
            y.parent.right_child = x
        else:
            y.parent.left_child = x

    x.right_child = y
    y.parent = x
    return root


# given a root and a node, and it will fix any violations in the tree and return the root of the fixed tree
def RB_fixup(root, z):
    new_root = root
    while z.parent is not None and z.parent.color == "red":
        if z.parent == z.parent.parent.left_child:
            uncle = z.parent.parent.right_child
            if uncle is not None and uncle.color == "red":
                z.parent.color = "black"
                uncle.color = "black"
                z.parent.parent.color = "red"
                z = z.parent.parent
                if z == root:
                    z.color = "black"
                    break
            else:
                if z == z.parent.right_child:
                    z = z.parent
                    new_root = left_rotate(new_root, z)
                z.parent.color = "black"
                z.parent.parent.color = "red"
                new_root = right_rotate(new_root, z.parent.parent)
        else:
            uncle = z.parent.parent.left_child
            if uncle is not None and uncle.color == "red":
                z.parent.color = "black"
                uncle.color = "black"
                z.parent.parent.color = "red"
                z = z.parent.parent
                if z == root:
                    z.color = "black"
                    break
            else:
                if z == z.parent.left_child:
                    z = z.parent
                    new_root = right_rotate(new_root, z)
                z.parent.color = "black"
                z.parent.parent.color = "red"
                new_root = left_rotate(new_root, z.parent.parent)
        new_root.color = "black"
    root = new_root
    return root


# normal BST-insertion
def bst_insert(node, parent, key):
    if node is None:
        inserted_node = Node(key, parent)
        return "insert", inserted_node, inserted_node
    if key < node.key:
        case, node.left_child, inserted_node = bst_insert(node.left_child, node, key)
    elif key > node.key:
        case, node.right_child, inserted_node = bst_insert(node.right_child, node, key)
    else:
        case = "no_insert"

    if case == "insert":
        node.size += 1
        return "insert", node, inserted_node
    else:
        return "no_insert", node, None


# our main insert function that the user can call
def insert_fix(root, node, key):
    case, head, inserted_node = bst_insert(node, None, key)
    if inserted_node is not None:
        root = RB_fixup(root, inserted_node)
    return root


# the tree initializer. It is given a key and returns the root of the created tree
def init_RB_tree(key):
    root = Node(key, None)
    root.color = "black"
    return root


# search for a given key in a RB-tree
def search_RB_tree(root, key):
    if root is None:
        return None
    if root.key == key:
        return root
    elif root.key > key:
        return search_RB_tree(root.left_child, key)
    else:
        return search_RB_tree(root.right_child, key)


# calculates the height of a given RB-tree. Height = # of edges in the longest path to a leaf(Nil)
def RB_tree_height(root):
    if root is None:
        return 0
    else:
        return 1 + max(RB_tree_height(root.left_child), RB_tree_height(root.right_child))


# print the size of a given RB-tree. Size = # of elements in the tree
def RB_tree_size(root):
    return root.size


# loads the file into a RB-tree and returns its root when finish
def load_dictionary():
    print("Loading dictionary.....")
    root = None
    with open('EN-US-Dictionary.txt', 'r') as f:
        new_root = init_RB_tree(f.readline().strip())
        for line in f:
            new_root = insert_fix(new_root, new_root, line.strip().lower())
        root = new_root
    print("Dictionary loaded successfully")
    return root


# calling load_dictionary to initialize and load the tree
RB_root = load_dictionary()

while True:
    print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nOperations Menu: ")
    print("1) Print Tree Size and Height\n2) Insert\n3) Look-Up\n4) Print Inorder\n5) Exit")
    operation = input("Enter Operation number: ")
    print("")

    if operation == "1":
        print(Fore.LIGHTBLUE_EX + "Tree size: " + str(RB_tree_size(RB_root)))
        print(Fore.LIGHTBLUE_EX + "Tree height: " + str(RB_tree_height(RB_root)))
    elif operation == "2":
        print("******Insert \"*+*\" if want to exist insert operation******")
        while True:
            insert_key = input("Insert:").lower()
            if insert_key == "*+*":
                break
            else:
                RB_root = insert_fix(RB_root, RB_root, insert_key)
        print(Fore.LIGHTBLUE_EX + "Tree size: " + str(RB_tree_size(RB_root)))
        print(Fore.LIGHTBLUE_EX + "Tree height: " + str(RB_tree_height(RB_root)))
    elif operation == "3":
        insert_key = input("Search for: ").lower()
        wanted_node = search_RB_tree(RB_root, insert_key)
        if wanted_node is None:
            print("--->" + insert_key + " is not in the tree!!")
        else:
            print("--->Found:\n\tKey:", wanted_node.key, "\n\tColor:", wanted_node.color)
        print(Fore.LIGHTBLUE_EX + "Tree size: " + str(RB_tree_size(RB_root)))
        print(Fore.LIGHTBLUE_EX + "Tree height: " + str(RB_tree_height(RB_root)))
    elif operation == "4":
        print("~~~~~~~~~~ Root =", RB_root.key, "~~~~~~~~~~")
        inorder_traversal(RB_root)
        print(Fore.LIGHTBLUE_EX + "Tree size: " + str(RB_tree_size(RB_root)))
        print(Fore.LIGHTBLUE_EX + "Tree height: " + str(RB_tree_height(RB_root)))
    elif operation == "5":
        break
    else:
        print(Fore.LIGHTRED_EX + "Invalid input!! " + operation + " is out of range!!")

    input("\nPress enter to return to Operations Menu...")
