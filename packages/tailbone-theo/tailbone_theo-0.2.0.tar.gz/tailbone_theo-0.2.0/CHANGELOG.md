
# Changelog
All notable changes to tailbone-theo will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.2.0 (2024-06-10)

### Feat

- **license**: declare project license as GNU GPL v3+
- switch from setup.cfg to pyproject.toml + hatchling

## [0.1.6] - 2020-09-25
### Changed
- Add basic LOC SMS support for theo-server machine.
- Use default Catapult web menu.
- Add support for multiple DB engines, for Catapult views.
- Always require mysql connector as dependency (in case mirror DB).
- Add basic feature to mirror POS DB in mysql or postgresql.

## [0.1.5] - 2020-09-22
### Changed
- Add initial fabric bundle for 'theo-server'.
- Define custom app settings.
- Include POS integration web templates, as configured.
- Add basic support for LOC SMS integration.

## [0.1.4] - 2020-09-19
### Changed
- Add the 'app' and 'fabric' extras to setup.py.
- Add some custom email profile settings.

## [0.1.3] - 2020-09-16
### Changed
- Remove hard-coded 'dev' tag when showing theo version.

## [0.1.2] - 2020-09-16
### Changed
- Ugh, require 'bouncer' extra from rattail also.

## [0.1.1] - 2020-09-16
### Changed
- Be sure to install rattail 'db' extra.

## [0.1.0] - 2020-09-16
### Added
- Initial release.
