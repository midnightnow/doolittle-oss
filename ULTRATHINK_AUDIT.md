# ULTRATHINK AUDIT: Clinical & Technical Rigor Protocol

> **Purpose**: This file MUST be completed before any clinical feature is merged.
> **Standard**: IEC 62304 / FDA SaMD Pre-Flight Checklist
> **Version**: 1.0.0 | 2026-01-10

---

## 1. Clinical Hypothesis & Adversarial Risk

### Objective
_[What is the clinical intent of this feature? Be specific about the patient outcome.]_

### Kill-Switch Scenarios (Hard-Fail Conditions)

These are conditions where the system MUST refuse to provide a result:

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Image blur > threshold | Return `null` + flag | Unreliable input invalidates analysis |
| Value outside biological bounds | Reject + Alert | Impossible physiology indicates data error |
| Confidence < species-specific threshold | Defer to veterinarian | Insufficient certainty for autonomous decision |
| Missing species context | Block processing | Cannot apply correct biological bounds |
| Known contraindicated combination | Hard block + warning | Patient safety override |

### Biological Guardrails

Define the min/max plausible values for ALL outputs:

| Species | Metric | Min | Max | Source | Notes |
|---------|--------|-----|-----|--------|-------|
| Feline | Heart Rate (bpm) | 120 | 280 | JAVMA | Stress can elevate to 240+ |
| Feline | Resp Rate (bpm) | 20 | 40 | Plumb's | >40 = tachypnea |
| Feline | Temperature (°C) | 37.5 | 39.5 | BSAVA | |
| Feline | FGS Pain Score | 0.0 | 1.0 | Evangelista 2019 | ≥0.39 = pain threshold |
| Canine | Heart Rate (bpm) | 60 | 180 | BSAVA | Breed-dependent |
| Canine | Resp Rate (bpm) | 10 | 35 | Plumb's | |
| Canine | Temperature (°C) | 37.5 | 39.2 | BSAVA | |
| Equine | Heart Rate (bpm) | 28 | 44 | Merck | Athletic horses lower |
| Equine | Resp Rate (bpm) | 8 | 16 | Merck | |

---

## 2. Bias & Variance Audit

### Species/Breed Coverage Matrix

| Species | Breeds Tested | Edge Cases Validated | Known Exceptions |
|---------|---------------|----------------------|------------------|
| Feline | [ ] DSH, [ ] Persian, [ ] Siamese | [ ] Brachycephalic RR | None documented |
| Canine | [ ] Labrador, [ ] GSD, [ ] Toy breeds | [ ] Sighthound HR/Creatinine | Greyhounds: elevated creatinine normal |
| Canine | [ ] Brachycephalic | [ ] Bulldogs RR baseline | Higher baseline RR normal |

### Data Pedigree

- **Primary Source**: _[e.g., Montreal FGS Database, Evangelista 2019, JAVMA Guidelines]_
- **Sample Size**: n = ___
- **Collection Period**: ___ to ___
- **Known Limitations**: _[e.g., "Limited exotic species data", "Urban clinic bias"]_
- **Peer Review Status**: [ ] Published [ ] Pre-print [ ] Internal validation

### Potential Bias Vectors

Check all that apply and document mitigation:

- [ ] **Breed name bias**: Does "Pit Bull" trigger different logic than "American Staffordshire"?
  - Mitigation: ___
- [ ] **Geographic terminology bias**: UK vs US terminology differences?
  - Mitigation: ___
- [ ] **Training data imbalance**: Over-representation of common breeds?
  - Mitigation: ___
- [ ] **Owner demographic assumptions**: Income/location affecting recommendations?
  - Mitigation: ___
- [ ] **Historical bias in source data**: Were historical norms established on limited populations?
  - Mitigation: ___

---

## 3. Architectural Compliance

### Schema Validation

- [ ] Uses `doolittle-core` Pydantic models (NOT legacy schemas)
- [ ] All numeric outputs have biological validators attached
- [ ] No raw vital values accepted without species context
- [ ] All outputs include confidence scores
- [ ] Uncertainty is explicitly modeled (not hidden)

### Canonical Schema Verification

```bash
# Run this check before merge:
python -c "from doolittle_core.models import VitalSigns; print('Schema OK')"
```

- [ ] Import succeeds
- [ ] No deprecation warnings
- [ ] Version matches: `doolittle-core >= 1.0.0`

### Dependency Audit

