import fitz  # PyMuPDF
import json
import sys
from pathlib import Path


def extract_text_blocks(pdf_path: str) -> dict:
    """
    Extract all text blocks with their coordinates from a PDF.

    Coordinate system note:
      - PyMuPDF uses top-left origin (x0, y0, x1, y1)
      - PDF.js also uses a coordinate system starting from top-left
        when rendered on canvas, so no Y-axis flip is needed.
    """
    doc = fitz.open(pdf_path)
    output = {
        "file": Path(pdf_path).name,
        "total_pages": len(doc),
        "pages": []
    }

    for page_index, page in enumerate(doc):
        page_width = page.rect.width
        page_height = page.rect.height

        # get_text("blocks") returns a list of:
        # (x0, y0, x1, y1, text, block_no, block_type)
        # block_type: 0 = text, 1 = image
        raw_blocks = page.get_text("blocks")

        blocks = []
        for block in raw_blocks:
            x0, y0, x1, y1, text, block_no, block_type = block

            if block_type != 0:  # skip image blocks
                continue

            text = text.strip()
            if not text:
                continue

            blocks.append({
                "block_no": block_no,
                "text": text,
                "x": x0,
                "y": y0,
                "width": x1 - x0,
                "height": y1 - y0,
                # Normalized coords (0–1) — useful for responsive rendering
                "x_norm": x0 / page_width,
                "y_norm": y0 / page_height,
                "width_norm": (x1 - x0) / page_width,
                "height_norm": (y1 - y0) / page_height,
            })

        output["pages"].append({
            "page": page_index + 1,          # 1-based to match PDF.js pageNumber
            "width": page_width,
            "height": page_height,
            "blocks": blocks
        })

    doc.close()
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_text_blocks.py <path/to/file.pdf> [output.json]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "text_blocks.json"

    data = extract_text_blocks(pdf_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    total_blocks = sum(len(p["blocks"]) for p in data["pages"])
    print(f"✓ Extracted {total_blocks} text blocks across {data['total_pages']} pages")
    print(f"✓ Saved to: {output_path}")