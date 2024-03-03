# _Resume Analyzer_

Analyze the resume document score based on job description. Extract the words using OCR, create word embeddings or tokens and check the similarity with job description embeddings.

_**PDF to Image Conversion:**_ The PDF resume is converted to images using pdf2image library.

_**Text Extraction from Images:**_ The text is extracted from the images using easyocr library.

_**Text Preprocessing:**_ The extracted text is preprocessed using SpaCy to remove stop words, lemmatize, and convert to lowercase.

_**Cosine Similarity Calculation:**_ The similarity between the preprocessed resume text and the job description text is calculated using TF-IDF vectors and cosine similarity.

_**Streamlit Interface:**_ Streamlit is used to create a user interface where users can upload the resume, input the job description, and see the similarity score.

_**Display Results:**_ The similarity score is displayed along with a pass/fail indication based on a predefined threshold

### How to use

```bash
streamlit run app.py 
```
