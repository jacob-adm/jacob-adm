# Field study

This study asked, for each tool, what already exists, what it covers, and where a real gap remains. It was carried out between 19 and 21 November 2026.

## Method

- **Documentation and use.** Each related project was read from its documentation and source and, where possible, run on the same inputs as our tool.
- **Testing.** Comparisons use pinned versions, a fixed test set and commands anyone can re-run. Results that could not be reproduced are left out.
- **Licences and attribution.** Every project is named and credited with its licence. Closed binaries were not reverse engineered. The Sysinternals study, for example, uses only Microsoft's public documentation, *Windows Internals* and Microsoft's MIT-licensed Linux and macOS ports.
- **Gate for a new tool.** A new tool is built only when no existing tool or service already covers the problem. Where one does, the right step is to adopt it, or to contribute the missing part upstream.

## Findings

1. **Prior art exists for every tool.** Coverage is fragmented, though: the pieces are spread across many small projects, or exist as an operating-system feature that few people know about. Related projects for each tool are listed in [related tools](related-tools.md).
2. **The gaps are specific.** These tools each fill a narrow gap:
   - git-overlap compares uncommitted work in worktrees, which is where parallel agents collide first.
   - git-surface reports, per branch and across many branches, the combination of workflow, hook, install, dependency and hidden-content changes.
   - devdrop is the only tool in the comparison that checks compatibility before installing, on both Android and iOS.
   - glassbox reports what an agent can reach. Sandboxes such as nono and Agent Safehouse enforce limits instead of reporting them.
3. **No further tool passed the gate.** Each candidate area probed (agent claim verification, branch conflict prediction, comparing a release with its source) already has several small tools. The suite is complete for now. Work continues on validating and improving the existing tools, not on adding new ones.
4. **Adopt instead of building.** The glassbox feasibility rounds decided against building an inference latency tool (oha and guidellm cover it), a hidden-text scanner for agent configuration (Snyk Agent Scan and others cover it), and model-API fault injection (llmposter and MockServer cover it). See [feasibility and prior art](https://github.com/jacob-adm/glassbox/blob/main/docs/feasibility.md).

## Related documents

- [Sysinternals Suite study](https://github.com/jacob-adm/glassbox/blob/main/docs/suite-study.md)
- [Merging and CI for agent workflows](https://github.com/jacob-adm/git-overlap/blob/main/docs/article.md)
- [trust-path benchmark](https://github.com/jacob-adm/trust-path/blob/main/docs/benchmark.md)
