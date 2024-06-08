CREATE TABLE IF NOT EXISTS account (
    id INTEGER NOT NULL,
    name VARCHAR(30) unique NOT NULL,
    status CHAR(1) CHECK (status IN ('O', 'C')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    data JSON NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE(name, data, created_at)
);

DROP TABLE  IF EXISTS balance;



