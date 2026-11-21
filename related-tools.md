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
