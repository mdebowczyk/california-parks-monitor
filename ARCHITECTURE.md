# System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    California Parks Monitor                      │
│                         (park_monitor.py)                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │ Reads Configuration
                                 ▼
                    ┌─────────────────────────┐
                    │      config.yaml        │
                    │  - Parks to monitor     │
                    │  - Target dates         │
                    │  - Notification settings│
                    │  - Check intervals      │
                    └─────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
        ┌─────────────────────┐   ┌─────────────────────┐
        │  Monitoring Loop    │   │   Logging System    │
        │  - Scheduled checks │   │  - File logging     │
        │  - Every 60 min     │   │  - Console output   │
        └─────────────────────┘   └─────────────────────┘
                    │
                    │ Makes API Requests
                    ▼
        ┌─────────────────────────────────┐
        │      Recreation.gov API         │
        │  https://www.recreation.gov/api │
        │  - Campground availability      │
        │  - Permit availability          │
        └─────────────────────────────────┘
                    │
                    │ Returns Data
                    ▼
        ┌─────────────────────────────────┐
        │    Availability Checker         │
        │  - Parse API responses          │
        │  - Filter June 2026 dates       │
        │  - Compare with previous checks │
        │  - Detect new availability      │
        └─────────────────────────────────┘
                    │
                    │ New Availability Found?
                    ▼
        ┌─────────────────────────────────┐
        │   Notification Manager          │
        │  - Format messages              │
        │  - Track sent notifications     │
        │  - Avoid duplicates             │
        └─────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    ┌──────┐  ┌─────────┐  ┌──────┐
    │Email │  │ Webhook │  │ SMS  │
    │(SMTP)│  │(Slack)  │  │(Twilio)│
    └──────┘  └─────────┘  └──────┘
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
            ┌──────────────┐
            │     User     │
            │  📧 📱 💬    │
            └──────────────┘
```

## Component Details

### 1. Main Monitor (park_monitor.py)

**Responsibilities:**
- Initialize configuration
- Setup logging
- Manage monitoring loop
- Coordinate all components

**Key Methods:**
- `__init__()` - Initialize monitor
- `check_all_parks()` - Main monitoring loop
- `run_scheduled()` - Schedule periodic checks
- `run_once()` - Single check execution

### 2. Configuration System (config.yaml)

**Structure:**
```yaml
parks:           # List of parks to monitor
target_dates:    # June 2026 date range
notifications:   # Email, webhook, SMS settings
monitoring:      # Check intervals, retries
logging:         # Log level, file location
```

**Features:**
- YAML format for easy editing
- Environment variable support
- Validation on load
- Secure credential storage

### 3. API Client

**Recreation.gov Integration:**
- Base URL: `https://www.recreation.gov/api`
- Endpoints:
  - `/search` - Find campgrounds/permits
  - `/camps/availability/campground/{id}` - Check availability
  - `/ticket/{id}` - Permit information

**Features:**
- Session management
- User-agent headers
- Timeout handling
- Retry logic

### 4. Availability Checker

**Process Flow:**
```
1. Query Recreation.gov API
   ↓
2. Parse JSON response
   ↓
3. Extract campsite data
   ↓
4. Filter by date range (June 2026)
   ↓
5. Check availability status
   ↓
6. Compare with previous results
   ↓
7. Identify new availability
```

**Data Structure:**
```python
{
    'campground_name': 'Upper Pines',
    'site_name': 'Site A001',
    'available_dates': ['2026-06-01', '2026-06-02', ...],
    'campground_id': '232447',
    'site_id': '12345'
}
```

### 5. Notification System

**Multi-Channel Architecture:**

```
Notification Manager
    │
    ├─► Email Handler
    │   ├─ SMTP Connection
    │   ├─ HTML Formatting
    │   └─ Send via Gmail/Outlook
    │
    ├─► Webhook Handler
    │   ├─ JSON Payload
    │   ├─ HTTP POST
    │   └─ Slack/Discord Format
    │
    └─► SMS Handler
        ├─ Twilio API
        ├─ Text Formatting
        └─ Send to Phone Numbers
```

**Notification Content:**
- Park name
- Campground/site details
- Available dates
- Direct booking links
- Formatted for each channel

### 6. Logging System

**Log Levels:**
- DEBUG: Detailed diagnostic info
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages

**Output Destinations:**
- File: `availability_monitor.log`
- Console: Real-time output
- Systemd journal (if deployed as service)

## Data Flow

### Startup Sequence

```
1. Load config.yaml
   ↓
2. Initialize logger
   ↓
3. Create HTTP session
   ↓
4. Validate configuration
   ↓
5. Start monitoring loop
```

### Check Cycle

```
┌─────────────────────────────────────┐
│  Start Check Cycle                  │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  For each park in config:           │
│  1. Log park name                   │
│  2. Check camping availability      │
│  3. Check permit availability       │
│  4. Process results                 │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  Availability found?                │
└─────────────────────────────────────┘
        │               │
       Yes             No
        │               │
        ▼               ▼
┌──────────────┐  ┌──────────────┐
│Send          │  │Log "No       │
│Notifications │  │availability" │
└──────────────┘  └──────────────┘
        │               │
        └───────┬───────┘
                │
                ▼
┌─────────────────────────────────────┐
│  Wait for next check interval       │
│  (default: 60 minutes)              │
└─────────────────────────────────────┘
                │
                ▼
        (Repeat cycle)
```

