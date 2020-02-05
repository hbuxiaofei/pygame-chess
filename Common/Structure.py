# -*- coding: utf-8 -*-
import queue


class Stack(object):
    """ 栈的抽象数据结构
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def destroy(self):
        self.items.clear()


class TreeNode(object):
    """ 树节点
    """

    MAX_CHILD_LIST = 1000000

    def __init__(self, data):
        self._deep = 0
        self._path = []
        self._data = data
        self._children = []
        self._parent = None

    def get_data(self):
        return self._data

    def set_deep(self, deep):
        self._deep = deep

    def get_deep(self):
        return self._deep

    def get_child(self):
        return self._children

    def set_parent(self, node):
        self._parent = node

    def get_parent(self):
        return self._parent

    def set_path(self, path):
        self._path = path

    def get_path(self):
        return self._path

    def add(self, node):
        if len(self._children) >= self.MAX_CHILD_LIST:
            return False
        else:
            node.set_deep(self._deep + 1)
            node.set_parent(self)
            length = len(self._children)
            path = self.get_path()
            node.set_path(path + [length+1])
            self._children.append(node)

    def get_elder(self):
        elder_list = []

        node = self
        while node._parent != None:
            node = node._parent
            elder_list.append(node)

        elder_list.reverse()
        return elder_list


class MultiTree(object):
    """ 多叉树
    """

    def __init__(self, data='root'):
        self._head = TreeNode(data)

    def get_head(self):
        return self._head

    def insert(self, path, data):
        """
            example:
                path = [1, 2, 3]
        """
        node = self._head
        for index in path:
            child = node.get_child()
            if index >= 1 and index <= len(child):
                node = child[index-1]
            else:
                return False
        node.add(TreeNode(data))

    def search(self, path):
        """
            example:
                path = [1, 2, 3, 1]
        """
        node = self._head
        for index in path:
            child = node.get_child()
            if index >= 1 and len(child) >= index:
                node = child[index-1]
            else:
                return None
        return node

    def travel(self, func=None):
        """ 层次遍历
            通过队列实现非递归层次遍历
        """
        node = self._head
        q = queue.Queue()
        q.put(node)
        while not q.empty():
            node = q.get()
            if func != None:
                func(node)
            for child in node.get_child():
                q.put(child)

    def get_height(self):
        height = 0
        def travel_func(node):
            nonlocal height
            length = len(node.get_path())
            if length > height:
                height = length
        self.travel(func=travel_func)
        return height

    def get_nodelist_by_deep(self, deep):
        """
            通过队列实现非递归层次遍历
        """
        nodelist = []

        node = self._head
        q = queue.Queue()
        q.put(node)
        is_enable_put = True
        while not q.empty():
            node = q.get()
            if node.get_deep() == deep:
                nodelist.append(node)
            if is_enable_put:
                for child in node.get_child():
                    if child.get_deep() <= deep:
                        q.put(child)
                    else:
                        is_enable_put = False
        return nodelist


def test_MultiTree():
    path = []
    mtree = MultiTree()
    node = mtree.get_head()
    print(path, node.get_path(), ":%s" % node.get_data())

    path = []
    mtree.insert(path, "1-1")
    mtree.insert(path, "1-2")
    mtree.insert(path, "1-3")

    # deep = 1
    path = [1]
    mtree.insert(path, "1-1-1")
    mtree.insert(path, "1-1-2")

    path = [2]
    mtree.insert(path, "1-2-1")
    mtree.insert(path, "1-2-2")

    path = [3]
    mtree.insert(path, "1-3-1")
    mtree.insert(path, "1-3-2")

    # deep = 2
    path = [1, 2]
    mtree.insert(path, "1-1-2-1")
    mtree.insert(path, "1-1-2-2")


    path = [1,2,2]
    node = mtree.search(path)
    print("child: ", path, node.get_path(), ":%s" % node.get_data())
    node = node.get_parent()
    path.pop()
    print("parent: ", path, node.get_path(), ":%s\n\n" % node.get_data())

    print("height:", mtree.get_height())
    def travel_func(node):
        print("deep:%d  data:%s" % (node.get_deep(), node.get_data()))
    mtree.travel(func=travel_func)

    print("\n\ndeep==0")
    nodelist = mtree.get_nodelist_by_deep(0)
    for node in nodelist:
        print("deep:%d  data:%s" % (node.get_deep(), node.get_data()))

    print("\n\ndeep==2")
    nodelist = mtree.get_nodelist_by_deep(2)
    for node in nodelist:
        print("deep:%d  data:%s" % (node.get_deep(), node.get_data()))



if __name__ == "__main__":
    test_MultiTree()

