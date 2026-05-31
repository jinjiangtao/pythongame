import random
import config

def test_initialize_cards():
    """测试卡片初始化逻辑"""
    shape_list = []
    
    pairs_per_shape = config.TOTAL_PAIRS // len(config.SHAPE_TYPES)
    cards_per_shape = pairs_per_shape * 2
    
    print(f"Total pairs needed: {config.TOTAL_PAIRS}")
    print(f"Shape types: {len(config.SHAPE_TYPES)}")
    print(f"Pairs per shape: {pairs_per_shape}")
    print(f"Cards per shape: {cards_per_shape}")
    print(f"Total cards needed: {config.TOTAL_CARDS}")
    print()
    
    for shape_type in config.SHAPE_TYPES:
        for _ in range(cards_per_shape):
            shape_list.append(shape_type)
    
    print(f"Generated shape_list length: {len(shape_list)}")
    print(f"Expected length: {config.TOTAL_CARDS}")
    print()
    
    # Count shapes
    shape_counts = {}
    for shape in shape_list:
        shape_counts[shape] = shape_counts.get(shape, 0) + 1
    
    print("Shape distribution:")
    for shape, count in shape_counts.items():
        print(f"  {shape}: {count} cards")
    
    print()
    
    # Verify
    if len(shape_list) == config.TOTAL_CARDS:
        print("✓ SUCCESS: shape_list length matches TOTAL_CARDS")
    else:
        print(f"✗ ERROR: shape_list length ({len(shape_list)}) != TOTAL_CARDS ({config.TOTAL_CARDS})")
    
    if all(count == cards_per_shape for count in shape_counts.values()):
        print(f"✓ SUCCESS: Each shape appears exactly {cards_per_shape} times")
    else:
        print("✗ ERROR: Shape distribution is incorrect")
    
    random.shuffle(shape_list)
    print(f"\nAfter shuffling: {len(shape_list)} cards (should be same)")

if __name__ == "__main__":
    test_initialize_cards()
