import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# This section imports the necessary libraries for the Streamlit page, data handling, and plotting charts.

# Fetch workstation data from backend
# This retrieves real-time data from the SIEM backend server.
# In case of failure, fall back to simulated data.
try:
    import requests
    response = requests.get("http://localhost:5000/get_workstations")
    if response.status_code == 200:
        workstations = response.json()
    else:
        raise Exception("Backend not available")
except:
    # Fallback to simulated data
    workstations = [
        {"IP": "192.168.1.10", "PC_Name": "Workstation1", "Processing_Status": "CPU: 45%", "Storage_Status": "Disk: 60%", "Connected": True, "PC_Type": "Desktop", "Image_URL": "https://via.placeholder.com/150?text=Desktop", "Login_Status": "Logged in since 10:00 AM"},
        {"IP": "192.168.1.11", "PC_Name": "Workstation2", "Processing_Status": "CPU: 30%", "Storage_Status": "Disk: 75%", "Connected": True, "PC_Type": "Laptop", "Image_URL": "https://via.placeholder.com/150?text=Laptop", "Login_Status": "Logged out at 5:00 PM"},
        {"IP": "192.168.1.12", "PC_Name": "Workstation3", "Processing_Status": "CPU: 80%", "Storage_Status": "Disk: 90%", "Connected": False, "PC_Type": "Desktop", "Image_URL": "https://via.placeholder.com/150?text=Desktop", "Login_Status": "Logged in since 9:00 AM"},
        {"IP": "192.168.1.13", "PC_Name": "Workstation4", "Processing_Status": "CPU: 20%", "Storage_Status": "Disk: 50%", "Connected": True, "PC_Type": "Laptop", "Image_URL": "https://via.placeholder.com/150?text=Laptop", "Login_Status": "Logged out at 6:00 PM"},
        {"IP": "192.168.1.14", "PC_Name": "Workstation5", "Processing_Status": "CPU: 65%", "Storage_Status": "Disk: 85%", "Connected": False, "PC_Type": "Desktop", "Image_URL": "https://via.placeholder.com/150?text=Desktop", "Login_Status": "Logged in since 11:00 AM"},
    ]

# Convert to DataFrame for easier handling
# This converts the list to a pandas DataFrame for data manipulation.
df = pd.DataFrame(workstations)

# Get workstation name from query parameters
# This retrieves the workstation name passed from the main dashboard.
query_params = st.query_params
workstation_name = query_params.get("workstation", None)

if workstation_name:
    # Find the workstation details
    # This filters the DataFrame to get the specific workstation's data.
    workstation_details = df[df["PC_Name"] == workstation_name].iloc[0]

    # Page title
    # This sets the title for the workstation details page.
    st.title(f"Workstation Details: {workstation_name}")

    # Display workstation image and basic info
    # This section shows the PC type image and basic details like name, type, IP.
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(workstation_details["Image_URL"], caption=workstation_details["PC_Type"])
    with col2:
        st.subheader("Basic Information")
        st.write(f"**PC Name:** {workstation_details['PC_Name']}")
        st.write(f"**PC Type:** {workstation_details['PC_Type']}")
        st.write(f"**IP Address:** {workstation_details['IP']}")
        st.write(f"**Connected:** {'Yes' if workstation_details['Connected'] else 'No'}")
        st.write(f"**Login Status:** {workstation_details['Login_Status']}")

    # Processor status
    # This displays the current processor (CPU) status.
    st.subheader("Processor Status")
    st.write(workstation_details["Processing_Status"])

    # Process details
    # This displays a list of running processes with CPU and memory usage.
    st.subheader("Process Details")
    if "Running_Processes" in workstation_details and workstation_details["Running_Processes"]:
        # Use real data from backend
        processes = workstation_details["Running_Processes"]
        # Rename keys for display
        display_processes = [
            {"Process Name": proc["Name"], "PID": proc["PID"], "CPU Usage": proc["CPU"], "Memory Usage": proc["Memory"]}
            for proc in processes
        ]
    else:
        # Fallback to simulated process data
        display_processes = [
            {"Process Name": "chrome.exe", "PID": "1234", "CPU Usage": "15%", "Memory Usage": "200 MB"},
            {"Process Name": "explorer.exe", "PID": "5678", "CPU Usage": "5%", "Memory Usage": "150 MB"},
            {"Process Name": "python.exe", "PID": "9101", "CPU Usage": "10%", "Memory Usage": "100 MB"},
        ]
    # Limit to top 30 processes
    display_processes = display_processes[:30]
    process_df = pd.DataFrame(display_processes)
    st.table(process_df)

    # Event Logs
    # This displays recent event logs from the workstation.
    st.subheader("Event Logs")
    if "Event_Logs" in workstation_details and workstation_details["Event_Logs"]:
        # Use real data from backend
        logs = workstation_details["Event_Logs"]
        # Rename keys for display
        display_logs = [
            {"Time": log["Time"], "Source": log["Source"], "Event ID": log["EventID"], "Message": log["Message"]}
            for log in logs
        ]
    else:
        # Fallback to simulated logs
        display_logs = [
            {"Time": "2023-10-01T10:00:00", "Source": "System", "Event ID": "1001", "Message": "System started"},
            {"Time": "2023-10-01T10:05:00", "Source": "System", "Event ID": "1002", "Message": "System event 2"},
            {"Time": "2023-10-01T10:10:00", "Source": "System", "Event ID": "1003", "Message": "System event 3"},
            {"Time": "2023-10-01T10:15:00", "Source": "Application", "Event ID": "2002", "Message": "Application error"},
        ]
    logs_df = pd.DataFrame(display_logs)
    # Filter to System logs only
    logs_df = logs_df[logs_df["Source"].isin(["System"])]
    # Add Level column based on Event ID or Message
    logs_df["Level"] = logs_df["Event ID"].apply(lambda x: "Error" if int(x) % 3 == 0 else "Warning" if int(x) % 3 == 1 else "Information")
    # Add links to log details
    logs_df["Details"] = logs_df["Event ID"].apply(lambda x: f'<a href="log_details?workstation={workstation_name}&log_id={x}" target="_blank">View</a>')
    st.write(logs_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Disk space pie chart
    # This parses the storage status and creates a pie chart showing used and free disk space.
    st.subheader("Disk Space")
    storage_str = workstation_details["Storage_Status"]
    used_percent = float(storage_str.split(": ")[1].replace("%", ""))
    free_percent = 100 - used_percent
    labels = ["Used", "Free"]
    sizes = [used_percent, free_percent]
    colors = ["red", "green"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Back to dashboard link
    # This provides a link to return to the main dashboard.
    st.markdown("[Back to Dashboard](/)")
else:
    st.error("No workstation specified.")
