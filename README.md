# SOC Detection & Response Platform (Sigma + Wazuh)

A hands-on detection engineering project: writing custom [Sigma](https://github.com/SigmaHQ/sigma) rules,
deploying them against a live Wazuh SIEM, and triggering an automated response when a high-severity
detection fires.

## Why this project

Most portfolio projects stop at "I ran a scanner and got a report." This one demonstrates the actual
SOC analyst / detection engineer workflow: **write a detection → validate it against real telemetry →
deploy it → prove it fires → respond to it.**

## Architecture

```
 Attacker VM  --->  Windows VM (Sysmon + Wazuh Agent)  --->  Wazuh Manager (Oracle Cloud)
                                                                     |
                                                          Sigma rules converted via
                                                          sigma-cli -> Wazuh rule format
                                                                     |
                                                          High-severity alert triggers
                                                          response-scripts/alert_response.py
                                                                     |
                                                          Slack/email notification
                                                          (or mock host-isolation action)
```

See `docs/architecture.md` for the full write-up.

## Repo structure

```
sigma-soc-platform/
├── README.md                          <- you are here
├── rules/
│   └── windows/
│       ├── process_creation/          <- Sigma rules for suspicious process activity
│       └── network_connection/        <- Sigma rules for suspicious network activity
├── response-scripts/
│   └── alert_response.py              <- listens for/receives high-severity alerts, takes action
├── docs/
│   ├── architecture.md                <- detailed architecture + design decisions
│   ├── mitre_mapping.md               <- table mapping each rule to MITRE ATT&CK techniques
│   └── setup.md                       <- step-by-step lab setup instructions
└── screenshots/                       <- demo screenshots / recording links go here
```

## Detections included

| Rule | Technique | MITRE ATT&CK | Status |
|---|---|---|---|
| `suspicious_powershell_encoded.yml` | Encoded PowerShell execution | T1059.001 | ✅ tested |
| _(---------------)_ | | | |

Full mapping in `docs/mitre_mapping.md`.

## Quick start

1. Read `docs/setup.md` for the Wazuh + Sysmon lab setup.
2. Convert rules to Wazuh format:
   ```bash
   pip install sigma-cli --break-system-packages
   sigma convert -t wazuh -p wazuh rules/windows/process_creation/suspicious_powershell_encoded.yml
   ```
3. Load the converted rule into your Wazuh manager's custom rules.
4. Trigger the technique on the monitored VM and confirm the alert fires.
5. Confirm `response-scripts/alert_response.py` reacts to the alert.

## Status

🚧 Work in progress — built over a 2-week sprint. See commit history for day-by-day progress.

## Author

Anxuan — [https://medium.com/@priyankabehera297537] · [https://www.linkedin.com/in/priyanka-behera-238b57314] · [TryHackMe: anxuanveritas]

## Environment setup

Before running the response script, set your Slack webhook URL as an environment variable
(never hardcode it in the script or commit it to the repo):

**PowerShell:**
$env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

**cmd:**
set SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

This only lasts for your current terminal session. You will need to set it again each time
you open a new terminal window.

## Testing the response script

cd response-scripts
python alert_response.py sample_alert.json

You should see a high-severity alert print to console, a real message post to your configured
Slack channel, and a mock host-isolation line print (host isolation is currently a placeholder,
not a real EDR/firewall integration - see docs/architecture.md for why).
