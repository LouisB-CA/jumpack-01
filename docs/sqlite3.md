
# SQLite Database Access Guide

This document explains how to inspect and query the database using the built-in Python `sqlite3` module, without requiring the standalone `sqlite3` binary.

## 1. Quick Inspect (Interactive Mode)

To open an interactive shell to explore the database:

```bash
python3 -m sqlite3 your_database.db

```

**Common internal commands:**

* `.tables` — List all table names.
* `.schema <table_name>` — Show the `CREATE` statement and column types.
* `.headers on` — Show column names in query results.
* `.mode column` — Format output into clean columns.
* `.exit` — Close the session.

---

## 2. Command Line One-Liners

Use these commands to get information quickly without entering the interactive prompt.

### Get Table Names

```bash
python3 -m sqlite3 your_database.db "SELECT name FROM sqlite_master WHERE type='table';"

```

### Get Column Names (Schema)

*Replace `table_name` with the name found in the previous step.*

```bash
python3 -m sqlite3 your_database.db "PRAGMA table_info(table_name);"

```

### Dump All Data

This command includes headers and formats the output for readability:

```bash
python3 -m sqlite3 -header -column your_database.db "SELECT * FROM table_name;"

```

---

## 3. Export to CSV

If you need to move the data into a spreadsheet, you can export it directly:

```bash
python3 -m sqlite3 -header -csv your_database.db "SELECT * FROM table_name;" > output.csv

```

---

## 4. Troubleshooting

* **File Permissions:** If you get a "Permission Denied" error, ensure your user has read access to the `.db` file.
* **Locked Database:** If the database is currently being written to by your Python application, you may see a "database is locked" error. Try closing the application before running CLI commands.


