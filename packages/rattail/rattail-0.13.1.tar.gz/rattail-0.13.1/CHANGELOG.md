
# Changelog
All notable changes to rattail will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.13.1 (2024-06-10)

### Fix

- move canonical app version to pyproject.toml

## v0.13.0 (2024-06-10)

### Feat

- switch from setup.cfg to pyproject.toml / hatchling

## v0.12.9 (2024-06-10)

### Feat

- add config snippet for new projects, to define static libcache
- define the `app_package` setting for new projects
- add `get_pkg_version()` convenience function

## v0.12.8 (2024-06-06)

### Feat

- project generator should make typer commands, not old-style
- remove old/unused project scaffold template
- add snippet for fanstatic/libcache when generating web project

### Fix

- fix missing import for `rattail make-config` command
- define the `-n` command flag as alias for `--no-init`

## v0.12.7 (2024-06-02)

### Fix

- fix datasync command args, per typer

## v0.12.6 (2024-06-01)

### Feat

- add setting to allow decimal quantities for ordering/receiving

### Fix

- fix `rattail datasync remove-settings` command line, per typer
- fix `--progress-socket` arg handling for typer commands

## v0.12.5 (2024-05-31)

### Fix

- fix args for `rattail populate-batch` command, per typer

## v0.12.4 (2024-05-31)

### Fix

- fix params for generic "run purge" command logic, per typer

## v0.12.3 (2024-05-31)

### Fix

- fix args for `rattail purge-batches` command, per typer

## v0.12.2 (2024-05-30)

### Feat

- log the `pflogsumm` command before running it

### Fix

- fix some commands/arguments, per typer

## v0.12.1 (2024-05-29)

### Feat

- include organic flag when normalizing product

## v0.12.0 (2024-05-29)

This release begins the migration to use `typer` for all commands,
instead of the "traditional" (now WuttJamaican-based) commands.

### Feat

- add `get_runas_user()` method for AppHandler
- move rich and prompt_toolkit things to separate module
- move `finalize_session()` function to `db.util` module
- move "install" command logic to separate handler/module
- move "import command runner" logic to separate handler
- add basic support for `typer` command system
- migrate all commands to use typer
- add command logic functions for running reports, purging things

### Fix

- fix subcommand runas user when caller provides username


## Older Releases

Please see `docs/OLDCHANGES.rst` for older release notes.
