from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""

        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()

                if page_text is None:
                    print(f"Warning: Page {page_num} has no text.")
                    continue

                text += f"\n\n--- Page {page_num} ---\n{page_text}"

            except Exception as e:
                print(f"Error: Reading page {page_num}: {e}!")
                continue

        return text.strip()


if __name__ == "__main__":
    pdf_path = "data/raw/walmart-10k.pdf"

    text = load_pdf(pdf_path)

    print("PDF loaded successfully.")
    print("Number of characters:", len(text))
    print("\nPreview:")
    print(text[:1000])