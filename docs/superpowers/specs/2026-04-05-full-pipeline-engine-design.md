# Design Spec: PolyLens Full Pipeline Engine (Approach C)

**Date:** 2026-04-05
**Author:** System (brainstorming session)
**Status:** Draft — for comparison with Approach B

---

## 1. Overview

This spec transforms PolyLens from a markdown-only prompt-chaining system into a proper pipeline engine with a hook registry, execution graph, event system, and programmatic API. Markdown becomes configuration files rather than execution prompts. The system supports complex DAGs, event-driven hooks, and is designed as a platform others build on programmatically.

**Approach:** Full Pipeline Engine. A Python-based execution engine with a proper plugin SDK, event bus, hook registry, and DAG execution model. Markdown files serve as configuration and documentation, not as prompt content.

**Design principles:**
- Programmatic first — Python API is the primary interface
- Event-driven — every pipeline stage emits events that hooks can subscribe to
- DAG execution — arbitrary dependency graphs between analysis stages
- Extensible SDK — developers write plugins against a stable API
- Backward compatible layer — existing markdown skills work through an adapter

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLI / Web API / SDK                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        Pipeline Engine Core                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ DAG Builder   │  │ Event Bus    │  │ Hook Registry            │  │
│  │ (parse config │  │ (pub/sub for │  │ (discover, load, manage  │  │
│  │  into graph)  │  │  all stages) │  │  hook lifecycle)         │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘  │
│         └─────────────────┼──────────────────────┘                  │
└───────────────────────────┼─────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        Execution Graph                               │
│                                                                      │
│  [Pre-Analysis] → [Lens Select] → [Reviews] → [Collision] → [Synth] │
│        │               │              │             │          │     │
│        ↓               ↓              ↓             ↓          ↓     │
│   [Hook A]         [Hook B]      [Hook C]     [Hook D]   [Hook E]   │
│        │               │              │             │          │     │
│        └───────────────┴──────────────┴─────────────┴──────────┘     │
│                              ↓                                        │
│                     [Validation] → [Post-Analysis]                    │
│                              ↓                                        │
│                     [Output Formatter]                                │
└─────────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        Adapters                                      │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐    │
│  │ Markdown Adapter     │  │ LLM Provider Adapter             │    │
│  │ (existing skills →   │  │ (abstracts OpenAI, Anthropic,    │    │
│  │  pipeline nodes)     │  │  local models, etc.)             │    │
│  └──────────────────────┘  └──────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

**New directories:**
- `src/` — Python package with engine core, event bus, hook registry, DAG builder
- `hooks/` — Hook implementations (Python modules with metadata)
- `plugins/` — User plugins (custom lenses, custom analysis steps)
- `config/` — Pipeline configurations (YAML/JSON, not markdown)
- `tests/` — Full test suite
- `docs/` — API documentation, migration guides

**Existing directories:**
- `skills/`, `orchestrators/`, `lenses/`, `engines/`, `prompts/` — adapted through compatibility layer, not modified directly

---

## 3. Pipeline Engine Core

### 3.1 DAG Builder

Parses pipeline configuration into a directed acyclic graph:

```yaml
# config/pipeline.yaml
pipeline:
  name: executive-review
  nodes:
    - id: pre-analysis
      type: stage
      stage: pre_analysis
      hooks: [inject-context, load-constraints]
    - id: lens-select
      type: stage
      stage: lens_selection
      hooks: [custom-scoring]
      depends_on: [pre-analysis]
    - id: reviews
      type: parallel
      nodes:
        - id: cto-review
          type: stage
          stage: review
          lens: CTO
        - id: ceo-review
          type: stage
          stage: review
          lens: CEO
        - id: cpo-review
          type: stage
          stage: review
          lens: CPO
      depends_on: [lens-select]
    - id: collision
      type: stage
      stage: collision
      hooks: [weight-conflicts]
      depends_on: [reviews]
    - id: synthesis
      type: stage
      stage: synthesis
      hooks: [custom-template]
      depends_on: [collision]
    - id: validation
      type: stage
      stage: validation
      depends_on: [synthesis]
    - id: post-analysis
      type: stage
      stage: post_analysis
      hooks: [webhook-notify, summarize]
      depends_on: [validation]
```

