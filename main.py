import cv2
import easyocr
import openai
import numpy as np
import requests
from streamlit_lottie import st_lottie
import streamlit as st

import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_coding = load_lottiefile(r"aman2.json")

#background
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://swosh-x.com/news/images/joomgrabber/2021-07/7ebc21cbb6.jpeg");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
set_bg_hack_url()

def sidebar_bg(side_bg_url):
    side_bg_ext = 'png'  # Replace with the appropriate file extension (e.g., jpg, png, etc.)

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url('{side_bg_url}');
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# URL for the sidebar background image
sidebar_image_url = "https://img.freepik.com/premium-photo/colorful-space-galaxy-cloud-nebula-stary-night_906149-2489.jpg"

sidebar_bg(sidebar_image_url)

# Set OpenAI API key
#api_key = st.text_input("Enter your API key:")
api_key = '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'
st.title("MedGuru Advisor")

# Display the entered API key
#st.write("You entered API key:", api_key)
openai.api_key = api_key



choice = st.radio("Choose an option", ('Image Upload', 'Webcam'))

if choice == 'Image Upload':
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Instance text detector
        reader = easyocr.Reader(['en'], gpu=False)

        # Detect text on image
        text_result = reader.readtext(img)

        threshold = 0.25
        recognized_text = ''
        for _, text, score in text_result:
            recognized_text += text + ' '
            if score > threshold:
                cv2.putText(img, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        st.subheader("Recognized Text:")
        st.write(recognized_text)

        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_column_width=True)

        # Generate response using OpenAI's GPT-3
        generated_text = openai.Completion.create(
            engine="text-davinci-003",
            prompt=recognized_text,
            max_tokens=200
        )

        st.subheader("MedGuru SUGGESSTION:")
        st.write(generated_text.choices[0].text.strip())

else:
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Access the webcam
    cap = cv2.VideoCapture(1)  # Change the value to use a different camera if needed
    capture_button = st.button("Capture Image")
    if capture_button:
        ret, frame = cap.read()
        if ret:
            # Detect text on captured frame
            text_result = reader.readtext(frame)

            threshold = 0.25
            recognized_text = ''
            for _, text, score in text_result:
                recognized_text += text + ' '
                if score > threshold:
                    cv2.putText(frame, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_column_width=True)

            st.subheader("Recognized Text:")
            st.write(recognized_text)

            # Generate response using OpenAI's GPT-3
            generated_text = openai.Completion.create(
                engine="text-davinci-003",
                prompt=recognized_text,
                max_tokens=200
            )

            st.subheader("Generated AI Response:")
            st.write(generated_text.choices[0].text.strip())


    # Release the camera and close all OpenCV windows after capturing the image
    cap.release()

#chatbot
def generate_response(prompt_text):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose a different engine if needed
        prompt=prompt_text,
        max_tokens=900  # Adjust the number of tokens for a longer response
    )

    return response.choices[0].text.strip()
# with st.sidebar:
#     st.title("MedGuru Advisor Chatbot")
#     st_lottie(lottie_coding, height=200, width=300)
#     prompt = st.text_input("for more suggestions Enter your opinion")
#     st.write("HI 👋  I am MedGuru bot")
#     generated_text = generate_response(prompt + " "+"medical advice")
#     if prompt:
#         st.write("MedGuru Response 🤖😁:")
#         st.write(generated_text)


# Display the local video with autoplay
video_path = r"asd.mp4"
st.video(video_path, start_time=0)

#chatbot
def generate_response(prompt_text):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose a different engine if needed
        prompt=prompt_text,
        max_tokens=900  # Adjust the number of tokens for a longer response
    )
    return response.choices[0].text.strip()
# Main content
st.title("MedGuru Advisor Chatbot")

# Toggle sidebar button
toggle_sidebar = st.button("MedGuru Advisor Chatbot", key="sidebar_button", on_click=None, args=None, kwargs=None, help=None)

# Sidebar content
if toggle_sidebar:
    with st.sidebar:
        st.title("MedGuru Advisor Chatbot")
        st_lottie(lottie_coding, height=200, width=300)
        prompt = st.text_input("For more suggestions, enter your opinion")
        st.write("HI 👋  I am MedGuru bot")
        generated_text = generate_response(prompt + " " + "medical advice")
        if prompt:
            st.write("MedGuru Response 🤖😁:")
            st.write(generated_text)


#Developers

# Function to display developer information
def show_developers():
    st.title("Developers")
    st.write(
        "Meet the team behind MedGuru Advisor! Here are the developers who contributed to this project:"
    )

    # Developer information with profile photos
    developers = [
        {
            "name": "Aman Chauhan",
            "bio": "Experienced in frontend development with expertise in HTML, CSS, and JavaScript.",
            "linkedin": "https://www.linkedin.com/in/aman-chauhan-128552256",
            "profile_photo": "https://media.licdn.com/dms/image/D5635AQHn9Inh4hXZ-g/profile-framedphoto-shrink_400_400/0/1693222064565?e=1703952000&v=beta&t=3nPXFqzGhEEu1fkoSDDxsw25gDooCwxwj0aV3UZMjkA",  # Insert the URL for the profile photo
        },
        {
            "name": "Vasu Johri",
            "bio": "Backend ninja skilled in Python, Flask, and databases.",
            "linkedin": "https://www.linkedin.com/in/vasu-johri-8b3b65245",
            "profile_photo": "https://media.licdn.com/dms/image/D5635AQHjz-2QLv6Mvg/profile-framedphoto-shrink_400_400/0/1683698010075?e=1703952000&v=beta&t=QWeApd2NG8_cDBN9hTTvzwNK0ug3wVWe2NRECRSE2JE",  # Insert the URL for the profile photo
        },
        # Add more developers as needed
    ]

    # Display developer information with circular profile photos
    for developer in developers:
        # Display circular profile photo above the name
        st.markdown(
            f'<img src="{developer["profile_photo"]}" alt="profile photo" style="width:100px; height:100px; border-radius:50%;">',
            unsafe_allow_html=True,
        )
        st.subheader(developer["name"])
        st.write(f"Bio: {developer['bio']}")
        if "linkedin" in developer:
            st.markdown(
                f'<a href="{developer["linkedin"]}" target="_blank">{developer["name"]} profile</a>',
                unsafe_allow_html=True,
            )
        st.write("---")

# Main content of the app
def main():
    # Button to display the developers' information
    if st.button("Show Developers"):
        show_developers()

if __name__ == "__main__":
    main()


st.header(":mailbox: Comments")

# Feedback form HTML
contact_form = """
<div class="feedback-form">
    <form action="https://formsubmit.co/amanchauhan20052005@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
</div>
"""

# CSS styles
css_styles = """
<style>
    /* Style inputs with type="text", type="email", and textareas */
    .feedback-form input[type=text], 
    .feedback-form input[type=email], 
    .feedback-form textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        margin-top: 6px;
        margin-bottom: 16px;
        resize: vertical;
    }

    /* Style the submit button with a specific background color etc */
    .feedback-form button[type=submit] {
        background-color: #04AA6D;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    /* When moving the mouse over the submit button, add a darker green color */
    .feedback-form button[type=submit]:hover {
        background-color: #45a049;
    }
</style>
"""

# Display the HTML and CSS
st.markdown(contact_form + css_styles, unsafe_allow_html=True)
