import streamlit as st
from Mashup102103554 import main  # Assuming your program1 is in a file named program1.py
import os
import shutil
from tempfile import mkdtemp
from zipfile import ZipFile
from flask_mail import Mail, Message
from flask import Flask

# Streamlit configuration
st.set_page_config(page_title="Mashup Web Service")

app = Flask(__name__)
# Email configuration
mail = Mail()
mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",  # Change this to your SMTP server address
    "MAIL_PORT":'465',
    "MAIL_USE_SSL":True,
    "MAIL_USE_TLS": False,  # Enable TLS encryption
    "MAIL_USERNAME":'cgupta_be21@thapar.edu',
    "MAIL_PASSWORD":'garz bugk ggjv kcnf'
}

app.config.update(mail_settings)
mail.init_app(app)

# Function to perform the mashup and send the result via email
def perform_mashup(singer_name, num_videos, audio_duration, email):
    try:
        # Perform mashup
        output_filename = f'{singer_name}_mashup.mp3'
        main(singer_name, num_videos, audio_duration, output_filename)
        # main()

        # Create a temporary directory to store the result files
        temp_dir = mkdtemp()

        # Move the output file to the temporary directory
        output_file_path = os.path.join(temp_dir, output_filename)
        shutil.move(output_filename, output_file_path)

        # Create a zip file containing the output file
        zip_file_path = os.path.join(temp_dir, 'mashup_result.zip')
        with ZipFile(zip_file_path, 'w') as zipf:
            zipf.write(output_file_path, arcname=output_filename)

        # Send the zip file via email
        msg = Message('Mashup Result', recipients=[email])
        msg.body = 'Please find the attached mashup result.'
        with open(zip_file_path, 'rb') as attachment:
            msg.attach('mashup_result.zip', 'application/zip', attachment.read())
        mail.send(msg)

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

        return True, None
    except Exception as e:
        return False, str(e)

# Streamlit web application
def main():
    st.title("Mashup Web Service")

    # User inputs
    singer_name = st.text_input("Singer Name",key="Singer_name_input")
    num_videos = st.number_input("Number of Videos", min_value=11, step=1,key="video")
    audio_duration = st.number_input("Duration of Each Video (seconds)", min_value=21, step=1,key="cut")
    email = st.text_input("Email Address",key="email_input")

    if st.button("Submit"):
        if not (singer_name and email):
            st.error("Please provide Singer Name and Email Address.")
        else:
            st.info("Performing mashup... This may take a while.")
            success, error = perform_mashup(singer_name, num_videos, audio_duration, email)
            if success:
                st.success("Mashup result sent to your email.")
            else:
                st.error(f"Failed to perform mashup: {error}")

if __name__ == "__main__":
    main()
