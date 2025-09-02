#!/usr/bin/env bash
set -Eeuo pipefail

# -----------------------------
# HW1 one-click runner
# - Creates venv and installs deps
# - Ensures .env exists (prompts if needed)
# - Starts MySQL service (macOS/Linux best-effort)
# - Executes main.py which runs ./sql/*.sql
# -----------------------------

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --------------- helpers ----------------
log()   { printf "\n\033[1;34m[INFO]\033[0m %s\n" "$*"; }
warn()  { printf "\n\033[1;33m[WARN]\033[0m %s\n" "$*"; }
err()   { printf "\n\033[1;31m[ERR ]\033[0m %s\n" "$*" >&2; }
die()   { err "$*"; exit 1; }

need() {
  command -v "$1" >/dev/null 2>&1 || die "Missing '$1'. Please install it and re-run."
}

# --------------- sanity checks ----------
[ -f "${PROJECT_ROOT}/main.py" ] || die "main.py not found. Run this from the project root (HW1/)."
[ -d "${PROJECT_ROOT}/sql" ]     || die "sql/ folder not found."

# --------------- python env -------------
PYTHON_BIN="${PYTHON_BIN:-python3}"
need "$PYTHON_BIN"

log "Creating virtual environment (.venv) if missing..."
if [ ! -d "${PROJECT_ROOT}/.venv" ]; then
  "$PYTHON_BIN" -m venv "${PROJECT_ROOT}/.venv"
fi

PY="${PROJECT_ROOT}/.venv/bin/python"
PIP="${PROJECT_ROOT}/.venv/bin/pip"

log "Upgrading pip..."
"$PY" -m pip install --upgrade pip >/dev/null

# Ensure requirements.txt exists
if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
  log "No requirements.txt found. Creating with defaults..."
  cat > "${PROJECT_ROOT}/requirements.txt" <<'REQS'
mysql-connector-python
python-dotenv
REQS
fi

log "Installing dependencies from requirements.txt..."
"$PIP" install -r "${PROJECT_ROOT}/requirements.txt"

# --------------- env setup --------------
ENV_FILE="${PROJECT_ROOT}/.env"

create_env_interactive() {
  log "Creating .env (DB connection settings). Press Enter to accept defaults."
  read -r -p "DB_HOST [127.0.0.1]: " _host;   _host="${_host:-127.0.0.1}"
  read -r -p "DB_PORT [3306]: " _port;        _port="${_port:-3306}"
  read -r -p "DB_USER [root]: " _user;        _user="${_user:-root}"
  read -r -s -p "DB_PASS (leave empty if none): " _pass; echo

  cat > "$ENV_FILE" <<EOF
DB_HOST=${_host}
DB_PORT=${_port}
DB_USER=${_user}
DB_PASS=${_pass}
EOF

  log ".env written."
}

if [ ! -f "$ENV_FILE" ]; then
  if [ -f "${PROJECT_ROOT}/.env.example" ]; then
    cp "${PROJECT_ROOT}/.env.example" "$ENV_FILE"
    warn "Copied .env.example -> .env. Updating interactively..."
    create_env_interactive
  else
    create_env_interactive
  fi
fi

# Export .env
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

# --------------- MySQL start ------------
is_mysql_up() {
  if command -v mysqladmin >/dev/null 2>&1; then
    if [ -n "${DB_PASS:-}" ]; then
      mysqladmin --host="$DB_HOST" --port="$DB_PORT" --user="$DB_USER" --password="$DB_PASS" ping >/dev/null 2>&1
    else
      mysqladmin --host="$DB_HOST" --port="$DB_PORT" --user="$DB_USER" ping >/dev/null 2>&1
    fi
  else
    nc -z "$DB_HOST" "$DB_PORT" >/dev/null 2>&1 || return 1
  fi
}

try_start_mysql_macos() {
  if command -v brew >/dev/null 2>&1; then
    log "Attempting to start MySQL via Homebrew..."
    brew services start mysql >/dev/null 2>&1 || true
    brew services start mysql@8.4 >/dev/null 2>&1 || true
  fi
  if command -v mysql.server >/dev/null 2>&1; then
    mysql.server start >/dev/null 2>&1 || true
  fi
}

try_start_mysql_linux() {
  if command -v systemctl >/dev/null 2>&1; then
    log "Attempting to start MySQL via systemd..."
    sudo systemctl start mysql >/dev/null 2>&1 || true
    sudo systemctl start mariadb >/dev/null 2>&1 || true
  elif command -v service >/dev/null 2>&1; then
    log "Attempting to start MySQL via service..."
    sudo service mysql start  >/dev/null 2>&1 || true
    sudo service mariadb start >/dev/null 2>&1 || true
  fi
}

start_mysql_if_needed() {
  if is_mysql_up; then
    log "MySQL is already running."
    return
  fi
  case "$(uname -s)" in
    Darwin) try_start_mysql_macos ;;
    Linux)  try_start_mysql_linux ;;
    *)      warn "Unknown OS; skipping auto-start of MySQL." ;;
  esac
  for _ in {1..10}; do
    if is_mysql_up; then
      log "MySQL is up."
      return
    fi
    sleep 2
  done
  warn "Couldn't verify MySQL is running. If you see 'Can't connect to local MySQL server' next,
please start it manually (e.g., 'brew services start mysql' on macOS) and run ./run.sh again."
}

start_mysql_if_needed

# --------------- run the pipeline -------
log "Executing main.py (this runs ./sql/*.sql in order)..."
"$PY" "${PROJECT_ROOT}/main.py"

log "Done! You should see commit messages and row counts above.
If you need screenshots, check the queries in sql/99_verify.sql."

