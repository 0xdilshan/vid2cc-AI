import pytest
from vid2cc_ai.formatter import format_timestamp

def test_format_timestamp_basic():
    """Test standard second-to-SRT conversion."""
    assert format_timestamp(61.5) == "00:01:01,500"

def test_format_timestamp_hours():
    """Test conversion when hours are involved."""
    # 3661 seconds = 1 hour, 1 minute, 1 second
    assert format_timestamp(3661.0) == "01:01:01,000"

def test_format_timestamp_milliseconds():
    """Test high-precision milliseconds."""
    assert format_timestamp(0.123) == "00:00:00,123"

def test_format_timestamp_zero():
    """Test the starting point."""
    assert format_timestamp(0.0) == "00:00:00,000"