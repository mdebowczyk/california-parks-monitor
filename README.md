# California National Parks Availability Monitor

An autonomous AI agent that monitors California national parks for camping and permit availability in June 2026 and sends notifications when slots become available.

## Features

- 🏕️ **Monitors 8 California National Parks:**
  - Yosemite National Park
  - Sequoia & Kings Canyon National Parks
  - Joshua Tree National Park
  - Death Valley National Park
  - Channel Islands National Park
  - Redwood National and State Parks
  - Lassen Volcanic National Park
  - Pinnacles National Park

- 📧 **Multiple Notification Methods:**
  - Email notifications (via SMTP)
  - Webhook notifications (Slack, Discord, etc.)
  - SMS notifications (via Twilio)

- ⚙️ **Configurable Monitoring:**
  - Set custom check intervals
  - Configure which parks to monitor
  - Choose between camping and permit checks
  - Customize notification preferences

- 📊 **Smart Tracking:**
  - Avoids duplicate notifications
  - Detailed logging
  - Retry logic for failed requests

## Installation

### 1. Clone or Download

Download all the files to a directory on your computer.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If you want SMS notifications, also install Twilio:
```bash
pip install twilio
```

### 3. Configure the Agent

Edit `config.yaml` to customize your monitoring preferences:

#### Email Notifications Setup

To enable email notifications, you'll need to configure SMTP settings. For Gmail:

1. Enable 2-factor authentication on your Google account
2. Generate an app-specific password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated password
3. Update `config.yaml`:

```yaml
notifications:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    sender_email: "your-email@gmail.com"
    sender_password: "your-app-password"  # Use the app password here
    recipient_emails:
      - "your-email@gmail.com"
```

#### Webhook Notifications Setup (Optional)

For Slack:
1. Create a Slack webhook: https://api.slack.com/messaging/webhooks
2. Update `config.yaml`:

```yaml
notifications:
  webhook:
    enabled: true
    url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

For Discord:
1. Create a Discord webhook in your server settings
2. Update `config.yaml` with the webhook URL

#### SMS Notifications Setup (Optional)

1. Sign up for Twilio: https://www.twilio.com/
2. Get your Account SID, Auth Token, and phone number
3. Update `config.yaml`:

```yaml
notifications:
  sms:
    enabled: true
    twilio_account_sid: "your-account-sid"
    twilio_auth_token: "your-auth-token"
    twilio_phone_number: "+1234567890"
    recipient_phone_numbers:
      - "+1234567890"
```

#### Customize Parks and Dates

Edit the parks list and target dates in `config.yaml`:

```yaml
parks:
  - name: "Yosemite National Park"
    park_id: "2991"
    check_camping: true
    check_permits: true

target_dates:
  start_date: "2026-06-01"
  end_date: "2026-06-30"
```

#### Adjust Check Interval

```yaml
monitoring:
  check_interval_minutes: 60  # Check every hour
```

## Usage

### Run Continuously (Recommended)

This will check for availability at regular intervals:

```bash
python park_monitor.py
```

The agent will:
- Check all configured parks immediately
- Continue checking at the interval specified in config.yaml
- Send notifications when availability is found
- Run until you stop it (Ctrl+C)

### Run Once

To perform a single check and exit:

```bash
python park_monitor.py --once
```

### Use Custom Config File

```bash
python park_monitor.py --config my_custom_config.yaml
```

## How It Works

1. **Data Source:** The agent uses Recreation.gov's API, which is the official reservation system for most national parks.

2. **Monitoring Process:**
   - Queries Recreation.gov for each configured park
   - Checks campground availability for June 2026
   - Checks permit/ticket availability (if enabled)
   - Compares results with previous checks

3. **Notifications:**
   - When new availability is detected, sends notifications via configured channels
   - Tracks what has been notified to avoid spam
   - Provides direct booking links in notifications

4. **Respectful API Usage:**
   - Includes delays between requests
   - Uses appropriate user agent headers
   - Implements retry logic with backoff

## Understanding Recreation.gov Reservations

### Booking Windows

Recreation.gov typically opens reservations:
- **Camping:** 6 months in advance (rolling window)
- **Permits:** Varies by park and permit type

For June 2026 reservations:
- Camping sites will likely open in December 2025
- Some permits may open earlier (lottery systems)

### Peak Season Considerations

June is peak season for California national parks:
- High demand, especially for Yosemite and Sequoia
- Sites fill up within minutes of release
- Having an automated monitor gives you an advantage

## Troubleshooting

### No Availability Found

- **Too Early:** Reservations for June 2026 may not be open yet
- **Already Booked:** Popular sites book quickly
- **Check Dates:** Verify target dates in config.yaml

### Email Not Sending

- Verify SMTP settings
- Check that you're using an app-specific password (not your regular password)
- Check spam folder
- Review logs for error messages

### API Errors

- Recreation.gov may have rate limits
- Increase check_interval_minutes if you see frequent errors
- Check your internet connection

### Logs

Check `availability_monitor.log` for detailed information:
```bash
tail -f availability_monitor.log
```

## Advanced Configuration

### Monitor Specific Campgrounds

You can modify the code to target specific campgrounds by their IDs. Check Recreation.gov URLs for campground IDs.

### Custom Notification Templates

Edit the `format_notification_message` method in `park_monitor.py` to customize email templates.

### Add More Parks

Add any park that uses Recreation.gov to the config:

```yaml
parks:
  - name: "Your Park Name"
    park_id: "PARK_ID"  # Find this on Recreation.gov
    check_camping: true
    check_permits: false
```

## Running as a Background Service

### Linux/Mac (using systemd)

Create a service file `/etc/systemd/system/park-monitor.service`:

```ini
[Unit]
Description=California Parks Availability Monitor
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/park-monitor
ExecStart=/usr/bin/python3 /path/to/park-monitor/park_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable park-monitor
sudo systemctl start park-monitor
```

### Windows (using Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\park_monitor.py`

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "park_monitor.py"]
```

Build and run:
```bash
docker build -t park-monitor .
docker run -d --name park-monitor park-monitor
```

## Important Notes

### Recreation.gov Terms of Service

- This tool is for personal use only
- Do not abuse the API with excessive requests
- Respect rate limits and use reasonable check intervals
- The default 60-minute interval is recommended

### Booking Tips

When you receive a notification:
1. **Act quickly** - popular sites book within minutes
2. **Have an account ready** - Create a Recreation.gov account in advance
3. **Save payment info** - Speed up the checkout process
4. **Be flexible** - Consider alternative dates or campgrounds

### Limitations

- Cannot guarantee you'll get a reservation (high competition)
- Recreation.gov may change their API without notice
- Some parks have lottery systems instead of first-come-first-served
- Permit systems vary by park and may require manual checking

## Support & Contributions

This is an open-source project. Feel free to:
- Report issues
- Suggest improvements
- Contribute code enhancements
- Share your success stories!

## License

This project is provided as-is for personal use. Use responsibly and in accordance with Recreation.gov's terms of service.

## Disclaimer

This tool is not affiliated with Recreation.gov, the National Park Service, or any government agency. It is an independent monitoring tool for personal use. Always verify availability directly on Recreation.gov before making travel plans.

---

**Happy Camping! 🏕️🌲**