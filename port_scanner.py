import socket
import argparse
import re
import sqlite3

def validate_ip(ip):
    pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(pattern, ip):
        return True
    return False

def scan_port(host, port, verbose, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                if verbose:
                    print(f"[+] Port {port} is open on {host}")
                return port
            else:
                if verbose:
                    print(f"[-] Port {port} is closed on {host}")
                return None
    except (socket.error, socket.timeout) as e:
        if verbose:
            print(f"[!] Could not connect to {host}:{port} - {e}")
        return None

def scan_ports(host, start_port, end_port, verbose, timeout=1):
    open_ports = []
    for port in range(start_port, end_port + 1):
        result = scan_port(host, port, verbose, timeout)
        if result is not None:
            open_ports.append(result)
    return open_ports

def create_database():
    conn = sqlite3.connect("exploitdb.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exploits (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            port INTEGER,
            exploit TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert_exploit(ip, port, exploit):
    conn = sqlite3.connect("exploitdb.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exploits (ip, port, exploit) VALUES (?, ?, ?)", (ip, port, exploit))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("host", help="Host to scan")
    parser.add_argument("start_port", type=int, help="Starting port")
    parser.add_argument("end_port", type=int, help="Ending port")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--timeout", type=float, default=1, help="Connection timeout in seconds")

    args = parser.parse_args()
    if not validate_ip(args.host):
        print("Invalid IP address")
        sys.exit(1)

    create_database()
    open_ports = scan_ports(args.host, args.start_port, args.end_port, args.verbose, args.timeout)
    for port in open_ports:
        insert_exploit(args.host, port, "Unknown exploit")
    print(f"Open ports: {open_ports}")