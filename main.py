import google.generativeai as genai
import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
genai.GenerationConfig(temperature = 0.7)

model = genai.GenerativeModel("gemini-pro-vision")

def get_response(image, imageType, captionType, language, input):
    prompt = f"""I am giving my image that I want to upload on a social media platform.
    Based on the given image which is a {imageType.upper()}, generate three {captionType.upper()} 
    captions for my social media post. Consider the below instructions: 
    INSTRUCTIONS:
    1. The captions should STRICTLY BE IN {language} LANGUAGE ONLY
    2. The captions should be unique
    3. The captions should describe the image and captivate the viewers and make the post memorable. 
    4. The captions should highlight the essence of the image, the location, the people or other things 
    present in the image. 
    5. If the image has only one person, write the captions in first person grammmar. 
    6. If the image has no person and has other things like scenary, animal, food etc, try to be 
    descriptive and creative in representing that. 
    7. THE OUTPUT SHOULD BE STRICTLY IN THE FORMAT:Caption1: output Caption2: output Caption3: output Hashtags: output. 
    8. DO NOT INCLUDE any hashtags in the captions and ONLY INCLUDE hashtags in the separate section.
    9. Do NOT GIVE MORE THAN 10 hashtags."""
    
    if input != "":
        response = model.generate_content([image, prompt, input])
    else:
        response = model.generate_content([image, prompt, ""])
    return response.text

st.set_page_config(page_title="Caption Generator")
st.header("Caption Generator")
st.info("""Select the suitable options and get a catchy and intuitive caption generated for your image. 
        Get ready to post it on your socials and shine""")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    imageType = st.selectbox("Image Type", options=["Selfie", "Solo Pic", "Scenary", "Group Photograph", 
                                                    "Memory", "Brand Marketing", "Animal", "Pet", 
                                                    "Food or Beverage", "Location", "Monument", "Other"], 
                                                    help="Select the type of photo")
    if imageType == "Other":
        imageType = st.text_input("Please specify", value="")
with col2:
    captionType = st.selectbox("Caption Type", options=["Catchy", "Intuitive", "Very Short", "One-word", 
                                                        "Professional", "Other"], 
                                                        help="Select the type of caption")
    if captionType == "Other":
        captionType = st.text_input("Please specify", value="")
with col3:
    languages = sorted(["Spanish", "French", "German", "Porteguese", "Italian", "Latin", "Hindi", 
                 "Bengali", "Marathi", "Mandarin", "Japanese", "Korean", "Arabic", "Tamil", "Telegu", 
                 "Kannada", "Greek", "Russian", "Urdu", "Other"])
    language = st.selectbox("Language", options=["English"] + languages,help="Select the language")
    if language == "Other":
        language = st.text_input("Please specify", value="")

input = st.text_input("Any additional details", value="")

uploaded_file = st.file_uploader("Choose an image", type=["JPEG", "JPG", "PNG"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file, formats=["JPEG", "JPG", "PNG"])
    st.image(image, caption="Uploaded Image", use_column_width=True)

st.text("")
submit = st.button("Generate captions", key="submit", type="primary", use_container_width=True)
if submit:
    if imageType == "":
        st.error("Please specify an image type")
    elif captionType == "":
        st.error("Please specify a caption type")
    else:
        try:
            captions = get_response(image, imageType, captionType, language, input)
            pos1 = captions.find("Caption2")
            caption1 = captions[10:pos1]
            captions = captions[pos1+10:]
            pos2 = captions.find("Caption3")
            caption2 = captions[:pos2]
            captions = captions[pos2+10:]
            pos3 = captions.find("Hashtags")
            caption3 = captions[:pos3]
            hashtags = captions[pos3+9:]

            print(caption1)
            print(caption2)
            print(caption3)
            print(hashtags)
            print("")

            st.subheader("Captions: ")
            st.markdown("1. " + caption1)
            st.markdown("2. " + caption2)
            st.markdown("3. " + caption3)
            st.divider()
            st.subheader("Hashtags: ")
            st.markdown(hashtags)
        except:
            if image is None:
                st.error("No image found. Please upload an image")
            else:
                st.error("Backend Error. Try Again")


