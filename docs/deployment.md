# Safe VPS deployment (offline synthetic prototype)

BuyerGuard BD is an offline demonstration app. It contains synthetic records and must not be presented as an official land-record service. No SSH or remote deployment is performed by this package.

## Recommended layout

Use a dedicated unprivileged account and keep the SQLite database outside the release directory:

```text
/srv/buyerguard-bd/
  current/       # extracted release
  shared/        # buyerguard.db and backups
  venv/          # Python virtual environment
```

## Install and configure

1. Install Python 3.11+, `python3-venv`, Nginx, and a system service manager on a supported Linux VPS.
2. Create `/srv/buyerguard-bd/current`, `/srv/buyerguard-bd/shared`, and `/etc/buyerguard-bd` owned by the `buyerguard` account.
3. Extract the release into `current`; create the virtual environment in `venv`; install `requirements.txt`.
4. Copy `.env.example` to `/etc/buyerguard-bd/buyerguard.env`, set a long random `SECRET_KEY`, and keep the file readable only by the service account.
5. Set `BUYERGUARD_DB=/srv/buyerguard-bd/shared/buyerguard.db`. On first start the app creates and seeds the synthetic database.
6. Install `deployment/systemd/buyerguard.service` and edit the Nginx example with the real hostname. Put TLS termination and HTTP-to-HTTPS redirect in front of the service.

The service binds Gunicorn to `127.0.0.1:8000`; it is not directly exposed to the internet. Do not enable Flask debug mode in production.

## Validation and operations

After starting the service, check `https://your-host/health`. Expected JSON includes `status: healthy`, `database: connected`, and a non-zero `plot_count`. Review service logs if this fails.

Before each release, stop or quiesce writes, copy the SQLite database to a dated backup, extract the new release, and restart the service. Keep at least one previous release and database backup for rollback. Do not overwrite a live database with a seed database.

This package does not include authentication, authorization, live government integrations, or production-grade multi-user persistence. Restrict access with the VPS firewall and application-layer access controls before using it beyond a private demonstration.
