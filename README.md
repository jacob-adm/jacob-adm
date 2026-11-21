<div align="center">

<h1>Jacob Adm<br><sub><sub>AI Automation Engineer</sub></sub></h1>

<p><a href="https://www.linkedin.com/in/jacobadm"><img src="https://img.shields.io/badge/LinkedIn-0F6378?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>&nbsp;<a href="https://github.com/jacob-adm/homebrew-tap"><img src="https://img.shields.io/badge/Homebrew-jacob--adm%2Ftap-0F6378?style=flat-square&logo=homebrew&logoColor=white" alt="Homebrew tap"></a>&nbsp;<img src="https://img.shields.io/badge/tools-8-0F6378?style=flat-square" alt="8 tools">&nbsp;<img src="https://img.shields.io/badge/licence-Apache--2.0-0F6378?style=flat-square" alt="Apache-2.0 licence"></p>

Command-line tools for branch hygiene, merge quality and software supply-chain security around AI coding agents.

</div>

## The suite

When several agents work on one repository at once, branches pile up quickly, collide in the same files, and sometimes change code that runs or is trusted: workflows, hooks, install scripts, dependencies.

Tools for each of these problems already exist, but they are spread across many projects. These tools attempt to fill the gaps that remained, and most of them can be chained together.

Each tool was then checked against the tools already available, in a field study; glassbox came directly out of one, a study of the Sysinternals Suite. The method was documentation, real use, testing, licence compliance and attribution, with no reverse engineering. The [field study](field-study.md) gives the method and findings, and [related tools](related-tools.md) shows other projects alongside these, for comparison.

## Where each tool runs

