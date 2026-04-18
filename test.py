import json
import pypdf

def extract_lines_with_coords(pdf_path: str, output_path: str):
    reader = pypdf.PdfReader(pdf_path)
    all_pages = []

    for page_num, page in enumerate(reader.pages):
        page_height = float(page.mediabox.height)
        chunks = []

        def visitor(text, cm, tm, font_dict, font_size):
            # tm is the text matrix [a,b,c,d,x,y]
            if not text.strip():
                return
            x = float(tm[4])
            y = float(tm[5])
            # pypdf uses PDF coords (origin bottom-left), flip Y for pdf.js
            y_flipped = page_height - y
            chunks.append({
                "text": text,
                "x": round(x, 2),
                "y": round(y, 2),
                "y_flipped": round(y_flipped, 2),
                "font_size": round(float(font_size), 2) if font_size else None,
            })

        page.extract_text(visitor_text=visitor)

        # Group chunks into lines: same Y (within tolerance) → same line
        tolerance = 2.0
        lines = []
        for chunk in sorted(chunks, key=lambda c: (c["y_flipped"], c["x"])):
            placed = False
            for line in lines:
                if abs(line["y_flipped"] - chunk["y_flipped"]) <= tolerance:
                    line["text"] += chunk["text"]
                    line["x_end"] = round(chunk["x"] + len(chunk["text"]) * chunk["font_size"] * 0.5, 2)
                    placed = True
                    break
            if not placed:
                lines.append({
                    "text": chunk["text"],
                    "x": chunk["x"],
                    "y_pdf": chunk["y"],        # PDF origin (bottom-left)
                    "y_flipped": chunk["y_flipped"],  # Screen origin (top-left)
                    "x_end": round(chunk["x"] + len(chunk["text"]) * (chunk["font_size"] or 10) * 0.5, 2),
                    "font_size": chunk["font_size"],
                })

        all_pages.append({"page": page_num + 1, "lines": lines})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_pages, f, indent=2, ensure_ascii=False)

    print(f"Wrote {sum(len(p['lines']) for p in all_pages)} lines → {output_path}")


extract_lines_with_coords("./(1) Synaptic transmission.pdf", "lines.json")