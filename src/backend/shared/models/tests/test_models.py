"""Unit tests for models module."""

import pytest
from datetime import datetime, timezone

from ..base_model import BaseModel
from ..identifier import Identifier
from ..timestamp import Timestamp
from ..pagination import PaginationParams, PaginatedResult


class TestBaseModel:
    """Tests for BaseModel serialization and validation."""

    def test_to_dict_basic(self):
        """Test basic dataclass serialization to dict."""
        from dataclasses import dataclass

        @dataclass
        class TestModel(BaseModel):
            name: str
            value: int

        model = TestModel("test", 42)
        result = model.to_dict()
        assert result == {"name": "test", "value": 42}

    def test_from_dict_basic(self):
        """Test basic dict deserialization."""
        from dataclasses import dataclass

        @dataclass
        class TestModel(BaseModel):
            name: str
            value: int

        data = {"name": "test", "value": 42}
        model = TestModel.from_dict(data)
        assert model.name == "test"
        assert model.value == 42

    def test_from_dict_missing_required_field(self):
        """Test error on missing required field."""
        from dataclasses import dataclass

        @dataclass
        class TestModel(BaseModel):
            name: str
            value: int

        with pytest.raises(ValueError, match="Missing required fields"):
            TestModel.from_dict({"name": "test"})

    def test_equality_by_value(self):
        """Test equality comparison."""
        from dataclasses import dataclass

        @dataclass
        class TestModel(BaseModel):
            name: str
            value: int

        model1 = TestModel("test", 42)
        model2 = TestModel("test", 42)
        model3 = TestModel("other", 99)

        assert model1 == model2
        assert model1 != model3

    def test_repr(self):
        """Test string representation."""
        from dataclasses import dataclass

        @dataclass
        class TestModel(BaseModel):
            name: str
            value: int

        model = TestModel("test", 42)
        repr_str = repr(model)
        assert "TestModel" in repr_str
        assert "name='test'" in repr_str
        assert "value=42" in repr_str


class TestIdentifier:
    """Tests for Identifier wrapper."""

    def test_generate_new_identifier(self):
        """Test UUID generation."""
        id1 = Identifier()
        id2 = Identifier()
        assert id1.value != id2.value
        assert len(id1.value) == 36  # UUID string length

    def test_parse_valid_uuid(self):
        """Test parsing valid UUID."""
        valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
        id_obj = Identifier(valid_uuid)
        assert id_obj.value == valid_uuid

    def test_parse_invalid_uuid(self):
        """Test error on invalid UUID."""
        with pytest.raises(ValueError, match="Invalid UUID"):
            Identifier("not-a-uuid")

    def test_identifier_equality(self):
        """Test identifier equality."""
        id1 = Identifier("550e8400-e29b-41d4-a716-446655440000")
        id2 = Identifier("550e8400-e29b-41d4-a716-446655440000")
        id3 = Identifier()
        assert id1 == id2
        assert id1 != id3

    def test_identifier_hashable(self):
        """Test identifier in sets and dicts."""
        id1 = Identifier("550e8400-e29b-41d4-a716-446655440000")
        id2 = Identifier("550e8400-e29b-41d4-a716-446655440000")

        id_set = {id1, id2}
        assert len(id_set) == 1

        id_dict = {id1: "value"}
        assert id_dict[id2] == "value"

    def test_identifier_comparison(self):
        """Test identifier sorting."""
        id1 = Identifier("550e8400-e29b-41d4-a716-446655440000")
        id2 = Identifier("660e8400-e29b-41d4-a716-446655440000")
        assert id1 < id2


class TestTimestamp:
    """Tests for Timestamp wrapper."""

    def test_generate_current_timestamp(self):
        """Test current UTC timestamp generation."""
        ts = Timestamp()
        assert ts.value.tzinfo == timezone.utc

    def test_parse_utc_datetime(self):
        """Test parsing UTC datetime."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        ts = Timestamp(dt)
        assert ts.value == dt

    def test_reject_naive_datetime(self):
        """Test error on naive datetime."""
        dt = datetime(2026, 7, 4, 12, 0, 0)
        with pytest.raises(ValueError, match="UTC"):
            Timestamp(dt)

    def test_iso_format(self):
        """Test ISO 8601 formatting."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        ts = Timestamp(dt)
        iso = ts.iso_format()
        assert "2026-07-04" in iso
        assert "12:00:00" in iso

    def test_from_iso_format(self):
        """Test parsing ISO 8601 string."""
        iso_str = "2026-07-04T12:00:00+00:00"
        ts = Timestamp.from_iso_format(iso_str)
        assert ts.value.year == 2026
        assert ts.value.month == 7
        assert ts.value.day == 4

    def test_unix_timestamp(self):
        """Test Unix timestamp conversion."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        ts = Timestamp(dt)
        unix_ts = ts.unix_timestamp()
        assert isinstance(unix_ts, float)
        assert unix_ts > 0

    def test_timestamp_equality(self):
        """Test timestamp equality."""
        dt = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        ts1 = Timestamp(dt)
        ts2 = Timestamp(dt)
        assert ts1 == ts2

    def test_timestamp_comparison(self):
        """Test timestamp chronological comparison."""
        dt1 = datetime(2026, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2026, 7, 4, 13, 0, 0, tzinfo=timezone.utc)
        ts1 = Timestamp(dt1)
        ts2 = Timestamp(dt2)

        assert ts1 < ts2
        assert ts1 <= ts2
        assert ts2 > ts1
        assert ts2 >= ts1


class TestPaginationParams:
    """Tests for PaginationParams."""

    def test_default_pagination(self):
        """Test default pagination values."""
        params = PaginationParams()
        assert params.offset == 0
        assert params.limit == 50

    def test_custom_pagination(self):
        """Test custom pagination values."""
        params = PaginationParams(offset=10, limit=20)
        assert params.offset == 10
        assert params.limit == 20

    def test_invalid_offset(self):
        """Test error on negative offset."""
        with pytest.raises(ValueError, match="non-negative"):
            PaginationParams(offset=-1)

    def test_invalid_limit(self):
        """Test error on invalid limit."""
        with pytest.raises(ValueError, match="positive"):
            PaginationParams(limit=0)

    def test_immutable(self):
        """Test immutability."""
        params = PaginationParams()
        with pytest.raises(AttributeError):
            params.offset = 5


class TestPaginatedResult:
    """Tests for PaginatedResult."""

    def test_basic_result(self):
        """Test basic paginated result."""
        items = [1, 2, 3]
        result = PaginatedResult(items=items, total_count=100, offset=0, limit=3, has_more=True)
        assert result.items == items
        assert result.total_count == 100
        assert result.has_more is True
        assert not result.is_empty()

    def test_empty_result(self):
        """Test empty paginated result."""
        result = PaginatedResult(items=[], total_count=0, offset=0, limit=50, has_more=False)
        assert result.is_empty()

    def test_items_exceed_limit(self):
        """Test error when items exceed limit."""
        with pytest.raises(ValueError, match="exceeds limit"):
            PaginatedResult(items=[1, 2, 3], total_count=100, offset=0, limit=2, has_more=True)

    def test_pagination_consistency(self):
        """Test error on inconsistent pagination."""
        with pytest.raises(ValueError, match="inconsistent"):
            PaginatedResult(
                items=[1, 2, 3],
                total_count=2,  # Items exceed total
                offset=0,
                limit=3,
                has_more=False,  # But has_more is False
            )
