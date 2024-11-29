import streamlit as st
from io import BytesIO
import subprocess
import os

def compress_pdf(file, compression_level):
    # Save the uploaded file to a temporary location
    input_path = "/tmp/input.pdf"
    output_path = "/tmp/output.pdf"
    
    with open(input_path, "wb") as f:
        f.write(file.read())
    
    # Define Ghostscript settings based on the selected compression level
    gs_compression_settings = {
        "screen": "/screen",
        "ebook": "/ebook",
        "printer": "/printer",
        "prepress": "/prepress"
    }
    
    # Get the Ghostscript setting for the selected compression level
    gs_setting = gs_compression_settings.get(compression_level, "/screen")
    
    # Run Ghostscript to compress the PDF
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        f"-dPDFSETTINGS={gs_setting}",
        "-dNOPAUSE",
        "-dBATCH",
        "-sOutputFile=" + output_path,
        input_path
    ]
    
    subprocess.run(gs_command, check=True)
    
    # Read the compressed file and return it as a BytesIO object
    with open(output_path, "rb") as f:
        compressed_file = BytesIO(f.read())
    
    return compressed_file

def main():
    st.title("PDF Compressor")
    
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    compression_level = st.selectbox("Select compression level", ["screen", "ebook", "printer", "prepress"])
    
    if st.button("Compress PDF"):
        if file is not None:
            compressed_file = compress_pdf(file, compression_level)
            st.download_button('Download Compressed PDF', compressed_file, file_name='compressed.pdf')

# Run the app
if __name__ == '__main__':
    main()