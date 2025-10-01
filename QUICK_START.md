# Quick Start Guide

Get your California National Parks availability monitor running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Email Notifications (2 minutes)

### For Gmail Users:

1. **Enable 2-Factor Authentication** on your Google account
   - Go to: https://myaccount.google.com/security

2. **Create an App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Edit config.yaml**
   - Open `config.yaml` in a text editor
   - Find the email section:
   ```yaml
   notifications:
     email:
       enabled: true
       smtp_server: "smtp.gmail.com"
       smtp_port: 587
       sender_email: "YOUR-EMAIL@gmail.com"  # ← Change this
       sender_password: "YOUR-APP-PASSWORD"   # ← Paste app password here
       recipient_emails:
         - "YOUR-EMAIL@gmail.com"             # ← Change this
   ```

### For Other Email Providers:

**Outlook/Hotmail:**
```yaml
smtp_server: "smtp-mail.outlook.com"
smtp_port: 587
```

**Yahoo:**
```yaml
smtp_server: "smtp.mail.yahoo.com"
smtp_port: 587
```

## Step 3: Test Your Setup (1 minute)

```bash
python test_monitor.py
```

This will:
- Verify your configuration
- Optionally send a test notification
- Confirm everything is working

## Step 4: Run the Monitor

```bash
python park_monitor.py
```

That's it! The monitor will now:
- Check for availability every hour
- Send you email notifications when spots open up
- Keep running until you stop it (Ctrl+C)

## What to Expect

### When Will Reservations Open?

For **June 2026** camping:
- Reservations typically open **6 months in advance**
- This means **December 2025** for June 2026
- The monitor will keep checking and notify you when they open

### First Run

On the first run, you'll likely see:
```
✗ No availability found in Yosemite National Park
✗ No availability found in Sequoia & Kings Canyon National Parks
...
```

This is normal! Reservations aren't open yet.

### When Availability Opens

You'll receive an email like this:

```
Subject: 🏕️ Availability Found: Yosemite National Park - June 2026

Available Campsites:
- Upper Pines Campground - Site A001
  Available dates: 2026-06-01, 2026-06-02, 2026-06-03...
  [Book Now]
```

**Act fast!** Popular sites book within minutes.

## Customization (Optional)

### Change Check Frequency

In `config.yaml`:
```yaml
monitoring:
  check_interval_minutes: 30  # Check every 30 minutes instead of 60
```

### Monitor Specific Parks Only

In `config.yaml`, comment out parks you don't want:
```yaml
parks:
  - name: "Yosemite National Park"
    park_id: "2991"
    check_camping: true
    check_permits: true
    
  # - name: "Joshua Tree National Park"  # ← Commented out
  #   park_id: "2782"
  #   check_camping: true
```

### Change Target Dates

In `config.yaml`:
```yaml
target_dates:
  start_date: "2026-06-15"  # Only check mid-June onwards
  end_date: "2026-06-30"
```

## Running 24/7

### On Your Computer

Just leave the terminal window open. The program runs continuously.

### On a Server (Recommended)

Deploy to a cloud server so it runs even when your computer is off:
- AWS EC2 (Free tier available)
- Google Cloud Compute Engine
- DigitalOcean Droplet ($5/month)
- Raspberry Pi at home

See README.md for detailed deployment instructions.

## Troubleshooting

### "No module named 'yaml'"
```bash
pip install pyyaml
```

### "Authentication failed" (Email)
- Make sure you're using an **app password**, not your regular password
- Check that 2-factor authentication is enabled

### "No availability found" (Always)
- This is normal before reservations open
- Reservations for June 2026 will open in December 2025
- The monitor will notify you when they become available

### Need Help?

Check the full README.md for:
- Detailed troubleshooting
- Advanced configuration
- Webhook and SMS setup
- Running as a background service

## Pro Tips

1. **Create a Recreation.gov account NOW**
   - Have your account ready before reservations open
   - Save your payment information
   - This saves precious seconds when booking

2. **Be flexible with dates**
   - Consider weekdays instead of weekends
   - Have backup date ranges ready

3. **Have multiple parks in mind**
   - If Yosemite is full, Sequoia might have availability
   - The monitor checks all parks for you

4. **Set up multiple notification methods**
   - Email + SMS ensures you don't miss alerts
   - Webhook to Slack if you're at work

5. **Test before December 2025**
   - Make sure everything works before reservations open
   - Run `python test_monitor.py` periodically

---

**You're all set! Happy camping! 🏕️**