"""
高效红黑树模板，支持O(log n)时间复杂度的各种操作
包含节点计数和基于索引的访问功能
"""

class RedBlackTreeNode:
    def __init__(self, val, isred=True):
        self.val = val
        self.isred = isred  # True表示红色，False表示黑色
        self.left = None
        self.right = None
        self.parent = None
        self.node_count = 1  # 当前节点为根的子树中节点的总数


class RedBlackTree:
    def __init__(self, compare_func=None):
        if compare_func is None:
            compare_func = lambda a, b: a < b
        self.compare = compare_func
        
        # 使用哨兵节点作为NIL节点
        self.NIL = RedBlackTreeNode(None, False)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.NIL.node_count = 0
        
        self.root = self.NIL

    def _update_node_count(self, node):
        """更新节点的node_count值"""
        if node != self.NIL:
            node.node_count = node.left.node_count + node.right.node_count + 1

    def _rotate_left(self, x):
        """左旋转操作"""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
            
        y.parent = x.parent
        
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.left = x
        x.parent = y
        
        # 更新node_count
        self._update_node_count(x)
        self._update_node_count(y)

    def _rotate_right(self, y):
        """右旋转操作"""
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
            
        x.parent = y.parent
        
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
            
        x.right = y
        y.parent = x
        
        # 更新node_count
        self._update_node_count(y)
        self._update_node_count(x)

    def _fix_insert(self, node):
        """修复插入后可能导致的红黑树性质破坏"""
        while node.parent.isred:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.isred:
                    # Case 1: 叔叔是红色
                    node.parent.isred = False
                    uncle.isred = False
                    node.parent.parent.isred = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: 叔叔是黑色且当前节点是右孩子
                        node = node.parent
                        self._rotate_left(node)
                    
                    # Case 3: 叔叔是黑色且当前节点是左孩子
                    node.parent.isred = False
                    node.parent.parent.isred = True
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                
                if uncle.isred:
                    # Case 1: 叔叔是红色
                    node.parent.isred = False
                    uncle.isred = False
                    node.parent.parent.isred = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        # Case 2: 叔布是黑色且当前节点是左孩子
                        node = node.parent
                        self._rotate_right(node)
                    
                    # Case 3: 叔叔是黑色且当前节点是右孩子
                    node.parent.isred = False
                    node.parent.parent.isred = True
                    self._rotate_left(node.parent.parent)
        
        self.root.isred = False

    def insert(self, val):
        """插入值val"""
        node = RedBlackTreeNode(val, True)
        node.left = self.NIL
        node.right = self.NIL
        node.node_count = 1
        
        parent = self.NIL
        current = self.root
        
        while current != self.NIL:
            parent = current
            if self.compare(val, current.val):
                current = current.left
            elif self.compare(current.val, val):
                current = current.right
            else:
                # 如果值已存在，可以选择不插入或更新
                return
        
        node.parent = parent
        
        if parent == self.NIL:
            self.root = node
        elif self.compare(val, parent.val):
            parent.left = node
        else:
            parent.right = node
        
        # 从插入节点开始向上更新node_count
        temp = node
        while temp != self.NIL:
            self._update_node_count(temp)
            temp = temp.parent
        
        self._fix_insert(node)

    # delete start
    def _transplant(self, u, v):
        """用v替换u"""
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _tree_minimum(self, node):
        """找到以node为根的子树中的最小节点"""
        while node.left != self.NIL:
            node = node.left
        return node

    def _fix_delete(self, x):
        """修复删除后可能导致的红黑树性质破坏"""
        while x != self.root and not x.isred:
            if x == x.parent.left:
                w = x.parent.right
                
                if w.isred:
                    w.isred = False
                    x.parent.isred = True
                    self._rotate_left(x.parent)
                    w = x.parent.right
                
                if not w.left.isred and not w.right.isred:
                    w.isred = True
                    x = x.parent
                else:
                    if not w.right.isred:
                        w.left.isred = False
                        w.isred = True
                        self._rotate_right(w)
                        w = x.parent.right
                    
                    w.isred = x.parent.isred
                    x.parent.isred = False
                    w.right.isred = False
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                
                if w.isred:
                    w.isred = False
                    x.parent.isred = True
                    self._rotate_right(x.parent)
                    w = x.parent.left
                
                if not w.right.isred and not w.left.isred:
                    w.isred = True
                    x = x.parent
                else:
                    if not w.left.isred:
                        w.right.isred = False
                        w.isred = True
                        self._rotate_left(w)
                        w = x.parent.left
                    
                    w.isred = x.parent.isred
                    x.parent.isred = False
                    w.left.isred = False
                    self._rotate_right(x.parent)
                    x = self.root
        
        x.isred = False

    def delete(self, val):
        """删除值为val的节点"""
        z = self.search_node(val)
        if z == self.NIL:
            return  # 值不存在
        
        y = z
        y_original_isred = y.isred
        
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._tree_minimum(z.right)
            y_original_isred = y.isred
            x = y.right
            
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.isred = z.isred
        
        # 从被删除节点的父节点开始，向上更新所有祖先的node_count
        # 首先更新x的父节点（即原来z或y的父节点）
        if x.parent != self.NIL:
            self._update_node_count(x.parent)
        
        # 然后向上更新所有祖先节点的node_count
        temp = x.parent
        while temp != self.NIL:
            self._update_node_count(temp)
            temp = temp.parent
        
        # 如果y替换了z（即原来z有两个子节点），需要额外处理
        if y != z:
            # 此时y是新的节点，它的子树结构已经改变，需要重新计算
            self._update_node_count(y)
            # 更新y的祖先
            temp = y.parent  # 注意：这里y.parent已经更新为原来z的parent
            while temp != self.NIL:
                self._update_node_count(temp)
                temp = temp.parent
        
        if not y_original_isred:
            self._fix_delete(x)
    # delete end

    def search_node(self, val):
        """查找值为val的节点"""
        current = self.root
        while current != self.NIL:
            if self.compare(val, current.val):
                current = current.left
            elif self.compare(current.val, val):
                current = current.right
            else:
                return current
        return self.NIL

    def search(self, val):
        """查找值是否存在"""
        return self.search_node(val) != self.NIL

    def bisect_left_node(self, t):
        """
        搜索值大于等于t的节点以及下标
        返回值：(节点, 下标) 或 (None, 总节点数) 如果没有找到大于等于t的节点
        """
        current = self.root
        index = 0  # 当前位置相对于全局的索引
        result_node = None
        result_index = float('inf')
        
        while current != self.NIL:
            if not self.compare(current.val, t):  # current.val >= t
                # 当前节点可能是一个候选答案
                # 计算当前节点的全局索引
                current_index = index + current.left.node_count
                
                if current_index < result_index:
                    result_node = current
                    result_index = current_index
                
                # 继续向左寻找可能存在的更小索引的满足条件的节点
                current = current.left
            else:
                # 当前节点值小于t，需要加上左子树节点数+1再向右走
                index += current.left.node_count + 1
                current = current.right
        
        if result_node is None:
            return None, self.root.node_count if self.root != self.NIL else 0
        else:
            return result_node, result_index

    def get_by_index(self, i):
        """
        获取从小到大第i个节点（0-indexed）
        返回值：节点对象或None（如果索引超出范围）
        """
        if i < 0 or (self.root == self.NIL) or i >= self.root.node_count:
            return None
        
        current = self.root
        
        while current != self.NIL:
            left_size = current.left.node_count
            
            if i < left_size:
                # 目标在左子树
                current = current.left
            elif i == left_size:
                # 找到了目标节点
                return current
            else:
                # 目标在右子树
                i -= (left_size + 1)
                current = current.right
        
        return None  # 理论上不会到达这里

    def size(self):
        """返回树中节点总数"""
        return self.root.node_count if self.root != self.NIL else 0

    def inorder_traversal(self):
        """中序遍历，返回值列表"""
        result = []
        
        def inorder_helper(node):
            if node != self.NIL:
                inorder_helper(node.left)
                result.append(node.val)
                inorder_helper(node.right)
        
        inorder_helper(self.root)
        return result

    def print_tree(self):
        """打印树的结构（用于调试）"""
        def print_helper(node, indent="", last=True):
            if node != self.NIL:
                print(indent, end="")
                if last:
                    print("R----", end="")
                    indent += "     "
                else:
                    print("L----", end="")
                    indent += "|    "
                
                color = "RED" if node.isred else "BLACK"
                print(f"{node.val}({color}, count={node.node_count})")
                print_helper(node.left, indent, False)
                print_helper(node.right, indent, True)
        
        if self.root == self.NIL:
            print("Empty tree")
        else:
            print_helper(self.root)


