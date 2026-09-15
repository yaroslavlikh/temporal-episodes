# Differences from the code that produced the results

Everything in `reproduction/` is copied byte for byte from the original research
workspace, with the exceptions below. None of them changes executable benchmark code.

## `research/temporal_episode_prototype.py` — one docstring example

The module docstring illustrated an episode with nicknames and quotes from a private
group chat. That example was replaced with a neutral one ("Alice's view of the release
plan"). Nothing else changed.

| | SHA-256 |
|---|---|
| original file | `eabdba46f397d0c807f95245f3b9c90006cd485643fa69f8fee37cf03a8d2dc0` |
| published file | `21b94870d62267a395157e8916892c54cd42f926a44019f1e74a49a51d644993` |
| AST with docstrings removed (identical for both) | `531aa213a08775d9f2362f04e68bf47f8399320526436e1c8d7fcf37fd042d3b` |

The original hash is the implementation hash recorded in the sealed GroupMemBench and
EverMemBench memory manifests. Consequence: `verify_episode_snapshot` against those
sealed manifests reports an implementation-hash mismatch for this one file. The
code-only hash can be recomputed from the published file:

```python
import ast, hashlib
tree = ast.parse(open("research/temporal_episode_prototype.py").read())
for node in ast.walk(tree):
    if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
print(hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest())
```

## Tests with neutral fixture names

`tests/test_temporal_episode_prototype.py` and `tests/test_versioned_memory_cells.py`
used names and phrases from the same private chat as fixture text. They now use neutral
names (Latin names stay Latin, Cyrillic names stay Cyrillic so case-folding checks are
unchanged) and neutral phrases. Assertions are unchanged. Tests are not part of any
manifest hash.

## `llm/groq_client.py` — placeholder

The original module belonged to a private application (Groq client, tracing and
application config). Every benchmark runner replaces `get_chat_model` with an
OpenAI-compatible provider before any model call, so the published placeholder only
raises if it is called unpatched.

## Not included

Application modules unrelated to the benchmarks (bot handlers, prompts, database code,
configuration) and any data derived from the private chat.
