from typing import List

from ...error import GraphQLError
from ...language import FragmentDefinitionNode, OperationDefinitionNode
from . import ValidationContext, ValidationRule

__all__ = ["NoUnusedFragmentsRule", "unused_fragment_message"]


def unused_fragment_message(frag_name):
    return "Fragment '{}' is never used.".format(frag_name)


class NoUnusedFragmentsRule(ValidationRule):
    """No unused fragments

    A GraphQL document is only valid if all fragment definitions are
    spread within operations, or spread within other fragments spread
    within operations.
    """

    def __init__(self, context):
        super().__init__(context)
        self.operation_defs = []
        self.fragment_defs = []

    def enter_operation_definition(self, node, *_args):
        self.operation_defs.append(node)
        return False

    def enter_fragment_definition(self, node, *_args):
        self.fragment_defs.append(node)
        return False

    def leave_document(self, *_args):
        fragment_names_used = set()
        get_fragments = self.context.get_recursively_referenced_fragments
        for operation in self.operation_defs:
            for fragment in get_fragments(operation):
                fragment_names_used.add(fragment.name.value)

        for fragment_def in self.fragment_defs:
            frag_name = fragment_def.name.value
            if frag_name not in fragment_names_used:
                self.report_error(
                    GraphQLError(unused_fragment_message(frag_name), [fragment_def])
                )
