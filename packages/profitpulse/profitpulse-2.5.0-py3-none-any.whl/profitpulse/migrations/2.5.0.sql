CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) UNIQUE,
    budget INTEGER NOT NULL
);

INSERT OR IGNORE INTO category (name, budget) VALUES ('Other', 0);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Savings', 26400);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Supermarket', 65000);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Education', 40000);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Health', 25000);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Personal', 25000);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Mobility', 15000);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Low Value', 300);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Energy', 400);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Housing', 2500);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Clean', 200);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Water', 100);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Internet', 50);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Pilates', 150);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Pool', 100);
INSERT OR IGNORE INTO category (name, budget) VALUES ('YouFit', 50);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Professional', 300);
INSERT OR IGNORE INTO category (name, budget) VALUES ('iCloud', 20);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Restoration', 500);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Allowance', 100);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Credit', 1000);
INSERT OR IGNORE INTO category (name, budget) VALUES ('Extraordinary', 700);

CREATE TABLE IF NOT EXISTS seller (
    name VARCHAR(30) PRIMARY KEY,
    alias VARCHAR(30) DEFAULT '',
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category(id)
)