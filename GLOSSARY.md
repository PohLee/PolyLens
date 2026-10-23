# PolyLens

PolyLens reviews decisions through multiple executive perspectives. This vocabulary
distinguishes a review's inputs, individual positions, and resulting decision artifact.

## Language

**Decision Brief**:
The standard multi-lens review artifact containing individual Lens Positions, their
alignment and conflicts, and either a completed recommendation or a pending decision split.
_Avoid_: Quality score, approved plan (a well-formed brief implies neither).

**Lens Position**:
One Lens's initial verdict, decision framing, concerns, endorsements, and non-negotiables.
It is distinct from the synthesized final decision.
_Avoid_: Final verdict, consensus.

**Lens Registry**:
The authoritative collection of Lens metadata and selection rules used across review modes.
Mode-specific embedded copies are projections, not additional authorities.
_Avoid_: Independent mode registry.

**Hook**:
An opt-in instruction or script declaration associated with a named review stage.
Its metadata determines its identity, ordering, and enabled state; its body contains instructions.
_Avoid_: Automatically executed script (the host remains responsible for execution).
