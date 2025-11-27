import streamlit as st
import pandas as pd

# Get query parameters
query_params = st.query_params
log_id = query_params.get("log_id", None)
workstation_name = query_params.get("workstation", None)

if log_id and workstation_name:
    st.title(f"Log Details for {workstation_name} - Event ID: {log_id}")

    # Fetch log details (in real scenario, from backend)
    # For now, simulate based on log_id
    # Assume logs are stored or fetched
    # Simulated log details
    try:
        import requests
        response = requests.get(f"http://localhost:5000/get_log_details?workstation={workstation_name}&log_id={log_id}")
        if response.status_code == 200:
            log_details = response.json()
        else:
            raise Exception("Backend not available")
    except:
        # Fallback simulation
        log_details = {
            "Time": "2023-10-01T10:00:00",
            "Source": "System" if int(log_id) % 2 == 0 else "Security",
            "Event ID": log_id,
            "Message": f"Detailed message for event {log_id}",
            "Level": "Information" if int(log_id) % 3 == 1 else "Warning" if int(log_id) % 3 == 2 else "Error",
            "Description": f"Full description of event {log_id}. This includes more context about what happened, potential causes, and recommendations.",
            "User": "SYSTEM",
            "Computer": workstation_name
        }

    st.subheader("Log Information")
    st.write(f"**Time:** {log_details['Time']}")
    st.write(f"**Source:** {log_details['Source']}")
    st.write(f"**Event ID:** {log_details['Event ID']}")
    st.write(f"**Level:** {log_details['Level']}")
    st.write(f"**Message:** {log_details['Message']}")
    st.write(f"**Description:** {log_details['Description']}")
    st.write(f"**User:** {log_details['User']}")
    st.write(f"**Computer:** {log_details['Computer']}")

    # Back link
    st.markdown(f"[Back to Workstation Details](workstation_details?workstation={workstation_name})")
else:
    st.error("Invalid log details request.")
