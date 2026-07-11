from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _extract_text_with_ocr(pdf_path):
    """
    OCR fallback for scanned PDFs.

    Requires optional system setup:
    - pip install pdf2image pytesseract
    - install Tesseract OCR
    - install Poppler for Windows
    """

    try:
        from pdf2image import convert_from_bytes, convert_from_path
        import pytesseract
    except ImportError as exc:
        raise RuntimeError(
            "This PDF looks scanned, so normal text extraction found no text. "
            "To read scanned PDFs, install OCR support: "
            "pip install pdf2image pytesseract, then install Tesseract OCR and Poppler."
        ) from exc

    try:
        if hasattr(pdf_path, "getvalue"):
            images = convert_from_bytes(pdf_path.getvalue())
        else:
            images = convert_from_path(str(pdf_path))
    except Exception as exc:
        raise RuntimeError(
            "This scanned PDF needs Poppler to convert pages into images. "
            "Install Poppler for Windows and add its bin folder to PATH."
        ) from exc

    documents = []

    for page_number, image in enumerate(images):
        try:
            text = pytesseract.image_to_string(image)
        except Exception as exc:
            raise RuntimeError(
                "This scanned PDF needs Tesseract OCR. Install Tesseract OCR "
                "for Windows and add it to PATH, then restart VS Code."
            ) from exc

        if not text.strip():
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "page": page_number,
                    "source": getattr(pdf_path, "name", str(pdf_path)),
                    "extraction": "ocr",
                },
            )
        )

    return documents


# ------------------------------------------------------
# Load PDF
# ------------------------------------------------------

def load_pdf(pdf_path):
    """
    Load a PDF and convert each page into a LangChain Document.
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "page": page_number,
                    "source": getattr(pdf_path, "name", str(pdf_path))
                }
            )
        )

    if documents:
        return documents

    return _extract_text_with_ocr(pdf_path)


# ------------------------------------------------------
# Split Documents
# ------------------------------------------------------

def split_documents(documents):
    """
    Split documents into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    return chunks
