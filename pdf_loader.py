from pypdf import PdfReader

# Reads PDF file and returns extracted text as one string
# Page markers are added so retrieved chunks keep approximate location
def load_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""

        for page_num, page in enumerate(reader.pages, start=1):
            try:
                # Extracts text from current PDF
                page_text = page.extract_text()

                # If contained scanned images return None
                if page_text is None:
                    print(f"Warning: Page {page_num} has no text.")
                    continue

                # Add page markers
                text += f"\n\n--- Page {page_num} ---\n{page_text}"

            except Exception as e:
                # Continue loading other pages if one fails
                print(f"Error: Reading page {page_num}: {e}!")
                continue

        return text.strip()

# Testing
if __name__ == "__main__":
    pdf_path = "data/raw/walmart-10K.pdf"

    text = load_pdf(pdf_path)

    print("PDF loaded successfully.")
    print("Number of characters:", len(text))
    print("\nPreview:")
    print(text[:1000])