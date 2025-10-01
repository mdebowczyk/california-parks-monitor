#!/usr/bin/env python3
"""
Test script for the park availability monitor
Tests configuration and notification systems without making actual API calls
"""

import yaml
import sys
from park_monitor import ParkAvailabilityMonitor


def test_configuration():
    """Test if configuration file is valid"""
    print("Testing configuration...")
    try:
        monitor = ParkAvailabilityMonitor('config.yaml')
        print("✓ Configuration loaded successfully")
        
        # Check parks
        parks = monitor.config.get('parks', [])
        print(f"✓ Found {len(parks)} parks configured")
        
        # Check dates
        start_date = monitor.config['target_dates']['start_date']
        end_date = monitor.config['target_dates']['end_date']
        print(f"✓ Target dates: {start_date} to {end_date}")
        
        return monitor
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return None


def test_email_config(monitor):
    """Test email configuration"""
    print("\nTesting email configuration...")
    
    email_config = monitor.config['notifications']['email']
    
    if not email_config.get('enabled'):
        print("⚠ Email notifications are disabled")
        return
    
    required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password', 'recipient_emails']
    missing = [field for field in required_fields if not email_config.get(field)]
    
    if missing:
        print(f"✗ Missing email configuration: {', '.join(missing)}")
    else:
        print("✓ Email configuration looks good")
        print(f"  SMTP Server: {email_config['smtp_server']}:{email_config['smtp_port']}")
        print(f"  Sender: {email_config['sender_email']}")
        print(f"  Recipients: {len(email_config['recipient_emails'])}")


def test_webhook_config(monitor):
    """Test webhook configuration"""
    print("\nTesting webhook configuration...")
    
    webhook_config = monitor.config['notifications']['webhook']
    
    if not webhook_config.get('enabled'):
        print("⚠ Webhook notifications are disabled")
        return
    
    if webhook_config.get('url'):
        print("✓ Webhook URL configured")
        print(f"  URL: {webhook_config['url'][:50]}...")
    else:
        print("✗ Webhook URL not configured")


def test_sms_config(monitor):
    """Test SMS configuration"""
    print("\nTesting SMS configuration...")
    
    sms_config = monitor.config['notifications']['sms']
    
    if not sms_config.get('enabled'):
        print("⚠ SMS notifications are disabled")
        return
    
    required_fields = ['twilio_account_sid', 'twilio_auth_token', 'twilio_phone_number', 'recipient_phone_numbers']
    missing = [field for field in required_fields if not sms_config.get(field)]
    
    if missing:
        print(f"✗ Missing SMS configuration: {', '.join(missing)}")
    else:
        print("✓ SMS configuration looks good")
        print(f"  Twilio Account: {sms_config['twilio_account_sid'][:10]}...")
        print(f"  Recipients: {len(sms_config['recipient_phone_numbers'])}")


def test_notification_system(monitor):
    """Test sending a test notification"""
    print("\nTesting notification system...")
    print("Would you like to send a test notification? (y/n): ", end='')
    
    try:
        response = input().strip().lower()
        if response == 'y':
            print("\nSending test notifications...")
            
            # Test email
            if monitor.config['notifications']['email']['enabled']:
                try:
                    monitor.send_email_notification(
                        "Test: Park Monitor Setup Complete",
                        "<h2>Test Notification</h2><p>Your California National Parks monitor is configured correctly!</p>"
                    )
                    print("✓ Test email sent")
                except Exception as e:
                    print(f"✗ Email test failed: {e}")
            
            # Test webhook
            if monitor.config['notifications']['webhook']['enabled']:
                try:
                    monitor.send_webhook_notification({
                        'test': True,
                        'message': 'Park monitor test notification'
                    })
                    print("✓ Test webhook sent")
                except Exception as e:
                    print(f"✗ Webhook test failed: {e}")
            
            # Test SMS
            if monitor.config['notifications']['sms']['enabled']:
                try:
                    monitor.send_sms_notification(
                        "Test: Your California National Parks monitor is set up correctly!"
                    )
                    print("✓ Test SMS sent")
                except Exception as e:
                    print(f"✗ SMS test failed: {e}")
        else:
            print("Skipping notification test")
    except KeyboardInterrupt:
        print("\nTest cancelled")


def main():
    """Run all tests"""
    print("=" * 60)
    print("California National Parks Monitor - Configuration Test")
    print("=" * 60)
    
    monitor = test_configuration()
    
    if not monitor:
        print("\n✗ Configuration test failed. Please fix config.yaml and try again.")
        sys.exit(1)
    
    test_email_config(monitor)
    test_webhook_config(monitor)
    test_sms_config(monitor)
    
    print("\n" + "=" * 60)
    print("Configuration Summary")
    print("=" * 60)
    
    enabled_notifications = []
    if monitor.config['notifications']['email']['enabled']:
        enabled_notifications.append("Email")
    if monitor.config['notifications']['webhook']['enabled']:
        enabled_notifications.append("Webhook")
    if monitor.config['notifications']['sms']['enabled']:
        enabled_notifications.append("SMS")
    
    if enabled_notifications:
        print(f"✓ Enabled notifications: {', '.join(enabled_notifications)}")
    else:
        print("⚠ No notifications enabled - you won't receive alerts!")
    
    print(f"✓ Monitoring {len(monitor.config['parks'])} parks")
    print(f"✓ Check interval: {monitor.config['monitoring']['check_interval_minutes']} minutes")
    
    test_notification_system(monitor)
    
    print("\n" + "=" * 60)
    print("Test complete! You're ready to run the monitor.")
    print("Run: python park_monitor.py")
    print("=" * 60)


if __name__ == '__main__':
    main()