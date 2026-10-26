# Casa della Salute — Management System

A small web application built with **Dash** (Plotly) and **Pony ORM** on top of **SQLite**, developed as a university project for the *Software Engineering* course. It implements a booking and records-management system for a primary-care clinic ("Casa della Salute") with doctors (*medici*), nurses (*infermieri*), patients (*pazienti*), and front-desk staff (*segreteria*).

> ⚠️ **Disclaimer:** This was written as a course assignment, not a production system. It was not optimized or refactored afterwards — expect duplicated code, some dead/commented-out code, inline business logic mixed with UI callbacks, and no automated tests. See [Known issues / things to review](#known-issues--things-to-review) before reusing or extending it.

## What the system does

The specification (`Esercizio2-2024-CasaSalute.pdf`, included in this archive, in Italian) describes a clinic with:

- 3 outpatient rooms (*ambulatori*) for adult visits and 1 for pediatric visits
- a dedicated procedure room for blood draws (*prelievi*) and one for dressings/medications (*medicazioni*), staffed by nurses
- several GPs ("doctors"), each with their own patients, who can stand in for one another when unavailable
- a shared front-desk/secretariat office

Depending on who logs in, the application exposes different features:

| Role | What they can do |
|---|---|
| **Front desk (segreteria)** | Register/remove doctors, nurses and patients; manage visit and procedure bookings; view nurses' room schedule |
| **Doctor (medico)** | Manage their visits (record outcome, urgency, regime, etc.); view past visits |
| **Nurse (infermiere)** | Manage procedures (blood draws/dressings); view past procedures and their own room schedule |
| **Patient (paziente)**, or an adult responsible for a patient under 14 | Book a visit or a procedure; view/print past visit and procedure outcomes |

The data model (patients, doctors, nurses, visits, procedures, rooms, substitutions, nurse schedules, etc.) is defined in `tabelledb.py` and mirrors the entities described in the assignment PDF.

## Files in this project

| File | Description |
|---|---|
| `login.py` | **Main entry point.** Builds the Pony ORM database connection/schema, creates the Dash app, defines every page layout (login screen, navbars per role, booking forms, management forms...) and all `@app.callback` functions that wire the UI together. Run this file to start the app. |
| `query.py` | All the database logic: authentication, inserting/removing doctors/nurses/patients, computing available visit/procedure slots, building the nurse room schedule, confirming bookings, recording outcomes, etc. Imported by `login.py`. |
| `tabelledb.py` | Defines the Pony ORM entities (`Utente`, `Medico`, `Infermiere`, `Paziente`, `Ambulatorio`, `Sala`, `Visita`, `Prestazione`, `Data`, `Controllo`, `Cura`, `Servizio`, `Sostituzione`) and the relationships between them, i.e. the database schema. Imported by `login.py`. |
| `casaSalute.db` | *(Not present in this repository.)* It's just the SQLite database file that gets generated locally the first time you run `login.py`. See the note below. |
| `Esercizio2-2024-CasaSalute.pdf` | The original assignment text (in Italian) describing the requirements this project implements. |

## ⚠️ About the database

You will **not** find a `casaSalute.db` file in this repository. `login.py` creates it from scratch, locally, the first time you run it.

In detail, `login.py` connects to `casaSalute.db` with `create_db=True` and calls `db.generate_mapping(create_tables=True)` on every run, so:

- if `casaSalute.db` doesn't exist in the folder, it gets created automatically the first time you run `login.py`;
- right after creation (empty database), `login.py` detects this via `check_riempimento` and seeds it with the default secretary account, the available dates (today up to 31 Dec 2026), rooms, outpatient clinics, and empty visit/procedure time slots;
- on subsequent runs, if `casaSalute.db` already exists and is populated, it's reused as-is (so your data persists between runs).

In short: **just run `login.py`** — make sure it sits in the same folder as `tabelledb.py` and `query.py`, and the database will be set up automatically on first launch.

## Requirements

- **Python**: the project was developed and byte-compiled against Python 3.8 and 3.10, so one of those versions is the safest choice. It may not run as-is on more recent Dash/Python combinations without adapting the imports (see below).
- Install the Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

`requirements.txt` pins older versions of the Dash sub-packages (`dash-core-components`, `dash-html-components`, `dash-table`) on purpose, because `login.py` imports them as separate packages (`import dash_core_components as dcc`, `import dash_html_components as html`, `import dash_table`). Since Dash 2.0, these were merged into the main `dash` package (`dash.dcc`, `dash.html`, `dash.dash_table`). If you'd rather use a modern Dash version, update the imports in `login.py` accordingly instead of installing the legacy packages — see [Known issues](#known-issues--things-to-review).

## How to run it

1. Make sure `login.py`, `query.py` and `tabelledb.py` are all in the same directory (no `.db` file needed — it will be generated automatically).
2. Install the dependencies: `pip install -r requirements.txt`
3. Start the app:

```bash
python login.py
```

4. Dash will start a local development server (by default at `http://127.0.0.1:8050/`). Open that address in your browser.

## Quick-start guide / how to use the app

### 1. First login — front desk (segreteria)

The front-desk account is seeded automatically the first time the app initializes the database, so you can log in immediately with:

- **Username:** `admin`
- **Password:** `pass0`

This is the only account that exists out of the box — everyone else (doctors, nurses, patients) has to be registered by the front desk first.

### 2. Registering staff and patients (as segreteria)

Once logged in as `admin`, use the navbar to reach:

- **Gestione medici** (Manage doctors) — add a doctor with their fiscal code, first/last name and specialty, or remove an existing one.
- **Gestione infermieri** (Manage nurses) — add a nurse with their fiscal code and first/last name, or remove an existing one.
- **Gestione pazienti** (Manage patients) — register a patient (first/last name, date/place of birth, email, and the GP they're affiliated with). If the patient is under 14, you register their adult responsible instead of an email of their own.

When a doctor, nurse or patient is created, the system **auto-generates their login credentials** rather than asking you to set them:

- **Username:** `name.surname` in lowercase (e.g. a patient named "Maria Rossi" gets `maria.rossi`)
- **Password:** an auto-incrementing string in the form `passN` (e.g. `pass1`, `pass2`, ...)

The confirmation message shown after registration includes the generated username, so make sure to note it down (and communicate it) — there's no "forgot password" flow.

### 3. Booking and managing visits/procedures (as segreteria)

From the same navbar, the front desk can also use **Gestione visita** / **Gestione prestazione** to book or update visits and procedures on behalf of patients, and **Gestione pazienti/medici/infermieri** to keep the roster up to date.

### 4. Logging in as a doctor or nurse

Once registered by the front desk, doctors and nurses log in with the generated `name.surname` / `passN` credentials from the same login screen. They'll see a role-specific navbar:

- **Doctors:** manage their visits (record outcome/urgency/regime) and view past visits.
- **Nurses:** manage procedures (blood draws/dressings), view past procedures, and view their own room-assignment schedule.

### 5. Logging in as a patient

Patients (or the adult responsible for a patient under 14) log in with their own `name.surname` / `passN` credentials and can:

- book a visit with their GP or, if unavailable, with a substitute doctor;
- book a procedure (blood draw or dressing);
- view and "print" (view on screen) the outcome of past visits and procedures.

> Note: the original spec mentions sending the patient a confirmation/notification e-mail after a booking and after a visit outcome is recorded. **This part is not actually implemented** in the code — only the patient's email address is stored in the database, no e-mail is actually sent. This was a deliberate scope choice: since this is a university coursework exercise, the e-mail addresses entered aren't real, so actual e-mail delivery was out of scope and never implemented. See below.

## Known issues / things to review

This project was written under coursework deadlines and was **not cleaned up afterwards**. Before reusing it, you may want to review/fix:

- **Legacy Dash packages**: `dash_core_components`, `dash_html_components`, and `dash_table` are deprecated standalone packages, merged into `dash` itself since Dash 2.0. The pinned old versions in `requirements.txt` work, but migrating `login.py` to `dash.dcc` / `dash.html` / `dash.dash_table` and a current Dash release would be more maintainable.
- **No e-mail sending**: the assignment asks for confirmation/notification e-mails to patients, but no mail-sending code (e.g. `smtplib`) is present — only the email field is stored. This was intentional: as a coursework exercise, the e-mail addresses used aren't real ones, so actually sending mail was never implemented. If this project is reused for something real, actual e-mail delivery (e.g. via `smtplib` or a transactional e-mail service) would need to be added.
- **Mixed responsibilities**: `login.py` mixes Dash layout definitions, callback wiring, and (via `query.py`) database access, all in very large files (2000+ lines for `login.py`, ~1300 for `query.py`). A cleaner version would separate layout, callbacks, and data-access layers into modules.
- **Plaintext passwords**: credentials (`Utente.password`) are stored and compared in plaintext in the SQLite database. There's no hashing, salting, or session/token-based auth — not suitable for anything beyond a local demo.
- **Leftover/commented-out code**: some functions (e.g. `insert_paz` in `query.py`) contain dead/commented branches and somewhat convoluted logic for generating sequential usernames/passwords/IDs, which could be simplified.
- **No automated tests**: there is no test suite; all functionality was verified manually during development.
- **Hardcoded date range**: `fill_date` seeds available dates from "today" through **31 December 2026** — after that date, no more bookable slots will exist until the logic/data is updated.

## Skills gained

This project was developed together with a fellow student as a two-person team for the *Ingegneria del Software* course. Working on it involved:

- **Requirements analysis**: translating a natural-language specification (the assignment PDF) into a concrete data model and a set of user roles/permissions.
- **Relational database design**: modeling entities, relationships, and multi-column primary/foreign keys (e.g. composite keys for `Visita`, `Prestazione`, `Controllo`, `Cura`, `Servizio`) using an ORM (Pony ORM) on top of SQLite.
- **Full-stack web development in Python**: building a multi-page, role-based web application with Dash, including dynamic layouts, forms, dropdowns, tables, and interactive callbacks.
- **Authentication & role-based access control**: implementing a login flow that routes different user types (front desk, doctor, nurse, patient/guardian) to different views and permissions.
- **Working with dates/times and business rules**: generating and validating available booking slots, handling minors vs. adult patients, and doctor substitutions.
- **Team collaboration on a shared codebase**: coordinating work between two developers on the same project (shared data model, shared conventions, splitting features) under a course deadline.
- **Scoping and prioritization**: deciding what was in scope for a graded exercise (e.g. leaving out real e-mail delivery, since the project doesn't use real addresses) versus what the specification literally asked for.

## Context

Educational project for the *Ingegneria del Software* course (academic year 2023–2024), developed in pairs. Provided as-is, for reference/review purposes.
