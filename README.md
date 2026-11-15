# CampusConnect — S6 ICT SBA Task 2 (Testing & Evaluation)

A small, deliberately insecure **campus phonebook** built for the HKDSE ICT
Elective B1 topic **Web Programming and Application**. Students test it, report
defects and evaluate whether it is ready for release. The app is wrapped in
Docker with **nginx as the reverse proxy** and a **SQLite** database that is
restored to its original state every 5 minutes.

> **Warning:** this application contains deliberate weaknesses for teaching.
> Run it only in an isolated teaching lab, with fictional data. Never expose it
> to the public internet, and never reuse the code in a real product.
>
> This repository is a classroom teaching resource. The teacher holds the
> staff/admin credentials and the answer key separately.

## What is inside

| Layer | Technology |
|---|---|
| Web entry point | nginx 1.27 (static files + reverse proxy to PHP-FPM) |
| Application | PHP 8.2 (PDO SQLite) |
| Front end | HTML, CSS, vanilla JavaScript |
| Database | SQLite, seeded with fictional users and contacts |
| Reset | A `db-restore` container replaces the live DB with the seed every 300 s |
| Orchestration | Docker Compose (3 services: `web`, `app`, `db-restore`) |

There are exactly **three HTML pages**:

1. `index.php` — sign in / register
2. `board.php` — phonebook search, listing and “add contact”
3. `admin.php` — staff console (users and contacts)

The code is intentionally compact: about **840 lines** across PHP, CSS, JS,
SQL, Docker and nginx files (documentation excluded).

## Quick start (local Docker Desktop)

```bash
docker compose up --build -d
```

Open <http://127.0.0.1:8080/>. The first build takes a moment while the PHP
image is prepared. Wait until `docker compose ps` shows the `app` service as
`healthy` if nginx returns a 502 on the very first request.

Default bind address is `127.0.0.1` (local only). To let students on the school
LAN connect, copy `.env.example` to `.env`, set `BIND_ADDR=0.0.0.0`, and restart:

```bash
cp .env.example .env      # then edit BIND_ADDR=0.0.0.0
docker compose up -d
```

Or pass the values directly:

```bash
# PowerShell
$env:BIND_ADDR="0.0.0.0"; $env:APP_PORT="8080"; docker compose up -d

# bash
BIND_ADDR=0.0.0.0 APP_PORT=8080 docker compose up -d
```

Then give students `http://<teacher-pc-LAN-IP>:8080/`.

### Student demo accounts

| Username | Password | Role |
|---|---|---|
| `alice` | `alice1234` | student |
| `bob` | `bob1234` | student |
| `carol` | `carol1234` | student |

The teacher holds the staff/admin credentials separately.

### Database reset

The `db-restore` sidecar sleeps for `RESTORE_INTERVAL_SECONDS` (default 300),
then atomically replaces `/data/app.db` with `/seed/app.db`. The seed is built
into the image from `db/seed.sql`, so every reset is identical.

- Change the interval (useful for a quick demo): set
  `RESTORE_INTERVAL_SECONDS=30` before `docker compose up -d`.
- Force a completely clean slate:
  ```bash
  docker compose down -v
  docker compose up -d --build
  ```
- Watch the reset log:
  ```bash
  docker compose logs -f db-restore
  ```
- The admin console shows the last reset time (read from `/data/restore.log`).

### Inspecting the database

The live SQLite file is in the `dbdata` volume at `/data/app.db`. You can query
it directly without installing anything on the host:

```bash
docker compose exec app sqlite3 /data/app.db ".tables"
docker compose exec app sqlite3 /data/app.db "SELECT id, username, role FROM users;"
docker compose exec app sqlite3 /data/app.db "SELECT id, name, phone FROM contacts LIMIT 5;"
```

The schema and dummy data are defined in `db/seed.sql`, which is the source of
truth used to build the pristine database at image build time.

The timer starts when the `db-restore` container starts. If you restart only the
app, the timer is unaffected. If you want the 5-minute clock to restart, restart
the `db-restore` service.

## Project layout

