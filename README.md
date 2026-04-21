# Soror Squad

`soror-squad` reads a roster **CSV** (for example, survey export) and prints **per-squad contact reports**: each squad lists members with **name**, **phone** (US numbers formatted as `(NPA) NXX-XXXX` when possible), and **email**. Members appear **sorted by name** within each squad; squads are ordered alphabetically.

The input file is expected to use the column headers from the original form (name, cell phone, email) and to put **squad membership in the last column**. That last column may contain **one or more squad names separated by commas**; a person listed in multiple squads appears under each squad.

## Usage

### Local

```bash
python main.py path/to/roster.csv
```

**Aligned table** (default): fixed-width columns under each `Squad:` heading.

**CSV-style blocks** (optional): each squad has a title line, then `Name,Phone,Email` rows; squads are separated by a blank line.

```bash
python main.py path/to/roster.csv --csv
```

### Docker

Mount your input file into the container at `/work/input.csv` and pass `input.csv` as the argument (the process working directory is `/work`).

```bash
docker run -v ./input.csv:/work/input.csv ghcr.io/managedkaos/soror-squad:main input.csv
```

Use an absolute path on the host if the file is not in the current directory, for example:

```bash
docker run -v "$PWD/my-roster.csv:/work/input.csv" ghcr.io/managedkaos/soror-squad:main input.csv
```

CSV-style output:

```bash
docker run -v ./input.csv:/work/input.csv ghcr.io/managedkaos/soror-squad:main input.csv --csv
```

## Development setup

1. Install development dependencies:

   ```bash
   make development-requirements
   ```

2. Install pre-commit hooks:

   ```bash
   make pre-commit-install
   ```

3. Run pre-commit on all files (optional):

   ```bash
   make pre-commit-run
   ```

### Pre-commit hooks

Hooks include Black, isort, flake8, bandit, detect-secrets, and common hygiene checks (merge conflicts, YAML/JSON, large files, whitespace, end-of-file).

### Make targets

- `make development-requirements` — install development dependencies
- `make pre-commit-install` — install pre-commit hooks
- `make pre-commit-run` — run pre-commit on all files
- `make pre-commit-clean` — remove pre-commit hooks
- `make lint` — run linting tools manually
- `make fmt` — format with black and isort