The DAG builder:
1. Parses config into node graph
2. Validates no cycles
3. Resolves dependencies
4. Computes execution order (topological sort)
5. Identifies parallelizable branches

### 3.2 Event Bus

Every pipeline stage emits events. Hooks subscribe to events they care about.

```python
# Event types
class PipelineEvent(Enum):
    PIPELINE_START = "pipeline.start"
    PIPELINE_END = "pipeline.end"
    STAGE_START = "stage.start"
    STAGE_END = "stage.end"
    STAGE_ERROR = "stage.error"
    HOOK_BEFORE = "hook.before"
    HOOK_AFTER = "hook.after"
    HOOK_ERROR = "hook.error"
    LENS_SELECTED = "lens.selected"
    REVIEW_COMPLETE = "review.complete"
    COLLISION_DETECTED = "collision.detected"
    SYNTHESIS_COMPLETE = "synthesis.complete"
    VALIDATION_COMPLETE = "validation.complete"

# Event payload
@dataclass
class Event:
    type: PipelineEvent
    stage: str
    timestamp: datetime
    payload: dict          # Stage-specific data
    context: PipelineContext  # Shared pipeline state
    metadata: dict         # Hook execution stats, etc.
```

**Event bus features:**
- Synchronous and async event handlers
- Event filtering (subscribe to specific stages, lenses, conditions)
- Event replay (for debugging and testing)
- Event persistence (optional, for audit trails)

### 3.3 Hook Registry

Discovers, loads, and manages hook lifecycle:

```python
# Hook interface
class Hook(ABC):
    @property
    def name(self) -> str: ...
    @property
    def stage(self) -> str: ...
    @property
    def order(self) -> int: ...
    @property
    def enabled(self) -> bool: ...

    @abstractmethod
    async def execute(self, event: Event, context: PipelineContext) -> HookResult: ...

# Hook result
@dataclass
class HookResult:
    success: bool
    output: dict           # Modifications to pipeline context
    error: str | None      # Error message if failed
    duration_ms: int       # Execution time
```

**Hook discovery:**
1. Scan `hooks/` directory for Python modules
2. Load modules with `Hook` subclass implementations
3. Register hooks by stage
4. Sort by order within stage
5. Validate hook dependencies (hook A requires hook B)

### 3.4 Execution Engine

Executes the DAG with proper error handling, timeouts, and parallelism:

```python
class PipelineExecutor:
    def __init__(self, dag: DAG, event_bus: EventBus, hook_registry: HookRegistry):
        ...

    async def execute(self, input: PipelineInput) -> PipelineOutput:
        # Topological sort
        execution_order = self.dag.topological_sort()

        # Execute nodes in order, parallelizing where possible
        for parallel_group in execution_order:
            tasks = [self.execute_node(node, context) for node in parallel_group]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            context.update(results)

        return context.final_output()
```

**Execution features:**
- Parallel execution of independent nodes
- Timeout per node (configurable)
- Retry on failure (configurable, with backoff)
- Circuit breaker for failing hooks
- Graceful degradation (skip failed hooks, continue pipeline)

---

## 4. Hook System

### 4.1 Hook Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Stage hooks** | Execute before/after a pipeline stage | Inject context, transform output |
| **Event hooks** | Subscribe to specific events | React to lens selection, collision detection |
| **Conditional hooks** | Execute only when condition is met | Security deep-dive if risk is high |
| **Transform hooks** | Modify pipeline context between stages | Convert output format, merge results |
| **Terminal hooks** | Execute at pipeline end (always) | Notifications, logging, metrics |

### 4.2 Hook Implementation

Hooks are Python modules with metadata:

```python
# hooks/inject_context.py
from polylens.hooks import Hook, HookResult
from polylens.context import PipelineContext

class InjectContextHook(Hook):
    name = "inject-context"
    stage = "pre_analysis"
    order = 1
    enabled = True

    async def execute(self, event, context: PipelineContext) -> HookResult:
        # Load context from file, API, or inline config
        project_context = await self.load_context(context.config)
        context.set("project_context", project_context)
        return HookResult(success=True, output={"context_injected": True})
```

### 4.3 Hook Configuration

