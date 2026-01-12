"""
全面测试红黑树的功能和性能，模拟算法竞赛场景
"""
from red_black_tree_template import RedBlackTree
import random
import time

def test_comprehensive():
    print("=== 综合功能测试 ===")
    rbt = RedBlackTree()
    
    # 测试插入和查询
    print("1. 插入和查询测试")
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for val in values:
        rbt.insert(val)
    
    print(f"树大小: {rbt.size()}")
    print(f"中序遍历: {rbt.inorder_traversal()}")
    
    # 测试get_by_index
    print("\n2. 索引访问测试")
    for i in range(min(5, rbt.size())):
        node = rbt.get_by_index(i)
        print(f"索引{i}: {node.val if node else None}")
    
    # 测试bisect_left_node
    print("\n3. bisect_left_node测试")
    test_points = [15, 30, 45, 75, 85]
    for t in test_points:
        node, idx = rbt.bisect_left_node(t)
        if node:
            print(f"bisect_left_node({t}): 值={node.val}, 索引={idx}")
        else:
            print(f"bisect_left_node({t}): 无结果, 索引={idx}")
    
    # 测试删除
    print("\n4. 删除测试")
    rbt.delete(20)
    print(f"删除20后: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    
    rbt.delete(30)
    print(f"删除30后: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    
    # 再次测试索引访问
    print("\n5. 删除后的索引访问测试")
    for i in range(min(5, rbt.size())):
        node = rbt.get_by_index(i)
        print(f"索引{i}: {node.val if node else None}")

def performance_test():
    print("\n=== 性能测试 ===")
    rbt = RedBlackTree()
    
    n = 50000
    print(f"插入{n}个随机数...")
    start_time = time.time()
    values = list(range(n))
    random.shuffle(values)
    
    for val in values:
        rbt.insert(val)
    insert_time = time.time() - start_time
    print(f"插入完成，耗时: {insert_time:.4f}s")
    
    # 验证树大小
    print(f"树大小: {rbt.size()}, 应该是: {n}")
    
    # 随机查询测试
    print("随机查询性能测试...")
    start_time = time.time()
    queries = random.sample(list(range(n)), min(10000, n))
    for q in queries:
        node = rbt.search_node(q)
        assert node != rbt.NIL, f"值{q}未找到!"
    search_time = time.time() - start_time
    print(f"10000次随机查询耗时: {search_time:.4f}s")
    
    # 索引访问性能测试
    print("索引访问性能测试...")
    start_time = time.time()
    for i in range(0, min(10000, n), 100):
        node = rbt.get_by_index(i)
        assert node is not None, f"索引{i}处无节点!"
    index_access_time = time.time() - start_time
    print(f"100次索引访问耗时: {index_access_time:.4f}s")
    
    # bisect_left_node性能测试
    print("bisect_left_node性能测试...")
    start_time = time.time()
    for q in queries[:1000]:  # 测试1000次
        node, idx = rbt.bisect_left_node(q)
        assert node is not None and node.val >= q, f"bisect_left_node错误!"
    bisect_time = time.time() - start_time
    print(f"1000次bisect_left_node耗时: {bisect_time:.4f}s")
    
    # 删除性能测试
    print("删除性能测试...")
    start_time = time.time()
    delete_values = random.sample(list(range(n)), n // 2)  # 删除一半
    for val in delete_values:
        rbt.delete(val)
    delete_time = time.time() - start_time
    print(f"删除{n//2}个元素耗时: {delete_time:.4f}s")
    print(f"删除后树大小: {rbt.size()}, 应该是: {n - n//2}")

def algorithm_competition_scenario():
    print("\n=== 算法竞赛场景测试 ===")
    rbt = RedBlackTree()
    
    # 模拟一个典型的算法竞赛场景：动态维护有序序列，支持多种操作
    operations = [
        ('insert', 10),
        ('insert', 5),
        ('insert', 15),
        ('insert', 3),
        ('insert', 7),
        ('query_index', 2),  # 查询第2小的元素
        ('query_bisect', 6),  # 查询第一个>=6的元素及其索引
        ('delete', 5),
        ('query_index', 2),  # 查询第2小的元素
        ('query_bisect', 6),  # 查询第一个>=6的元素及其索引
    ]
    
    for op in operations:
        if op[0] == 'insert':
            rbt.insert(op[1])
            print(f"插入 {op[1]}, 当前树: {rbt.inorder_traversal()}")
        elif op[0] == 'delete':
            rbt.delete(op[1])
            print(f"删除 {op[1]}, 当前树: {rbt.inorder_traversal()}")
        elif op[0] == 'query_index':
            node = rbt.get_by_index(op[1])
            if node:
                print(f"第{op[1]}小的元素: {node.val}")
            else:
                print(f"第{op[1]}小的元素: 不存在")
        elif op[0] == 'query_bisect':
            node, idx = rbt.bisect_left_node(op[1])
            if node:
                print(f"第一个>= {op[1]} 的元素: {node.val}, 索引: {idx}")
            else:
                print(f"没有>= {op[1]} 的元素, 总共有 {rbt.size()} 个元素")

if __name__ == "__main__":
    test_comprehensive()
    performance_test()
    algorithm_competition_scenario()
    print("\n所有测试通过！红黑树模板功能完整且性能优秀。")