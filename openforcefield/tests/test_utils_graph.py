"""
Units tests for openforcefield.utils.graph
"""
from openforcefield.utils import graph


def test_transitive_reduction():
    """Test transitive graph reduction utility."""
    dummy_graph1 = {
        "A": ["B", "C"],
        "B": ["C"],
        "C": []
    }

    graph.apply_transitive_reduction(dummy_graph1)

    assert (len(dummy_graph1["A"]) == 1 and
            len(dummy_graph1["B"]) == 1 and
            len(dummy_graph1["C"]) == 0 and
            dummy_graph1["A"][0] == "B" and
            dummy_graph1["B"][0] == "C")

    dummy_graph2 = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": []
    }

    graph.apply_transitive_reduction(dummy_graph2)

    assert (len(dummy_graph2["A"]) == 2 and
            len(dummy_graph2["B"]) == 1 and
            len(dummy_graph2["C"]) == 1 and
            len(dummy_graph2["D"]) == 0 and
            dummy_graph2["A"][0] == "B" and
            dummy_graph2["A"][1] == "C" and
            dummy_graph2["B"][0] == "D" and
            dummy_graph2["C"][0] == "D")


def test_find_roots():
    """Test find graph roots utility."""
    dummy_graph1 = {
        "A": ["C"],
        "B": ["D"],
        "C": ["E"],
        "D": ["E"],
        "E": []
    }

    root_nodes = graph.find_root_nodes(dummy_graph1)

    assert (len(root_nodes) == 2)
    assert "A" in root_nodes and "B" in root_nodes


def test_topological_sort():
    """Test topological sort graph utility."""

    dummy_graph1 = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": ["E"],
        "E": []
    }

    sorted_order = graph.topological_sort(dummy_graph1)

    assert (sorted_order[0] == "A" and
            sorted_order[1] == "B" and
            sorted_order[2] == "C" and
            sorted_order[3] == "D" and
            sorted_order[4] == "E")

    dummy_graph2 = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }

    sorted_order = graph.topological_sort(dummy_graph2)

    has_order_1 = (sorted_order[0] == "A" and
                   sorted_order[1] == "B" and
                   sorted_order[2] == "C" and
                   sorted_order[3] == "D")

    has_order_2 = (sorted_order[0] == "A" and
                   sorted_order[1] == "C" and
                   sorted_order[2] == "B" and
                   sorted_order[3] == "D")

    assert (len(sorted_order) == len(dummy_graph2))
    assert has_order_1 or has_order_2


def test_is_acyclic():
    """Test graph utility cycle detection."""

    dummy_graph1 = {
    }

    assert graph.is_acyclic(dummy_graph1)

    dummy_graph2 = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }

    assert not graph.is_acyclic(dummy_graph2)

    dummy_graph3 = {
        "A": ["B"],
        "B": ["C"],
        "C": []
    }

    assert graph.is_acyclic(dummy_graph3)

    dummy_graph4 = {
        "A": ["B"],
        "B": ["C"],
        "C": ["B"]
    }

    assert not graph.is_acyclic(dummy_graph4)