```yaml
# config/hooks.yaml
hooks:
  inject-context:
    enabled: true
    config:
      context_file: ./project-context.md
      include_git_history: true
  webhook-notify:
    enabled: false
    config:
      url: https://hooks.slack.com/services/xxx
      events: [pipeline.end]
      format: slack
```

### 4.4 Plugin SDK

Full SDK for developers to write custom plugins:

```python
# plugins/custom_lens.py
from polylens.plugins import Plugin, LensPlugin
from polylens.context import PipelineContext

class CustomLensPlugin(LensPlugin):
    """Custom lens that analyzes regulatory compliance impact."""

    name = "regulatory-compliance"
    version = "1.0.0"

    async def analyze(self, problem: str, context: PipelineContext) -> dict:
        # Custom analysis logic
        return {
            "verdict": "MODIFY",
            "concerns": ["GDPR Article 25 implications"],
            "recommendations": ["Add data protection impact assessment"],
        }

# Plugin registration
plugin = CustomLensPlugin()
```

**SDK features:**
- Base classes for hooks, lenses, validators, formatters
- Context API for reading/writing pipeline state
- Config API for hook-specific configuration
- Logging API with structured logging
- Testing utilities (mock context, event replay)

---

## 5. Framework Harness

### 5.1 Multi-Instance Orchestration

The pipeline engine natively supports multi-instance orchestration through DAG composition:

```yaml
# config/orchestration.yaml
orchestration:
  pipelines:
    - id: technical-review
      config: config/technical-review.yaml
    - id: business-impact
      config: config/business-impact.yaml
      depends_on:
        - pipeline: technical-review
          output_transform: extract_risk_register
    - id: security-deep-dive
      config: config/security-deep-dive.yaml
      depends_on:
        - pipeline: technical-review
          condition: "risk_register.severity >= HIGH"

  merge_strategy: unified_dashboard
```

**Orchestration features:**
- Pipeline composition (pipelines within pipelines)
- Output transforms between pipeline stages
- Conditional execution based on previous results
- Parallel pipeline execution with merge strategies
- Pipeline-level timeouts and retries

### 5.2 Execution Modes

| Mode | Description |
|------|-------------|
| **Sequential** | Run pipelines in order, feed output to next |
| **Parallel** | Run independent pipelines concurrently, merge results |
| **Conditional** | Evaluate conditions, selectively run pipelines |
| **Fan-out/Fan-in** | Run one pipeline, fan out to many, fan back in |
| **Loop** | Repeat pipeline until convergence criteria met |

### 5.3 Output Merging

Multiple merge strategies:

| Strategy | Description |
|----------|-------------|
| `unified_dashboard` | Combine all verdicts, deduplicate conflicts, unified risk register |
| `last_wins` | Last pipeline's output becomes final output |
| `merge_by_section` | Merge specific sections across pipelines |
| `custom` | User-defined merge function |

---

## 6. Reasoning Control

### 6.1 Configuration

```yaml
# config/reasoning.yaml
reasoning:
  depth: standard
  min_lenses: 2
  max_lenses: 4
  constraints:
    - "Budget: under $50K"
    - "Timeline: Q2 2026"
  llm:
    provider: openai
    model: gpt-4
    temperature: 0.3
    max_tokens: 4000
  output:
    format: full
    include_sections: [all]
    custom_template: null
```

### 6.2 Depth Levels

| Level | Behavior |
|-------|----------|
| `surface` | Minimal lenses, no research, fast response |
| `standard` | Default behavior, balanced depth |
| `deep` | Extended research, web searches, git analysis, deeper frameworks |
| `exhaustive` | All relevant lenses, maximum research, multiple analytical frameworks |

### 6.3 LLM Provider Abstraction

The engine abstracts LLM providers so you can swap models:

```yaml
llm:
  provider: anthropic  # openai | anthropic | local | custom
  model: claude-sonnet-4-20250514
  fallback:
    provider: openai
    model: gpt-4
```

---

## 7. Validation Harness

### 7.1 Validation Pipeline

Validation is its own pipeline stage with pluggable validators:

