"""Composition root: concrete construction stays outside the client."""

from prototype import CompiledRules, GraphNode, QueryDraft, new_request, observe


def demo() -> tuple[bool, bool, bool, bool, int]:
    shared = GraphNode("filter", ["reviewed"])
    root = GraphNode("query", edges=[shared, shared])
    shared.edges.append(root)
    exemplar = QueryDraft(
        request_id="template", rules=CompiledRules(revision=3, operations=("scan",)), root=root
    )
    exemplar.cache["old"] = "synthetic-value"
    result = new_request(exemplar, request_id="request-a", expected_revision=3)
    result.root.edges[0].tags.append("local")
    return (
        result.root is not root,
        result.root.edges[0] is result.root.edges[1],
        result.root.edges[0].edges[0] is result.root,
        result.rules is exemplar.rules,
        observe(result).cache_entries,
    )


if __name__ == "__main__":
    print(demo())
