Kujo Repository Hardening, Performance & Efficiency Mega Prompt
Mission
Perform a deep, evidence-driven audit, cleanup, optimization, and hardening pass of this repository.
You are working on one Kujo ecosystem repository at a time.
Your job is not merely to find problems.
Your job is to:
understand the repository as it actually exists,
establish behavioral and performance baselines,
identify meaningful problems and inefficiencies,
implement justified improvements,
prove that existing behavior has not regressed,
leave the repository cleaner, faster, safer, easier to maintain, and easier for both humans and AI agents to work with.
Treat this as a production-grade engineering pass.
The standard is the Kujo way:
AI-native, agentic, explicit, measurable, deterministic where practical, hardened, regression-resistant, efficient, and designed for long-term maintainability.
Do not perform cosmetic churn.
Do not rewrite code merely because you prefer another style.
Do not optimize benchmarks at the expense of real behavior.
Do not weaken safety, validation, observability, errors, diagnostics, compatibility, or correctness to make the code appear smaller or faster.
Scope Boundary
The repository you are currently operating inside is the write scope.
You may inspect related Kujo repositories, documentation, packages, public APIs, dependency contracts, and downstream consumers when necessary to understand compatibility.
However:
do not casually modify sibling repositories,
do not introduce cross-repository breaking changes,
do not assume an internal-looking API has no external consumers,
do not change public contracts without proving compatibility,
do not require ecosystem-wide rewrites merely to make this repository prettier.
If an improvement legitimately requires another repository to change, document it clearly as a cross-repository follow-up rather than hiding the dependency.
The goal is to make each repository independently stronger while preserving the integrity of the wider Kujo ecosystem.
Non-Negotiable Rules
No regressions
Existing supported behavior must continue working unless there is strong evidence that the behavior is a bug.
Before changing important behavior, identify:
current behavior,
public API,
CLI behavior,
serialization formats,
configuration formats,
environment variables,
filesystem behavior,
exit codes,
error contracts,
package interfaces,
network interfaces,
generated artifacts,
integration points,
documented contracts,
tests covering the behavior,
known downstream consumers.
Preserve backward compatibility wherever reasonably possible.
If behavior must change, explain exactly why and provide migration compatibility where appropriate.
No shortcut fixes
Do not:
disable tests,
weaken assertions,
hide errors,
swallow exceptions,
add arbitrary sleeps,
increase timeouts to conceal race conditions,
remove validation because it is expensive,
silently truncate required data,
bypass security boundaries,
hardcode environment-specific behavior,
duplicate implementations to avoid understanding existing architecture,
introduce brittle regex parsing when structured data exists,
replace deterministic behavior with opaque heuristics,
add broad fallbacks that conceal actual failures,
mark broken behavior as expected merely to make CI pass.
Fix root causes.
Evidence before optimization
Do not assume something is slow, expensive, verbose, unsafe, or wasteful simply because it looks that way.
Measure or demonstrate it whenever practical.
Separate:
measured fact,
code-supported inference,
likely issue,
hypothesis.
Do not invent performance claims or percentage improvements.
Phase 0 — Understand the Repository
Before making changes, establish ground truth.
Inspect:
repository structure,
source code,
package/build configuration,
public APIs,
CLI interfaces,
tests,
fixtures,
benchmarks,
examples,
documentation,
generated files,
CI workflows,
release configuration,
dependency graph,
security-sensitive code,
persistence/state,
network behavior,
concurrency,
subprocess usage,
filesystem behavior,
environment/config loading,
agent-facing instructions,
Skills,
MCP/tool schemas,
model/provider integrations,
logging and observability.
Identify:
repository purpose,
primary users,
important execution paths,
public contracts,
performance-sensitive paths,
security boundaries,
compatibility requirements,
major dependencies,
known integrations with other Kujo repositories.
Record the exact branch and commit SHA inspected.
Do not rely solely on README descriptions.
Read the implementation.
Phase 1 — Establish the Baseline
Run the existing verification suite before changing anything.
Determine what the repository currently supports:
build,
tests,
lint,
formatting,
static analysis,
type checking,
benchmarks,
integration tests,
E2E tests,
examples,
smoke tests,
security checks.
Record failures that existed before your changes.
Where performance matters, establish representative baseline measurements.
Potential measurements include:
execution latency,
startup time,
build time,
memory use,
CPU use,
filesystem operations,
network requests,
subprocess count,
allocations,
binary size,
generated output size,
model input tokens,
model output tokens,
tool-schema tokens,
context payload size,
log/output volume.
Only measure dimensions relevant to this repository.
Do not create meaningless benchmarks merely to produce numbers.
Phase 2 — Code Complexity & Cleanup Audit
Search systematically for unnecessary complexity.
Look for:
duplicated logic,
duplicate abstractions,
dead code,
unreachable paths,
unused features,
obsolete compatibility shims,
excessive indirection,
wrappers that add no semantic value,
needless conversions,
repeated parsing,
repeated serialization/deserialization,
repeated filesystem reads,
unnecessary cloning/copying,
unnecessary allocations,
giant functions,
giant modules,
deeply nested branching,
unclear state transitions,
overly broad interfaces,
excessively generic abstractions,
premature abstractions,
abstractions used once,
inconsistent implementations of the same concept,
scattered constants,
repeated validation logic,
redundant configuration,
stale TODO/FIXME/HACK comments,
stale feature flags,
commented-out code,
debug leftovers.
Simplify where doing so materially improves the system.
Do not collapse clean abstractions simply to reduce line count.
The metric is clarity and maintainability, not fewer lines.
Phase 3 — Runtime Performance
Audit real execution paths for unnecessary work.
Investigate where relevant:
algorithmic complexity,
hot loops,
repeated computation,
duplicate parsing,
unnecessary copies,
excessive allocation,
repeated hashing,
repeated filesystem traversal,
inefficient globbing,
repeated process spawning,
blocking work in asynchronous paths,
lock contention,
unnecessary synchronization,
redundant network calls,
missing batching,
missing streaming,
unnecessary buffering,
oversized intermediate structures,
repeated initialization,
failure/retry amplification,
inefficient serialization.
Prefer architectural improvements over micro-optimizations.
For meaningful performance changes:
establish the baseline,
implement the improvement,
rerun the same benchmark,
compare results,
verify behavior equivalence.
Do not claim an improvement without evidence.
Phase 4 — Memory & Resource Efficiency
Audit lifetime and ownership of resources.
Look for:
unnecessarily retained data,
unbounded collections,
caches without bounds,
caches without invalidation,
duplicate copies of large data,
resources kept alive longer than required,
unreleased files/processes/connections,
unbounded queues,
unbounded log accumulation,
unbounded retry state,
unnecessary full-file buffering,
unnecessary full-response buffering,
temporary files not cleaned correctly.
Ensure resource bounds are explicit where necessary.
Do not introduce caching without a correctness and invalidation model.
Phase 5 — Token & Agent Context Efficiency
If this repository participates in AI or agent workflows, perform a focused token-efficiency pass.
Audit:
prompts,
Skills,
agent instructions,
MCP schemas,
tool schemas,
tool results,
generated instructions,
repository context,
handoffs,
retries,
replay,
model-visible logs,
status messages,
error payloads,
model responses.
Look for:
eager loading of rarely needed information,
repeated context,
repeated policies,
duplicate schemas,
duplicate repository summaries,
parent context copied into child agents,
full conversation replay,
giant tool outputs,
unnecessary stack traces,
entire files returned when summaries or references would suffice,
verbose machine-to-machine prose,
repeated examples,
unnecessary final-answer verbosity.
Prefer:
minimum sufficient context at the point it is needed.
Consider:
progressive disclosure,
load-on-demand references,
capability-scoped tool registration,
typed handoffs,
content-addressed artifacts,
read-once/reference-later patterns,
compact structured state,
selective evidence retrieval,
summary/detail response formats,
stable machine-readable contracts,
deterministic context selection.
Never save tokens by removing context necessary for correctness, safety, or reliable execution.
Where useful, establish token/context baselines and regression tests.
Phase 6 — Output & Command Efficiency
Treat command and tool output as a first-class efficiency problem.
Audit:
command output,
logs,
debug output,
CI logs,
errors,
status reporting,
tool results,
generated reports.
Look for places where massive output is pushed directly into humans or agents when only a small receipt is normally required.
Prefer a pattern similar to:
execute → preserve evidence → emit concise receipt
Detailed evidence should remain available when needed.
Do not destroy observability merely to make output smaller.
Phase 7 — Error Handling & Failure Semantics
Audit every important failure boundary.
Look for:
swallowed errors,
vague errors,
incorrect exit codes,
panic paths,
unchecked assumptions,
silent fallback behavior,
partial writes,
corrupted state after failure,
ambiguous retries,
retries of non-idempotent operations,
retry storms,
missing cleanup,
errors without actionable context,
internal details leaked unnecessarily,
huge error payloads,
inconsistent error types.
Errors should be:
structured where appropriate,
actionable,
deterministic,
safe,
inspectable,
concise by default,
detailed when requested or necessary.
Test failure paths, not only success paths.
Phase 8 — Security Hardening
Treat security as architecture, not linting.
Audit relevant trust boundaries:
user input,
CLI arguments,
paths,
filenames,
archives,
environment variables,
config files,
repository content,
model-generated content,
prompts,
tool results,
external APIs,
MCP requests,
network responses,
subprocess arguments,
shell execution,
serialization,
deserialization,
temporary files,
credentials,
secrets,
permissions,
sandbox boundaries.
Investigate:
path traversal,
command injection,
argument injection,
prompt/context injection,
log injection,
terminal escape/control characters,
unsafe deserialization,
SSRF,
credential leakage,
insecure temporary files,
race conditions,
TOCTOU,
symlink attacks,
permission mistakes,
overly broad filesystem access,
overly broad network access,
unsafe default capabilities,
unbounded resource consumption,
denial-of-service surfaces.
Prefer deny-by-default behavior where the repository controls capabilities or untrusted execution.
Preserve legitimate functionality.
Do not bolt security checks on randomly. Put validation at the correct trust boundary.
Phase 9 — Concurrency, Determinism & State
Where relevant, inspect:
parallel execution,
async behavior,
workers,
subprocesses,
file writes,
caches,
locks,
shared state,
checkpoints,
sessions,
retries,
resume behavior.
Look for:
race conditions,
non-atomic updates,
duplicate execution,
stale reads,
inconsistent lock ordering,
partial state,
lost updates,
nondeterministic output where determinism is expected,
replay producing different behavior,
retrying operations that already succeeded.
Add concurrency or race tests when practical.
Prefer explicit state transitions.
Phase 10 — API & Contract Quality
Audit public and semi-public interfaces.
Evaluate:
API consistency,
naming,
return types,
error contracts,
configuration,
CLI UX,
JSON schemas,
environment variables,
file formats,
protocol compatibility,
versioning.
Find accidental complexity or inconsistency.
Do not perform gratuitous breaking redesigns.
Where an interface is awkward but established, compatibility is more important than elegance unless a safe migration path exists.
Phase 11 — Dependencies & Supply Chain
Audit dependencies and build inputs.
Look for:
unused dependencies,
duplicate functionality already available internally or in the standard library,
unnecessary dependency weight,
outdated packages,
insecure dependencies,
overly broad feature flags,
runtime dependencies that could be build-time,
build dependencies that leak into runtime,
non-reproducible versions,
questionable install scripts,
unnecessary transitive dependency trees.
Reduce dependency surface where there is a clear benefit.
Do not replace a proven dependency with hand-written code merely to reduce dependency count.
Assess maintenance and security tradeoffs.
Phase 12 — Tests & Verification
The repository should leave this pass with stronger proof of correctness.
Identify important behavior that currently lacks tests.
Prioritize tests for:
public behavior,
regression-prone paths,
bugs discovered during this audit,
security boundaries,
failure paths,
concurrency,
serialization,
compatibility,
CLI contracts,
performance-sensitive paths,
agent/tool dispatch where applicable.
Avoid brittle implementation-detail tests unless necessary.
Test behavior.
For every important fix, add or improve regression coverage whenever practical.
Phase 13 — CI & Regression Ratchets
Determine what improvements can be locked in automatically.
Possible ratchets include:
test coverage for important behavior,
lint/static-analysis gates,
dependency checks,
security tests,
performance budgets,
binary-size budgets,
generated-output checks,
deterministic snapshot checks,
token/context budgets,
tool-schema budgets,
command-output budgets.
Ratchets must be stable.
Do not add flaky CI.
Intentional future growth must have a documented mechanism for updating a baseline rather than encouraging people to bypass the gate.
Phase 14 — Documentation Accuracy
Audit documentation against actual behavior.
Look for:
stale commands,
stale APIs,
obsolete examples,
undocumented features,
undocumented breaking behavior,
docs describing behavior that does not exist,
generated documentation drift,
unnecessarily verbose agent-facing docs,
duplicate sources of truth.
Update documentation affected by your changes.
Do not rewrite unrelated documentation simply for style.
Prefer one authoritative source of truth with generated derivatives where practical.
Phase 15 — AI-Native Developer Experience
Because this is part of the Kujo ecosystem, explicitly ask:
Is this repository unusually easy for an AI agent to understand, operate, debug, verify, and safely modify?
Inspect whether an agent can efficiently determine:
what the repository does,
where important code lives,
how to build it,
how to test it,
how to validate a change,
important architectural boundaries,
public contracts,
security constraints,
common workflows,
failure interpretation.
Look for avoidable agent friction such as:
giant instruction files,
contradictory instructions,
scattered conventions,
hidden required commands,
ambiguous repository structure,
duplicated documentation,
noisy command output,
enormous schemas,
unclear error messages,
missing machine-readable interfaces,
tests that cannot be run selectively.
Improve agent ergonomics where doing so also improves engineering quality.
Do not create AI-specific complexity that makes the repository worse for humans.
Phase 16 — Dead Weight Review
Identify things that should potentially be removed.
Candidates may include:
genuinely dead code,
abandoned experiments,
obsolete compatibility logic,
unused dependencies,
duplicate scripts,
old generated assets,
dead CI workflows,
unused test fixtures,
outdated examples,
stale configuration.
Before removing anything, prove it is not required by:
supported functionality,
release processes,
downstream consumers,
tests,
documentation,
compatibility contracts.
When uncertain, preserve it and document the uncertainty.
Phase 17 — Implement Improvements
After the audit, implement all high-confidence improvements that belong within the current repository and can be safely verified.
Prioritize:
P0
Correctness, security, data integrity, dangerous concurrency, broken contracts, severe reliability problems.
P1
Meaningful performance problems, major resource waste, significant token/context waste, major maintainability problems, missing critical tests.
P2
Useful simplification, dependency cleanup, smaller efficiency improvements, improved observability, improved developer/agent experience.
P3
Cosmetic or low-value improvements.
Do not spend substantial time on P3 while meaningful P0–P2 work remains.
Do not blindly implement every possible idea discovered during the audit.
Use engineering judgment.
Phase 18 — Verify the Completed Repository
After implementation, rerun everything relevant:
build,
full test suite,
lint,
formatting,
static analysis,
type checks,
integration tests,
E2E tests,
examples,
security tests,
benchmarks,
performance tests,
token/context tests,
generated-output verification.
Compare against the baseline.
For performance or efficiency changes, provide before/after numbers where measured.
For behavioral changes, prove the intended behavior.
For security fixes, include regression tests when feasible.
Do not declare success while known regressions introduced by this work remain.
Cross-Repository Findings
If you discover a problem outside the current repository, record it separately.
For each cross-repository finding provide:
affected repository,
dependency or contract involved,
evidence,
impact,
recommended change,
whether the current repository requires that change,
compatibility concerns.
Do not silently expand the implementation scope.
Required Final Report
Create or update a repository-local audit report such as:
docs/audits/repository-hardening.md
Use another location if the repository already has an established convention.
The report must include:
Repository
repository name
branch
starting SHA
ending SHA
purpose
important dependencies/integrations
Baseline
What was tested and measured before changes.
Findings
A table:
ID
Priority
Area
Finding
Evidence
Action
Status
Changes Implemented
For every meaningful change:
problem,
root cause,
implementation,
files affected,
tests added/changed,
compatibility considerations,
measured impact where applicable.
Performance & Efficiency
Include applicable before/after data for:
runtime,
memory,
build,
binary/output size,
token/context usage,
output verbosity,
dependency surface.
Do not include meaningless dimensions.
Security
Summarize trust boundaries reviewed, vulnerabilities fixed, tests added, and remaining concerns.
Compatibility
Explicitly state whether:
public APIs changed,
CLI behavior changed,
file formats changed,
schemas changed,
config changed,
environment variables changed,
external consumers may be affected.
Cross-Repository Follow-Ups
List anything requiring another Kujo repository.
Remaining Work
Classify remaining work as:
P0
P1
P2
P3
Needs more evidence
Not worth changing
Verification Receipt
Provide the exact commands executed and whether they passed.
Keep verbose logs in artifacts/files when appropriate rather than dumping enormous output into the final response.
Final Response
Do not give me a giant narrative.
Return a concise engineering receipt containing:
Result
What was accomplished.
Major Improvements
The highest-value changes.
Measured Impact
Before/after numbers that are actually supported.
Verification
Tests/checks run and results.
Remaining Issues
Only meaningful unresolved work.
Cross-Repo Follow-Ups
Anything that must happen elsewhere.
Commit
Final SHA if changes were committed.
Definition of Done
This task is not complete until:
the actual repository has been thoroughly inspected,
baseline behavior has been established,
existing failures have been distinguished from new failures,
meaningful complexity has been reviewed,
runtime/resource performance has been reviewed where relevant,
token/context efficiency has been reviewed where relevant,
command/tool output efficiency has been reviewed,
security boundaries have been reviewed,
failure handling has been reviewed,
concurrency/state behavior has been reviewed where relevant,
dependencies have been reviewed,
public contracts have been checked,
important missing regression tests have been added,
justified high-confidence improvements have been implemented,
documentation affected by those changes is accurate,
CI/regression ratchets have been added where worthwhile,
the full relevant verification suite passes,
performance claims are backed by measurements,
token claims are backed by measurements or explicitly labeled estimates,
no known regression introduced by this work remains,
cross-repository requirements are explicitly documented,
the repository is demonstrably cleaner and stronger than when the task started.
The objective is not to produce a big diff.
The objective is to produce a better repository.
Reduce accidental complexity.
Reduce unnecessary work.
Reduce unnecessary tokens.
Reduce unnecessary dependencies.
Reduce unnecessary output.
Strengthen boundaries.
Strengthen tests.
Strengthen determinism.
Strengthen observability.
Preserve useful behavior.
Measure what matters.
Leave behind regression gates so the improvements survive future development.
Do the work completely.