```
.
├── docker-compose.yml          # nginx + PHP-FPM + reset sidecar
├── .dockerignore
├── nginx/default.conf          # reverse proxy, static files, fastcgi_pass app:9000
├── php/
│   ├── Dockerfile              # PHP 8.2-FPM + pdo_sqlite + seed DB
│   ├── entrypoint.sh           # creates/chowns /data/app.db on first boot
│   └── restore.sh              # 5-minute reset loop
├── app/
│   ├── index.php               # page 1: login / register
│   ├── board.php               # page 2: phonebook
│   ├── admin.php               # page 3: admin console
│   ├── inc/bootstrap.php       # DB, session, helpers, shared layout
│   ├── assets/style.css
│   ├── assets/app.js
│   └── secret.key
├── db/seed.sql                 # schema + dummy users/contacts
└── docs/
    ├── STUDENT_INSTRUCTIONS.md
    └── RUBRIC.md
```

## Deploying to GCP Compute Engine

The app is intentionally vulnerable, so the firewall rule is the most important
step. **Do not use `0.0.0.0/0`.** Use the public IP of the school/classroom
network, and shut the instance down after the lesson.

1. Create a small VM (Ubuntu 22.04 LTS, `e2-small` is enough):

   ```bash
   gcloud compute instances create campusconnect \
     --zone=asia-east2-a \
     --machine-type=e2-small \
     --image-family=ubuntu-2204-lts \
     --image-project=ubuntu-os-cloud \
     --tags=campusconnect
   ```

2. Allow only your classroom's public IP (replace the example address):

   ```bash
   gcloud compute firewall-rules create campusconnect-web \
     --allow=tcp:8080 \
     --source-ranges=203.0.113.10/32 \
     --target-tags=campusconnect
   ```

3. SSH in and install Docker Engine plus the Compose plugin:

   ```bash
   gcloud compute ssh campusconnect --zone=asia-east2-a
   curl -fsSL https://get.docker.com | sudo sh
   sudo usermod -aG docker "$USER"
   newgrp docker
   docker compose version
   ```

4. Upload or clone the project, then start it. Use a **private** repository
   if you keep teacher-only material in the project.

   ```bash
   git clone <your-private-repo> campusconnect
   cd campusconnect
   BIND_ADDR=0.0.0.0 APP_PORT=8080 docker compose up -d --build
   ```

5. Browse to `http://<VM-external-IP>:8080/`.

6. After the lesson:

   ```bash
   docker compose down -v
   gcloud compute instances stop campusconnect --zone=asia-east2-a
   ```

Notes:

- Keep SSH restricted to IAP or your own IP. Never open port 8080 to
  `0.0.0.0/0`.
- The VM's external IP may change after a stop/start. Reserve a static IP if
  students need a stable URL.
- If you need HTTPS, terminate it in front of nginx (GCP HTTPS load balancer,
  Caddy, or a TLS-enabled nginx). HTTPS protects credentials in transit but does
  **not** fix the application vulnerabilities students are testing.
- Do not attach a powerful service account to the VM.
- The reset sidecar is a convenience for shared classroom use, not a security
  control.

## Customising

| Change | Where |
|---|---|
| Seed users/contacts | `db/seed.sql`, then rebuild (`docker compose up --build -d`) |
| Reset interval | `RESTORE_INTERVAL_SECONDS` environment variable |
| Port / bind address | `APP_PORT`, `BIND_ADDR` environment variables |
| Styling | `app/assets/style.css` |
| App behaviour | `app/index.php`, `app/board.php`, `app/admin.php` |

## Troubleshooting

| Symptom | Check |
|---|---|
| `docker compose` cannot connect | Start Docker Desktop and wait for the engine |
| nginx returns 502 | `docker compose ps`; wait for `app` to become healthy; `docker compose logs app` |
| Port 8080 already in use | Set `APP_PORT=8081` |
| Data did not reset | `docker compose logs db-restore`; confirm the interval; restart the service |
| Login fails after a reset | The reset restored the seed users; use a seeded account again |
| Windows line-ending problems | `php/*.sh` must keep LF endings; do not convert the repo to CRLF |

## Documentation

- **Student brief:** [`docs/STUDENT_INSTRUCTIONS.md`](docs/STUDENT_INSTRUCTIONS.md)
- **Marking rubric:** [`docs/RUBRIC.md`](docs/RUBRIC.md)
- **Curriculum reference:** [Elective B1 – Web Programming and Application](https://spycit.notion.site/Elective-B1-Web-Programming-and-Application-c9960271cb1d43d1883b5bfaabdaef2e?pvs=74)
