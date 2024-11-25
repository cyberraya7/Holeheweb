import streamlit as st 

import subprocess 

import json 

import re 

import time 

import pandas as pd 

from io import BytesIO 

  

# Email validation function 

def is_valid_email(email): 

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" 

    return re.match(email_regex, email) 

  

# Function to run Holehe and process the output 

def run_holehe(email, holehe_command="holehe"): 

    try: 

        start_time = time.time() 

        # Run the Holehe command and capture output 

        result = subprocess.run( 

            [holehe_command, email], 

            capture_output=True, 

            text=True 

        ) 

        execution_time = time.time() - start_time 

  

        # Check for output 

        if result.stdout: 

            return result.stdout, execution_time 

        else: 

            return "No results found.", execution_time 

  

    except FileNotFoundError: 

        raise FileNotFoundError("Holehe is not installed or not in the system PATH.") 

    except Exception as e: 

        raise RuntimeError(f"An error occurred: {e}") 

  

# Function to prepare files for download 

def prepare_download(data, filename, file_format="json"): 

    buffer = BytesIO() 

    if file_format == "json": 

        buffer.write(json.dumps(data, indent=4).encode("utf-8")) 

        mime = "application/json" 

    if file_format == "csv": 

        df = pd.DataFrame(data) 

        buffer.write(df.to_csv(index=False).encode("utf-8")) 

        mime = "text/csv" 

    elif file_format == "text": 

        buffer.write(data.encode("utf-8")) 

        mime = "text/plain" 

    else: 

        raise ValueError("Unsupported file format.") 

  

    buffer.seek(0) 

    return buffer, mime 

  

# Function to parse and summarize results 

def summarize_results(output): 

    try: 

        data = json.loads(output) 

        summary = { 

            "Total Accounts Found": len(data), 

            "Services": [service.get("name", "Unknown") for service in data], 

        } 

     return data, summary 

     except json.JSONDecodeError: 

     return None, None 

  

# Main function for Streamlit 

def main(): 

    st.title("🔍 Holehe Email Checker") 

    st.write("Check which websites are linked to a specific email address using **Holehe**.") 

  

    # Input for the email address 

    email = st.text_input("Enter the email address to check:") 

  

    # Configurable Holehe command 

    holehe_command = st.text_input("Custom Holehe Command (optional):", value="holehe") 

  

    # Button to trigger the check 

    if st.button("Check Email"): 

        if email: 

            # Validate email format 

            if not is_valid_email(email): 

                st.error("❌ Invalid email format. Please enter a valid email address.") 

                return 

  

            st.write(f"🔎 Checking accounts for email: **{email}**") 

            with st.spinner("Running Holehe... Please wait."): 

                try: 

                    # Run Holehe and get results 

                    output, exec_time = run_holehe(email, holehe_command) 

  

                    # Display execution time 

                    st.success(f"✅ Completed in {exec_time:.2f} seconds!") 

  

                    # Summarize results 

                    data, summary = summarize_results(output) 

  

                    if data: 

                        # Display summary 

                        st.write("### Summary:") 

                        st.json(summary) 

  

                        # Expandable details 

                        with st.expander("🔍 Detailed Results (JSON)"): 

                            st.json(data) 

  

                        # Filter results by service 

                        services = summary["Services"] 

                        selected_service = st.selectbox("Filter by service:", ["All"] + services) 

                        if selected_service != "All": 

                            filtered_data = [d for d in data if d.get("name") == selected_service] 

                            st.write(f"### Results for {selected_service}:") 

                            st.json(filtered_data) 

  

                        # Download options 

                        st.write("### Download Results:") 

                        json_buffer, json_mime = prepare_download(data, f"{email}_results.json", "json") 

                        st.download_button("📥 Download as JSON", json_buffer, file_name=f"{email}_results.json", mime=json_mime) 

  

                        csv_buffer, csv_mime = prepare_download(data, f"{email}_results.csv", "csv") 

                        st.download_button("📥 Download as CSV", csv_buffer, file_name=f"{email}_results.csv", mime=csv_mime) 

  

                    else: 

                        st.warning("No results found or data could not be parsed.") 

                        with st.expander("Raw Output"): 

                            st.text(output) 

  

                    # Always provide raw output for download 

                    st.write("### Download Raw Output:") 

                    raw_buffer, raw_mime = prepare_download(output, f"{email}_raw_output.txt", "text") 

                    st.download_button("📥 Download Raw Output", raw_buffer, file_name=f"{email}_raw_output.txt", mime=raw_mime) 

  

                except FileNotFoundError: 

                    st.error("❌ Holehe is not installed or not found in the system PATH. Please ensure it is properly installed.") 

                except RuntimeError as e: 

                    st.error(f"⚠️ {e}") 

        else: 

            st.warning("⚠️ Please enter an email address.") 

  

# Run the app 

if __name__ == "__main__": 

    main() 
