import pandas as pd
from cs50_project import calculate_50dma, calculate_200dma, get_golden_cross, persistent_golden_cross

def test_calculate_50dma_basic():
    df = pd.DataFrame({"adjClose": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    df = calculate_50dma(df, short_window=3)
    # The 3rd value should be average of 1,2,3 = 2.0
    assert df["50_DMA"].iloc[2] == 2.0

def test_calculate_200dma_constant():
    df = pd.DataFrame({"adjClose": [1] * 200})
    df = calculate_200dma(df, long_window=200)
    # The first valid 200_DMA value should be 1.0
    assert df["200_DMA"].iloc[-1] == 1.0

def test_get_golden_cross_detects_cross():
    # Build a DataFrame where 50_DMA crosses 200_DMA on last day
    df = pd.DataFrame({
        "adjClose": [10, 11, 12, 13, 14],
        "50_DMA":   [9, 9, 9, 9, 11],  # Crosses above
        "200_DMA":  [10, 10, 10, 10, 10]
    })
    df = get_golden_cross(df)
    # Golden cross on the last day
    assert df["Golden_Cross"].iloc[-1] == True

def test_persistent_golden_cross_counts_correctly():
    df = pd.DataFrame({
        "Golden_Cross": [False, True, True, True, False]
    })
    df = persistent_golden_cross(df, days=3)
    # 3-day streak should trigger True on the 3rd day
    assert df["Golden_Cross_Persist"].iloc[3] == True
    
if __name__ == "__main__":
    test_calculate_50dma_basic()
    test_calculate_200dma_constant()
    test_get_golden_cross_detects_cross()
    test_persistent_golden_cross_counts_correctly()
    print("All tests passed.")
