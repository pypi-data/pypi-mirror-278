
# Changelog
All notable changes to rattail-nationbuilder will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.3.0 (2024-06-10)

### Feat

- switch from setup.cfg to pyproject.toml + hatchling

## [0.2.0] - 2024-05-29
### Changed
- Migrate all commands to use `typer`.

## [0.1.14] - 2023-12-01
### Changed
- Update subcommand entry point group names, per wuttjamaican.

## [0.1.13] - 2023-09-16
### Changed
- Limit page size to 100, for fetching Person records from NB API.

## [0.1.12] - 2023-09-15
### Changed
- Add rattail provider for NationBuilder integration.

## [0.1.11] - 2023-09-13
### Changed
- Fix schema inconsistencies.

## [0.1.10] - 2023-09-12
### Changed
- Assume null if NB person tags are empty.

## [0.1.9] - 2023-09-12
### Changed
- Add cache table, importer for NationBuilder donations.

## [0.1.8] - 2023-09-12
### Changed
- Fix manifest again..omg.

## [0.1.7] - 2023-09-12
### Changed
- Fix manifest...omg.

## [0.1.6] - 2023-09-12
### Changed
- Add alembic scripts to manifest.

## [0.1.5] - 2023-09-12
### Changed
- Add cache table, importer for NationBuilder People.

## [0.1.4] - 2023-09-07
### Changed
- Add web API methods for fetching donations from NationBuilder.

## [0.1.3] - 2023-05-25
### Changed
- Should actually use requests session for web api.

## [0.1.2] - 2023-05-17
### Changed
- Replace `setup.py` contents with `setup.cfg`.

## [0.1.1] - 2023-05-11
### Changed
- Add `max_retries` config for NationBuilder API.
- Add `max_pages` arg for API `get_people_with_tag()` method.

## [0.1.0] - 2023-05-08
### Added
- Initial version, basic API client only.
