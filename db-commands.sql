CREATE TABLE accounts (account_id INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL, email VARCHAR(255) NOT NULL, hash text NOT NULL, account_pic VARCHAR(255), lang VARCHAR(16))

CREATE TABLE items (item_id INTEGER PRIMARY KEY, account_id INTEGER, item VARCHAR(30), descr VARCHAR(60), quantity REAL, qnt_units VARCHAR(10), date TEXT);

CREATE TABLE wishlist (wishlist_id INTEGER PRIMARY KEY, wishlist_item VARCHAR(30), descr VARCHAR(60), wishlist_quantity REAL, wishlist_qnt_units VARCHAR(10), date TEXT, account_id INTEGER)

CREATE TABLE history (history_id INTEGER PRIMARY KEY, history_item VARCHAR(30), descr VARCHAR(60), history_quantity REAL, history_qnt_units VARCHAR(10), date TEXT, history_event VARCHAR(10), account_id INTEGER)