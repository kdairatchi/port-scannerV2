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