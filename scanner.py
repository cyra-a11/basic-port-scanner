import socket
import threading

def scan_port(ip, port, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    
    if sock.connect_ex((ip, port)) == 0:
        # Get service name
        service = services.get(port, "Unknown")
        
        # Try to grab banner
        try:
            banner = sock.recv(1024).decode(errors='ignore').strip()[:40]
        except:
            banner = ""
        
        open_ports.append((port, service, banner))
    
    sock.close()

# Common services
services = {
    21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
}

# Get target
target = input("Target IP: ")
choice = input("Scan (1) Common ports or (2) All ports? ")

# Choose ports
if choice == "2":
    ports = range(1, 65536)
else:
    ports = list(services.keys())

print(f"\nScanning {target}...\n")

# Store results
open_ports = []

# Scan each port in separate thread
for port in ports:
    t = threading.Thread(target=scan_port, args=(target, port, open_ports))
    t.start()

# Wait for all threads to finish
threading.Event().wait(5)  # Give 5 seconds max

# Show results
open_ports.sort()
for port, service, banner in open_ports:
    if banner:
        print(f"[+] {port} - {service} - {banner}")
    else:
        print(f"[+] {port} - {service}")

print(f"\nTotal: {len(open_ports)} open ports")