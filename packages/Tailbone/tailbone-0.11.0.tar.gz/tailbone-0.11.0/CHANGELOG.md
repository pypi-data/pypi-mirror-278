
# Changelog
All notable changes to Tailbone will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.11.0 (2024-06-10)

### Feat

- switch from setup.cfg to pyproject.toml + hatchling

## v0.10.16 (2024-06-10)

### Feat

- standardize how app, package versions are determined

### Fix

- avoid deprecated config methods for app/node title

## v0.10.15 (2024-06-07)

### Fix

- do *not* Use `pkg_resources` to determine package versions

## v0.10.14 (2024-06-06)

### Fix

- use `pkg_resources` to determine package versions

## v0.10.13 (2024-06-06)

### Feat

- remove old/unused scaffold for use with `pcreate`

- add 'fanstatic' support for sake of libcache assets

## v0.10.12 (2024-06-04)

### Feat

- require pyramid 2.x; remove 1.x-style auth policies

- remove version cap for deform

- set explicit referrer when changing app theme

- add `<b-tooltip>` component shim

- include extra styles from `base_meta` template for butterball

- include butterball theme by default for new apps

### Fix

- fix product lookup component, per butterball

## v0.10.11 (2024-06-03)

### Feat

- fix vue3 refresh bugs for various views

- fix grid bug for tempmon appliance view, per oruga

- fix ordering worksheet generator, per butterball

- fix inventory worksheet generator, per butterball

## v0.10.10 (2024-06-03)

### Feat

- more butterball fixes for "view profile" template

### Fix

- fix focus for `<b-select>` shim component

## v0.10.9 (2024-06-03)

### Feat

- let master view control context menu items for page

- fix the "new custorder" page for butterball

### Fix

- fix panel style for PO vs. Invoice breakdown in receiving batch

## v0.10.8 (2024-06-02)

### Feat

- add styling for checked grid rows, per oruga/butterball

- fix product view template for oruga/butterball

- allow per-user custom styles for butterball

- use oruga 0.8.9 by default

## v0.10.7 (2024-06-01)

### Feat

- add setting to allow decimal quantities for receiving

- log error if registry has no rattail config

- add column filters for import/export main grid

- escape all unsafe html for grid data

- add speedbumps for delete, set preferred email/phone in profile view

- fix file upload widget for oruga

### Fix

- fix overflow when instance header title is too long (butterball)

## v0.10.6 (2024-05-29)

### Feat

- add way to flag organic products within lookup dialog

- expose db picker for butterball theme

- expose quickie lookup for butterball theme

- fix basic problems with people profile view, per butterball

## v0.10.5 (2024-05-29)

### Feat

- add `<tailbone-timepicker>` component for oruga

## v0.10.4 (2024-05-12)

### Fix

- fix styles for grid actions, per butterball

## v0.10.3 (2024-05-10)

### Fix

- fix bug with grid date filters

## v0.10.2 (2024-05-08)

### Feat

- remove version restriction for pyramid_beaker dependency

- rename some attrs etc. for buefy components used with oruga

- fix "tools" helper for receiving batch view, per oruga

- more data type fixes for ``<tailbone-datepicker>``

- fix "view receiving row" page, per oruga

- tweak styles for grid action links, per butterball

### Fix

- fix employees grid when viewing department (per oruga)

- fix login "enter" key behavior, per oruga

- fix button text for autocomplete

## v0.10.1 (2024-04-28)

### Feat

- sort list of available themes

- update various icon names for oruga compatibility

- show "View This" button when cloning a record

- stop including 'falafel' as available theme

### Fix

- fix vertical alignment in main menu bar, for butterball

- fix upgrade execution logic/UI per oruga

## v0.10.0 (2024-04-28)

This version bump is to reflect adding support for Vue 3 + Oruga via
the 'butterball' theme.  There is likely more work to be done for that
yet, but it mostly works at this point.

### Feat

- misc. template and view logic tweaks (applicable to all themes) for
  better patterns, consistency etc.

- add initial support for Vue 3 + Oruga, via "butterball" theme


## Older Releases

Please see `docs/OLDCHANGES.rst` for older release notes.
