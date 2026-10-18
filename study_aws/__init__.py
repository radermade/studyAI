"""Allowlisted, read-only AWS validators for Phase 2 labs.

Every validator maps to an explicit service/action allowlist of read-only
`Describe`/`List`/`Get` operations. No validator mutates AWS resources, and
credentials come only from a named profile or the standard chain.
"""