```python
# validators/contract.py
from polylens.validators import Validator, ValidationResult

class ContractValidator(Validator):
    name = "contract"

    async def validate(self, output: dict, context: PipelineContext) -> ValidationResult:
        required_sections = ["verdict_alignment", "conflict_map", "final_decision"]
        missing = [s for s in required_sections if s not in output]
        return ValidationResult(
            passed=len(missing) == 0,
            score=1.0 if len(missing) == 0 else 0.0,
            details={"missing_sections": missing},
        )
```

### 7.2 Validation Types

| Type | What it validates | Config |
|------|-------------------|--------|
| **Contract** | Output format compliance | Required sections, verdict format |
| **Quality gate** | Analysis depth and completeness | Minimum score threshold |
| **Consistency** | Cross-lens fact checking | Enable/disable specific checks |
| **Regression** | Output drift vs. baseline | Baseline file path, tolerance |
| **Performance** | Execution time, token usage | Max duration, max tokens |

### 7.3 Validation Output

```json
{
  "validation": {
    "contract": {"passed": true, "score": 1.0},
    "quality_gate": {"passed": true, "score": 0.85},
    "consistency": {
      "passed": false,
      "score": 0.7,
      "issues": [
        {"type": "timeline_mismatch", "lenses": ["CEO", "CTO"], "details": "..."}
      ]
    },
    "regression": {"passed": true, "delta": {"verdicts_changed": 0, "risks_added": 2}},
    "performance": {"duration_ms": 45000, "tokens_used": 12500}
  }
}
```

---

## 8. API Interface

### 8.1 Python SDK

```python
from polylens import Pipeline

# Simple usage
pipeline = Pipeline.from_config("config/pipeline.yaml")
result = await pipeline.run("Should we migrate from PostgreSQL to MongoDB?")
print(result.decision_brief)

# Programmatic usage
pipeline = Pipeline()
pipeline.add_stage("pre_analysis", hooks=[InjectContextHook()])
pipeline.add_stage("lens_selection", hooks=[CustomScoringHook()])
pipeline.add_parallel_stage("reviews", nodes=[
    LensReview(lens="CTO"),
    LensReview(lens="CEO"),
    LensReview(lens="CPO"),
])
pipeline.add_stage("collision")
pipeline.add_stage("synthesis")
pipeline.add_stage("validation", validators=[ContractValidator(), QualityGateValidator()])

result = await pipeline.run(problem, config=reasoning_config)
```

### 8.2 CLI

```bash
# Run pipeline
polylens run "Your problem here" --config config/pipeline.yaml

# Run with specific orchestration
polylens run --orchestration config/orchestration.yaml "Your problem"

# Validate existing output
polylens validate docs/polylens/reviews/260405_migration_r1.md

# List hooks
polylens hooks list

# Run with custom plugin
polylens run --plugin plugins/custom_lens.py "Your problem"

# Dry run (validate config without executing)
polylens dry-run --config config/pipeline.yaml
```

### 8.3 REST API (Optional)

```http
POST /api/v1/pipeline/run
Content-Type: application/json

{
  "problem": "Should we migrate from PostgreSQL to MongoDB?",
  "config": "executive-review",
  "hooks": ["inject-context"],
  "reasoning": {"depth": "deep"}
}
```

---

## 9. Directory Structure

