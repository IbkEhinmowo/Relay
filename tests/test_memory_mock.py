import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from Core.Integrations.memory import Memory

def test_memory_operations_mocked():
    """Test memory operations without Redis setup"""
    print("--- Testing Memory Operations (Mocked) ---")

    # Create Memory instance
    memory = Memory("test_user_123")

    # Test add operation
    with patch.object(memory.r, 'rpush') as mock_rpush:
        memory.add("test content")
        mock_rpush.assert_called_once_with("memory:user:test_user_123", "test content")
        print("✅ Memory add test passed")

    # Test list operation
    mock_data = [b"item1", b"item2", b"item3"]
    with patch.object(memory.r, 'lrange', return_value=mock_data) as mock_lrange:
        result = memory.list()
        mock_lrange.assert_called_once_with("memory:user:test_user_123", 0, -1)
        assert result == ["item1", "item2", "item3"]
        print("✅ Memory list test passed")

    # Test delete operation
    with patch.object(memory.r, 'exists', return_value=True), \
         patch.object(memory.r, 'lset') as mock_lset, \
         patch.object(memory.r, 'lrem') as mock_lrem:

        memory.delete(2)  # Delete item at index 2 (1-based)

        # Should convert to 0-based index (1)
        mock_lset.assert_called_once_with("memory:user:test_user_123", 1, "__DELETED__")
        mock_lrem.assert_called_once_with("memory:user:test_user_123", 1, "__DELETED__")
        print("✅ Memory delete test passed")

def test_memory_changing_mocked():
    """Test memory changing operation"""
    print("--- Testing Memory Changing (Mocked) ---")

    memory = Memory("test_user_123")

    with patch.object(memory.r, 'exists', return_value=True), \
         patch.object(memory.r, 'lset') as mock_lset:

        memory.changing(3, "new content")  # Change item at index 3 (1-based)

        # Should convert to 0-based index (2)
        mock_lset.assert_called_once_with("memory:user:test_user_123", 2, "new content")
        print("✅ Memory changing test passed")

if __name__ == "__main__":
    test_memory_operations_mocked()
    test_memory_changing_mocked()
    print("--- All Memory Tests Completed ---")