- [ ] No new dependencies added
- [ ] If new dependency required:
  - [ ] Security review completed
  - [ ] License compatible (MIT/Apache/BSD)
  - [ ] Version pinned in pyproject.toml
  - [ ] Justification documented: ___

---

## 4. Self-Validation Countermeasures

### The Four Vows of Rigor

1. **Vow of Plausibility**: No value shall be emitted that contradicts the species' biological limits.
2. **Vow of Traceability**: Every algorithm change must reference a peer-reviewed source.
3. **Vow of Explainability**: The system must provide the "why" for every recommendation.
4. **Vow of Stability**: Models must pass the `vetsimbench` deterministic stress-test suite.

### Blind Review Confirmation

> **Critical**: The person who writes the implementation CANNOT write the validation tests.

| Role | Name | GitHub Handle | Date |
|------|------|---------------|------|
| Implementation Author | | @___ | |
| Validation Logic Author | | @___ | |
| Test Suite Author | | @___ | |

- [ ] I confirm implementation and validation authors are DIFFERENT people
- [ ] I confirm test author did not see implementation before writing tests

### Devil's Advocate Review

- **Designated Skeptic**: @___
- **Review Date**: ___

**Failure Modes Identified** (minimum 3 required):

1. **Failure Mode**: ___
   - Likelihood: [ ] Low [ ] Medium [ ] High
   - Impact: [ ] Low [ ] Medium [ ] High [ ] Critical
   - Mitigation: ___

2. **Failure Mode**: ___
   - Likelihood: [ ] Low [ ] Medium [ ] High
   - Impact: [ ] Low [ ] Medium [ ] High [ ] Critical
   - Mitigation: ___

3. **Failure Mode**: ___
   - Likelihood: [ ] Low [ ] Medium [ ] High
   - Impact: [ ] Low [ ] Medium [ ] High [ ] Critical
   - Mitigation: ___

**Counter-Evidence Documented** (minimum 1 required):

- Evidence against this approach: ___
- Source: ___
- Why we proceeded anyway: ___

### Pre-Registration (Hypothesis Locking)

- **Hypothesis ID**: HYP-___
- **Expected Outcome**: ___
- **Success Criteria**: ___
- **Failure Criteria**: ___
- **Registered Before Implementation**: [ ] Yes [ ] No
- **Registration Commit Hash**: ___

---

## 5. Clinical Review Board (CRB) Governance

### Decision Context Weighting

| Decision Type | Primary Weight (0.6) | Secondary Weight (0.3) | Safety Buffer (0.1) |
|---------------|---------------------|------------------------|---------------------|
| Emergency Triage | Senior Clinician | Board Rep (Liability) | Pet Owner Rep |
| End-of-Life | Ethicist | Pet Owner Rep | Legal Expert |
| Routine Lab Review | Data Scientist | Senior Clinician | Skeptic |
| Drug Interaction | Board Rep | Senior Clinician | Ethicist |

### CRB Consensus Requirement

- [ ] Decision requires CRB sign-off (High-risk category)
- [ ] CRB Session ID: ___
- [ ] Consensus Score: ___ / 1.0
- [ ] Override authorized: [ ] Yes [ ] No

---

## 6. Testing Requirements

### Adversarial Test Coverage

- [ ] `test_biological_impossibility.py` passes
- [ ] `test_breed_blindness.py` passes
- [ ] `test_species_edge_cases.py` passes
- [ ] `test_confidence_overreach.py` passes

### Regression Tests

- [ ] All existing tests pass
- [ ] No new test failures introduced
- [ ] Coverage threshold met (≥80%)

### VetSimBench Validation

```bash
# Run benchmark suite:
pytest testing/vetsimbench/ -v --benchmark
```

- [ ] Benchmark suite passes
- [ ] No performance regression (latency within 10% of baseline)
- [ ] Deterministic outputs verified

---

## 7. Approval Chain

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Implementation Lead | | | [ ] Approved |
| Clinical Skeptic (Devil's Advocate) | | | [ ] Approved |
| CRB Representative (if required) | | | [ ] Approved |
| Final Merge Authority | | | [ ] Approved |

---

## 8. Post-Merge Monitoring

### 30-Day Watch Period

- [ ] Monitoring dashboard configured
- [ ] Alert thresholds set for:
  - [ ] Impossible value rejections (should increase initially, then stabilize)
  - [ ] Confidence score distribution (watch for drift)
  - [ ] Error rate by species (watch for disparities)

### Rollback Plan

- **Rollback Trigger**: ___
- **Rollback Procedure**: ___
- **Rollback Owner**: @___

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-10
**Next Review**: 2026-04-10
