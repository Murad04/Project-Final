MSSQL Database Setup (VS Code `mssql` extension)

Overview
- The file `schema_mssql.sql` creates a database named `sql_app` and the tables: `users`, `products`, `orders`, `order_items`.
- This README explains how to run the script using the Microsoft SQL Server (mssql) VS Code extension.

Run with VS Code `mssql` extension
1. Install the extension: "SQL Server (mssql)" by Microsoft (if not already installed).
2. Open the Command Palette (Ctrl+Shift+P) and run: `MS SQL: Connect`.
   - Choose or create a connection. You can use Windows Authentication (Integrated) for local instances or SQL Login for remote servers.
   - If you added workspace settings, a couple of example connection profiles are available in `.vscode/settings.json` (fill placeholders before using).
3. Open `schema_mssql.sql` in the editor.
4. In the editor window, ensure the status bar shows the connection you want (bottom-right or the connection picker at the top-right of the editor).
5. Click the "Execute Query" (play) button in the editor title, or right-click the editor and choose "Execute Query". The extension will run the batches (it supports `GO`).
6. Confirm the `sql_app` database appears in your server's Databases list and that tables were created.

Run with `sqlcmd` (alternative)
- Using Windows Authentication (SQLEXPRESS):
```bash
sqlcmd -S .\\SQLEXPRESS -i "d:\\Personal\\ADA-GWU Master\\ML\\Project Final\\schema_mssql.sql"
```
- Using SQL Authentication:
```bash
sqlcmd -S <SERVER_NAME> -U <USERNAME> -P <PASSWORD> -i "d:\\Personal\\ADA-GWU Master\\ML\\Project Final\\schema_mssql.sql"
```

Notes
- The script uses `GO` batch separators and `SYSUTCDATETIME()` for timestamps.
- If you prefer a different database name, edit the `CREATE DATABASE [sql_app]` line in `schema_mssql.sql`.
- Do not store real credentials in `.vscode/settings.json` if this workspace is shared.

Need help?
- I can run the script for you (via `sqlcmd`) if you provide a reachable server or if you want me to run it against a local `SQLEXPRESS` instance available on this machine.
- I can also adapt the script to a different database name or schema changes if needed.
