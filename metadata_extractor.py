import re

# Extracts basic SEC filing metedata from the beginning of document
def extract_metadata(text: str, source_path: str = "") -> dict:
    # Inspects only the first part of documents
    preview = text[:5000]

    # Filing type
    filing_type = "Unknown"
    if re.search(r"FORM\s+10-K", preview, re.IGNORECASE):
        filing_type = "10-K"
    elif re.search(r"FORM\s+10-Q", preview, re.IGNORECASE):
        filing_type = "10-Q"
    elif re.search(r"FORM\s+8-K", preview, re.IGNORECASE):
        filing_type = "8-K"

    # Company name
    company = "Unknown Company"

    # Multiple regex patterns to detect company name
    company_patterns = [
        r"\n\s*([A-Z][A-Z0-9&.,'\-\s]+?)\s*\n\s*\(Exact name of registrant",

        r"Exact name of registrant.*?\n\s*([A-Z][A-Z0-9&.,'\-\s]+)",

        r"FORM\s+(?:10-K|10-Q|8-K).*?\n\s*([A-Z][A-Z0-9&.,'\-\s]+?)\s*\n",
    ]

    for pattern in company_patterns:
        company_match = re.search(pattern, preview, re.IGNORECASE | re.DOTALL)

        if company_match:
            possible_company = company_match.group(1).strip()

            # Avoid bad matches
            if len(possible_company) > 3 and "SECURITIES" not in possible_company.upper():
                company = possible_company.title()
                break

    # Fiscal year
    year = "Unknown"

    year_match = re.search(
        r"For the fiscal year ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})",
        preview,
        re.IGNORECASE
    )

    if year_match:
        year = year_match.group(1).split()[-1]

    # Fallback for year
    if year == "Unknown":
        fallback_year = re.search(r"\b(20\d{2})\b", preview)
        if fallback_year:
            year = fallback_year.group(1)

    return {
        "company": company,
        "filing_type": filing_type,
        "year": year,
        "source": source_path
    }

# Testing
if __name__ == "__main__":
    from pdf_loader import load_pdf

    pdf_path = "data/raw/costco-8K.pdf"
    text = load_pdf(pdf_path)

    metadata = extract_metadata(text, pdf_path)
    print(metadata)