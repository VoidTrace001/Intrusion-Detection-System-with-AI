import hashlib
import json
import os
import threading
from datetime import datetime

class ImmutableLedger:
    def __init__(self, ledger_file="threat_ledger.log"):
        self.ledger_file = ledger_file
        self.last_hash = "0" * 64
        self.is_compromised = False
        self.lock = threading.Lock()
        
        # Load the chain or start a new one
        if os.path.exists(self.ledger_file) and os.path.getsize(self.ledger_file) > 0:
            self.verify_integrity()
        else:
            self._create_genesis_block()

    def _create_genesis_block(self):
        """Creates the initial 'Block 0' of the Threat Ledger."""
        with self.lock:
            genesis_entry = {
                "timestamp": datetime.now().isoformat(),
                "prev_hash": "0" * 64,
                "data": "Genesis Block: AI-IDS Threat Ledger Initialized."
            }
            self.last_hash = self._calculate_hash(genesis_entry)
            self._write_to_ledger(genesis_entry, self.last_hash)

    def add_entry(self, data):
        """Adds a new cryptographically linked entry to the ledger."""
        with self.lock:
            if self.is_compromised:
                print("[!] Refusing to add entry to compromised ledger.")
                return None
                
            entry = {
                "timestamp": datetime.now().isoformat(),
                "prev_hash": self.last_hash,
                "data": data
            }
            new_hash = self._calculate_hash(entry)
            self.last_hash = new_hash
            self._write_to_ledger(entry, new_hash)
            return new_hash

    def _calculate_hash(self, entry):
        # Create a copy to avoid modifying the original entry
        entry_copy = entry.copy()
        if "hash" in entry_copy:
            entry_copy.pop("hash")
        entry_string = json.dumps(entry_copy, sort_keys=True).encode()
        return hashlib.sha256(entry_string).hexdigest()

    def _write_to_ledger(self, entry, current_hash):
        try:
            with open(self.ledger_file, "a", encoding='utf-8') as f:
                entry["hash"] = current_hash
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[!] Error writing to ledger: {e}")

    def verify_integrity(self):
        """Scans the entire ledger to ensure no one has tampered with past logs."""
        print("[*] Verifying Threat Ledger Integrity...")
        try:
            expected_prev_hash = "0" * 64
            last_valid_hash = expected_prev_hash
            
            with open(self.ledger_file, "r", encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    entry = json.loads(line)
                    current_hash = entry.get("hash")
                    
                    # 1. Check link
                    if entry["prev_hash"] != expected_prev_hash:
                        print(f"[!] INTEGRITY BREACH: Ledger chain broken at {entry['timestamp']}")
                        self.is_compromised = True
                        return False
                    
                    # 2. Check hash
                    actual_hash = self._calculate_hash(entry)
                    if actual_hash != current_hash:
                        print(f"[!] INTEGRITY BREACH: Block tampered at {entry['timestamp']}")
                        self.is_compromised = True
                        return False
                    
                    expected_prev_hash = current_hash
                    last_valid_hash = current_hash
            
            self.last_hash = last_valid_hash
            self.is_compromised = False
            print("[+] Threat Ledger Integrity Verified. Zero Tampering Detected.")
            return True
        except Exception as e:
            print(f"[!] Ledger Verification Error: {e}")
            self.is_compromised = True
            return False
