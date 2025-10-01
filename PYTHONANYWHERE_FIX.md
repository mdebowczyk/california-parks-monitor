# Fixing PythonAnywhere Proxy Error

## The Problem

You're seeing this error:
```
ProxyError('Unable to connect to proxy', OSError('Tunnel connection failed: 403 Forbidden'))
```

**Cause:** PythonAnywhere's free tier restricts outbound internet access to a whitelist of approved sites. Recreation.gov is NOT on this whitelist.

## Solutions

### Option 1: Upgrade PythonAnywhere (Simplest)

**Cost:** $5/month for "Hacker" plan

**Steps:**
1. Go to PythonAnywhere dashboard
2. Click "Account" → "Upgrade"
3. Select "Hacker" plan
4. Your script will work immediately

### Option 2: Oracle Cloud Free Tier (BEST FREE OPTION)

**Cost:** $0 forever (truly free, not trial)

**What you get:**
- 2 AMD VMs (1GB RAM each)
- 200GB storage
- Full internet access
- No restrictions

**Setup Steps:**

1. **Sign up:**
   - Go to https://www.oracle.com/cloud/free/
   - Create account (credit card required for verification, won't charge)

2. **Create VM:**
   - Click "Create a VM Instance"
   - Choose "Ubuntu 22.04"
   - Select "Always Free Eligible" shape (VM.Standard.E2.1.Micro)
   - Download SSH private key
   - Click "Create"

3. **Connect to VM:**
   ```bash
   ssh -i your-private-key.key ubuntu@your-vm-ip-address
   ```

4. **Install Python and dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git
   ```

5. **Upload your project:**
   
   **Method A - Using Git (recommended):**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
   
   **Method B - Using SCP from your computer:**
   ```bash
   # From your local computer
   scp -i your-private-key.key -r /path/to/project ubuntu@your-vm-ip:~/
   ```

6. **Install requirements:**
   ```bash
   cd your-project-folder
   pip3 install -r requirements.txt
   ```

7. **Configure:**
   ```bash
   nano config.yaml
   # Edit your email settings
   ```

8. **Test:**
   ```bash
   python3 park_monitor.py --once
   ```

9. **Set up as service (runs 24/7):**
   ```bash
   sudo nano /etc/systemd/system/park-monitor.service
   ```
   
   Paste this:
   ```ini
   [Unit]
   Description=California Parks Availability Monitor
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/your-project-folder
   ExecStart=/usr/bin/python3 /home/ubuntu/your-project-folder/park_monitor.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

10. **Enable and start:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable park-monitor
    sudo systemctl start park-monitor
    ```

11. **Check status:**
    ```bash
    sudo systemctl status park-monitor
    ```

12. **View logs:**
    ```bash
    sudo journalctl -u park-monitor -f
    ```

### Option 3: Render Free Tier

**Cost:** $0 (750 hours/month free)

**Steps:**

1. **Sign up:** https://render.com

2. **Connect GitHub:**
   - Push your code to GitHub
   - Connect repository to Render

3. **Create Background Worker:**
   - Click "New +"
   - Select "Background Worker"
   - Choose your repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `python park_monitor.py`

4. **Deploy**

**Note:** Service may spin down after inactivity. Add this to keep it alive:

```python
# Add to park_monitor.py
import os
if os.environ.get('RENDER'):
    # Render-specific keep-alive
    pass
```

### Option 4: Google Cloud Run

**Cost:** $0 (within free tier limits)

**Requirements:** Modify script to work as HTTP service

**Steps:**

1. **Install Google Cloud SDK**

2. **Authenticate:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/park-monitor
   gcloud run deploy park-monitor \
     --image gcr.io/YOUR_PROJECT_ID/park-monitor \
     --platform managed \
     --region us-central1
   ```

4. **Set up Cloud Scheduler** to trigger daily

### Option 5: Run Locally

**Cost:** $0 (just electricity)

**Windows:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily
4. Action: Start program
   - Program: `python`
   - Arguments: `C:\path\to\park_monitor.py`

**Mac/Linux:**
See DEPLOYMENT_GUIDE.md for systemd/launchd setup

### Option 6: Raspberry Pi

**Cost:** $35-75 one-time

**Power:** ~3-5W (very low)

**Setup:**
1. Install Raspberry Pi OS
2. Follow Linux deployment guide
3. Runs 24/7 at home

## Comparison Table

| Platform | Cost | Internet Access | Setup | Reliability |
|----------|------|-----------------|-------|-------------|
| PythonAnywhere Free | $0 | ❌ Blocked | Easy | N/A |
| PythonAnywhere Paid | $5/mo | ✅ Full | Easy | High |
| **Oracle Cloud Free** | **$0** | **✅ Full** | **Medium** | **High** |
| Render Free | $0 | ✅ Full | Easy | Medium |
| Google Cloud Run | $0* | ✅ Full | Hard | High |
| Local Computer | $0 | ✅ Full | Easy | Medium |
| Raspberry Pi | $35-75 | ✅ Full | Medium | High |

## Recommended Solution

**For completely free hosting:** Use **Oracle Cloud Free Tier**

**Why:**
- ✅ Truly free forever (not a trial)
- ✅ No internet restrictions
- ✅ Full VM control
- ✅ Reliable infrastructure
- ✅ Can run 24/7

**For simplicity:** Upgrade PythonAnywhere to $5/month

## Quick Test on Your Computer

Before deploying anywhere, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Edit config
nano config.yaml

# Test once
python park_monitor.py --once

# If it works, run continuously
python park_monitor.py
```

## Need Help?

1. **Oracle Cloud setup issues:** Check their documentation at https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
2. **Script errors:** Check `availability_monitor.log`
3. **Email not working:** Run `python test_monitor.py`

## Next Steps

1. Choose a hosting option (Oracle Cloud recommended)
2. Follow the setup steps above
3. Test with `python park_monitor.py --once`
4. Set up as service for 24/7 operation
5. Monitor logs to ensure it's working

Your script will work perfectly once deployed to any platform with full internet access!