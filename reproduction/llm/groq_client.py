"""Placeholder for the original chat-model client.

Every benchmark runner in this package replaces ``get_chat_model`` with an
OpenAI-compatible provider before any model call (see paper_benchmark_common.py
and the SocialMemBench runners). The original module belonged to a private
application and is intentionally not part of this reproduction package.
"""


def get_chat_model(*_args, **_kwargs):
    raise RuntimeError("get_chat_model must be patched by a benchmark runner before use")
