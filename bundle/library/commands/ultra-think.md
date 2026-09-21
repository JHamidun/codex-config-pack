---
name: "ultra-think"
description: "Deep analysis and problem solving with multi-dimensional thinking"
---

# Codex execution contract

This recipe was adapted from a pinned public source. Its domain guidance is reusable;
its historical provider examples are not a live capability registry.

1. Resolve `${CODEX_PACK_ROOT}` from the installed `hamidun-pack` entrypoint. It is a documentation root, not an environment variable automatically created by Codex.
2. Native tool mapping: Claude `Read/Glob/Grep` means available file/search tools; `Bash` means the current shell; `Write/Edit/MultiEdit` means the supported patch/file tool. Claude `Task/Agent` means native collaboration with a concrete bounded subtask, only when delegation is authorized. Tool names inside old examples are illustrative, not callable API schemas.
3. Claude slash commands become catalog recipes. They are not automatically registered as Codex slash commands. Pass arguments explicitly in the task.
4. Do not execute files ending in `.source`, upstream hook examples, or paths containing `UPSTREAM_HOME`. They are quarantined reference code, NOT a validated runtime. A dependent workflow must first receive a reviewed Codex-owned adapter with explicit state/output roots and tests, or use an available native capability.
5. Do not load secrets, session databases, private memory, or Claude model/provider defaults. Resolve integrations and named environment variables only when required and authorized.
6. Model IDs, MCP names, permission snippets and scheduled-job examples in the source are historical. Check current supported equivalents. Never activate them just because a recipe mentions them.
7. Prefer native image generation, documents and browser tooling where available. Do not install dependencies or authorize a third party as a side effect of reading this recipe.
8. Preserve scope and output requirements. Mark unavailable dependencies clearly; do not claim a recipe passed a live test from a syntax/manifest check.

## Adapted domain recipe


# Deep Analysis and Problem Solving Mode

Deep analysis and problem solving mode

## Instructions

1. **Initialize Ultra Think Mode**
   - Acknowledge the request for enhanced analytical thinking
   - Set context for deep, systematic reasoning
   - Prepare to explore the problem space comprehensively

2. **Parse the Problem or Question**
   - Extract the core challenge from: $ARGUMENTS
   - Identify all stakeholders and constraints
   - Recognize implicit requirements and hidden complexities
   - Question assumptions and surface unknowns

3. **Multi-Dimensional Analysis**
   Approach the problem from multiple angles:
   
   ### Technical Perspective
   - Analyze technical feasibility and constraints
   - Consider scalability, performance, and maintainability
   - Evaluate security implications
   - Assess technical debt and future-proofing
   
   ### Business Perspective
   - Understand business value and ROI
   - Consider time-to-market pressures
   - Evaluate competitive advantages
   - Assess risk vs. reward trade-offs
   
   ### User Perspective
   - Analyze user needs and pain points
   - Consider usability and accessibility
   - Evaluate user experience implications
   - Think about edge cases and user journeys
   
   ### System Perspective
   - Consider system-wide impacts
   - Analyze integration points
   - Evaluate dependencies and coupling
   - Think about emergent behaviors

4. **Generate Multiple Solutions**
   - Brainstorm at least 3-5 different approaches
   - For each approach, consider:
     - Pros and cons
     - Implementation complexity
     - Resource requirements
     - Potential risks
     - Long-term implications
   - Include both conventional and creative solutions
   - Consider hybrid approaches

5. **Deep Dive Analysis**
   For the most promising solutions:
   - Create detailed implementation plans
   - Identify potential pitfalls and mitigation strategies
   - Consider phased approaches and MVPs
   - Analyze second and third-order effects
   - Think through failure modes and recovery

6. **Cross-Domain Thinking**
   - Draw parallels from other industries or domains
   - Apply design patterns from different contexts
   - Consider biological or natural system analogies
   - Look for innovative combinations of existing solutions

7. **Challenge and Refine**
   - Play devil's advocate with each solution
   - Identify weaknesses and blind spots
   - Consider "what if" scenarios
   - Stress-test assumptions
   - Look for unintended consequences

8. **Synthesize Insights**
   - Combine insights from all perspectives
   - Identify key decision factors
   - Highlight critical trade-offs
   - Summarize innovative discoveries
   - Present a nuanced view of the problem space

9. **Provide Structured Recommendations**
   Present findings in a clear structure:
   ```
   ## Problem Analysis
   - Core challenge
   - Key constraints
   - Critical success factors
   
   ## Solution Options
   ### Option 1: [Name]
   - Description
   - Pros/Cons
   - Implementation approach
   - Risk assessment
   
   ### Option 2: [Name]
   [Similar structure]
   
   ## Recommendation
   - Recommended approach
   - Rationale
   - Implementation roadmap
   - Success metrics
   - Risk mitigation plan
   
   ## Alternative Perspectives
   - Contrarian view
   - Future considerations
   - Areas for further research
   ```

10. **Meta-Analysis**
    - Reflect on the thinking process itself
    - Identify areas of uncertainty
    - Acknowledge biases or limitations
    - Suggest additional expertise needed
    - Provide confidence levels for recommendations

## Usage Examples

```bash
# Architectural decision
/ultra-think Should we migrate to microservices or improve our monolith?

# Complex problem solving
/ultra-think How do we scale our system to handle 10x traffic while reducing costs?

# Strategic planning
/ultra-think What technology stack should we choose for our next-gen platform?

# Design challenge
/ultra-think How can we improve our API to be more developer-friendly while maintaining backward compatibility?
```

## Key Principles

- **First Principles Thinking**: Break down to fundamental truths
- **Systems Thinking**: Consider interconnections and feedback loops
- **Probabilistic Thinking**: Work with uncertainties and ranges
- **Inversion**: Consider what to avoid, not just what to do
- **Second-Order Thinking**: Consider consequences of consequences

## Output Expectations

- Comprehensive analysis (typically 2-4 pages of insights)
- Multiple viable solutions with trade-offs
- Clear reasoning chains
- Acknowledgment of uncertainties
- Actionable recommendations
- Novel insights or perspectives