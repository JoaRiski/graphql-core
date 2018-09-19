if False:  # pragma: no cover
    from typing import Optional, List

from .or_list import or_list

__all__ = ["quoted_or_list"]


def quoted_or_list(items):
    # type: (List[str]) -> Optional[str]
    """Given [A, B, C] return "'A', 'B', or 'C'".

    Note: We use single quotes here, since these are also used by repr().
    """
    return or_list(["'{}'".format(item) for item in items])
