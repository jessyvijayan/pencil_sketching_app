import streamlit as st
import cv2
import numpy as np
from PIL import Image

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    def dodge(x,y):
        return cv2.divide(x,255-y,scale=256)

    def pencil_sketch(img):
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_invert = cv2.bitwise_not(img_gray)
        img_smoothing = cv2.GaussianBlur(img_invert,(21,21),sigmaX=0,sigmaY=0)
        final_img = dodge(img_gray,img_smoothing)
        return(final_img)

    st.title('Pencilsketch App')
    st.write('This app converts photos to pencil sketches')

    file_image = st.sidebar.file_uploader('Upload photos',type = ['jpeg','jpg','png','jfif'])
    if file_image is None:
        st.write('No file has been uploaded')
    else:    
        input_img = Image.open(file_image)
        finalsketch = pencil_sketch(np.array(input_img))
        st.write('**Input Photo**')
        st.image(file_image)
        st.write('**Output Photo**')
        st.image(finalsketch)


