# 🔐 File Integrity Checker

A defensive Python security utility that monitors files using cryptographic hashes and detects unauthorized or unexpected modifications.

## 🎯 Core Capabilities

- SHA-256 file hashing
- Baseline snapshot creation
- Baseline comparison
- Added / modified / deleted file detection
- Recursive directory scanning
- JSON baseline storage
- Explainable integrity alerts
- Risk scoring
- CustomTkinter GUI
- Safe demo simulator
- Unit tests

## 🧠 How It Works

```text
Directory
   │
   ▼
File Discovery
   │
   ▼
SHA-256 Hashing
   │
   ▼
Baseline Snapshot
   │
   ▼
Later Scan
   │
   ▼
Hash Comparison
   │
   ├── ADDED
   ├── MODIFIED
   ├── DELETED
   └── UNCHANGED
          │
          ▼
    Risk Assessment
```

## 📊 Detection Model

| Event | Default Risk |
|---|---:|
| Unchanged | 0 |
| Added | 20 |
| Modified | 50 |
| Deleted | 60 |

The overall risk is capped at **100**.

```text
0–19     NORMAL
20–39    LOW
40–59    MEDIUM
60–79    HIGH
80–100   CRITICAL
```

A file being modified is not automatically malicious. Legitimate software updates, configuration changes, and user edits can produce alerts.

## 🚀 Features

### Baseline
- Select a directory
- Hash files recursively
- Save a JSON baseline
- Store file size and modification metadata

### Verification
- Compare current filesystem state with baseline
- Detect modified files
- Detect newly created files
- Detect deleted files
- Detect unreadable files
- Generate explainable findings

### Dashboard
- Current monitored path
- Baseline status
- File count
- Modified/added/deleted counts
- Risk score
- Severity
- Event log

### Safe Demo
The **Demo Changes** feature creates synthetic comparison data in memory. It does not alter monitored files.

## 🔒 Security Notes

SHA-256 is used for integrity verification.

The checker does not:

- execute scanned files
- modify monitored files
- upload files
- collect file contents
- send telemetry externally
- delete suspicious files

Only file metadata and cryptographic hashes are stored in the baseline.

## 📂 Project Structure

```text
File-Integrity-Checker/
│
├── src/
│   ├── main.py
│   ├── app/
│   │   ├── __init__.py
│   │   └── gui.py
│   ├── integrity/
│   │   ├── __init__.py
│   │   ├── hasher.py
│   │   ├── scanner.py
│   │   └── comparer.py
│   ├── simulator/
│   │   ├── __init__.py
│   │   └── scenarios.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── header.py
│   │   ├── controls.py
│   │   ├── risk_meter.py
│   │   └── event_log.py
│   └── config/
│       ├── __init__.py
│       └── theme.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## 📦 Installation

```bash
git clone https://github.com/aryanshrma03/File-Integrity-Checker.git
cd File-Integrity-Checker

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

## ▶️ Run

```bash
python src/main.py
```

## 🛠️ Usage

### 1. Select Directory

Choose the directory that should be monitored.

### 2. Create Baseline

Click **Create Baseline**.

The application calculates SHA-256 hashes for files and stores them in a JSON baseline.

### 3. Verify Integrity

Click **Verify Integrity** later.

The current state is compared against the baseline.

### 4. Review Findings

The dashboard reports:

```text
UNCHANGED
ADDED
MODIFIED
DELETED
UNREADABLE
```

## 📄 Baseline Format

Example:

```json
{
  "version": 1,
  "algorithm": "sha256",
  "root": "example",
  "files": {
    "config/settings.ini": {
      "sha256": "....",
      "size": 1024,
      "mtime_ns": 123456789
    }
  }
}
```

Only hashes and metadata are stored.

## ⚠️ Limitations

A hash mismatch proves that file content changed relative to the baseline; it does not prove why the change happened.

For production deployment, consider:

- Signed baselines
- Baseline encryption
- Access controls
- Trusted administrator workflow
- Windows Event Log integration
- File-system event monitoring
- SIEM integration
- Digital-signature verification
- Alert persistence
- Tamper-resistant storage

## 🔮 Future Improvements

- [ ] Real-time filesystem monitoring
- [ ] SQLite event history
- [ ] Windows service mode
- [ ] Linux daemon mode
- [ ] Digital-signature verification
- [ ] YARA integration
- [ ] JSON/CSV report export
- [ ] Email/webhook notifications
- [ ] MITRE ATT&CK mapping
- [ ] SIEM integration

## 👨‍💻 Author

**Aryan Sharma**

Cybersecurity-focused Python project demonstrating cryptographic integrity verification and defensive file monitoring.
