-- I used this file to plan out the tables

CREATE TABLE transactions
(
    id INTEGER PRIMARY KEY NOT NULL,
    ttype TEXT NOT NULL,
    ttime DATETIME DEFAULT CURRENT_TIMESTAMP,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    tcash NUMERIC NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE assets
(
    id INTEGER PRIMARY KEY NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);