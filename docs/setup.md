# Lab Setup

## Components

- **Wazuh manager** — Oracle Cloud Free Tier VM (Ampere A1, 4 OCPU / 24GB RAM tier is free
  and gives enough headroom that your local 8GB laptop doesn't have to run the manager)
- **Windows victim VM** — Sysmon installed, Wazuh agent installed, forwarding to the manager
- **Attacker box** — can just be your host laptop or a small Kali VM, only needs to reach
  the Windows VM on the same network

## Steps

1. **Provision the Oracle Cloud VM**
   - Ubuntu 22.04, Ampere A1 shape, free tier
   - Open inbound ports 1514/tcp (agent comms), 1515/tcp (agent enrollment), 55000/tcp (API), 443/tcp (dashboard) in the Security List/NSG

2. **Install Wazuh manager**
   - Use the official all-in-one install script from the Wazuh docs (search "Wazuh quickstart install" for the current script — it changes between versions, don't rely on a cached command)
   - Confirm the dashboard loads at `https://<oracle-vm-ip>`

3. **Prepare the Windows VM**
   - Install Sysmon with a solid config (SwiftOnSecurity's sysmon-config is the standard starting point — search for it, don't guess the XML)
   - Install the Wazuh agent, point it at your Oracle VM's IP, enroll it
   - Confirm the agent shows "Active" in the Wazuh dashboard

4. **Validate telemetry is flowing**
   - Run `whoami` or open Notepad on the Windows VM
   - Confirm the event shows up in the Wazuh dashboard within a few seconds
   - **Do not proceed to rule-writing until this works** — this is the step most likely to eat your schedule

5. **Fallback plan if Oracle Cloud networking is a headache**
   - Run Wazuh manager locally in Docker (`wazuh-docker` single-node quickstart)
   - Run the Windows VM in VirtualBox/VMware on the same host-only or NAT network
   - Same result, no cloud firewall rules to fight

## Testing a technique end-to-end

1. On the Windows VM, run: `powershell.exe -enc <base64>` (any harmless base64, e.g. `echo hi` encoded)
2. Confirm the event appears in Wazuh under Sysmon Event ID 1 (process creation)
3. Once your Sigma rule is converted and loaded, confirm the *converted rule* — not just raw Sysmon — fires as an alert
4. Only then wire in `response-scripts/alert_response.py`
