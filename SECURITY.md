# Security Policy

## Reporting

Please report vulnerabilities privately:

- ramprakashdhulipudi@gmail.com

## Threat Model (v0.1)

In scope:
- prompt payload abuse through oversized requests
- risk model bypass via adversarial tokenization patterns
- accidental exposure of sensitive prompt text in logs

Out of scope:
- tenant authz/rbac
- cryptographic signing of prompt artifacts

## Baseline Controls

- max prompt character guard (`PD_MAX_PROMPT_CHARS`)
- strict request schema validation
- deterministic scoring and no code execution paths
- no persistence of prompts by default

## Hardening Recommendations

- add API auth and request-level rate limits
- redact or hash sensitive tokens in logs
- enforce org-level policy packs for risk keywords
- store approved prompt versions with immutable audit trails
