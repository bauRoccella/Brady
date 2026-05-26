# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This project runs on a remote Virtual Machine. Some dependencies (notably `MODEL` and VM-resident helper functions like `LOAD_EXCEL_DATA`, `COMMIT_DATA`, `EXIT`, etc.) are **not declared in these files** — they are injected at runtime by the VM environment. Do not try to resolve or install them locally.

There is no build system, test suite, or package manager here. The scripts are executed directly by the VM's Python interpreter.

## File Overview

Two files, tightly coupled:

- **`AAA_BTSObject.py`** (~10,800 lines): Generic SDK/library for managing cellular network elements (BTS — Base Transceiver Station). Acts as middleware between the VM-resident `MODEL` library and deployment scripts. Defines `BTSObject`, `BaseObject`, `BitObject`, and ~80 standalone wrapper functions.

- **`Argentina_TA_5G_V2.0.py`** (~1,600 lines): Country-specific deployment automation script. Imports everything from `AAA_BTSObject` via `from CommonClass.AAA_BTSObject import *`, then orchestrates 5G network expansion for Argentina (Telefonica MNC=07, Personal MNC=34) across two regions: AMBA and SUR.

## Architecture

```
Argentina_TA_5G_V2.0.py   ← specific deployment script
    ↓  imports *
AAA_BTSObject.py           ← generic telecom SDK
    ↓  delegates to
MODEL (VM runtime)         ← telecom data model (not in repo)
    ↓  persists via
COMMIT_DATA() / save_moc() ← network config database (VM)
```

### Data flow in Argentina script

1. Load Excel config (`Argentina_TA_5G*` workbook) via `bts_obj.get_data_from_excel()`
2. Parse site metadata: region (`AMBA` / `SUR`), operator, BBU type
3. Branch on region → call `nr_tx_expansion()` to create IP/VLAN/SCTP config
4. Call `create_gnodeb_op()` → gNodeB radio operator setup
5. Call `create_5g_hw()` → physical layer (RRU chains, sectors)
6. Per-cell loop: `nr_cell_expansion()` → NRCell + NRDUCell creation
7. Configure neighboring: NrExternalCell, NrNRelationship (LTE-NR NSA), NrNFreq
8. Configure Carrier Aggregation and SCG frequencies
9. Persist everything via `bts_obj.save_moc()`

### Key patterns in AAA_BTSObject.py

- `@API_RECORD` decorator marks all public BTSObject methods
- `MODEL.<MocName>` dynamic attribute access is the entry point for all network element types
- `MOD`, `WHERE`, `BIT` are operator-like objects (operator overloading) used to build update expressions: `field == value` chains passed as `*updater_list`
- `APPEND_MODE` / `OVERWRITE_MODE` control whether existing data is merged or replaced
- The cache key format is `"Inner Summary=filename.controller"` — fragile string concatenation

## Known Disasters (Refactoring Targets)

### AAA_BTSObject.py

1. **Exact code duplicate** in `convert_Str2Int_Ipv6()` (~lines 87–213): two 60-line blocks of identical logic for IPv6 conversion
2. **Bare `except: pass`** throughout — silently swallows exceptions, destroys debuggability
3. **No type hints anywhere**; parameters are documented only in inline comments, some in Chinese
4. **Magic numbers and hardcoded strings** pervasive: MOC names, node types, exclude lists — no constants file
5. **`BaseObject` violates SRP**: loads data, saves data, queries, converts, manages IP — should be split
6. **`BTSObject`** accumulates all technology-specific methods (GSM/UMTS/LTE/5G) in one class
7. **Performance**: `get_free_id_list()` worst-case iterates 65,535 times; `del_Duplicate()` creates a new list per comparison
8. **Typo**: `targtget_data` (should be `target_data`) used in several methods

### Argentina_TA_5G_V2.0.py

1. **`nr_tx_expansion()`** (~lines 94–343): entire AMBA block (~130 lines) is near-duplicated for SUR; only differences are variable name prefixes (`tp_` vs `mvs_`) and hardcoded IPs/VLANs — must be extracted to a parameterized function with a region config dict
2. **Operator-specific logic** (Telefonica vs Personal) is scattered across multiple functions instead of centralized
3. **Hardcoded frequencies**: ARFCN values like `629280`, `637440`, SSB offsets embedded directly
4. **Two parallel cell lists** (`tp_newnr_celllist`, `mvs_newnr_celllist`) processed in nearly identical loops — should be unified
5. **Excel column names assumed** (`"*gNodeB ID"`, `"Region"`, `"Escenario con IPs correctas pero sin 5G"`) — no schema validation; fails silently or at runtime if columns are missing
6. **No bounds checking** on `get_para_list_from_moc(...)[2]` style index access (line ~861)
7. **Global state**: `bts_obj`, `siteinfo`, `region`, `nename` are de-facto globals with no dependency injection

## Refactoring Priority

| Priority | Target |
|---|---|
| P0 | Remove IPv6 duplicate in `convert_Str2Int_Ipv6()` |
| P0 | Replace bare `except` with specific exception types |
| P0 | Add bounds checking before index access on list returns |
| P1 | Extract AMBA/SUR config into a region config dict; parameterize `nr_tx_expansion()` |
| P1 | Centralize MCC/MNC/VLAN/frequency constants (YAML or module-level dict) |
| P1 | Unify `tp_newnr_celllist` / `mvs_newnr_celllist` parallel loops |
| P2 | Add type hints to all new/touched functions |
| P2 | Replace magic-number frequencies with named constants |
| P3 | Split `AAA_BTSObject.py` into focused modules (data_io, ip_utils, bts_object, etc.) |
