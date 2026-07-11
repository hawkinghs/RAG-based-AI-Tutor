from io import BytesIO
import re
import textwrap


def _clean_text(text: str) -> str:
    text = re.sub(r"[*_`#>\[\]]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("latin-1", "replace").decode("latin-1")


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def create_text_pdf(title: str, content: str) -> bytes:
    """
    Create a simple downloadable PDF without external dependencies.
    """

    title = _clean_text(title or "Study Material")
    content = _clean_text(content or "")

    lines = [title, ""]
    for paragraph in content.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(paragraph, width=88) or [""])

    pages = []
    page_lines = []

    for line in lines:
        page_lines.append(line)
        if len(page_lines) >= 48:
            pages.append(page_lines)
            page_lines = []

    if page_lines:
        pages.append(page_lines)

    if not pages:
        pages = [["Study Material"]]

    objects = []

    def add_object(value: str) -> int:
        objects.append(value)
        return len(objects)

    font_obj = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_refs = []

    for page in pages:
        commands = ["BT", "/F1 11 Tf", "50 780 Td", "14 TL"]
        for line in page:
            commands.append(f"({_escape_pdf_text(line)}) Tj")
            commands.append("T*")
        commands.append("ET")
        stream = "\n".join(commands)
        content_obj = add_object(
            f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream"
        )
        page_obj = add_object(
            "<< /Type /Page /Parent 0 0 R "
            f"/MediaBox [0 0 612 792] /Resources << /Font << /F1 {font_obj} 0 R >> >> "
            f"/Contents {content_obj} 0 R >>"
        )
        page_refs.append(page_obj)

    pages_obj = add_object(
        "<< /Type /Pages /Kids ["
        + " ".join(f"{ref} 0 R" for ref in page_refs)
        + f"] /Count {len(page_refs)} >>"
    )

    for ref in page_refs:
        objects[ref - 1] = objects[ref - 1].replace("/Parent 0 0 R", f"/Parent {pages_obj} 0 R")

    catalog_obj = add_object(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>")

    buffer = BytesIO()
    buffer.write(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(buffer.tell())
        buffer.write(f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1"))

    xref_offset = buffer.tell()
    buffer.write(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    buffer.write(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        buffer.write(f"{offset:010d} 00000 n \n".encode("latin-1"))

    buffer.write(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF"
        ).encode("latin-1")
    )

    return buffer.getvalue()
