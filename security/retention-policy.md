# 🛡️ SOC2 Retention & Access Policy

## Log Retention
- All audit logs retained for **90 days** (SOC2 CC7.2)  
- Automatic daily rotation + cleanup: `find /var/log/policyfx/audit -name "*.log" -mtime +90 -delete`  
- Logs encrypted at rest (AES256 via filesystem encryption)

## Access Control
- Read-only access granted only to:  
  • `audit-team` group (via `sudo usermod -aG audit-team puyuam`)  
  • `root` (for rotation cron)  
- No write access outside `immutable-log.py`

## Immutable Integrity
- Logs are append-only — no edits or deletions permitted  
- Each line SHA256-signed with payload (prevents tampering)  
- Signed hash included in every log entry

---
✅ Compliant with SOC2 Trust Services Criteria: CC6.1 (Logical Access), CC7.2 (Change Management)