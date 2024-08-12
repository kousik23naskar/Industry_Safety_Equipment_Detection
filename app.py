import streamlit as st
import base64
from helper import train_model, predict_image, live_detection


# Set the page configuration
st.set_page_config(page_title="Safety Equipment Detection", page_icon="🦺", layout="wide")

# Title
#st.title("Safety Equipment Detection 👷 🥽 🦺 🧤 🥾 🛠️")
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5em;
    }
    </style>
    <h1 class="title">Safety Equipment Detection 👷 🛠️</h1>
    """, unsafe_allow_html=True)


# Sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.selectbox("Choose a page:", ["Home", "Train", "Predict", "Live Detection"])

# Home Page
if choice == "Home":
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://media.licdn.com/dms/image/D5612AQGsnDoKTrvsyw/article-cover_image-shrink_600_2000/0/1697783823369?e=2147483647&v=beta&t=Vxr-3wPAezmYM4_LWF9jXUYjMTZ_ptjStDIChyIVlbY", use_column_width=True, caption="Ensuring Safety in Industrial Environments")

    with col2:
        st.subheader("Welcome to the Safety Equipment Detection App!")
        st.write("""
        This application is designed to help you detect essential safety equipment in images using cutting-edge deep learning techniques.
        
        **Key Features:**
        - **Training**: Train the model with your own dataset.
        - **Prediction**: Upload an image to detect safety equipment like helmets, gloves, safety glasses, etc.
        - **Real-Time Processing**: Fast and efficient prediction results.

        Stay safe and ensure all necessary safety gear is in place before starting any industrial operation.
        """)

# Train Page
elif choice == "Train":
    st.subheader("Model Training")
    st.write("Click the button below to start training the model using the available dataset.")
    if st.button("Start Training"):
        train_model()

# Predict Page
elif choice == "Predict":
    st.subheader("Safety Equipment Prediction")
    st.write("Upload an image to predict the safety equipment present.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpeg","jpg","png"])

        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", width=300)
            # Convert the image to base64 string
            image_data = base64.b64encode(uploaded_file.read()).decode('utf-8')
    
    with col2:
        # Run prediction
        st.write("")
        st.write("")
        if st.button("Start Prediction"):
            if uploaded_file is not None:
                with st.spinner("Processing..."):
                    result = predict_image(image_data)
                    if result:
                        st.success("Prediction Done!")

                # Display the predicted image
                if result:
                    st.image(f"data:image/jpeg;base64,{result}", caption="Predicted Image", width=300)


# Live Detection Page
elif choice == "Live Detection":
    if st.button("Start Live Detection"):
        live_detection()


# Footer
st.markdown("""
<style>
.developer-label {
    position: fixed;
    bottom: 0;
    width: calc(100% - var(--sidebar-width, 0px)); /* Adjust width based on sidebar */
    text-align: center;
    background-color: #f0f0f0;
    padding: 10px;
    border-top: 1px solid #ddd;
    left: var(--sidebar-width, 0px); /* Adjust position based on sidebar */
}
</style>
<div class="developer-label">
    <p>Developed by Kousik Naskar | Email: <a href="mailto:kousik23naskar@gmail.com">kousik23naskar@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)