# 使用示例
if __name__ == "__main__":
    # 基本功能测试
    rbt = RedBlackTree()
    
    # 插入一些值
    values = [10, 5, 15, 3, 7, 12, 18]
    for val in values:
        rbt.insert(val)
    
    print("树的中序遍历:", rbt.inorder_traversal())
    print("树的大小:", rbt.size())
    
    # 测试bisect_left_node
    print("\n测试bisect_left_node:")
    for t in [4, 7, 9, 16]:
        node, idx = rbt.bisect_left_node(t)
        if node:
            print(f"bisect_left_node({t}): 节点值={node.val}, 索引={idx}")
        else:
            print(f"bisect_left_node({t}): 无结果, 索引={idx}")
    
    # 测试get_by_index
    print("\n测试get_by_index:")
    for i in range(rbt.size()):
        node = rbt.get_by_index(i)
        if node:
            print(f"get_by_index({i}): {node.val}")
    
    # 删除测试
    print("\n删除节点7后:")
    rbt.delete(7)
    print("树的中序遍历:", rbt.inorder_traversal())
    print("树的大小:", rbt.size())
    
    # 自定义比较函数测试
    print("\n使用自定义比较函数（降序）:")
    rbt_desc = RedBlackTree(compare_func=lambda a, b: a > b)
    for val in [10, 5, 15, 3, 7, 12, 18]:
        rbt_desc.insert(val)
    print("降序树的中序遍历:", rbt_desc.inorder_traversal())
    
    # 字符串测试
    print("\n字符串测试:")
    rbt_str = RedBlackTree()
    for s in ["banana", "apple", "cherry", "date"]:
        rbt_str.insert(s)
    print("字符串树的中序遍历:", rbt_str.inorder_traversal())
    
    # 统计逆序对测试（类似LeetCode 315题）
    print("\n统计逆序对测试:")
    def count_smaller(nums):
        """
        对于数组中的每个元素，计算右侧比它小的元素个数
        """
        if not nums:
            return []
        
        result = [0] * len(nums)
        rbt = RedBlackTree()
        
        # 从右到左遍历
        for i in range(len(nums)-1, -1, -1):
            # 查找有多少个已插入的数字小于nums[i]
            node, idx = rbt.bisect_left_node(nums[i])
            if node:
                # 找到第一个>=nums[i]的元素，那么比nums[i]小的数量就是idx
                result[i] = idx
            else:
                # 没有找到>=nums[i]的元素，说明所有已插入的都比nums[i]小
                result[i] = rbt.size()
            
            rbt.insert(nums[i])
        
        return result
    
    test_nums = [5, 2, 6, 1]
    print(f"输入数组: {test_nums}")
    print(f"右侧比当前元素小的个数: {count_smaller(test_nums)}")
    # 应该输出[2, 1, 1, 0]