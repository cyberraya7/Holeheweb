Installation
python3 -m venv new_env
source new_env/bin/activate
pip install streamlit
pip install httpx
pip3 install holehe

Save the script as app.py

import streamlit as st
import subprocess
import json
# Define the main function
def main():
    st.title("Holehe Email Checker")
    st.write("Check which sites are linked to a specific email address.")
    # Get the email address from user input
    email = st.text_input("Enter the email address to check:")
    if st.button("Check Email"):
        if email:
            st.write(f"Checking accounts for email: {email}")
            try:
                # Run the holehe command and capture output
                result = subprocess.run(
                    ['holehe', email],
                    capture_output=True,
                    text=True,
                    check=True  # Ensure that subprocess raises an error on failure
                )
                # Check if there's any output
                if result.stdout:
                    # Try parsing output as JSON
                    try:
                        data = json.loads(result.stdout)
                        st.json(data)  # Display JSON result in Streamlit
                    except json.JSONDecodeError:
                        # If it's not JSON, display raw text
                        st.text("Raw Output:")
                        st.text(result.stdout)
                    # Add download button for raw output
                    st.download_button(
                        label="Download Raw Output",
                        data=result.stdout,
                        file_name="holehe_raw_output.txt",
                        mime="text/plain",
                    )
                else:
                    st.write("No results found.")
            except subprocess.CalledProcessError as e:
                st.write("Error executing Holehe command.")
                st.text(e.output)
            except Exception as e:
                st.write(f"An unexpected error occurred: {e}")
        else:
            st.write("Please enter a valid email address.")
# Run the app
if __name__ == "__main__":
    main()

Run
streamlit run app.py
