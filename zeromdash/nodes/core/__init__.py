"""Shared infrastructure for ZeroMDASH graph nodes."""

from . import (
    chain_compatibility,
    chain_context,
    chain_qualification,
    config,
    constants,
    context,
    domain_registry,
    gather_qualification,
    gather_evidence,
    hypothesis_batch,
    invocation,
    io,
    limits,
    locations,
    patch_manifest,
    planning,
    primitive_qualification,
    priority,
    qualification,
    report_dedup,
    result_artifacts,
    reporting,
    repository,
    search,
)

CORE_MODULES = (
    constants,
    config,
    io,
    limits,
    locations,
    priority,
    context,
    domain_registry,
    gather_qualification,
    gather_evidence,
    hypothesis_batch,
    qualification,
    primitive_qualification,
    chain_compatibility,
    chain_context,
    chain_qualification,
    report_dedup,
    result_artifacts,
    repository,
    patch_manifest,
    invocation,
    search,
    planning,
    reporting,
)

__all__: list[str] = []
for _module in CORE_MODULES:
    for _name in getattr(_module, "__all__", ()):
        globals()[_name] = getattr(_module, _name)
        if _name not in __all__:
            __all__.append(_name)
