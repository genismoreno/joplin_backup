# joplin_backup
Sends a backup of joplin database via email (delivered to same email).

## Gmail
It's proven to work with gmail accounts.
If 2-factor auth is activated, follow this [link](https://www.interviewqs.com/blog/py-email).

## How to run

From the project root:
`EMAIL=<email_address> PASSWORD=<email_password> DATABASE_FP=<joplin_database_abs_file_path> python3 main.py`

The standard Joplin database file in Ubuntu is placed under the user sub-directory: `.config/joplin-desktop/database.sqlite`.

### Recommendation
Create a `.env` file and place the env vars there.
Example:
```
LOG_LEVEL=INFO
EMAIL=my_email@qustodio.com
PASSWORD=my_secret_password_123
DATABASE_FP=/home/user/.config/joplin-desktop/database.sqlite
```

### Run from bash
Create a `run_backup.sh` file as follows:
```
#!/usr/bin/env bash

set -a
source .env
set +a

python3 main.py
```

Run: `bash run_backup.sh`
