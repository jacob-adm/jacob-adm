# Replaying the 2026 supply-chain attacks

The suite was tested against five real supply-chain attacks from 2026, seven releases in all, to see whether each tool
raises a warning on the actual attack and not only on examples written for its tests. This page
lists what was run, what each tool reported, what it missed, and what was changed as a result.

## Method

Replaying an attack means showing a tool what the attack left behind. Nothing was installed,
built or run.

- **The TanStack worm.** The attack entered through TanStack/router's GitHub Actions workflows.
  trust-path read those workflow files from the repository's public git history at `b1c061a`, the
  last commit on `main` before the attack. That commit holds no attack code.
- **The six malicious package releases.** PyPI and npm removed these releases. Copies came from
  [DataDog's malicious software packages dataset](https://github.com/DataDog/malicious-software-packages-dataset),
  a public research dataset that stores each package in a password-protected zip. release-drift
  compared each one with the clean release before it, taken from PyPI or npm.
- **Isolation.** The zips were opened only inside a container with no network, a read-only file
  system, no Linux capabilities and an unprivileged user, with the samples mounted read-only and
  unpacked into memory that cannot execute files. The samples were deleted after the run. Only
  their SHA-256 hashes and the tools' output were kept.

## Results

| Attack | Source | Tool | Before | After |
| --- | --- | --- | --- | --- |
| TanStack worm (May) | [postmortem](https://tanstack.com/blog/npm-supply-chain-compromise-postmortem) | trust-path | No record | `cache` path from `bundle-size.yml` to `release.yml`, which holds `id-token: write` (0.6.0) |
| LiteLLM 1.82.7 | [GHSA-5mg7-485q-xm76](https://github.com/advisories/GHSA-5mg7-485q-xm76) | release-drift | `blob added` in `litellm/proxy/proxy_server.py` | Same |
| LiteLLM 1.82.8 | [GHSA-5mg7-485q-xm76](https://github.com/advisories/GHSA-5mg7-485q-xm76) | release-drift | `pth added litellm_init.pth` | Same |
| tensorlake 0.5.144 | [GHSA-8g63-53c9-65j2](https://github.com/tensorlakeai/tensorlake/security/advisories/GHSA-8g63-53c9-65j2) | release-drift | `blob added` (14) and `url-host added` (4) in `lib/Math_Symbol.js` | Same |
| Cline 2.3.0 | [GHSA-9ppg-jx86-fqw7](https://github.com/cline/cline/security/advisories/GHSA-9ppg-jx86-fqw7) | release-drift | `npm-script added postinstall=npm install -g openclaw@latest` | Same |
| plain-crypto-js 4.2.1 | [axios postmortem](https://github.com/axios/axios/issues/10636) | release-drift | `npm-script added postinstall=node setup.js` | Same |
| axios 1.14.1 | [axios postmortem](https://github.com/axios/axios/issues/10636) | release-drift | No record | `dependency added dependencies plain-crypto-js` (0.2.0) |

"Before" is trust-path 0.5.0 and release-drift 0.1.2, the versions the replays ran on. "After" is
the first release with the fix.

## What was missed, and what changed

- **The TanStack worm.** The attacker's code ran in a `pull_request_target` job with read-only
  permissions and no secrets, so trust-path found no path in that job. The credential was reached
  through the GitHub Actions cache: the job's shared setup action saved a cache that the release
  workflow restored. trust-path 0.6.0 follows a job that runs pull request code through the cache
  to the default-branch jobs that use the same cache step
  ([The Actions cache](https://github.com/jacob-adm/trust-path/blob/main/docs/model.md#the-actions-cache)).
- **axios 1.14.1.** The release changed only `package.json`, to add the dependency
  `plain-crypto-js`, whose install script carried the payload. release-drift 0.2.0 reports the
  dependencies a release adds.
- **An unpacked directory one level too high.** The first run passed each npm sample as the
  directory above `package/`. That is not the documented form, and release-drift silently
  compared it one level too high and missed the install scripts. Repacked as `.tgz`, both were
  reported. release-drift 0.2.0 reads that directory from inside `package/`.

## Checks that keep passing

- trust-path's benchmark runs TanStack/router at `b1c061a`
  ([benchmark](https://github.com/jacob-adm/trust-path/blob/main/docs/benchmark.md)).
- release-drift's `tests/test_replays.py` rebuilds each package attack from harmless stand-ins
  with the same shape and asserts the record above.

## Limits

- **A record is a warning, not a verdict.** How often the same kinds of record appear for ordinary
  releases has not been measured yet.
- **axios after the fix** was checked against the clean 1.14.0 `package.json` with the added
  dependency, the change the attack made, not against the deleted sample.
- **tensorlake.** The advisory says the payload ran through a `preinstall` hook. The sample's root
  `package.json` held no install script, and release-drift reported the encoded code and new hosts
  instead. The difference is not resolved.
- **Not replayed.** axios 0.30.4, the second malicious axios release, is not in the dataset.
