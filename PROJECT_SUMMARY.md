# California National Parks Availability Monitor - Project Summary

## Overview

This is a complete, production-ready AI agent that monitors California national parks for camping and permit availability in June 2026 and sends notifications when slots become available.

## What's Included

### Core Files

1. **park_monitor.py** (17.8 KB)
   - Main monitoring agent
   - Checks Recreation.gov API for availability
   - Sends notifications via email, webhook, and SMS
   - Includes error handling, retry logic, and logging
   - Runs continuously on a schedule

2. **config.yaml** (2.2 KB)
   - Configuration file for all settings
   - Parks to monitor (8 California national parks)
   - Target dates (June 2026)
   - Notification settings (email, webhook, SMS)
   - Monitoring intervals and logging preferences

3. **requirements.txt** (245 bytes)
   - Python dependencies
   - Minimal requirements for easy installation

### Documentation

4. **README.md** (8.6 KB)
   - Comprehensive documentation
   - Feature overview
   - Installation instructions
   - Configuration guide
   - Usage examples
   - Troubleshooting section

5. **QUICK_START.md** (4.8 KB)
   - 5-minute setup guide
   - Step-by-step instructions
   - Common configurations
   - Pro tips for success

6. **DEPLOYMENT_GUIDE.md** (11.5 KB)
   - Multiple deployment options
   - Cloud deployment (AWS, GCP, DigitalOcean)
   - Docker deployment
   - Raspberry Pi setup
   - Monitoring and maintenance
   - Security best practices

### Testing & Configuration

7. **test_monitor.py** (6.5 KB)
   - Configuration validation
   - Test notification system
   - Verify setup before running

8. **.env.example** (710 bytes)
   - Environment variables template
   - Alternative to editing config.yaml

### Deployment Files

9. **Dockerfile** (333 bytes)
   - Docker container configuration
   - For containerized deployment

10. **docker-compose.yml** (352 bytes)
    - Docker Compose configuration
    - Easy container orchestration

11. **.gitignore** (419 bytes)
    - Git ignore rules
    - Protects sensitive configuration

## Features

### Monitoring Capabilities

✅ **8 California National Parks:**
- Yosemite National Park
- Sequoia & Kings Canyon National Parks
- Joshua Tree National Park
- Death Valley National Park
- Channel Islands National Park
- Redwood National and State Parks
- Lassen Volcanic National Park
- Pinnacles National Park

✅ **Availability Checking:**
- Campground availability
- Permit/ticket availability
- Specific date ranges (June 2026)
- Multiple sites per park

✅ **Smart Notifications:**
- Email (SMTP)
- Webhook (Slack, Discord, etc.)
- SMS (Twilio)
- Avoids duplicate notifications
- Includes direct booking links

### Technical Features

✅ **Robust Implementation:**
- Error handling and retry logic
- Configurable check intervals
- Detailed logging
- Session management
- Rate limiting respect

✅ **Flexible Deployment:**
- Run locally
- Cloud deployment (AWS, GCP, etc.)
- Docker containers
- Raspberry Pi
- Background service

✅ **Easy Configuration:**
- YAML configuration file
- Environment variables support
- Test script included
- Multiple notification channels

## How It Works

### Data Source
Uses **Recreation.gov API** - the official reservation system for U.S. national parks.

### Monitoring Process
1. Queries Recreation.gov for each configured park
2. Checks campground availability for June 2026
3. Checks permit/ticket availability (if enabled)
4. Compares results with previous checks
5. Sends notifications when new availability is found

### Notification Flow
1. Availability detected
2. Formats notification message with details
3. Sends via configured channels (email, webhook, SMS)
4. Tracks notification to avoid duplicates
5. Provides direct booking links

### Scheduling
- Runs continuously in a loop
- Configurable check interval (default: 60 minutes)
- Respectful API usage with delays
- Automatic retry on failures

## Setup Time

- **Minimum Setup:** 5 minutes (email only)
- **Full Setup:** 15-30 minutes (all features)
- **Deployment:** 30-60 minutes (cloud/Docker)

## Requirements

### System Requirements
- Python 3.11 or higher
- Internet connection
- 50 MB disk space
- Minimal CPU/RAM (runs efficiently)

