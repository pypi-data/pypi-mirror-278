from typing import NotRequired, TypedDict

__all__ = ["build_error_chain"]


class ErrorChainNode(TypedDict):
    cause: NotRequired["ErrorChainNode"]
    message: str
    type: str


def build_error_chain(error: BaseException) -> ErrorChainNode:
    message = str(error)
    node: ErrorChainNode = {"message": message, "type": type(error).__qualname__}
    cause = error.__cause__
    if cause is not None:
        node["cause"] = build_error_chain(cause)
    return node
