
# Changelog
All notable changes to rattail-quickbooks will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.2.0 (2024-06-11)

### Feat

- **license**: declare project license as GNU GPL v3+
- switch from setup.cfg to pyproject.toml + hatchling

## [0.1.4] - 2024-06-03
### Changed
- Add schema for mapping QB bank accounts to vendor+store combo.

## [0.1.3] - 2023-06-01
### Changed
- Replace `setup.py` contents with `setup.cfg`.

## [0.1.2] - 2023-05-11
### Changed
- Avoid deprecated import for `OrderedDict`.

## [0.1.1] - 2022-12-21
### Changed
- Include alembic version scripts in built dist.

## [0.1.0] - 2022-12-21
### Added
- Initial version, mostly for sake of "export invoices to Quickbooks" feature.
