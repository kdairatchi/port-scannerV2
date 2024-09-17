# port-scannerV2


**port_scanner.py**
```python
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
```

**database.py**
```python
import sqlite3

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

def get_exploits():
    conn = sqlite3.connect("exploitdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exploits")
    exploits = cursor.fetchall()
    conn.close()
    return exploits
```

**exploitdb.py**
```python
import requests

def get_exploitdb_data():
    url = "https://exploit-db.com/exploits.csv"
    response = requests.get(url)
    data = response.text
    return data

def parse_exploitdb_data(data):
    exploits = []
    for line in data.splitlines():
        exploit = line.split(",")
        exploits.append(exploit)
    return exploits

def insert_exploits(exploits):
    for exploit in exploits:
        insert_exploit(exploit[0], exploit[1], exploit[2])
```

**main.py**
```python
import port_scanner
import database
import exploitdb

def main():
    port_scanner.create_database()
    open_ports = port_scanner.scan_ports("127.0.0.1", 1, 1024, True, 1)
    for port in open_ports:
        database.insert_exploit("127.0.0.1", port, "Unknown exploit")
    exploitdb_data = exploitdb.get_exploitdb_data()
    exploits = exploitdb.parse_exploitdb_data(exploitdb_data)
    for exploit in exploits:
        database.insert_exploit(exploit[0], exploit[1], exploit[2])

if __name__ == "__main__":
    main()
```

**README.md**
```markdown
# Port Scanner and ExploitDB Integration

This repository contains a port scanner and ExploitDB integration script.

## Requirements

*   Python 3.x
*   sqlite3
*   requests

## Usage

1.  Clone the repository: `git clone https://github.com/kdairatchi/port-scanner-exploitdb.git`
2.  Install the requirements: `pip install -r requirements.txt`
3.  Run the script: `python main.py`

## Note

This script is for educational purposes only. Do not use it to scan or exploit systems without permission.
```

**requirements.txt**
```
sqlite3
requests
```

Please note that this is just an example code, and you may need to modify it to suit your specific requirements. Additionally, this code assumes that you have the `sqlite3` and `requests` libraries installed. If you don't have these libraries installed, you can install them using pip:

```bash
pip install sqlite3 requests
```

