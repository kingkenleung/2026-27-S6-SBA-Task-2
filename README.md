# CampusConnect — S6 ICT SBA Task 2 (Testing & Evaluation)

A small, deliberately insecure **campus phonebook** built for the HKDSE ICT
Elective B1 topic **Web Programming and Application**. Students test it, report
defects and evaluate whether it is ready for release. The app is wrapped in
Docker with **nginx as the reverse proxy** and a **SQLite** database that is
restored to its original state every 5 minutes.

> **Warning:** this application contains deliberate weaknesses for teaching.
> The classroom instance is intentionally reachable from home, so treat it as a
> temporary public lab: use fictional data only, keep the admin account private,
> monitor the VM, and shut it down after the unit. Never reuse the code in a
> real product.
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
    ├── STUDENT_INSTRUCTIONS.docx
    ├── RUBRIC.md
    └── make_docx.py
```

## Deploying to GCP Compute Engine (cheapest)

The cheapest practical machine is **e2-micro** (2 shared vCPU, 1 GB RAM) with
**Ubuntu 22.04 LTS**, a **10 GB standard persistent disk**, and no service
account. Two regions make sense:

| Region | Trade-off | Approx. cost while running 24/7 |
|---|---|---|
| `us-central1` (Iowa) | Always Free e2-micro + 30 GB standard disk; higher latency from HK | ~US$3.65/month for the external IPv4 + small egress |
| `asia-east2` (Hong Kong) | Low latency for HK classrooms; not free-tier eligible | ~US$12.6/month (compute + IPv4 + disk) |

If you are still inside the US$300 / 90-day Free Trial, use `asia-east2` for the
better classroom experience. After the trial, use `us-central1` if the absolute
lowest cost matters, or keep `asia-east2` for about US$12/month.

Avoid **Spot/preemptible** VMs for a live lesson: they can be stopped with 30
seconds' notice.

### 1. Set up the project

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable compute.googleapis.com iap.googleapis.com
```

### 2. Firewall: home access

This classroom deployment lets students work from home, so port 8080 is open to
the internet:

```bash
gcloud compute firewall-rules create campusconnect-web \
  --allow=tcp:8080 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=campusconnect \
  --description="CampusConnect home-access lab"
```

If the rule already exists, update it:

```bash
gcloud compute firewall-rules update campusconnect-web --source-ranges=0.0.0.0/0
```

> The app is intentionally vulnerable and now publicly reachable. Use fictional
> data only, keep the admin account private, and shut the VM down after the unit.

SSH via IAP only:

```bash
gcloud compute firewall-rules create campusconnect-ssh \
  --allow=tcp:22 \
  --source-ranges=35.235.240.0/20 \
  --target-tags=campusconnect \
  --description="SSH via Identity-Aware Proxy only"
```

`35.235.240.0/20` is Google's IAP TCP-forwarding range. This lets you SSH from
Cloud Shell or any authorised machine without exposing port 22 to the school
network.

To **restrict** the app to the school later, run `curl -4 ifconfig.me` from a
school machine and update the web rule:

```bash
gcloud compute firewall-rules update campusconnect-web --source-ranges=YOUR_SCHOOL_IP/32
```

If this is a dedicated project, check whether the default network has a broad
SSH rule and remove it if you do not need it:

```bash
gcloud compute firewall-rules list --filter="name=default-allow-ssh"
# gcloud compute firewall-rules delete default-allow-ssh
```

### 3. Create the VM

For the absolute cheapest (US free tier):

```bash
gcloud compute instances create campusconnect \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard \
  --tags=campusconnect \
  --no-service-account \
  --no-scopes \
  --metadata=enable-oslogin=TRUE
```

For Hong Kong, change `--zone=us-central1-a` to `--zone=asia-east2-a`.

### 4. SSH in and add swap

```bash
gcloud compute ssh campusconnect --zone=us-central1-a --tunnel-through-iap
```

1 GB of RAM is enough for this app, but a 1 GB swap file makes the first Docker
build safer:

```bash
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
free -h
```

### 5. Install Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
newgrp docker
docker compose version
```

If `newgrp` does not take effect, log out and SSH in again, or prefix commands
with `sudo`.

### 6. Clone and configure

```bash
git clone https://github.com/kingkenleung/2026-27-S6-SBA-Task-2.git
cd 2026-27-S6-SBA-Task-2
cat > .env <<'EOF'
BIND_ADDR=0.0.0.0
APP_PORT=8080
RESTORE_INTERVAL_SECONDS=300
EOF
```

### 7. Start

```bash
docker compose up -d --build
docker compose ps
curl -s http://127.0.0.1:8080/healthz
```

The first build takes a few minutes. Wait for `app` to show `healthy`.

### 8. Open the app

Get the external IP:

```bash
gcloud compute instances describe campusconnect \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

Browse to `http://EXTERNAL_IP:8080/`.

Use the student accounts (`alice` / `alice1234`, etc.). Staff access is for the
teacher. The database resets every 5 minutes.

### 9. Cost control

Create a small budget alert in **Billing → Budgets & alerts** (for example
US$5 or US$10). Stop the VM when the class is not using it:

```bash
gcloud compute instances stop campusconnect --zone=us-central1-a
gcloud compute instances start campusconnect --zone=us-central1-a
```

An ephemeral external IP is released when the VM stops and may change when it
starts. Reserve a static IP only if you need a stable URL (it is billed even
while the VM is stopped).

After the unit, delete the VM and disk:

```bash
gcloud compute instances delete campusconnect \
  --zone=us-central1-a --delete-disks=all
gcloud compute firewall-rules delete campusconnect-web campusconnect-ssh
```

### Notes

- Keep SSH restricted to IAP.
- The current deployment allows home access, so port 8080 is open to the
  internet. The app is intentionally vulnerable; use fictional data only,
  monitor the VM, and shut it down after the unit. To restrict it again, set
  `--source-ranges=YOUR_SCHOOL_IP/32`.
- Use a dedicated, low-privilege project with no real data.
- HTTP is used for this temporary lab. Add HTTPS if you keep the app beyond the
  unit or use real data.
- The reset sidecar is a convenience, not a security control.

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

- **Student brief (Markdown):** [`docs/STUDENT_INSTRUCTIONS.md`](docs/STUDENT_INSTRUCTIONS.md)
- **Student brief (DOCX):** [`docs/STUDENT_INSTRUCTIONS.docx`](docs/STUDENT_INSTRUCTIONS.docx)
- **Marking rubric:** [`docs/RUBRIC.md`](docs/RUBRIC.md)

The DOCX is generated from the Markdown with:

```bash
python docs/make_docx.py
```

- **Curriculum reference:** [Elective B1 – Web Programming and Application](https://spycit.notion.site/Elective-B1-Web-Programming-and-Application-c9960271cb1d43d1883b5bfaabdaef2e?pvs=74)
