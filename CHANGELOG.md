# Changelog

## [1.2.1](https://github.com/nhm7/homebrew-aged-upgrade/compare/v1.2.0...v1.2.1) (2026-05-16)


### Bug Fixes

* enable line buffering on stdout to preserve log output order ([#21](https://github.com/nhm7/homebrew-aged-upgrade/issues/21)) ([f9962f5](https://github.com/nhm7/homebrew-aged-upgrade/commit/f9962f5dfef4850a6236d8ceb2ec1317bed975fa))

## [1.2.0](https://github.com/nhm7/homebrew-aged-upgrade/compare/v1.1.0...v1.2.0) (2026-05-16)


### Features

* interactive autoupdate conflict prompt, formula caveats, and resilience fixes ([#19](https://github.com/nhm7/homebrew-aged-upgrade/issues/19)) ([8936482](https://github.com/nhm7/homebrew-aged-upgrade/commit/8936482edf0df09dd287f20cfd431e8a716095cf))

## [1.1.0](https://github.com/nhm7/homebrew-aged-upgrade/compare/v1.0.1...v1.1.0) (2026-05-16)


### Features

* rename formula to aged-upgrade, fix install UX and correctness issues ([#17](https://github.com/nhm7/homebrew-aged-upgrade/issues/17)) ([ed94cb5](https://github.com/nhm7/homebrew-aged-upgrade/commit/ed94cb546a83f2ea664ade5e69e2b5b0e4e401ac))


### Bug Fixes

* pass --repo to gh pr merge so it works without a local checkout ([#15](https://github.com/nhm7/homebrew-aged-upgrade/issues/15)) ([34d4086](https://github.com/nhm7/homebrew-aged-upgrade/commit/34d4086fca75c4cae4f6ab0f6c51163be5cd941d))

## [1.0.1](https://github.com/nhm7/homebrew-aged-upgrade/compare/v1.0.0...v1.0.1) (2026-05-16)


### Bug Fixes

* correct README install commands and enable auto-merge on release PRs ([#14](https://github.com/nhm7/homebrew-aged-upgrade/issues/14)) ([39cd008](https://github.com/nhm7/homebrew-aged-upgrade/commit/39cd0086e7f74976091f9338ef8b65819027dcc4))
* formula URLs, python dep, tap command, brew outdated stderr ([#11](https://github.com/nhm7/homebrew-aged-upgrade/issues/11)) ([f7005c6](https://github.com/nhm7/homebrew-aged-upgrade/commit/f7005c626e4aa83983bb1f5fe2239f7e28ad346b))
* update URLs for repo rename and consolidate CI jobs ([#12](https://github.com/nhm7/homebrew-aged-upgrade/issues/12)) ([51904d0](https://github.com/nhm7/homebrew-aged-upgrade/commit/51904d06f7bf209dad919d779d7df9b8b8eb0e11))

## [1.0.0](https://github.com/nhm7/brew-aged-upgrade/compare/v0.1.0...v1.0.0) (2026-05-16)


### ⚠ BREAKING CHANGES

* stable 1.0.0 release — state-file delay tracking and launchd CLI ([#9](https://github.com/nhm7/brew-aged-upgrade/issues/9))

### Features

* stable 1.0.0 release — state-file delay tracking and launchd CLI ([#9](https://github.com/nhm7/brew-aged-upgrade/issues/9)) ([8cfa26d](https://github.com/nhm7/brew-aged-upgrade/commit/8cfa26d58a48cfea425aa5f5b8b4c09ed70e1ed0))