## Deployment Architectures

### Local Deployment

```
┌──────────────────────────┐
│   Your Computer          │
│                          │
│  ┌────────────────────┐  │
│  │  Python Process    │  │
│  │  park_monitor.py   │  │
│  └────────────────────┘  │
│           │              │
│           ▼              │
│  ┌────────────────────┐  │
│  │  config.yaml       │  │
│  │  logs/             │  │
│  └────────────────────┘  │
└──────────────────────────┘
           │
           ▼ Internet
┌──────────────────────────┐
│   Recreation.gov         │
└──────────────────────────┘
```

### Cloud Deployment (AWS EC2)

```
┌─────────────────────────────────┐
│         AWS Cloud               │
│                                 │
│  ┌───────────────────────────┐  │
│  │   EC2 Instance            │  │
│  │   (Ubuntu)                │  │
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  systemd service    │  │  │
│  │  │  park-monitor       │  │  │
│  │  └─────────────────────┘  │  │
│  │           │               │  │
│  │           ▼               │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  Python Process     │  │  │
│  │  │  park_monitor.py    │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Docker Deployment

```
┌─────────────────────────────────┐
│      Docker Host                │
│                                 │
│  ┌───────────────────────────┐  │
│  │   Container               │  │
│  │   park-monitor            │  │
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  Python 3.11        │  │  │
│  │  │  + Dependencies     │  │  │
│  │  └─────────────────────┘  │  │
│  │           │               │  │
│  │           ▼               │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  park_monitor.py    │  │  │
│  │  └─────────────────────┘  │  │
│  │                           │  │
│  │  Volumes:                 │  │
│  │  - config.yaml (mounted)  │  │
│  │  - logs/ (mounted)        │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## Security Architecture

### Credential Management

```
┌─────────────────────────────────┐
│  Sensitive Data Storage         │
│                                 │
│  config.yaml (chmod 600)        │
│  ├─ Email password              │
│  ├─ Twilio credentials          │
│  └─ Webhook URLs                │
│                                 │
│  Alternative: .env file         │
│  ├─ Environment variables       │
│  └─ Not committed to git        │
└─────────────────────────────────┘
```

### Network Security

```
Monitor → HTTPS → Recreation.gov API
   │
   ├─→ TLS/SSL → SMTP Server (Email)
   │
   ├─→ HTTPS → Webhook (Slack/Discord)
   │
   └─→ HTTPS → Twilio API (SMS)
```

## Scalability Considerations

### Current Design
- Single-threaded
- Sequential park checking
- Suitable for 8-10 parks
- ~60 minute check intervals

### Potential Optimizations
- Parallel park checking (threading)
- Async HTTP requests
- Database for tracking
- Multiple instances for redundancy

## Error Handling

```
API Request
    │
    ├─► Success → Process Data
    │
    ├─► Timeout → Retry (3x)
    │
    ├─► Rate Limit → Backoff & Retry
    │
    └─► Error → Log & Continue
```

## Monitoring & Observability

### Logs Capture

```
INFO:  Normal operations
WARN:  Potential issues
ERROR: Failures (with retry)
DEBUG: Detailed diagnostics
```

### Metrics Tracked

- Check cycles completed
- Parks checked per cycle
- Availability found
- Notifications sent
- Errors encountered
- API response times

## Technology Stack

```
┌─────────────────────────────────┐
│  Language: Python 3.11+         │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│  Core Libraries:                │
│  - requests (HTTP)              │
│  - pyyaml (Config)              │
│  - schedule (Scheduling)        │
│  - smtplib (Email)              │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│  Optional:                      │
│  - twilio (SMS)                 │
│  - python-dateutil (Dates)      │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│  Deployment:                    │
│  - Docker                       │
│  - systemd                      │
│  - Cloud platforms              │
└─────────────────────────────────┘
```

## Performance Characteristics

- **Memory Usage:** ~50-100 MB
- **CPU Usage:** <5% (mostly idle)
- **Network:** ~1-5 KB per check
- **Disk:** Logs grow ~1 MB/day
- **Startup Time:** <1 second
- **Check Duration:** 10-30 seconds

## Future Architecture Enhancements

### Potential Additions

1. **Web Dashboard**
   ```
   Flask/FastAPI → HTML/JS Frontend
   └─ Real-time status
   └─ Historical data
   └─ Configuration UI
   ```

2. **Database Integration**
   ```
   SQLite/PostgreSQL
   └─ Availability history
   └─ Notification tracking
   └─ Analytics
   ```

3. **Multi-User Support**
   ```
   User Management
   └─ Individual configs
   └─ Separate notifications
   └─ Shared monitoring
   ```

---

**This architecture provides a solid foundation for reliable, scalable park availability monitoring.**