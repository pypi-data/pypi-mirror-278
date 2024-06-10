# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [0-based versioning](https://0ver.org/).

## [Unreleased]

## v0.16.4 (2024-06-09)

- Add `deps` session to `nox`
- Bump deps
- Remove `tox` dep
- Update `nox` session output in contributing doc

## v0.16.3 (2024-06-02)

- Bump deps
- Fix incorrect `nox` session description
- Remove unused `doc` section from `Pipfile`

## v0.16.2 (2024-05-26)

- Add `cov` (coverage) session to `nox`
- Bump deps and `pre-commit` hooks
- Switch to `nox` from `tox`

## v0.16.1 (2024-05-19)

- Add `doc` session to `nox`
- Bump deps
- Move doc generation related deps to `dev` group
- Remove subheaders from changelog

## v0.16.0 (2024-05-12)

- Add `rotate` subcommand to rotate an image
- Add initial `lint` session for `nox`
- Bump deps, `pre-commit` hooks, and Python versions in `pyenv`

## v0.15.0 (2024-05-05)

- Add `-v` or `--verbose` flag to toggle the debug logs of PIL
- Bump deps and `pre-commit` hooks
- Remove empty lines in help message
- Resize image to the right aspect ratio based on image's dimension
- Resize watermark font based on the image's dimension
- Show absolute image path in logs

## v0.14.0 (2024-04-28)

- Add `animate` subcommand to create animated `gif` image
- Bump deps and `pre-commit` hooks

## v0.13.0 (2024-04-21)

- Bump deps
- Support processing multiple images at once
- Update missing help message in readme

## v0.12.0 (2024-04-14)

- Add `-pd` or `--padding` option to set the padding of watermark text block
- Bump deps, `pre-commit` hooks, and Python versions for `pyenv`
- Fix `auto` subcommand missing `padding` field
- Fix missing closing parenthesis in help message
- Update missing subcommand help message in README

## v0.11.0 (2024-04-07)

- Add `montage` subcommand to join multiple images
- Bump deps
- Update missing subcommand help message in README

## v0.10.0 (2024-03-31)

- Add `info` subcommand to show EXIF data from image
- Bump deps
- Fix incorrect action in log when running `auto` subcommand
- Ignore `pylint` W0212 rule
- Update help message in README
- Update incorrect comment for `save_image` helper function

## v0.9.1 (2024-03-24)

- Fix newline in `sys.version` output in Python 3.8
- Implement open image using the default program
- Refactor all subcommand to use `save_image` global helper function

## v0.9.0 (2024-03-17)

- Add `-op` or `--open` flag to open the image using default program
- Bump deps and `pre-commit` hook

## v0.8.0 (2024-03-10)

- Add `auto` subcommand to auto adjust (resize, contrast, sharpen, and watermark) of an image
- Add `contrast` subcommand to adjust contrast of an image
- Bump `pre-commit` hook
- Log using the subcommand name instead of generic name

## v0.7.0 (2024-03-03)

- Add `sharpen` subcommand to sharpen image
- Set sharpen parameters through `-p` or `--percent` option
- Set sharpen parameters through `-r` or `--radius` option
- Set sharpen parameters through `-t` or `--threshold` option

## v0.6.1 (2024-02-18)

- Allow setting of different border width through `-wt`, `-wr`, `-wb`, and `wl`
  option
- Remove extra lines in help message in README.md

## v0.6.0 (2024-02-18)

- Add `resize` subcommand to resize image

## v0.5.0 (2024-02-11)

- Add `-od` or `--output-dir` global option to set default output directory
- Add missing types in doc
- Log when saving image

## v0.4.0 (2024-02-04)

- Add `-o` or `--overwrite` global flag to overwrite modified image

## v0.3.1 (2024-01-28)

- Add `-w` or `--width` option to `fotolab border` subcommand
- Add `-c` or `--color` option to `fotolab border` subcommand
- Fix border not added to image

## v0.3.0 (2024-01-21)

- Add `fotolab border` subcommand to add border for an image
- Fix incorrect subcommand wording
- Ignore `__repr__` in code coverage
- Ignore duplicate code linting rule
- Test `quiet` flag

## v0.2.0 (2024-01-14)

- Add `fotolab env` subcommand for debugging and bug reporting purpose
- Fix incorrect metavar for `--font-color`

## v0.1.1 (2024-01-07)

- Bump project and `pre-commit` hooks deps
- Generate project documentation using `sphinx`

## v0.1.0 (2024-01-01)

- Initial public release
