# Related tools

Other projects that work on the same problems, shown alongside the suite so you can choose what to stack. This is not a ranking. The tools often answer different questions, and many of them work well together. Each comparison names the versions and the date of the test, and counts apply only to the test set described. Licences are as reported by GitHub on 21 November 2026.

## Branch conflicts: git-overlap

Test, 21 November 2026: 48 real branches of one public repository, 1,128 pairs, 13 of which conflict textually according to `git merge-tree`. git-overlap 0.4.0, Grove at its main branch and Clash 0.2.0 were each run on the same branches.

| Tool | What it answers | On the test set |
|:--|:--|:--|
| git-overlap | Which pairs conflict textually, and on which files | 155 same-file pairs; 13 reported as conflicts, all 13 true |
| [Grove](https://github.com/NathanDrake2406/grove) (Apache-2.0) | Symbol-level overlap, ranked red, yellow and green, plus a suggested merge order | The 13 conflicting pairs: 5 red, 8 yellow |
| [Clash](https://github.com/clash-sh/clash) (MIT) | Which branches share conflicting files | All 13 conflicting pairs among 945 pairs reported |
| git-parsec ([erishforG/git-parsec](https://github.com/erishforG/git-parsec), MIT) | Related work on parallel branches | Not run in this test |
| `git merge-tree` | A trial merge of one pair, built into git | Used to establish the 13 true conflicts |

None of the three tested tools saw conflicts between uncommitted edits in two worktrees. git-overlap 0.5.0 added this with `worktree:PATH` refs. Grove offers symbol-level analysis and a merge order, and Grove and Clash both offer a single command and a live view, none of which git-overlap has.

## Branches that touch trusted code: git-surface

Prior art: GitHub marks files that contain hidden Unicode in its web view, and push rulesets can block changes to given paths. CODEOWNERS, actions/labeler, Danger and dependency-review-action each cover part of this in CI. git-surface runs locally, per branch, across many branches.

Hidden characters, on a corpus of 21 invisible or reordering character classes:

| Tool | Classes found |
|:--|:--|
| git-surface 0.2.0 | 21 of 21 |
| [anti-trojan-source](https://github.com/lirantal/anti-trojan-source) 1.13.1 (Apache-2.0) | 18 of 21 |

## GitHub Actions trust paths: trust-path

| Tool | Licence |
|:--|:--|
| [zizmor](https://github.com/zizmorcore/zizmor) | MIT |
| [poutine](https://github.com/boostsecurityio/poutine) | Apache-2.0 |
| [octoscan](https://github.com/synacktiv/octoscan) | GPL-3.0 |
| [Gato-X](https://github.com/AdnaneKhan/gato-x) | Apache-2.0 |

The [trust-path benchmark](https://github.com/jacob-adm/trust-path/blob/main/docs/benchmark.md) runs trust-path on pinned public repositories and, when zizmor is installed, shows for each workflow file where each tool reports injection.

## Release contents: release-drift

Related approaches: `npm diff`, built into npm, compares two package versions; [check-sdist](https://github.com/henryiii/check-sdist) (BSD-3-Clause) checks a Python source distribution against its git tree; PyPI and npm provenance attestations record where a release was built. release-drift compares two releases, or a release with its tagged source, and reports what new code runs at install or startup. Its [source comparison](https://github.com/jacob-adm/release-drift/blob/main/docs/source-comparison.md) lists every file it accepts without comparing, and why.

## Bug lifespans: bug-age

Test: the developer-informed oracle from Rosa et al., ICSE 2021, "Evaluating SZZ Implementations Through a Developer-informed Oracle", limited to Python: 83 fixes in the 80 smallest repositories that still exist.

| Tool | Precision | Recall | F1 |
|:--|:--|:--|:--|
| bug-age 2.2.1, primary nominee | 0.68 | 0.59 | 0.63 |
| [PyDriller](https://github.com/ishepard/pydriller) 2.12, B-SZZ (Apache-2.0) | 0.51 | 0.77 | 0.61 |

bug-age's Python profile leaves out fixes that change only test files, because it measures product bugs. The oracle includes them. PyDriller is a general library for mining git history. bug-age is a pipeline that produces lifespans, reports and an explorer.

## Agent reach: glassbox

| Tool | Licence | Approach |
|:--|:--|:--|
| [nono](https://github.com/nolabs-ai/nono) | Apache-2.0 | Sandbox: enforces policy, rolls back tracked directories |
| [Agent Safehouse](https://github.com/eugene1g/agent-safehouse) | Apache-2.0 | Sandbox for coding agents |
| glassbox | Apache-2.0 | Reports what a process can read, write and reach, inside or outside a sandbox |

glassbox reports what a process can reach and nono and Agent Safehouse enforce limits, so they fit together. `glassbox reach --since` compares a run inside a sandbox with one outside it. glassbox's commands carry over concepts from Sysinternals AccessChk, RAMMap and Autoruns, written clean-room from public sources. See the [Sysinternals Suite study](https://github.com/jacob-adm/glassbox/blob/main/docs/suite-study.md).

## Installing on devices: devdrop

Static comparison of source, 21 November 2026. No devices were driven for the other tools.

| Tool | Licence | Platforms | Every target in one command | Checks before installing |
|:--|:--|:--|:--|:--|
| devdrop | Apache-2.0 | Android, iOS | Yes | Yes |
| [mobilecli](https://github.com/mobile-next/mobilecli) | see repository | Android, iOS | One device per command | No (profile checked only when re-signing) |
| [mobile-toolkit](https://github.com/IGPenguin/mobile-toolkit) | MIT | Android, iOS | Yes (`-a`) | No |
| [simvyn](https://github.com/pranshuchittora/simvyn) | MIT | Android, iOS | Yes | No |
| [native-run](https://github.com/ionic-team/native-run) | MIT | Android, iOS | One target | No |
| [madb](https://github.com/vanadium-archive/madb) | BSD-3-Clause | Android | Yes | No |

Other tools offer things devdrop does not: re-signing an `.ipa` for a device and remote devices (mobilecli), control of the app beyond installing, built for agents (simvyn, mobilecli), and installation through npm or Homebrew.

## Merging pull requests together: pr-merge-audit

The [merging and CI article mapping](https://github.com/jacob-adm/git-overlap/blob/main/docs/article.md) shows which points of Xuchen Yao's article pr-merge-audit and git-overlap cover, and which they leave open. pr-merge-audit emits one tested batch. It is not a continuous merge queue.

## One verdict over several tools: suite-gate

Test, 27 November 2026: one demo branch that adds a `pull_request_target` workflow putting the pull request title in a step with a secret, an `AGENTS.md` instruction file and an npm `postinstall` script, and edits a file another open branch also edits. Every tool below was run on it. Scanners came from their release archives or pinned packages, and the MCP servers were called over MCP as an agent would call them. The branch is built to be stopped, so a tool doing its job reports the problem or blocks it.

| Tool | Licence | What it answers | On the test branch |
|:--|:--|:--|:--|
| suite-gate 0.2.0 | Apache-2.0 | Which of the audit tools apply to what a branch changes, and one verdict from a versioned rules file, with every finding and its evidence. Also an MCP server, a GitHub Action and a check of what an agent session left behind | Blocks it, reporting the workflow change, the agent file and the install script, two paths from the title to the secret and to a write permission, the dependency file, and the overlap with the other branch |
| [SecGate](https://github.com/Stelnyx/SecGate) 0.3.3 | MIT | One command, one report and one exit code over Semgrep, Gitleaks, osv-scanner, Trivy and npm audit, with SARIF output and a security score | Blocks it, reporting Semgrep's shell injection rule on the workflow and `package.json` without a lockfile. Run with Semgrep 1.130.0, Gitleaks 8.24.0, osv-scanner 2.0.2 and Trivy 0.76.2 |
| [sast-mcp-server](https://github.com/Skyrxin/sast-mcp-server) 0.8.3 | MIT | An MCP server that runs up to eleven code scanners in parallel, removes duplicate findings and exports SARIF | Reports one finding, Semgrep's shell injection rule on the workflow, with the same four scanners |
| [reviewdog](https://github.com/reviewdog/reviewdog) 0.21.3 | MIT | The output of any analysis tool as review comments on a pull request, by default only on the lines it adds | Given Semgrep's SARIF, comments on the added workflow line with the shell injection rule |
| [MegaLinter](https://github.com/oxsecurity/megalinter) security image 9.4.0 | AGPL-3.0 | Linters for many languages and formats in one CI job, with one report | Blocks it. Checkov, KICS and Semgrep each report the shell injection on the workflow, and its other 12 security linters pass |
| [GitHub code scanning](https://docs.github.com/en/code-security/code-scanning), CodeQL 2.27.6 default setup | GitHub service | SARIF from any tool in one place, and a merge blocked on its alerts | Fails the pull request's check with one critical code injection alert on the workflow line. Default setup reads workflows only when the default branch already has one. With none there, it read the Python files and raised no alert |
| [Semgrep MCP](https://github.com/semgrep/mcp), in semgrep 1.185.0 | MIT | Semgrep scans for an agent over MCP. The standalone repository is deprecated in favour of the semgrep binary | Given the four changed files, reports one finding, the shell injection rule on the workflow |
| [Mergeward](https://github.com/pOkY-dev/mergeward) at commit 74aab7b | No licence file | A GitHub Action for pull requests written by agents, with deterministic scans, model triage for unclear cases and human approval. Its README describes it as a prototype | Reports the branch as clean, run locally without a model key and with its default configuration of Gitleaks, Semgrep's security-audit pack and a curl to shell pattern |

Every tool that ran Semgrep's GitHub Actions rules, Checkov, KICS or CodeQL caught the workflow injection on the same line. These tools combine scanners that read code for vulnerabilities, secrets and vulnerable dependencies, and most of them scan the whole directory. suite-gate combines tools that read what a branch changes since its base in what runs or is trusted, so it also reported the agent file, the install script and the overlap, and not the missing lockfile. The two kinds stack. A SecGate job, a code scanning upload or reviewdog can run beside the suite-gate Action on the same pull request.
