from functools import partial
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

from pdfminer.high_level import extract_text_to_fp
from pywebio import config, session, start_server
from pywebio.input import file_upload
from pywebio.output import clear, put_buttons, put_code, put_markdown, toast, use_scope
from pywebio.session import download, run_js

config(title="Pypdf2")


def extract_text_from_pdf(pdf_file: dict[str, Any]) -> str:
    pdf_buffer = BytesIO(pdf_file['content'])
    text_buffer = StringIO()
    extract_text_to_fp(pdf_buffer, text_buffer)
    return text_buffer.getvalue()


def click_to_download(filename: str, text: bytes) -> None:
    download(
        filename,
        text,
    )
    toast('Text file downloaded')


def copy_to_clipboard(text: str) -> None:
    clipboard_setup = """
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
    run_js(clipboard_setup)
    run_js("writeText(text)", text=text)
    toast('Text copied to the clipboard')


def process_pdf() -> None:
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
            help_text="sample.pdf",
        )
        clear('text-output-area')

        text_output = extract_text_from_pdf(pdf_file)
        text_filename = f"{Path(pdf_file['filename']).stem}.txt"

        with use_scope('text-output-area'):
            put_markdown(
                """
                ### Text Output
                """,
            )

            put_code(text_output, rows=10)
            put_buttons(
                [
                    "Copy to Clipboard",
                    'Click to Download',
                ],
                onclick=[
                    partial(copy_to_clipboard, text=text_output),
                    partial(
                        click_to_download,
                        filename=text_filename,
                        text=text_output.encode(),
                    ),
                ],
            )


def render_description():
    put_markdown(
        """
        # Pypdf2

        A simple Python web service that allows you to convert your PDF documents to text.
        Extract text from PDF files without compromising privacy, security, and ownership.

        ## Features

        -   Converts PDF documents to text
        -   Simple and easy-to-use web interface
        -   Fast and efficient text extraction
        """,
    )


def main():
    session.run_js(
        'WebIO._state.CurrentSession.on_session_close(()=>{setTimeout(()=>location.reload(), 4000})',
    )

    render_description()
    process_pdf()


if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
