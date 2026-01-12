from red_black_tree_template import RedBlackTree

def debug_delete():
    rbt = RedBlackTree()
    
    # 插入值
    values = [10, 5, 15, 3, 7, 12, 18]
    for val in values:
        rbt.insert(val)
        print(f"插入 {val}, 树大小: {rbt.size()}")
    
    print(f"删除前: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    rbt.print_tree()
    
    print("\n删除叶子节点3后:")
    rbt.delete(3)
    print(f"结果: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    rbt.print_tree()
    
    print("\n删除有两个子节点的节点5后:")
    rbt.delete(5)
    print(f"结果: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    rbt.print_tree()
    
    print("\n删除根节点10后:")
    rbt.delete(10)
    print(f"结果: {rbt.inorder_traversal()}, 大小: {rbt.size()}")
    rbt.print_tree()

if __name__ == "__main__":
    debug_delete()