"""Checked Protocol substitution without runtime registration."""

from prototype import CompiledRules, DraftPrototype, GraphNode, QueryDraft

exemplar: DraftPrototype = QueryDraft(
    request_id="template",
    rules=CompiledRules(revision=1, operations=("scan",)),
    root=GraphNode("query"),
)
created: QueryDraft = exemplar.clone(request_id="request-a", expected_revision=1)
