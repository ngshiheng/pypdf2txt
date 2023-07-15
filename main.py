from pywebio import start_server
from pywebio.input import file_upload


def main():
    pdf_file = file_upload(
        "Select PDF",
        accept="application/pdf",
        max_size="1M",
        multiple=False,
    )
    print(pdf_file)


if __name__ == "__main__":
    start_server(main, port=8080, debug=True)
