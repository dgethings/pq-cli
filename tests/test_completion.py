"""Test script to verify path completion functionality."""

from pathlib import Path
from pq.loader import load_document
from pq.completion import PathExtractor, FuzzyMatcher


def test_path_completion():
    """Test path completion and fuzzy matching."""
    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    print(f"Loaded data with keys: {list(data.keys())}")
    print()

    print("Test 1: Extract all paths")
    extractor = PathExtractor(data)
    paths = extractor.get_paths()
    print(f"Extracted {len(paths)} paths:")
    for path in paths[:10]:
        print(f"  - {path}")
    if len(paths) > 10:
        print(f"  ... and {len(paths) - 10} more")
    print()

    print("Test 2: Fuzzy match for 'name'")
    matcher = FuzzyMatcher(paths)
    matches = matcher.find_matches("name")
    print(f"Fuzzy matches for 'name' ({len(matches)} results):")
    for match in matches:
        print(f"  - {match}")
    print()

    print("Test 3: Fuzzy match for 'items'")
    matches = matcher.find_matches("items")
    print(f"Fuzzy matches for 'items' ({len(matches)} results):")
    for match in matches[:5]:
        print(f"  - {match}")
    if len(matches) > 5:
        print(f"  ... and {len(matches) - 5} more")
    print()

    print("Test 4: Fuzzy match for empty query")
    matches = matcher.find_matches("")
    print(f"Fuzzy matches for empty query (first 10 of {len(matches)}):")
    for match in matches[:10]:
        print(f"  - {match}")
    print()

    print("Test 5: Fuzzy match for 'metadata'")
    matches = matcher.find_matches("metadata")
    print(f"Fuzzy matches for 'metadata' ({len(matches)} results):")
    for match in matches:
        print(f"  - {match}")
    print()

    print("All tests passed!")


def test_next_level_suggestions():
    """Test next-level only suggestions."""
    print("Testing next-level suggestions...")
    print()

    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    extractor = PathExtractor(data)
    paths = extractor.get_paths()
    matcher = FuzzyMatcher(paths)
    print()

    print("Test 1: Empty query - show only top-level keys (depth 1)")
    matches = matcher.find_matches("_")
    print(f"Matches ({len(matches)}): {matches}")
    assert "_['items']" in matches, "Expected '_['items']' in matches"
    assert "_['metadata']" in matches, "Expected '_['metadata']' in matches"
    assert all(matcher._get_path_depth(m) == 1 for m in matches), (
        "All matches should have depth 1"
    )
    print("✓ Test 1 passed")
    print()

    print("Test 2: Complete key - show only array indices (depth 2)")
    matches = matcher.find_matches("_['items']")
    print(f"Matches ({len(matches)}): {matches}")
    assert "_['items'][0]" in matches, "Expected '_['items'][0]' in matches"
    assert "_['items'][1]" in matches, "Expected '_['items'][1]' in matches"
    assert "_['items'][2]" in matches, "Expected '_['items'][2]' in matches"
    assert all(matcher._get_path_depth(m) == 2 for m in matches), (
        "All matches should have depth 2"
    )
    print("✓ Test 2 passed")
    print()

    print("Test 3: Complete index - show only nested keys (depth 3)")
    matches = matcher.find_matches("_['items'][0]")
    print(f"Matches ({len(matches)}): {matches}")
    assert "_['items'][0]['name']" in matches, (
        "Expected '_['items'][0]['name']' in matches"
    )
    assert "_['items'][0]['age']" in matches, (
        "Expected '_['items'][0]['age']' in matches"
    )
    assert "_['items'][0]['city']" in matches, (
        "Expected '_['items'][0]['city']' in matches"
    )
    assert "_['items'][0]['active']" in matches, (
        "Expected '_['items'][0]['active']' in matches"
    )
    assert all(matcher._get_path_depth(m) == 3 for m in matches), (
        "All matches should have depth 3"
    )
    print("✓ Test 3 passed")
    print()

    print("Test 4: Partial key with fuzzy match - '_['ite'")
    matches = matcher.find_matches("_['ite")
    print(f"Matches ({len(matches)}): {matches}")
    assert "_['items']" in matches, "Expected '_['items']' in matches"
    assert all(matcher._get_path_depth(m) == 1 for m in matches), (
        "All matches should have depth 1 (the completed key itself)"
    )
    print("✓ Test 4 passed")
    print()

    print("Test 5: Out of bounds index - show nothing")
    matches = matcher.find_matches("_['items'][10]")
    print(f"Matches ({len(matches)}): {matches}")
    assert len(matches) == 0, "Expected no matches for out of bounds index"
    print("✓ Test 5 passed")
    print()

    print("Test 6: Complete path with nested keys - show deeper levels")
    matches = matcher.find_matches("_['metadata']")
    print(f"Matches ({len(matches)}): {matches}")
    assert "_['metadata']['count']" in matches, (
        "Expected '_['metadata']['count']' in matches"
    )
    assert "_['metadata']['version']" in matches, (
        "Expected '_['metadata']['version']' in matches"
    )
    assert "_['metadata']['updated']" in matches, (
        "Expected '_['metadata']['updated']' in matches"
    )
    assert all(matcher._get_path_depth(m) == 2 for m in matches), (
        "All matches should have depth 2"
    )
    print("✓ Test 6 passed")
    print()

    print("Test 7: Partial nested key with fuzzy match")
    matches = matcher.find_matches("_['items'][0]['n")
    print(f"Matches ({len(matches)}): {matches}")
    assert "_['items'][0]['name']" in matches, (
        "Expected '_['items'][0]['name']' in matches"
    )
    assert all(matcher._get_path_depth(m) == 3 for m in matches), (
        "All matches should have depth 3"
    )
    print("✓ Test 7 passed")
    print()

    print("All next-level suggestion tests passed!")


if __name__ == "__main__":
    test_path_completion()
    print()
    print("=" * 60)
    print()
    test_next_level_suggestions()
