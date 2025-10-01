#!/usr/bin/env python3
"""
California National Parks Availability Monitor
Monitors Recreation.gov for camping and permit availability in June 2026
"""

import requests
import yaml
import logging
import time
import smtplib
import json
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import schedule


class ParkAvailabilityMonitor:
    """Monitor national park availability and send notifications"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the monitor with configuration"""
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.base_url = "https://www.recreation.gov/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.found_availability = {}  # Track what we've already notified about
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            raise
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        # Create logger
        self.logger = logging.getLogger('ParkMonitor')
        self.logger.setLevel(log_level)
        
        # File handler
        if log_config.get('log_file'):
            fh = logging.FileHandler(log_config['log_file'])
            fh.setLevel(log_level)
            fh.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(fh)
        
        # Console handler
        if log_config.get('console_output', True):
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(ch)
    
    def check_campground_availability(self, park_id: str, park_name: str) -> List[Dict]:
        """Check campground availability for a specific park"""
        self.logger.info(f"Checking campground availability for {park_name}")
        
        available_sites = []
        start_date = self.config['target_dates']['start_date']
        end_date = self.config['target_dates']['end_date']
        
        try:
            # Get campgrounds for the park
            campgrounds_url = f"{self.base_url}/search"
            params = {
                'fq': f'entity_id:{park_id}',
                'start': 0,
                'size': 100
            }
            
            response = self.session.get(campgrounds_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                for campground in results:
                    if campground.get('entity_type') == 'campground':
                        campground_id = campground.get('entity_id')
                        campground_name = campground.get('name')
                        
                        # Check availability for this campground
                        avail = self._check_specific_campground(
                            campground_id, 
                            campground_name,
                            start_date,
                            end_date
                        )
                        if avail:
                            available_sites.extend(avail)
            else:
                self.logger.warning(f"Failed to fetch campgrounds for {park_name}: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error checking {park_name}: {e}")
        
        return available_sites
    
    def _check_specific_campground(self, campground_id: str, campground_name: str, 
                                   start_date: str, end_date: str) -> List[Dict]:
        """Check availability for a specific campground"""
        available = []
        
        try:
            # Recreation.gov availability API endpoint
            avail_url = f"{self.base_url}/camps/availability/campground/{campground_id}"
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            response = self.session.get(avail_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                campsites = data.get('campsites', {})
                
                for site_id, site_data in campsites.items():
                    site_name = site_data.get('site')
                    availabilities = site_data.get('availabilities', {})
                    
                    # Check each date in June 2026
                    available_dates = [
                        date for date, status in availabilities.items()
                        if status == 'Available'
                    ]
                    
                    if available_dates:
                        available.append({
                            'campground_name': campground_name,
                            'campground_id': campground_id,
                            'site_name': site_name,
                            'site_id': site_id,
                            'available_dates': available_dates
                        })
                        
        except Exception as e:
            self.logger.debug(f"Error checking campground {campground_id}: {e}")
        
        return available
    
    def check_permit_availability(self, park_id: str, park_name: str) -> List[Dict]:
        """Check permit availability for a specific park"""
        self.logger.info(f"Checking permit availability for {park_name}")
        
        available_permits = []
        
        try:
            # Search for permits/tickets for this park
            permits_url = f"{self.base_url}/search"
            params = {
                'fq': f'entity_id:{park_id}',
                'fq': 'entity_type:ticket',
                'start': 0,
                'size': 100
            }
            
            response = self.session.get(permits_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                for permit in results:
                    permit_id = permit.get('entity_id')
                    permit_name = permit.get('name')
                    
                    # Check if permits are available for June 2026
                    if self._check_permit_dates(permit_id):
                        available_permits.append({
                            'permit_name': permit_name,
                            'permit_id': permit_id,
                            'park_name': park_name
                        })
                        
        except Exception as e:
            self.logger.error(f"Error checking permits for {park_name}: {e}")
        
        return available_permits
    
    def _check_permit_dates(self, permit_id: str) -> bool:
        """Check if a specific permit has availability"""
        try:
            # This would need to be customized based on the specific permit API
            # Recreation.gov has different endpoints for different permit types
            return False  # Placeholder
        except Exception as e:
            self.logger.debug(f"Error checking permit {permit_id}: {e}")
            return False
    
    def send_email_notification(self, subject: str, body: str):
        """Send email notification"""
        if not self.config['notifications']['email']['enabled']:
            return
        
        try:
            email_config = self.config['notifications']['email']
            
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = ', '.join(email_config['recipient_emails'])
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)
            
            self.logger.info(f"Email notification sent: {subject}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
    
    def send_webhook_notification(self, data: dict):
        """Send webhook notification (Slack, Discord, etc.)"""
        if not self.config['notifications']['webhook']['enabled']:
            return
        
        try:
            webhook_url = self.config['notifications']['webhook']['url']
            
            # Format for Slack/Discord
            payload = {
                'text': f"🏕️ New Availability Found!\n\n{json.dumps(data, indent=2)}"
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("Webhook notification sent successfully")
            else:
                self.logger.warning(f"Webhook notification failed: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Failed to send webhook: {e}")
    
    def send_sms_notification(self, message: str):
        """Send SMS notification via Twilio"""
        if not self.config['notifications']['sms']['enabled']:
            return
        
        try:
            from twilio.rest import Client
            
            sms_config = self.config['notifications']['sms']
            client = Client(sms_config['twilio_account_sid'], sms_config['twilio_auth_token'])
            
            for recipient in sms_config['recipient_phone_numbers']:
                client.messages.create(
                    body=message,
                    from_=sms_config['twilio_phone_number'],
                    to=recipient
                )
            
            self.logger.info("SMS notification sent successfully")
            
        except ImportError:
            self.logger.error("Twilio library not installed. Run: pip install twilio")
        except Exception as e:
            self.logger.error(f"Failed to send SMS: {e}")
    
    def format_notification_message(self, park_name: str, available_sites: List[Dict], 
                                   available_permits: List[Dict]) -> tuple:
        """Format notification message for email and other channels"""
        
        # HTML email body
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h2 {{ color: #2c5f2d; }}
                .site {{ background-color: #f0f8f0; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .permit {{ background-color: #f0f0f8; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .dates {{ color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h2>🏕️ New Availability Found for {park_name}!</h2>
            <p><strong>Target Period:</strong> June 2026</p>
        """
        
        if available_sites:
            html_body += "<h3>Available Campsites:</h3>"
            for site in available_sites:
                dates_str = ', '.join(site['available_dates'][:5])
                if len(site['available_dates']) > 5:
                    dates_str += f" ... (+{len(site['available_dates']) - 5} more)"
                
                html_body += f"""
                <div class="site">
                    <strong>{site['campground_name']}</strong> - {site['site_name']}<br>
                    <span class="dates">Available dates: {dates_str}</span><br>
                    <a href="https://www.recreation.gov/camping/campgrounds/{site['campground_id']}">Book Now</a>
                </div>
                """
        
        if available_permits:
            html_body += "<h3>Available Permits:</h3>"
            for permit in available_permits:
                html_body += f"""
                <div class="permit">
                    <strong>{permit['permit_name']}</strong><br>
                    <a href="https://www.recreation.gov/ticket/{permit['permit_id']}">Check Availability</a>
                </div>
                """
        
        html_body += """
            <p><em>This is an automated notification from your California National Parks Availability Monitor.</em></p>
        </body>
        </html>
        """
        
        # Plain text for SMS
        text_body = f"New availability in {park_name} for June 2026! "
        if available_sites:
            text_body += f"{len(available_sites)} campsites available. "
        if available_permits:
            text_body += f"{len(available_permits)} permits available. "
        text_body += "Check your email for details."
        
        return html_body, text_body
    
    def check_all_parks(self):
        """Check availability for all configured parks"""
        self.logger.info("=" * 60)
        self.logger.info("Starting availability check for all parks")
        self.logger.info("=" * 60)
        
        for park in self.config['parks']:
            park_name = park['name']
            park_id = park['park_id']
            
            self.logger.info(f"\nChecking {park_name}...")
            
            available_sites = []
            available_permits = []
            
            # Check camping availability
            if park.get('check_camping', True):
                available_sites = self.check_campground_availability(park_id, park_name)
            
            # Check permit availability
            if park.get('check_permits', False):
                available_permits = self.check_permit_availability(park_id, park_name)
            
            # Send notifications if new availability found
            if available_sites or available_permits:
                notification_key = f"{park_name}_{len(available_sites)}_{len(available_permits)}"
                
                # Only notify if this is new availability
                if notification_key not in self.found_availability:
                    self.logger.info(f"✓ Found availability in {park_name}!")
                    
                    html_msg, text_msg = self.format_notification_message(
                        park_name, available_sites, available_permits
                    )
                    
                    # Send notifications
                    self.send_email_notification(
                        f"🏕️ Availability Found: {park_name} - June 2026",
                        html_msg
                    )
                    
                    self.send_webhook_notification({
                        'park': park_name,
                        'campsites': len(available_sites),
                        'permits': len(available_permits)
                    })
                    
                    self.send_sms_notification(text_msg)
                    
                    # Mark as notified
                    self.found_availability[notification_key] = datetime.now()
            else:
                self.logger.info(f"✗ No availability found in {park_name}")
            
            # Be respectful with API calls
            time.sleep(2)
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Availability check completed")
        self.logger.info("=" * 60 + "\n")
    
    def run_once(self):
        """Run a single check cycle"""
        try:
            self.check_all_parks()
        except Exception as e:
            self.logger.error(f"Error during check cycle: {e}")
    
    def run_scheduled(self):
        """Run the monitor on a schedule"""
        interval = self.config['monitoring']['check_interval_minutes']
        
        self.logger.info(f"Starting scheduled monitoring (checking every {interval} minutes)")
        self.logger.info("Press Ctrl+C to stop\n")
        
        # Run immediately on start
        self.run_once()
        
        # Schedule regular checks
        schedule.every(interval).minutes.do(self.run_once)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.logger.info("\nMonitoring stopped by user")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Monitor California National Parks for June 2026 availability'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (default: run continuously)'
    )
    
    args = parser.parse_args()
    
    monitor = ParkAvailabilityMonitor(args.config)
    
    if args.once:
        monitor.run_once()
    else:
        monitor.run_scheduled()


if __name__ == '__main__':
    main()