```
polylens/
├── src/                                # NEW: Python package
│   ├── polylens/
│   │   ├── __init__.py
│   │   ├── engine/
│   │   │   ├── __init__.py
│   │   │   ├── dag.py                  # DAG builder and executor
│   │   │   ├── event_bus.py            # Pub/sub event system
│   │   │   ├── hook_registry.py        # Hook discovery and lifecycle
│   │   │   ├── pipeline.py             # Pipeline orchestration
│   │   │   └── context.py              # Shared pipeline context
│   │   ├── hooks/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Hook base class
│   │   │   ├── pre_analysis.py
│   │   │   ├── lens_select.py
│   │   │   ├── review.py
│   │   │   ├── collision.py
│   │   │   ├── synthesis.py
│   │   │   └── post_analysis.py
│   │   ├── plugins/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Plugin base class
│   │   │   └── lens_plugin.py          # Lens plugin base
│   │   ├── validators/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Validator base class
│   │   │   ├── contract.py
│   │   │   ├── quality_gate.py
│   │   │   ├── consistency.py
│   │   │   └── regression.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── markdown.py             # Existing skills adapter
│   │   │   └── llm.py                  # LLM provider abstraction
│   │   ├── cli.py                      # CLI interface
│   │   └── config.py                   # Configuration management
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── fixtures/
├── hooks/                              # Hook implementations
│   ├── inject_context.py
│   ├── custom_scoring.py
│   ├── webhook_notify.py
│   └── ...
├── plugins/                            # User plugins
│   └── custom_lens.py
├── config/                             # Pipeline configurations
│   ├── pipeline.yaml
│   ├── orchestration.yaml
│   ├── reasoning.yaml
│   └── hooks.yaml
├── skills/                             # Existing (adapted through layer)
├── orchestrators/                      # Existing (adapted through layer)
├── lenses/                             # Existing (adapted through layer)
├── engines/                            # Existing (adapted through layer)
├── prompts/                            # Existing (adapted through layer)
├── tools/
│   ├── validate_markdown_contracts.py  # Existing
│   └── harness.py                      # DEPRECATED — replaced by src/
└── docs/
    └── api/                            # NEW: API documentation
```

---

## 10. Edge Cases & Error Handling

| Scenario | Behavior |
|----------|----------|
| Circular dependency in DAG | Detect before execution, raise `CycleError` |
| Hook timeout | Circuit breaker opens, hook skipped, logged |
| Hook failure | Logged, pipeline continues (unless hook is marked critical) |
| LLM provider failure | Fallback to secondary provider, or fail gracefully |
| Parallel node failure | Log error, continue with remaining nodes, note in output |
| Condition evaluation error | Log warning, skip conditional node, continue |
| Validation failure | Report in output, do not block delivery |
| Config validation error | Fail before execution with clear error message |
| Plugin incompatibility | Detect at load time, report version mismatch |

---

## 11. Testing Strategy

1. **Unit tests** — DAG builder, event bus, hook registry, validators, config parser
2. **Integration tests** — Full pipeline execution with real LLM calls (mocked in CI)
3. **Plugin tests** — SDK test harness, mock context, event replay
4. **Contract tests** — Ensure plugin API is stable, hook interface is correct
5. **Performance tests** — Pipeline execution time, memory usage, token efficiency
6. **Regression tests** — Compare output against baseline briefs
7. **Existing validation** — `python3 tools/validate_markdown_contracts.py` must still pass

---

## 12. Migration Path

**Phase 1: Foundation (3-4 days)**
- Python package structure
- DAG builder and executor
- Event bus
- Hook registry base
- Config parser

**Phase 2: Hook System (3-4 days)**
- Hook base class and lifecycle
- Stage hooks (pre-analysis, post-analysis)
- Script hook execution
- Hook discovery and registration

**Phase 3: Pipeline Integration (3-4 days)**
- Markdown adapter (existing skills → pipeline nodes)
- LLM provider adapter
- Full pipeline execution
- CLI interface

**Phase 4: Advanced Features (3-4 days)**
- Parallel execution
- Conditional routing
- Plugin SDK
- Validation harness

**Phase 5: Polish & Documentation (3-4 days)**
- REST API (optional)
- Performance optimization
- API documentation
- Migration guide
- Examples and tutorials

**Total: 15-20 days**

---

## 13. Effort Comparison with Approach B

| Aspect | Approach B | Approach C |
|--------|------------|------------|
| **Development time** | 5-8 days | 15-20 days |
| **Architecture change** | Minimal (add files) | Major (new package, adapters) |
| **Backward compatibility** | Native (no changes needed) | Requires adapter layer |
| **Runtime dependency** | Small (single script) | Full Python package |
| **Maintenance burden** | Low | Medium-High |
| **Extensibility** | Good (markdown + scripts) | Excellent (full SDK) |
| **User complexity** | Low (markdown-first) | Medium (Python API + config) |
| **Platform readiness** | No | Yes |

---

## 14. Non-Goals

- Replacing existing PolyLens markdown skills (adapted through layer)
- Real-time streaming output
- Web UI for pipeline management
- Multi-tenant support
- Distributed execution (single-process only for v1)
- Custom DSL for pipeline configuration (YAML only for v1)
