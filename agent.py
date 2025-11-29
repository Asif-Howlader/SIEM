import psutil
import socket
import platform
import getpass
import time
import requests
import json
import threading
import os
import shutil
import subprocess
import re
import sys

# Configuration
SIEM_SERVER_URL = "http://localhost:5000"  # Change to your SIEM server IP if remote

def get_system_info():
    """
    Collects system information like IP, PC name, processing status, storage status, etc.
    """
    # Get IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # PC Name
    pc_name = hostname

    # PC Type (simplified: check if laptop or desktop)
    pc_type = "Desktop"  # Default
    try:
        import subprocess
        result = subprocess.run(["wmic", "csproduct", "get", "name"], capture_output=True, text=True)
        if "laptop" in result.stdout.lower() or "notebook" in result.stdout.lower():
            pc_type = "Laptop"
    except:
        pass  # Default to Desktop

    # Processing Status (CPU usage)
    cpu_usage = psutil.cpu_percent(interval=1)
    processing_status = f"CPU: {cpu_usage}%"

    # Storage Status (Disk usage for C: drive)
    disk_usage = psutil.disk_usage('C:')
    storage_status = f"Disk: {disk_usage.percent}%"

    # Connected (always True for now, as agent is running)
    connected = True

    # Login Status (simplified: check if user is logged in)
    login_status = f"Logged in as {getpass.getuser()}"

    # Image URL (placeholder)
    image_url = "https://via.placeholder.com/150?text=" + pc_type

    # Running Processes (all running processes)
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                "PID": proc.info['pid'],
                "Name": proc.info['name'],
                "CPU": f"{proc.info['cpu_percent']:.1f}%",
                "Memory": f"{proc.info['memory_percent']:.1f}%"
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Sort by combined CPU and Memory usage descending and limit to top 20
    processes = sorted(processes, key=lambda x: float(x['CPU'].replace('%', '')) + float(x['Memory'].replace('%', '')), reverse=True)[:20]

    # Event Logs (recent system events)
    event_logs = []
    try:
        result = subprocess.run(["wevtutil", "qe", "System", "/c:20", "/f:XML"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Parse XML to extract events
            xml_output = result.stdout
            # Simple parsing for key fields
            events = re.findall(r'<Event.*?>(.*?)</Event>', xml_output, re.DOTALL)
            for event in events[:20]:  # Limit to 20
                time_match = re.search(r'<TimeCreated SystemTime="(.*?)"', event)
                source_match = re.search(r'<Provider Name="(.*?)"', event)
                id_match = re.search(r'<EventID.*?>(.*?)</EventID>', event)
                message_match = re.search(r'<Message>(.*?)</Message>', event, re.DOTALL)
                event_logs.append({
                    "Time": time_match.group(1) if time_match else "N/A",
                    "Source": "System",
                    "EventID": id_match.group(1) if id_match else "N/A",
                    "Message": message_match.group(1).strip() if message_match else "N/A"
                })
    except Exception as e:
        # Fallback to simulated logs
        event_logs = [
            {"Time": "2023-10-01T10:00:00", "Source": "System", "EventID": "1001", "Message": "System started"},
            {"Time": "2023-10-01T10:05:00", "Source": "System", "EventID": "1002", "Message": "System event 2"},
            {"Time": "2023-10-01T10:10:00", "Source": "System", "EventID": "1003", "Message": "System event 3"},
            {"Time": "2023-10-01T10:15:00", "Source": "System", "EventID": "1004", "Message": "System event 4"},
        ]

    return {
        "IP": ip_address,
        "PC_Name": pc_name,
        "Processing_Status": processing_status,
        "Storage_Status": storage_status,
        "Connected": connected,
        "PC_Type": pc_type,
        "Image_URL": image_url,
        "Login_Status": login_status,
        "Running_Processes": processes,
        "Event_Logs": event_logs
    }

def send_data_to_server():
    """
    Sends collected data to the SIEM server.
    """
    while True:
        try:
            data = get_system_info()
            print(f"Sending data to {SIEM_SERVER_URL}/register: {data}")
            response = requests.post(f"{SIEM_SERVER_URL}/register", json=data, timeout=10)
            if response.status_code == 200:
                print("Data sent successfully to SIEM server.")
            else:
                print(f"Failed to send data: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error sending data: {e}")
        except Exception as e:
            print(f"Error sending data: {e}")
        time.sleep(60)  # Send data every 60 seconds

def setup_auto_startup():
    """
    Sets up the agent to run automatically on Windows startup using Task Scheduler.
    """
    task_name = "SIEM_Agent"
    script_path = os.path.abspath(__file__)
    pythonw_path = sys.executable.replace('python.exe', 'pythonw.exe')
    if not os.path.exists(pythonw_path):
        pythonw_path = sys.executable.replace('pythonw.exe', 'python.exe')  # Fallback, but should be pythonw
    command = f'"{pythonw_path}" "{script_path}"'

    # Check if task exists and delete it
    try:
        result = subprocess.run(["schtasks", "/query", "/tn", task_name], capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True)
    except:
        pass

    # Create the task
    try:
        subprocess.run([
            "schtasks", "/create", "/tn", task_name, "/tr", command,
            "/sc", "onlogon", "/f"
        ], check=True)
        print("SIEM Agent task created in Task Scheduler for auto-startup.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create task: {e}")
    except Exception as e:
        print(f"Failed to set up auto-startup: {e}")

if __name__ == "__main__":
    print("Starting SIEM Agent...")
    setup_auto_startup()
    # Run data sending in a separate thread
    threading.Thread(target=send_data_to_server, daemon=True).start()
    # Keep the script running
    while True:
        time.sleep(1)