| Stage | Question | Tool | Install | Version |
|:--|:--|:--|:--|:--|
| Before an agent runs | What can this process read, write and reach on this machine? | [glassbox](https://github.com/jacob-adm/glassbox) | `brew install jacob-adm/tap/glassbox` | <a href="https://github.com/jacob-adm/glassbox/releases/latest"><img src="https://img.shields.io/github/v/release/jacob-adm/glassbox?style=flat-square&color=0F6378&label=release" alt="glassbox latest release"></a> |
| Branches pile up | Which branches change workflows, hooks, install scripts, lockfiles or hidden content? | [git-surface](https://github.com/jacob-adm/git-surface) | `pip install git-surface` | <a href="https://pypi.org/project/git-surface/"><img src="https://img.shields.io/pypi/v/git-surface?style=flat-square&color=0F6378&label=PyPI" alt="git-surface on PyPI"></a> |
| | Which branches will conflict with each other, including uncommitted work in worktrees? | [git-overlap](https://github.com/jacob-adm/git-overlap) | `pip install git-overlap` | <a href="https://pypi.org/project/git-overlap/"><img src="https://img.shields.io/pypi/v/git-overlap?style=flat-square&color=0F6378&label=PyPI" alt="git-overlap on PyPI"></a> |
| Before merge | Can PR titles, issue bodies or fork code reach a secret or publishing token in GitHub Actions? | [trust-path](https://github.com/jacob-adm/trust-path) | `pip install trust-path` | <a href="https://pypi.org/project/trust-path/"><img src="https://img.shields.io/pypi/v/trust-path?style=flat-square&color=0F6378&label=PyPI" alt="trust-path on PyPI"></a> |
| | Do all open pull requests merge and pass tests together? | [pr-merge-audit](https://github.com/jacob-adm/pr-merge-audit) | `pip install pr-merge-audit` | <a href="https://pypi.org/project/pr-merge-audit/"><img src="https://img.shields.io/pypi/v/pr-merge-audit?style=flat-square&color=0F6378&label=PyPI" alt="pr-merge-audit on PyPI"></a> |
| Dependencies and releases | What changed between two releases, and what new code runs at install or startup? | [release-drift](https://github.com/jacob-adm/release-drift) | `pip install release-drift` | <a href="https://pypi.org/project/release-drift/"><img src="https://img.shields.io/pypi/v/release-drift?style=flat-square&color=0F6378&label=PyPI" alt="release-drift on PyPI"></a> |
| Afterwards (any project) | How long did fixed bugs live, in commits, days and releases? | [bug-age](https://github.com/jacob-adm/bug-age) | `pip install bug-age` | <a href="https://pypi.org/project/bug-age/"><img src="https://img.shields.io/pypi/v/bug-age?style=flat-square&color=0F6378&label=PyPI" alt="bug-age on PyPI"></a> |

Every tool documents its exit statuses, so it can run in CI or act as a gate for an agent. trust-path, release-drift, glassbox and devdrop print JSON with `--json`, git-surface and git-overlap write tab-separated records, and pr-merge-audit and bug-age write JSON result files.

## Stacking the tools

Branch triage: give one list of branches to both git commands.

```sh
git for-each-ref --format='%(refname:short)' refs/heads/agent/ > branches
git surface main < branches                        # which branches touch code that runs or is trusted
git footprint main < branches | git overlap | git pairmerge --onto main   # which pairs conflict
```

`git pairmerge` needs git 2.43 or later.

Follow up on what git-surface reports:

- For a `ci` record, run `trust-path --ref <branch>` to check whether the changed workflow exposes a secret to untrusted text.
- For a `deps` record, download both versions of the dependency into two existing directories with `release-drift fetch pypi NAME VERSION DIR` (or `npm`), then compare them with `release-drift diff OLD NEW`.
- git-overlap predicts conflicts from the files each branch changes. pr-merge-audit then confirms them by merging the pull requests and running the tests.

Gate an agent:

```sh
glassbox reach --strict --json > reach.json && my-agent
```

The agent starts only when no sensitive location, such as SSH keys or cloud credentials, is readable.

These stacks are shell pipelines: there is no single command or packaged CI action that runs them. The tested stacks, with their real output, are in [git-surface: using it with other tools](https://github.com/jacob-adm/git-surface/blob/main/docs/other-tools.md) and [glassbox: using glassbox with other tools](https://github.com/jacob-adm/glassbox/blob/main/docs/integration.md).

## Mobile: devdrop

<a href="https://github.com/jacob-adm/devdrop/releases/latest"><img src="https://img.shields.io/github/v/release/jacob-adm/devdrop?style=flat-square&color=0F6378&label=release" alt="devdrop latest release"></a>

[devdrop](https://github.com/jacob-adm/devdrop) installs one Android or iOS build on every attached phone, tablet, emulator and simulator at once. It checks each device before installing and skips any device the build cannot run on, with the reason: minimum SDK or iOS version, CPU architecture, simulator build versus device build, and provisioning profile.

- Use it to try a release candidate on every device on the desk with one command.
- Use it to boot a set of emulators and simulators, install, launch and collect launch logs.
- Use it in CI: `--json` and `--junit FILE` report each device's result.

```sh
pip install git+https://github.com/jacob-adm/devdrop
```

## Workstation

[ai-automation-engineer-workstation](https://github.com/jacob-adm/ai-automation-engineer-workstation) is a hardened, reproducible development environment for running autonomous coding agents on Ubuntu and macOS. It provides package bootstrapping, supply-chain quarantine, credential isolation, git worktree isolation for concurrent agents and task-queue supervision.

- Try it without changing your machine: `./tests/sandbox.sh` opens a throwaway Ubuntu 24.04 container.
- Use it every day on Ubuntu 22.04 or 24.04, on a PC, a VM, WSL2 or a cloud server.
- Use it on a headless cloud GPU server with `./install.sh --profile cloud`.

## Status and limits

- **New.** All eight were first published in November 2026 and have been tested on demo and public repositories.
- **trust-path** covers ground that zizmor, poutine, octoscan and Gato-X also cover. Its benchmark shows where it and zizmor report the same findings and where they differ. Some of those differences may belong upstream rather than in a separate tool.
- **release-drift** checks PyPI and npm releases. Its README cites the incidents it is built to catch, but a worked example on one of them is not published yet.
- **git-overlap** reports textual conflicts only. Symbol-level overlap, a merge order and a live view are in Grove, not here. git-overlap and git-surface write tab-separated text, not JSON.
- **bug-age** measures any Rust or Python project after the fact. Nothing in it is specific to AI agents.
- **glassbox** runs on macOS and Linux. It reports what a process can reach and does not enforce anything; pair it with a sandbox for that.
- **devdrop** is tested on emulators, simulators and a physical iPhone, not yet on physical Android devices or iPads. It is not on PyPI.

## Studies

| Study | What it covers |
|:--|:--|
| [Field study](field-study.md) | Method and findings: prior art for every tool, and where the gaps were |
| [Related tools](related-tools.md) | Other projects alongside these, with what each covers and how they were tested |
| [Sysinternals Suite study](https://github.com/jacob-adm/glassbox/blob/main/docs/suite-study.md) | All 79 Suite tools: licence position, which concepts carry over to macOS, Linux and agent tooling |
| [Feasibility and prior art](https://github.com/jacob-adm/glassbox/blob/main/docs/feasibility.md) | Each glassbox candidate checked against existing projects, with a decision to build, skip or adopt |
| [Merging and CI for agent workflows](https://github.com/jacob-adm/git-overlap/blob/main/docs/article.md) | Xuchen Yao's article mapped point by point to git-overlap and pr-merge-audit |
| [How long do bugs live?](https://github.com/jacob-adm/bug-age/blob/main/article/ARTICLE.md) | Bug lifespans in two Rust codebases, every figure checked against the data |
| [trust-path benchmark](https://github.com/jacob-adm/trust-path/blob/main/docs/benchmark.md) | Pinned public repositories, with zizmor's findings shown per workflow file |

Browse by topic:
[supply-chain-security](https://github.com/search?q=user%3Ajacob-adm+topic%3Asupply-chain-security&type=repositories) ·
[security-tools](https://github.com/search?q=user%3Ajacob-adm+topic%3Asecurity-tools&type=repositories) ·
[git-tools](https://github.com/search?q=user%3Ajacob-adm+topic%3Agit-tools&type=repositories) ·
[ai-agents](https://github.com/search?q=user%3Ajacob-adm+topic%3Aai-agents&type=repositories) ·
[mobile](https://github.com/search?q=user%3Ajacob-adm+topic%3Amobile&type=repositories)
