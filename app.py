import streamlit as st
from pdf2image import convert_from_bytes
from pdf_to_csv.converter import extract_text_from_area
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.set_page_config(layout="wide")
st.title("📄 PDF to CSV with Manual Table Area Selection")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file:
    pages = convert_from_bytes(uploaded_file.read())
    st.sidebar.markdown("### Page Navigation")
    page_num = st.sidebar.slider("Select page", 1, len(pages), 1)
    image = pages[page_num - 1]

    st.subheader(f"Page {page_num}")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="rect",
        key="canvas",
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        for obj in canvas_result.json_data["objects"]:
            left = obj["left"]
            top = obj["top"]
            width = obj["width"]
            height = obj["height"]
            coords = (left, top, left + width, top + height)
            st.markdown(f"**Extracting from area:** {coords}")
            text = extract_text_from_area(image, coords)
            st.text_area("Extracted Text", text, height=300)
            st.download_button("Download as CSV", text.replace("\n", "
"), file_name="output.csv")