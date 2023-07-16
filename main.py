from functools import partial
from io import BytesIO, StringIO
from pathlib import Path

from pdfminer.high_level import extract_text_to_fp
from pywebio import config, start_server
from pywebio.input import file_upload
from pywebio.output import (
    clear,
    put_buttons,
    put_code,
    put_markdown,
    toast,
    use_scope,
)
from pywebio.session import download, run_js

config(title="Pypdf2txt")


def copy_to_clipboard(code):
    CLIPBOARD_SETUP = """
    window.writeText = function(text) {
        const input = document.createElement('textarea');
        input.style.opacity  = 0;
        input.style.position = 'absolute';
        input.style.left = '-100000px';
        document.body.appendChild(input);

        input.value = text;
        input.select();
        input.setSelectionRange(0, text.length);
        document.execCommand('copy');
        document.body.removeChild(input);
        return true;
    }
    """
    run_js(CLIPBOARD_SETUP)
    run_js("writeText(text)", text=code)
    toast('The text has been copied to the clipboard')


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
        """,
    )


def render_file_upload():
    put_markdown(
        """
        ## Convert PDF To Text
        """,
    )

    while True:
        pdf_file = file_upload(
            "Select PDF",
            accept="application/pdf",
            max_size="10M",
            multiple=False,
            help_text="example.pdf",
        )

        clear('text-output-area')

        pdf_buffer = BytesIO(pdf_file['content'])
        text_buffer = StringIO()

        extract_text_to_fp(pdf_buffer, text_buffer)

        output_str = text_buffer.getvalue()
        download_text_filename = f"{Path(pdf_file['filename']).stem}.txt"

        with use_scope('text-output-area'):
            put_markdown(
                """
                ### Text Output
                """,
            )

            put_code(output_str)
            put_buttons(
                [
                    "Copy to Clipboard",
                    'Click to Download',
                ],
                onclick=[
                    partial(copy_to_clipboard, code=output_str),
                    lambda: download(
                        download_text_filename,
                        output_str.encode(),
                    ),
                ],
            )


def main():
    render_description()
    render_file_upload()


if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
