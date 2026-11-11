-- Demo database for "VoltaSur Energía", a FICTIONAL electricity utility.
-- All names, accounts and amounts are invented for this portfolio.

CREATE TABLE customers (
    account_number   VARCHAR(12) PRIMARY KEY,
    full_name        TEXT        NOT NULL,
    document_last4   CHAR(4)     NOT NULL,          -- used only to verify identity
    email            TEXT        NOT NULL,
    supply_address   TEXT        NOT NULL,
    zone             TEXT        NOT NULL,
    tariff           TEXT        NOT NULL,
    automatic_debit  BOOLEAN     NOT NULL DEFAULT FALSE
);

CREATE TABLE invoices (
    id               SERIAL PRIMARY KEY,
    invoice_number   TEXT        UNIQUE NOT NULL,
    account_number   VARCHAR(12) REFERENCES customers(account_number),
    period           TEXT        NOT NULL,           -- e.g. 2026-09
    issue_date       DATE        NOT NULL,
    due_date         DATE        NOT NULL,
    consumption_kwh  NUMERIC(10,2) NOT NULL,
    subtotal         NUMERIC(12,2) NOT NULL,
    taxes            NUMERIC(12,2) NOT NULL,
    total            NUMERIC(12,2) NOT NULL,
    status           TEXT        NOT NULL CHECK (status IN ('paid','pending','overdue'))
);

CREATE TABLE planned_outages (
    id          SERIAL PRIMARY KEY,
    zone        TEXT        NOT NULL,
    starts_at   TIMESTAMPTZ NOT NULL,
    ends_at     TIMESTAMPTZ NOT NULL,
    reason      TEXT        NOT NULL
);

CREATE TABLE handoff_requests (
    id              SERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    account_number  VARCHAR(12),
    topic           TEXT NOT NULL,
    summary         TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'open'
);

INSERT INTO customers VALUES
 ('100200300', 'Martina Gómez',   '4821', 'martina.gomez@example.com', 'Av. Siempreviva 742, Villa Norte', 'NORTE', 'T1-R2 Residencial', TRUE),
 ('100200301', 'Julián Ferreyra', '1937', 'julian.f@example.com',      'Calle Falsa 123, Barrio Sur',     'SUR',   'T1-R1 Residencial', FALSE),
 ('100200302', 'Panadería La Espiga SRL', '7710', 'admin@laespiga.example', 'Ruta 9 km 12, Parque Industrial', 'OESTE', 'T2 Comercial', FALSE);

INSERT INTO invoices (invoice_number, account_number, period, issue_date, due_date, consumption_kwh, subtotal, taxes, total, status) VALUES
 ('A-0001-00045871', '100200300', '2026-08', '2026-09-01', '2026-09-15', 312.00, 41200.00, 8652.00, 49852.00, 'paid'),
 ('A-0001-00049920', '100200300', '2026-09', '2026-10-01', '2026-10-15', 287.00, 38110.00, 8003.10, 46113.10, 'paid'),
 ('A-0001-00053310', '100200300', '2026-10', '2026-11-01', '2026-11-17', 301.00, 40050.00, 8410.50, 48460.50, 'pending'),
 ('A-0001-00049921', '100200301', '2026-09', '2026-10-01', '2026-10-15', 198.00, 24300.00, 5103.00, 29403.00, 'overdue'),
 ('A-0001-00053311', '100200301', '2026-10', '2026-11-01', '2026-11-17', 205.00, 25150.00, 5281.50, 30431.50, 'pending'),
 ('B-0002-00011020', '100200302', '2026-10', '2026-11-01', '2026-11-17', 2410.00, 389000.00, 81690.00, 470690.00, 'pending');

INSERT INTO planned_outages (zone, starts_at, ends_at, reason) VALUES
 ('NORTE', now() + interval '2 days', now() + interval '2 days 4 hours', 'Reemplazo de transformador en subestación Norte'),
 ('OESTE', now() + interval '5 days', now() + interval '5 days 3 hours', 'Mantenimiento preventivo de línea de media tensión');
