import re
import random
from datetime import datetime

class SecurityAssistant:
    def __init__(self, firewall_ref=None, osint_ref=None, ledger_ref=None, stats_ref=None, set_defcon_func=None):
        self.firewall = firewall_ref
        self.osint = osint_ref
        self.ledger = ledger_ref
        self.stats = stats_ref or {}
        self.set_defcon = set_defcon_func
        self.context = {}

    def update_context(self, stats):
        self.stats = stats

    def get_response(self, query):
        query = query.lower().strip()
        
        # 1. COMMAND: SET DEFCON
        match = re.search(r"set defcon (\d)", query)
        if match:
            level = int(match.group(1))
            if 1 <= level <= 5:
                if self.set_defcon:
                    self.set_defcon(level)
                    return f"**[COMMAND EXECUTED]** DEFCON level updated to **{level}**. Global threat posture adjusted."
                return "Error: Control link failure."
            return "Invalid DEFCON level. Range: 1-5."

        # 2. COMMAND: BLOCK IP
        match = re.search(r"block ([\d\.]+)", query)
        if match:
            ip = match.group(1)
            if self.firewall:
                success = self.firewall.block_ip(ip, duration_minutes=60)
                if success:
                    return f"**[TARGET NEUTRALIZED]** IP `{ip}` has been blocked by the firewall for 60 minutes."
                return f"Failed to block `{ip}`. Check privileges or IP format."
            return "Firewall module offline."

        # 3. ANALYSIS: ANALYZE IP
        match = re.search(r"analyze ([\d\.]+)", query)
        if match:
            ip = match.group(1)
            return self._analyze_target(ip)

        # 4. REPORT: SITREP (Situation Report)
        if "report" in query or "status" in query or "sitrep" in query:
            return self._generate_sitrep()

        # 5. GENERAL INTELLIGENCE
        if "attacks" in query:
            count = self.stats.get("total_attacks", 0)
            top_attack = self._get_top_attack()
            return f"**INTELLIGENCE REPORT**\n\nTotal Confirmed Threats: **{count}**\nPrimary Vector: **{top_attack}**\nCurrent DEFCON: **{self.stats.get('defcon')}**"
        
        if "honeypot" in query:
            hits = self.stats.get("honeypot_hits", 0)
            return f"**DECEPTION GRID STATUS**\n\nActive Traps: **4 (SSH, SQL, FTP, VNC)**\nConfirmed Kills (Hits): **{hits}**\nStatus: **ACTIVE**"

        return "UNKNOWN COMMAND. Available protocols:\n- `Set DEFCON [1-5]`\n- `Block [IP]`\n- `Analyze [IP]`\n- `Sitrep` (Status Report)"

    def _analyze_target(self, ip):
        # Check recent alerts for this IP
        alerts = [a for a in self.stats.get("recent_alerts", []) if a['src_ip'] == ip]
        
        # OSINT Lookup
        reputation = 0
        if self.osint:
            reputation = self.osint.check_reputation(ip)
        
        status = "**UNKNOWN**"
        if reputation > 50: status = "**HOSTILE**"
        elif reputation == 0: status = "**NEUTRAL**"
        
        history = "No recent activity."
        if alerts:
            last_attack = alerts[0]['attack_type']
            history = f"Recently flagged for **{last_attack}**."

        return (
            f"**TARGET ANALYSIS: {ip}**\n"
            f"-----------------------\n"
            f"Global Reputation: **{reputation}%**\n"
            f"Classification: {status}\n"
            f"Local History: {history}\n"
            f"Recommended Action: {'**BLOCK IMMEDIATELY**' if reputation > 50 else 'Monitor'}"
        )

    def _generate_sitrep(self):
        health = self.stats.get("system_health", {})
        defcon = self.stats.get("defcon", 5)
        active = "ONLINE" if self.stats.get("is_active") else "OFFLINE"
        
        return (
            f"**SITUATION REPORT (SITREP)**\n"
            f"----------------------------\n"
            f"System Status: **{active}**\n"
            f"Threat Condition: **DEFCON {defcon}**\n"
            f"CPU Load: **{health.get('cpu', 0)}%** | RAM: **{health.get('ram', 0)}%**\n"
            f"Total Packets Scanned: **{self.stats.get('total_packets', 0)}**\n"
            f"Ledger Integrity: **{'SECURE' if self.stats.get('ledger_integrity') else 'COMPROMISED'}**\n"
            f"**Orders:** Maintain vigilance."
        )

    def _get_top_attack(self):
        dist = self.stats.get("attack_distribution", {})
        if not dist: return "None"
        return max(dist, key=dist.get)
