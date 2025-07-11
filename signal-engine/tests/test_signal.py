import pytest
import pandas as pd
from main import apply_strategy

def test_generate_signal_format():
    mock_data = [
        {'EMA_FAST': 10, 'EMA_SLOW': 12},
        {'EMA_FAST': 11, 'EMA_SLOW': 11.5},
        {'EMA_FAST': 13, 'EMA_SLOW': 11}
    ]

    mock_df = pd.DataFrame(mock_data)

    signal = apply_strategy(mock_df)

    assert signal is not None
    assert signal["type"] in ["buy", "sell"]
    assert "strength" in signal