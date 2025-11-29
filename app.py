<<<<<<< HEAD
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# This section imports the necessary libraries for the Streamlit app, data handling, and plotting charts.

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
# This converts the list to a pandas DataFrame for table display and data manipulation.
df = pd.DataFrame(workstations)

# Streamlit app title
# This sets the main title of the dashboard.
st.title("SIEM Dashboard")

# Section 1: Table view of workstations
# This displays a table showing IP, PC_Name, Storage_Status, and a Details View link for each workstation.
st.header("Workstation Profiles")

# Display table headers
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    st.write("**IP**")
with col2:
    st.write("**PC Name**")
with col3:
    st.write("**Storage Status**")
with col4:
    st.write("**Details View**")

# Display each workstation row with a button to the details page
for index, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        st.write(row["IP"])
    with col2:
        st.write(row["PC_Name"])
    with col3:
        st.write(row["Storage_Status"])
    with col4:
        if st.button("View", key=f"view_{row['PC_Name']}"):
            st.session_state.selected_workstation = row['PC_Name']
            st.switch_page("pages/workstation_details.py")

# Section 3: Charts for connected vs not connected percentages
# This section calculates and displays pie and bar charts showing the percentage of connected and not connected workstations.
st.header("Connection Status Overview")

# Calculate counts
if df.empty or "Connected" not in df.columns:
    connected_count = 0
    not_connected_count = 0
else:
    connected_count = df["Connected"].sum()
    not_connected_count = len(df) - connected_count
labels = ["Connected", "Not Connected"]
sizes = [connected_count, not_connected_count]

# Pie Chart
# This creates a pie chart using matplotlib to visualize the connection status percentages.
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

# Bar Chart
# This creates a bar chart using Streamlit's built-in charting to show the counts.
chart_data = pd.DataFrame({
    "Status": labels,
    "Count": sizes
})
st.bar_chart(chart_data.set_index("Status"))
=======
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# This section imports the necessary libraries for the Streamlit app, data handling, and plotting charts.

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
# This converts the list to a pandas DataFrame for table display and data manipulation.
df = pd.DataFrame(workstations)

# Streamlit app title
# This sets the main title of the dashboard.
st.title("SIEM Dashboard")

# Section 1: Table view of workstations
# This displays a table showing IP, PC_Name, Storage_Status, and a Details View link for each workstation.
st.header("Workstation Profiles")

# Display table headers
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    st.write("**IP**")
with col2:
    st.write("**PC Name**")
with col3:
    st.write("**Storage Status**")
with col4:
    st.write("**Details View**")

# Display each workstation row with a button to the details page
for index, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        st.write(row["IP"])
    with col2:
        st.write(row["PC_Name"])
    with col3:
        st.write(row["Storage_Status"])
    with col4:
        if st.button("View", key=f"view_{row['PC_Name']}"):
            st.session_state.selected_workstation = row['PC_Name']
            st.switch_page("pages/workstation_details.py")

# Section 3: Charts for connected vs not connected percentages
# This section calculates and displays pie and bar charts showing the percentage of connected and not connected workstations.
st.header("Connection Status Overview")

# Calculate counts
if df.empty or "Connected" not in df.columns:
    connected_count = 0
    not_connected_count = 0
else:
    connected_count = df["Connected"].sum()
    not_connected_count = len(df) - connected_count
labels = ["Connected", "Not Connected"]
sizes = [connected_count, not_connected_count]

# Pie Chart
# This creates a pie chart using matplotlib to visualize the connection status percentages.
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

# Bar Chart
# This creates a bar chart using Streamlit's built-in charting to show the counts.
chart_data = pd.DataFrame({
    "Status": labels,
    "Count": sizes
})
st.bar_chart(chart_data.set_index("Status"))
>>>>>>> 5e655e79216164d43a8729455c86af4ba8282057
