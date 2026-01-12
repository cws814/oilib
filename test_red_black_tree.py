from red_black_tree_template import RedBlackTree

def test_basic_operations():
    print("=== 测试基本操作 ===")
    rbt = RedBlackTree()
    
    # 测试空树
    print(f"空树大小: {rbt.size()}")
    print(f"搜索不存在的值: {rbt.search(5)}")
    print(f"获取不存在的索引: {rbt.get_by_index(0)}")
    print(f"bisect_left_node(0) on empty tree: {rbt.bisect_left_node(0)}")
    
    # 插入值
    values = [10, 5, 15, 3, 7, 12, 18, 1, 6, 8, 20]
    for val in values:
        rbt.insert(val)
        print(f"插入 {val}, 树大小: {rbt.size()}")
    
    print(f"中序遍历: {rbt.inorder_traversal()}")
    
    # 测试搜索
    print(f"搜索10: {rbt.search(10)}")
    print(f"搜索9: {rbt.search(9)}")
    
    # 测试get_by_index
    print("\n测试get_by_index:")
    for i in range(rbt.size()):
        node = rbt.get_by_index(i)
        if node:
            print(f"  索引{i}: {node.val}")

def test_bisect_left_node():
    print("\n=== 测试bisect_left_node ===")
    rbt = RedBlackTree()
    
    # 插入值
    values = [10, 5, 15, 3, 7, 12, 18]
    for val in values:
        rbt.insert(val)
    
    print(f"树内容: {rbt.inorder_traversal()}")
    
    # 测试各种情况
    test_vals = [0, 3, 4, 7, 9, 10, 19, 20]
    for t in test_vals:
        node, idx = rbt.bisect_left_node(t)
        if node:
            print(f"  bisect_left_node({t}): 节点值={node.val}, 索引={idx}")
        else:
            print(f"  bisect_left_node({t}): 无结果, 索引={idx}")

def test_deletion():
    print("\n=== 测试删除操作 ===")
    rbt = RedBlackTree()
    
    values = [10, 5, 15, 3, 7, 12, 18]
    for val in values:
        rbt.insert(val)
    
    print(f"删除前: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    
    # 删除不同类型的节点
    rbt.delete(3)  # 叶子节点
    print(f"删除叶子节点3后: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    
    rbt.delete(5)  # 有两个子节点的节点
    print(f"删除有两个子节点的节点5后: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    
    rbt.delete(10)  # 根节点
    print(f"删除根节点10后: {rbt.inorder_traversal()}, 大小: {rbt.size()}")

def test_edge_cases():
    print("\n=== 测试边界情况 ===")
    rbt = RedBlackTree()
    
    # 单节点树
    rbt.insert(5)
    print(f"单节点树: {rbt.inorder_traversal()}")
    print(f"get_by_index(0): {rbt.get_by_index(0).val if rbt.get_by_index(0) else None}")
    node, idx = rbt.bisect_left_node(5)
    print(f"bisect_left_node(5): {node.val if node else None}, {idx}")
    node, idx = rbt.bisect_left_node(3)
    print(f"bisect_left_node(3): {node.val if node else None}, {idx}")
    
    # 删除唯一节点
    rbt.delete(5)
    print(f"删除后树大小: {rbt.size()}")
    print(f"bisect_left_node(5) on empty: {rbt.bisect_left_node(5)}")

def performance_test():
    print("\n=== 性能测试 ===")
    import time
    
    rbt = RedBlackTree()
    
    # 插入大量数据
    n = 10000
    start_time = time.time()
    for i in range(n):
        rbt.insert(i * 2)  # 插入偶数以增加随机性
    insert_time = time.time() - start_time
    print(f"插入{n}个元素耗时: {insert_time:.4f}s")
    
    # 测试随机访问
    start_time = time.time()
    for i in range(0, n, 100):  # 每100个取一个样本
        node = rbt.get_by_index(i)
        assert node.val == i * 2
    access_time = time.time() - start_time
    print(f"随机索引访问耗时: {access_time:.4f}s")
    
    # 测试bisect操作
    start_time = time.time()
    for i in range(0, n, 100):
        node, idx = rbt.bisect_left_node(i * 2 + 1)
        if node:
            assert node.val >= i * 2 + 1
    bisect_time = time.time() - start_time
    print(f"bisect_left_node操作耗时: {bisect_time:.4f}s")
    
    print(f"最终树大小: {rbt.size()}")

if __name__ == "__main__":
    test_basic_operations()
    test_bisect_left_node()
    test_deletion()
    test_edge_cases()
    performance_test()
    print("\n所有测试通过！")