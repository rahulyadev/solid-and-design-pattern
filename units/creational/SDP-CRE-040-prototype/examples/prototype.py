"""Original synthetic query-draft exemplars with an explicit ownership contract.

Trusted, request-local Python objects only. No I/O, concurrent snapshot, or arbitrary
plugin deserialization is promised. See README for the production boundaries.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Protocol, final


class CopyPolicyError(ValueError):
    """Stable, allow-listed error code; never include source values."""


@final
@dataclass(eq=False, slots=True)
class GraphNode:
    label: str
    tags: list[str] = field(default_factory=list)
    edges: list[GraphNode] = field(default_factory=list)

    def __copy__(self) -> GraphNode:
        if type(self) is not GraphNode:
            raise CopyPolicyError("unsupported_node_type")
        return GraphNode(self.label, self.tags, self.edges)

    def __deepcopy__(self, memo: dict[int, object]) -> GraphNode:
        if type(self) is not GraphNode:
            raise CopyPolicyError("unsupported_node_type")
        # A shell must exist before following a back edge. Treat all other memo
        # entries as opaque; forward this same dictionary for every child.
        result = object.__new__(GraphNode)
        memo[id(self)] = result
        result.label = self.label
        result.tags = deepcopy(self.tags, memo)
        result.edges = deepcopy(self.edges, memo)
        return result


def validate_graph(root: GraphNode, *, max_nodes: int = 100) -> int:
    """Iterative identity traversal: cycles are legal; invalid labels are not."""
    seen: set[int] = set()
    pending = [root]
    while pending:
        node = pending.pop()
        if type(node) is not GraphNode:
            raise CopyPolicyError("unsupported_node_type")
        if id(node) in seen:
            continue
        seen.add(id(node))
        if len(seen) > max_nodes:
            raise CopyPolicyError("graph_budget_exceeded")
        if not node.label.strip():
            raise CopyPolicyError("empty_node_label")
        pending.extend(node.edges)
    return len(seen)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CompiledRules:
    revision: int
    operations: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.revision < 1 or not self.operations:
            raise CopyPolicyError("invalid_rules")
        # Frozen is shallow. Enforce the immutable representation at this seam.
        if type(self.operations) is not tuple or any(type(op) is not str for op in self.operations):
            raise CopyPolicyError("mutable_rules")


@final
@dataclass(eq=False, slots=True, kw_only=True, repr=False)
class QueryDraft:
    request_id: str
    rules: CompiledRules
    root: GraphNode
    cache: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise CopyPolicyError("empty_request_id")
        validate_graph(self.root)

    def clone(self, *, request_id: str, expected_revision: int) -> QueryDraft:
        """Fresh draft, isolated graph, shared rules, empty cache; source untouched.

        Caller owns the source exclusively throughout validation and traversal.
        Neither this method nor the Protocol grants cross-tenant authorization.
        """
        if type(self) is not QueryDraft:
            raise CopyPolicyError("unsupported_draft_type")
        if not request_id.strip() or request_id == self.request_id:
            raise CopyPolicyError("fresh_request_id_required")
        if self.rules.revision != expected_revision:
            raise CopyPolicyError("stale_revision")
        validate_graph(self.root)
        candidate = deepcopy(self.root)  # New memo for each top-level operation.
        return QueryDraft(request_id=request_id, rules=self.rules, root=candidate)

    def __copy__(self) -> QueryDraft:
        raise CopyPolicyError("use_clone_with_fresh_identity")

    def __deepcopy__(self, memo: dict[int, object]) -> QueryDraft:
        raise CopyPolicyError("use_clone_with_fresh_identity")


class DraftPrototype(Protocol):
    """Client seam for configured exemplars, not constructor selection."""

    def clone(self, *, request_id: str, expected_revision: int) -> QueryDraft: ...


def new_request(
    prototype: DraftPrototype, *, request_id: str, expected_revision: int
) -> QueryDraft:
    return prototype.clone(request_id=request_id, expected_revision=expected_revision)


@dataclass(frozen=True, slots=True)
class CloneObservation:
    node_count: int
    revision: int
    cache_entries: int


def observe(draft: QueryDraft) -> CloneObservation:
    """Allow-listed counts, never request IDs, labels, tags, or cached data."""
    return CloneObservation(validate_graph(draft.root), draft.rules.revision, len(draft.cache))