### Account Requirements
- Email account (Gmail recommended)
- Optional: Twilio account for SMS
- Optional: Slack/Discord for webhooks

## Usage Scenarios

### Scenario 1: Personal Use
- Monitor favorite parks
- Get notified when reservations open
- Book quickly before sites fill up

### Scenario 2: Group Planning
- Monitor multiple parks
- Share notifications with group
- Coordinate booking strategy

### Scenario 3: Flexible Travel
- Monitor all parks
- Take first available
- Maximize chances of getting a spot

## Timeline

### Current Status (September 2025)
- Reservations for June 2026 not yet open
- Monitor will show "No availability found"
- This is expected and normal

### December 2025
- Reservations for June 2026 will open
- Monitor will detect availability
- Notifications will be sent
- **Action required:** Book quickly!

### June 2026
- Enjoy your camping trip! 🏕️

## Success Tips

1. **Start Early**
   - Set up the monitor now
   - Test notifications work
   - Be ready when reservations open

2. **Be Prepared**
   - Create Recreation.gov account now
   - Save payment information
   - Have backup dates/parks in mind

3. **Act Fast**
   - Popular sites book in minutes
   - Have phone/computer ready
   - Multiple notification methods help

4. **Be Flexible**
   - Consider weekdays vs weekends
   - Multiple parks increase chances
   - Alternative dates as backup

## Support & Maintenance

### Monitoring
- Check logs periodically
- Verify service is running
- Test notifications monthly

### Updates
- Configuration changes: Edit config.yaml and restart
- Code updates: Pull new version and restart
- No updates needed for normal operation

### Troubleshooting
- Comprehensive troubleshooting in README.md
- Test script for validation
- Detailed error logging

## Security & Privacy

✅ **Secure by Design:**
- Credentials stored locally only
- No data sent to third parties
- HTTPS for all API calls
- Configurable notification privacy

✅ **Best Practices:**
- Use app-specific passwords
- Restrict file permissions
- Keep software updated
- Don't commit config to git

## Cost Analysis

### Free Options
- Local computer (electricity only)
- AWS Free Tier (12 months)
- Google Cloud Free Tier
- Raspberry Pi (one-time ~$50)

### Paid Options
- DigitalOcean: $4-6/month
- Heroku: $7/month
- SMS notifications: Pay per message

### Recommended
- **Budget:** Raspberry Pi or local computer
- **Reliability:** AWS EC2 or DigitalOcean
- **Simplicity:** Heroku or Google Cloud Run

## Limitations & Disclaimers

### Limitations
- Cannot guarantee you'll get a reservation
- Recreation.gov may change their API
- High competition for popular sites
- Some parks use lottery systems

### Disclaimers
- Not affiliated with Recreation.gov or NPS
- For personal use only
- Respect API rate limits
- Use responsibly

### Legal
- Complies with Recreation.gov terms of service
- Reasonable request intervals
- No automated booking (notifications only)
- User must manually complete reservations

## Future Enhancements

Possible improvements (not included):
- Web dashboard for monitoring
- Historical availability tracking
- Price monitoring
- Automated booking (requires careful implementation)
- Mobile app
- Multi-user support

## Project Statistics

- **Total Files:** 11
- **Total Lines of Code:** ~800
- **Documentation Pages:** 4
- **Setup Time:** 5-30 minutes
- **Supported Parks:** 8
- **Notification Methods:** 3
- **Deployment Options:** 6+

## Quick Links

- **Start Here:** QUICK_START.md
- **Full Documentation:** README.md
- **Deployment:** DEPLOYMENT_GUIDE.md
- **Test Setup:** `python test_monitor.py`
- **Run Monitor:** `python park_monitor.py`

## Contact & Support

This is an open-source project provided as-is. For issues:
1. Check documentation
2. Review logs
3. Run test script
4. Verify configuration

## License

Provided for personal use. Use responsibly and in accordance with Recreation.gov's terms of service.

---

## Getting Started

1. **Read QUICK_START.md** (5 minutes)
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Configure email in config.yaml**
4. **Test setup:** `python test_monitor.py`
5. **Run monitor:** `python park_monitor.py`

---

**Ready to secure your California camping adventure! 🏕️🌲**

*Created: September 2025*
*Target: June 2026 Reservations*
*Status: Production Ready*