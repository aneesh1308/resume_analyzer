import streamlit as st
import tempfile
from pdf2image import convert_from_path
import easyocr
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load Spacy model
nlp = spacy.load('en_core_web_sm')

# Function to convert PDF to images
def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images


# Function to extract text from image using EasyOCR and split into single words
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    extracted_text = []
    for result in results:
        words = result[1].split(' ')  # Split only when a space occurs
        extracted_text.extend(words)
    return extracted_text


# Function to preprocess the text using Spacy
def preprocess_text(text):
    doc = nlp(text)
    processed_text = ' '.join([token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha])
    return processed_text


# Function to analyze the resume and job description
def analyze_resume(resume_text, job_description):
    processed_resume_text = preprocess_text(resume_text)
    processed_job_description = preprocess_text(job_description)
    vectorizer = TfidfVectorizer()
    resume_vector = vectorizer.fit_transform([processed_resume_text])
    job_vector = vectorizer.transform([processed_job_description])

    # Calculate the cosine similarity
    similarity_score = cosine_similarity(resume_vector, job_vector)[0][0]
    return similarity_score


# Streamlit app
def main():
    st.title("Resume Analyzer")
    st.write("Upload a PDF resume and provide a job description.")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

    # Job description input
    job_description = st.text_area("Enter the job description")

    email_id = st.text_input("Enter your email ID")

    # Submit button
    submit_button = st.button("Analyze Resume")

    if uploaded_file is not None and job_description != "" and submit_button:
        # Read uploaded resume PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf.write(uploaded_file.read())

        # Convert PDF to images
        images = convert_pdf_to_images(temp_pdf.name)

        # Extract text from images
        extracted_text = []
        for i, image in enumerate(images):
            # Save image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
                image.save(temp_image.name)

            st.image(image, caption=f"Page {i + 1}", use_column_width=True)
            extracted_text = extract_text_from_image(temp_image.name)

        # Preprocess the extracted text
        processed_resume_text = preprocess_text(' '.join(extracted_text))
        processed_job_description = preprocess_text(job_description)

        # Analyze the resume and job description
        similarity_score = analyze_resume(processed_resume_text, processed_job_description)

        # Display the similarity score
        threshold = 0.6  # Set the similarity score threshold

        st.subheader("Resume-Job Description Similarity Score")
        score = round(similarity_score * 100, 2)
        st.write(score)

        # Check if the similarity score is above the threshold
        if similarity_score > threshold:
            st.markdown('<p style="color:green;font-size:20px">&#x2713; Resume Passed</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:red;font-size:20px">&#x2713; Resume failed</p>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
