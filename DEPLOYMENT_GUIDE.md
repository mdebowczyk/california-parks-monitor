# Deployment Guide

This guide covers various ways to deploy your California National Parks availability monitor to run 24/7.

## Table of Contents

1. [Local Computer (Simple)](#local-computer)
2. [Cloud Deployment (Recommended)](#cloud-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Raspberry Pi](#raspberry-pi)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Computer

### Windows

**Using Task Scheduler:**

1. Open Task Scheduler (search in Start menu)
2. Click "Create Basic Task"
3. Name: "Park Monitor"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
   - Program: `C:\Python311\python.exe` (adjust to your Python path)
   - Arguments: `C:\path\to\park_monitor.py`
   - Start in: `C:\path\to\` (folder containing the script)
6. Finish and test

**Keep Computer Awake:**
- Settings → System → Power & Sleep
- Set "When plugged in, PC goes to sleep after" to "Never"

### macOS

**Using launchd:**

1. Create file `~/Library/LaunchAgents/com.parkmonitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.parkmonitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/park_monitor.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

2. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.parkmonitor.plist
```

### Linux

**Using systemd:**

1. Create `/etc/systemd/system/park-monitor.service`:

```ini
[Unit]
Description=California Parks Availability Monitor
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/park-monitor
ExecStart=/usr/bin/python3 /home/your-username/park-monitor/park_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable park-monitor
sudo systemctl start park-monitor
```

3. Check status:
```bash
sudo systemctl status park-monitor
```

4. View logs:
```bash
sudo journalctl -u park-monitor -f
```

---

## Cloud Deployment

### AWS EC2 (Free Tier Available)

**Setup:**

1. **Launch EC2 Instance:**
   - Go to AWS Console → EC2
   - Launch Instance
   - Choose: Ubuntu Server 22.04 LTS (Free tier eligible)
   - Instance type: t2.micro (Free tier)
   - Create/select key pair
   - Allow SSH (port 22) in security group
   - Launch

2. **Connect to Instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

4. **Upload Files:**
```bash
# From your local machine
scp -i your-key.pem -r * ubuntu@your-instance-ip:~/park-monitor/
```

5. **Setup as Service:**
```bash
sudo nano /etc/systemd/system/park-monitor.service
```

Paste the systemd service file (see Linux section above), then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable park-monitor
sudo systemctl start park-monitor
```

**Cost:** Free for 12 months (750 hours/month), then ~$8/month

### Google Cloud Platform

**Setup:**

1. **Create VM Instance:**
   - Go to Compute Engine → VM Instances
   - Create Instance
   - Machine type: e2-micro (Free tier)
   - Boot disk: Ubuntu 22.04 LTS
   - Allow HTTP/HTTPS traffic
   - Create

2. **Connect via SSH** (browser-based)

3. **Follow same steps as AWS** for installation and service setup

**Cost:** Free tier includes 1 e2-micro instance

### DigitalOcean

**Setup:**

1. **Create Droplet:**
   - Choose Ubuntu 22.04
   - Basic plan: $4-6/month
   - Choose datacenter region
   - Add SSH key
   - Create

2. **Connect and Setup:**
```bash
ssh root@your-droplet-ip
```

3. **Follow Linux setup steps**

**Cost:** $4-6/month

### Heroku (Simple but Paid)

**Setup:**

1. **Install Heroku CLI:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Create Procfile:**
```
worker: python park_monitor.py
```

3. **Deploy:**
```bash
heroku login
heroku create your-park-monitor
git init
git add .
git commit -m "Initial commit"
git push heroku main
heroku ps:scale worker=1
```

**Cost:** ~$7/month for hobby dyno

---

## Docker Deployment

### Local Docker

**Build and Run:**

```bash
# Build image
docker build -t park-monitor .

# Run container
docker run -d \
  --name park-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/logs:/app/logs \
  park-monitor
```

**Using Docker Compose:**

```bash
docker-compose up -d
```

**View Logs:**
```bash
docker logs -f park-monitor
```

**Stop:**
```bash
docker stop park-monitor
```

### Docker on Cloud

**AWS ECS:**

1. Push image to ECR
2. Create ECS cluster
3. Create task definition
4. Run task

**Google Cloud Run:**

```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/park-monitor
gcloud run deploy park-monitor --image gcr.io/PROJECT-ID/park-monitor
```

---

## Raspberry Pi

Perfect for 24/7 home deployment with minimal power consumption.

**Setup:**

1. **Install Raspberry Pi OS:**
   - Use Raspberry Pi Imager
   - Choose Raspberry Pi OS Lite (64-bit)
   - Configure WiFi and SSH

2. **Connect and Update:**
```bash
ssh pi@raspberrypi.local
sudo apt update && sudo apt upgrade -y
```

3. **Install Python and Dependencies:**
```bash
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

4. **Copy Files:**
```bash
# From your computer
scp -r * pi@raspberrypi.local:~/park-monitor/
```

5. **Setup as Service:**
```bash
sudo nano /etc/systemd/system/park-monitor.service
```

Use the systemd service file from Linux section, then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable park-monitor
sudo systemctl start park-monitor
```

**Advantages:**
- Low power consumption (~3-5W)
- One-time cost (~$35-75)
- Runs 24/7 at home
- No monthly fees

---

## Monitoring & Maintenance

### Check if Service is Running

**Linux/Mac:**
```bash
ps aux | grep park_monitor
```

**Docker:**
```bash
docker ps | grep park-monitor
```

**Systemd:**
```bash
sudo systemctl status park-monitor
```

### View Logs

**File logs:**
```bash
tail -f availability_monitor.log
```

**Systemd logs:**
```bash
sudo journalctl -u park-monitor -f
```

**Docker logs:**
```bash
docker logs -f park-monitor
```

### Restart Service

**Systemd:**
```bash
sudo systemctl restart park-monitor
```

**Docker:**
```bash
docker restart park-monitor
```

### Update Configuration

1. Edit `config.yaml`
2. Restart the service

**Systemd:**
```bash
sudo systemctl restart park-monitor
```

**Docker:**
```bash
docker restart park-monitor
```

### Update Code

1. Pull/download new code
2. Restart service

**Docker:**
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Backup Configuration

**Important:** Backup your `config.yaml` (contains passwords)

```bash
# Create backup
cp config.yaml config.yaml.backup

# Secure it
chmod 600 config.yaml.backup
```

### Monitor Resource Usage

**Check CPU/Memory:**
```bash
top
htop  # if installed
```

**Check disk space:**
```bash
df -h
```

**Check log file size:**
```bash
du -h availability_monitor.log
```

### Log Rotation

Prevent logs from filling disk:

**Create `/etc/logrotate.d/park-monitor`:**
```
/path/to/availability_monitor.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### Health Checks

**Create a simple health check script:**

```bash
#!/bin/bash
# health_check.sh

if pgrep -f park_monitor.py > /dev/null; then
    echo "✓ Park monitor is running"
    exit 0
else
    echo "✗ Park monitor is not running"
    # Optionally restart
    sudo systemctl restart park-monitor
    exit 1
fi
```

**Run via cron every hour:**
```bash
crontab -e
# Add:
0 * * * * /path/to/health_check.sh
```

---

## Troubleshooting

### Service Won't Start

1. Check logs for errors
2. Verify Python path in service file
3. Check file permissions
4. Verify config.yaml is valid

### High CPU Usage

- Increase `check_interval_minutes` in config
- Check for infinite loops in logs

### Memory Issues

- Monitor log file size
- Implement log rotation
- Restart service periodically

### Network Issues

- Check internet connectivity
- Verify firewall rules
- Test Recreation.gov accessibility

### Email Not Sending

- Verify SMTP credentials
- Check firewall/security groups allow outbound port 587
- Test with `test_monitor.py`

---

## Security Best Practices

1. **Never commit config.yaml to git** (contains passwords)
2. **Use environment variables** for sensitive data
3. **Restrict file permissions:**
   ```bash
   chmod 600 config.yaml
   ```
4. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```
5. **Use SSH keys** instead of passwords
6. **Enable firewall:**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   ```

---

## Cost Comparison

| Option | Setup Difficulty | Monthly Cost | Reliability |
|--------|-----------------|--------------|-------------|
| Local Computer | Easy | $0 (electricity) | Medium |
| Raspberry Pi | Medium | $0 (after purchase) | High |
| AWS EC2 Free Tier | Medium | $0 (12 months) | High |
| DigitalOcean | Easy | $4-6 | High |
| Google Cloud | Medium | $0 (free tier) | High |
| Heroku | Easy | $7 | High |

---

## Recommended Setup

**For Beginners:** Start with local computer or Raspberry Pi

**For Reliability:** AWS EC2 or DigitalOcean

**For Simplicity:** Heroku or Google Cloud Run

**For Cost:** Raspberry Pi (one-time cost) or AWS Free Tier

---

## Getting Help

If you encounter issues:

1. Check logs first
2. Run `python test_monitor.py`
3. Verify configuration
4. Check network connectivity
5. Review this guide's troubleshooting section

---

**Happy Deploying! 🚀**