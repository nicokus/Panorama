CREATE TABLE invoices (
    id VARCHAR(255) PRIMARY KEY,
    data JSONB
);

CREATE TABLE vouchers (
    id VARCHAR(255) PRIMARY KEY,
    data JSONB
);

CREATE TABLE payments (
    id VARCHAR(255) PRIMARY KEY,
    data JSONB
);