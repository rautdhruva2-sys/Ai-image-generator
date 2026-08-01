import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from urllib.parse import quote
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables
load_dotenv()

IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "generated_images")


# Create image folder
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)



# Page Configuration
st.set_page_config(
    page_title="AI Image Creator",
    page_icon="🎨",
    layout="centered"
)


st.title("🎨 AI Image Creator - Text to Image")
st.write("Generate AI images using your text prompt")



# Available styles

styles = {
    "Realistic":
    "A highly realistic photograph with detailed textures, natural lighting, and professional camera quality",

    "Cartoon":
    "A colorful cartoon style illustration with creative characters and smooth animation style",

    "Anime":
    "A detailed anime artwork with expressive characters, vibrant colors, and Japanese animation style",

    "Watercolor":
    "A beautiful watercolor painting style with artistic brush strokes and soft colors",

    "Cyberpunk":
    "A futuristic cyberpunk illustration with neon lights, advanced technology, futuristic city, cinematic lighting",

    "Fantasy":
    "A magical fantasy artwork with mythical elements, dramatic atmosphere, and cinematic details"
}



# User Input

prompt = st.text_input(
    "Enter your image description:",
    placeholder="Example: A cat sitting in a futuristic city"
)


style = st.selectbox(
    "Choose Image Style:",
    list(styles.keys())
)



def enhance_prompt(user_prompt, selected_style):

    enhanced = f"""
    {styles[selected_style]}.
    Create an image of {user_prompt}.
    Highly detailed, 8K quality, cinematic composition,
    professional digital artwork.
    """

    return enhanced.strip()



def generate_image(final_prompt):

    try:

        encoded_prompt = quote(final_prompt)

        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        )


        response = requests.get(url, timeout=60)


        if response.status_code == 200:

            image = Image.open(
                BytesIO(response.content)
            )

            return image

        else:
            return None


    except Exception as e:

        st.error(f"API Error: {e}")

        return None




if st.button("Generate Image 🚀"):


    if prompt.strip() == "":

        st.warning("Please enter a prompt")


    else:


        with st.spinner("Creating your AI image..."):


            final_prompt = enhance_prompt(
                prompt,
                style
            )


            image = generate_image(
                final_prompt
            )


            if image:


                # Save image

                filename = (
                    f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )


                save_path = os.path.join(
                    IMAGE_FOLDER,
                    filename
                )


                image.save(save_path)



                st.success(
                    "Image generated successfully!"
                )


                st.subheader("Selected Style")

                st.info(style)



                st.subheader(
                    "Final Enhanced Prompt"
                )

                st.write(final_prompt)



                st.subheader(
                    "Generated Image"
                )

                st.image(
                        "image.png",
                           use_column_width=True
)



                st.subheader(
                    "Image Save Location"
                )

                st.code(
                    save_path
                )



                # Download Button

                with open(
                    save_path,
                    "rb"
                ) as file:


                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name=filename,
                        mime="image/png"
                    )


            else:

                st.error(
                    "Image generation failed"
                )