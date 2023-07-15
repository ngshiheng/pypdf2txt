from io import BytesIO, StringIO

from pdfminer.high_level import extract_text_to_fp
from pywebio import start_server
from pywebio.input import file_upload
from pywebio.output import put_code, put_markdown


def render_description():
    put_markdown(
        """
        # Pypdf2txt

        A simple Python web service that allows you to convert your PDF documents to text. This provides a user-friendly and efficient way to extract text from PDF files without compromising privacy, data security, and ownership.

        ## Features

        -   Converts PDF documents to text
        -   Simple and easy-to-use web interface
        -   Supports processing multiple PDF files simultaneously
        -   Fast and efficient text extraction
        """
    )


def render_file_upload():
    put_markdown(
        """
        ## Convert PDF To Text
        """
    )

    pdf_file = file_upload(
        "Select PDF",
        accept="application/pdf",
        max_size="10M",
        multiple=False,
        help_text="example.pdf",
    )
    pdf_buffer = BytesIO(pdf_file['content'])
    output_text = StringIO()

    extract_text_to_fp(pdf_buffer, output_text)
    put_code(output_text.getvalue())


def main():
    render_description()
    render_file_upload()


if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
