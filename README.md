# Grafana Git Sync demo

Repo for recording **Grafana Dashboards as Code with Git Sync (Grafana 13)**.

Git Sync only cares about the files under [`dashboards/`](dashboards/). The sample checkout app is here so you can play with a real service and optional Prometheus panel, without cluttering the synced path.

## What is in here

| Path | Purpose |
|------|---------|
| `dashboards/checkout-service.json` | Dashboard titled **Checkout service**. Stat panel **Error rate** uses TestData = `3.1`, green below red threshold `5`. |
| `app/` | Tiny Flask checkout service with `checkout_error_rate_percent`. |
| `docker-compose.yml` | Checkout app + Prometheus for optional live metrics. |

## Wire Git Sync (Grafana Cloud 13.x)

1. Create a fine-grained GitHub PAT on **this repository only**, with:
   - Administration: read
   - Contents: read and write
   - Metadata: read
   - Pull requests: read and write
   - Webhooks: read and write  
   Webhooks require you to be a **repo admin**.
2. In Grafana: **Administration → General → Provisioning → GitHub**.
3. Paste the repo URL and token → **Configure repository**.
4. Branch: `main`. Path: `dashboards`. Folder sync on. Display name: `grafana-dashboards` (or this repo name).
5. Additional settings:
   - **Enable pull request option when saving**: on
   - **Enable push to configured branch**: **off**
6. Finish. Open **Checkout service** in the provisioned folder.

### Recording beat (matches the script)

1. Confirm **Error rate** reads `3.1` and is **green** (TestData; say the value is fake).
2. Edit the panel → change red threshold from `5` to `2` → Save → new branch (not main).
3. You see red + preview banner. An incognito Viewer still sees green.
4. Open the PR. Diff is one number: `"value": 5` → `"value": 2`.
5. Merge. Webhook pulls main. Viewer sees red, no banner.

Optional: protect `main` so a PR is required.

## Optional: run the sample app locally

```bash
docker compose up -d --build
./app/loadgen.sh
```

- App: http://localhost:18000/health  
- Metrics: http://localhost:18000/metrics  
- Prometheus: http://localhost:19090  

In Grafana Cloud, add a Prometheus datasource that can reach a tunnel/public scrape target if you want the **Error rate (live app)** panel to work. For the video, leave that panel alone and use the TestData **Error rate** panel only.

Change the live error rate without a PR:

```bash
ERROR_RATE_PERCENT=6 docker compose up -d --build checkout
```

## TestData datasource note

The TestData panel uses `"uid": "grafana"`. If Grafana says the datasource is missing, edit the panel once, pick **TestData**, and save via Git Sync so the UID matches your stack.
