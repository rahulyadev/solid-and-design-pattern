"""Identity assertions express the copy policy, not allocation addresses."""

from copy import copy, deepcopy

import pytest
from hypothesis import given
from hypothesis import strategies as st
from prototype import (
    CompiledRules,
    CopyPolicyError,
    GraphNode,
    QueryDraft,
    new_request,
    observe,
    validate_graph,
)
from run_prototype_demo import demo


def exemplar() -> QueryDraft:
    child = GraphNode("filter", ["reviewed"])
    root = GraphNode("query", edges=[child, child])
    child.edges.append(root)
    return QueryDraft(
        request_id="template", rules=CompiledRules(revision=3, operations=("scan",)), root=root
    )


def test_clone_contract() -> None:
    source = exemplar()
    source.cache["old"] = "value"
    result = new_request(source, request_id="a", expected_revision=3)
    assert result is not source and result.root is not source.root
    assert result.rules is source.rules
    assert result.request_id == "a" and source.request_id == "template"
    assert result.cache == {} and source.cache == {"old": "value"}
    assert result.root.edges[0] is result.root.edges[1]
    assert result.root.edges[0].edges[0] is result.root
    result.root.edges[0].tags.append("local")
    assert source.root.edges[0].tags == ["reviewed"]
    source.root.tags.append("source-edit")
    assert result.root.tags == []


def test_two_clones_have_separate_graphs_and_caches() -> None:
    source = exemplar()
    a = source.clone(request_id="a", expected_revision=3)
    b = source.clone(request_id="b", expected_revision=3)
    a.root.edges[0].tags.clear()
    a.cache["a"] = "a"
    assert b.root.edges[0].tags == ["reviewed"] and b.cache == {}


def test_shallow_node_has_shared_children_and_containers() -> None:
    source = exemplar().root
    result = copy(source)
    assert result is not source
    assert result.edges is source.edges and result.tags is source.tags
    assert result.edges[0].edges[0] is source


def test_one_memo_preserves_aliases_across_roots() -> None:
    child = GraphNode("shared")
    a, b = GraphNode("a", edges=[child]), GraphNode("b", edges=[child])
    pair = deepcopy([a, b])
    assert pair[0].edges[0] is pair[1].edges[0]
    assert deepcopy(a).edges[0] is not deepcopy(b).edges[0]


@pytest.mark.parametrize("request_id", ["", "  ", "template"])
def test_fresh_identity_required(request_id: str) -> None:
    with pytest.raises(CopyPolicyError, match="fresh_request_id_required"):
        exemplar().clone(request_id=request_id, expected_revision=3)


def test_stale_revision_is_rejected_without_touching_source() -> None:
    source = exemplar()
    source.cache["keep"] = "yes"
    with pytest.raises(CopyPolicyError, match="stale_revision"):
        source.clone(request_id="a", expected_revision=4)
    assert source.cache == {"keep": "yes"}
    assert source.root.edges[0].edges[0] is source.root


@pytest.mark.parametrize("operation", [copy, deepcopy])
def test_generic_draft_copy_is_rejected(operation: object) -> None:
    assert callable(operation)
    with pytest.raises(CopyPolicyError, match="use_clone_with_fresh_identity"):
        operation(exemplar())


def test_source_revalidated_after_external_mutation() -> None:
    source = exemplar()
    source.root.edges[0].label = ""
    with pytest.raises(CopyPolicyError, match="empty_node_label"):
        source.clone(request_id="a", expected_revision=3)
    assert source.root.edges[0].label == ""


def test_iterative_validation_handles_cycles_and_limit() -> None:
    source = exemplar()
    assert validate_graph(source.root) == 2
    with pytest.raises(CopyPolicyError, match="graph_budget_exceeded"):
        validate_graph(source.root, max_nodes=1)


@pytest.mark.parametrize("revision,operations", [(0, ("scan",)), (1, ())])
def test_invalid_rules(revision: int, operations: tuple[str, ...]) -> None:
    with pytest.raises(CopyPolicyError, match="invalid_rules"):
        CompiledRules(revision=revision, operations=operations)


def test_observation_and_repr_do_not_expose_graph_or_cache() -> None:
    source = exemplar()
    source.cache["secret-reference"] = "synthetic-sensitive-value"
    assert observe(source).node_count == 2
    assert observe(source).cache_entries == 1
    assert "secret-reference" not in repr(observe(source)) + repr(source)
    assert "synthetic-sensitive-value" not in repr(observe(source)) + repr(source)


@given(st.lists(st.text(), max_size=15))
def test_tag_mutation_is_isolated(tags: list[str]) -> None:
    source = exemplar()
    source.root.tags = tags
    result = source.clone(request_id="a", expected_revision=3)
    assert result.root.tags == tags and result.root.tags is not tags
    result.root.tags.append("new")
    assert source.root.tags == tags


def test_demo() -> None:
    assert demo() == (True, True, True, True, 0)


def test_mutable_rules_representation_is_rejected() -> None:
    with pytest.raises(CopyPolicyError, match="mutable_rules"):
        CompiledRules(revision=1, operations=["scan"])


@pytest.mark.parametrize("operation", [copy, deepcopy])
def test_unreviewed_node_subclass_is_rejected(operation) -> None:
    extended = type("ExtendedNode", (GraphNode,), {})
    source = extended("query")
    with pytest.raises(CopyPolicyError, match="unsupported_node_type"):
        operation(source)


def test_unreviewed_draft_subclass_is_rejected() -> None:
    extended = type("ExtendedDraft", (QueryDraft,), {})
    source = extended(
        request_id="template",
        rules=CompiledRules(revision=1, operations=("scan",)),
        root=GraphNode("query"),
    )
    with pytest.raises(CopyPolicyError, match="unsupported_draft_type"):
        source.clone(request_id="a", expected_revision=1)


def test_failed_graph_copy_does_not_publish_or_change_source(monkeypatch) -> None:
    import prototype

    source = exemplar()
    source.cache["keep"] = "yes"
    previous = exemplar()
    result = previous

    def fail_after_partial_copy(
        root: GraphNode, memo: dict[int, object] | None = None
    ) -> GraphNode:
        if memo is not None:
            return deepcopy(root, memo)
        partial = deepcopy(root)
        partial.tags.append("partial")
        raise RuntimeError("synthetic_copy_failure")

    monkeypatch.setattr(prototype, "deepcopy", fail_after_partial_copy)
    with pytest.raises(RuntimeError, match="synthetic_copy_failure"):
        result = source.clone(request_id="a", expected_revision=3)
    assert result is previous
    assert source.root.tags == [] and source.cache == {"keep": "yes"}
    assert source.root.edges[0].edges[0] is source.root


def test_source_tags_container_alias_is_preserved_inside_clone() -> None:
    source = exemplar()
    source.root.tags = source.root.edges[0].tags
    result = source.clone(request_id="a", expected_revision=3)
    assert result.root.tags is result.root.edges[0].tags
    assert result.root.tags is not source.root.tags


def test_direct_construction_rejects_empty_request_id() -> None:
    with pytest.raises(CopyPolicyError, match="empty_request_id"):
        QueryDraft(
            request_id=" ",
            rules=CompiledRules(revision=1, operations=("scan",)),
            root=GraphNode("query"),
        )
