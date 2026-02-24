# Sitemap Generator — README

## Overview

- **Frontend:** Static HTML hosted on GitHub Pages at `https://sup.sg/seo.html`
- **Backend API:** Go crawler running on VPS at `https://seo.sup.sg`
- **VPS IP:** `23.94.92.135`
- **Files on VPS:** `/home/clawbot/seo-crawler/`
- **Go source:** `main8912v5.go`
- **Binary:** `crawler`
- **Access log:** `access.csv`
- **Port:** `8912` (internal, nginx proxies to it)

---

## Server Stack

| Component | Role |
|-----------|------|
| Go binary (`crawler`) | Crawls websites and returns sitemap.xml |
| systemd (`sitemap.service`) | Keeps the Go binary running, auto-starts on reboot |
| nginx | Handles HTTPS, proxies `/crawl` etc. to Go on port 8912 |
| certbot | Issues and auto-renews SSL certificate for `seo.sup.sg` |

---

## API Endpoints

| Endpoint | Tier | Max Depth | Max Pages | Rate Limit |
|----------|------|-----------|-----------|------------|
| `/crawl` | Standard | 2 | 50 | 5 req / 5 min per IP |
| `/sitemap_generator` | Standard | 2 | 50 | 5 req / 5 min per IP |
| `/seo_sitemap_generator` | Standard | 2 | 50 | 5 req / 5 min per IP |
| `/sitemap_premium` | Premium | 3 | 300 | 5 req / 1 min per IP |

All endpoints accept a single query parameter: `?url=https://example.com`

---

## Initial Setup (one-time)

### 1. DNS
Add an A record in your DNS provider:
- **Name:** `seo`
- **Value:** `23.94.92.135`

### 2. Install dependencies on VPS
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx golang -y
```

### 3. nginx config
```bash
sudo nano /etc/nginx/sites-available/sitemap-api
```

Paste:
```nginx
server {
    listen 80;
    server_name seo.sup.sg;
    location / {
        return 301 https://sup.sg/seo.html;
    }
    location /crawl {
        proxy_pass http://localhost:8912/crawl;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        add_header Access-Control-Allow-Origin "https://sup.sg";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type";

        if ($request_method = OPTIONS) {
            return 204;
        }

        proxy_read_timeout 300s;
        proxy_connect_timeout 10s;
    }

    location /sitemap_generator {
        proxy_pass http://localhost:8912/sitemap_generator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        add_header Access-Control-Allow-Origin "https://sup.sg";
        proxy_read_timeout 300s;
    }

    location /seo_sitemap_generator {
        proxy_pass http://localhost:8912/seo_sitemap_generator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        add_header Access-Control-Allow-Origin "https://sup.sg";
        proxy_read_timeout 300s;
    }

    location /sitemap_premium {
        proxy_pass http://localhost:8912/sitemap_premium;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        add_header Access-Control-Allow-Origin "https://sup.sg";
        proxy_read_timeout 300s;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/sitemap-api /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default   # remove default nginx page
sudo nginx -t
sudo systemctl reload nginx
```

### 4. SSL certificate (Let's Encrypt)
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8912/tcp
sudo ufw reload
sudo certbot --nginx -d seo.sup.sg
```
Certbot auto-renews — nothing else needed.

### 5. Build the Go binary
```bash
cd /home/clawbot/seo-crawler
go build -o crawler main8912v5.go
```

### 6. systemd service
```bash
sudo nano /etc/systemd/system/sitemap.service
```

Paste:
```ini
[Unit]
Description=Sitemap Crawler
After=network.target

[Service]
ExecStart=/home/clawbot/seo-crawler/crawler
WorkingDirectory=/home/clawbot/seo-crawler
Restart=always
RestartSec=5
User=clawbot

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sitemap
sudo systemctl start sitemap
sudo systemctl status sitemap
```

---

## Day-to-Day Operations

### Updating the Go source (`main8912v5.go`)
```bash
cd /home/clawbot/seo-crawler
go build -o crawler main8912v5.go
sudo systemctl restart sitemap
```

### Updating nginx config
```bash
sudo nano /etc/nginx/sites-available/sitemap-api
sudo nginx -t
sudo systemctl reload nginx
```

### Updating the frontend (`seo.html`)
Just edit and push to the GitHub Pages repo. No VPS restart needed.

### Restarting the Go server
```bash
sudo systemctl restart sitemap
```

### Stopping the Go server
```bash
sudo systemctl stop sitemap
```

### After a VPS reboot
Everything starts automatically — nginx and the Go server both start on boot via systemd. Verify with:
```bash
sudo systemctl status sitemap
sudo systemctl status nginx
```

---

## Logs

### Go server logs (crawl activity)
```bash
sudo journalctl -u sitemap -f
```

### Access log (API calls — CSV)
```bash
cat /home/clawbot/seo-crawler/access.csv
```
Columns: `datetime, endpoint, ip, domain`

### nginx error log
```bash
sudo tail -f /var/log/nginx/error.log
```

---

## Checking Things Are Running

```bash
# Is the Go server listening on 8912?
sudo ss -tlnp | grep 8912

# Is nginx running?
sudo systemctl status nginx

# Is the Go server running?
sudo systemctl status sitemap

# Test the API directly
curl "https://seo.sup.sg/crawl?url=https://example.com"
```

---

## File Summary

| File | Location |
|------|----------|
| Go source | `/home/clawbot/seo-crawler/main8912v5.go` |
| Go binary | `/home/clawbot/seo-crawler/crawler` |
| Access log | `/home/clawbot/seo-crawler/access.csv` |
| nginx config | `/etc/nginx/sites-available/sitemap-api` |
| systemd service | `/etc/systemd/system/sitemap.service` |
| Frontend | GitHub Pages repo → `seo.html` |