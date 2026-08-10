# Architecture & Design Decisions

## Why Sigma instead of writing Wazuh rules directly

Sigma decouples the *detection logic* from the *SIEM implementation*. Writing rules in Sigma
first, then converting with `sigma-cli`/pySigma, means the same rule could later be pointed at
Splunk, Elastic, or Microsoft Sentinel without rewriting the logic — this is the actual value
Sigma provides in real SOC environments, and it's worth calling out explicitly in interviews.

## Why Wazuh instead of full ELK

- Bundles agent, manager, indexer, and dashboard together — less to configure
- Free and open source, no licensing friction
- Native support for Sysmon-based Windows telemetry
- Lighter resource footprint than standing up ELK + Winlogbeat + Sysmon separately, which
  matters running on a free-tier cloud VM

## Why Oracle Cloud Free Tier for the manager

Keeps the Wazuh manager off the local 8GB RAM laptop, which otherwise struggles running a
SIEM + a Windows VM + an attacker VM simultaneously.

## Detection → Response flow

1. Attacker technique executes on the Windows VM
2. Sysmon logs the event, Wazuh agent forwards it to the manager
3. The manager evaluates it against loaded rules (including our Sigma-derived ones)
4. A match generates an alert with a rule level
5. `alert_response.py` receives/polls for alerts ≥ threshold and takes action

## Known limitations (be upfront about these in interviews)

- The "isolation" response action is mocked, not a real EDR/firewall integration — stated
  clearly rather than implied as production-grade
- Rules are tuned against a small, clean lab dataset, not a noisy real-world environment,
  so false-positive rates here don't reflect production tuning effort
- This is a learning/demo project, not a hardened production SOC platform — framing it
  honestly is more credible to an interviewer than overstating scope
