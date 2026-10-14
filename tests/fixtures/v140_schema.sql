
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    full_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'operatore')),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    auth_version INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE COLLATE NOCASE,
    category TEXT,
    value TEXT,
    description TEXT NOT NULL,
    laboratory TEXT,
    cabinet TEXT,
    door TEXT,
    shelf TEXT,
    drawer TEXT,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reorder_threshold INTEGER NOT NULL DEFAULT 0 CHECK (reorder_threshold >= 0),
    target_quantity INTEGER NOT NULL DEFAULT 0 CHECK (target_quantity >= 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movement_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_id TEXT NOT NULL UNIQUE,
    movement_type TEXT NOT NULL CHECK (movement_type IN ('prelievo', 'restituzione')),
    recipient TEXT NOT NULL,
    note TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    operator_snapshot TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_id INTEGER NOT NULL REFERENCES components(id),
    movement_type TEXT NOT NULL CHECK (
        movement_type IN ('prelievo', 'restituzione', 'carico', 'rettifica_carico', 'rettifica_scarico')
    ),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    delta INTEGER NOT NULL CHECK (delta != 0),
    balance_after INTEGER NOT NULL CHECK (balance_after >= 0),
    recipient TEXT,
    note TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    operator_snapshot TEXT,
    operation_id TEXT,
    batch_id INTEGER REFERENCES movement_batches(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reorder_lines (
    component_id INTEGER PRIMARY KEY REFERENCES components(id) ON DELETE CASCADE,
    desired_quantity INTEGER NOT NULL CHECK (desired_quantity > 0),
    set_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_components_code ON components(code);
CREATE INDEX IF NOT EXISTS idx_components_category ON components(category);
CREATE INDEX IF NOT EXISTS idx_movements_component ON movements(component_id);
CREATE INDEX IF NOT EXISTS idx_movements_created ON movements(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reorder_lines_updated ON reorder_lines(updated_at DESC);

CREATE TRIGGER IF NOT EXISTS movements_no_update
BEFORE UPDATE ON movements
BEGIN
    SELECT RAISE(ABORT, 'Lo storico movimenti non può essere modificato');
END;

CREATE TRIGGER IF NOT EXISTS movements_no_delete
BEFORE DELETE ON movements
BEGIN
    SELECT RAISE(ABORT, 'Lo storico movimenti non può essere cancellato');
END;

CREATE TRIGGER IF NOT EXISTS movement_batches_no_update
BEFORE UPDATE ON movement_batches
BEGIN
    SELECT RAISE(ABORT, 'I gruppi di movimento non possono essere modificati');
END;

CREATE TRIGGER IF NOT EXISTS movement_batches_no_delete
BEFORE DELETE ON movement_batches
BEGIN
    SELECT RAISE(ABORT, 'I gruppi di movimento non possono essere cancellati');
END;
