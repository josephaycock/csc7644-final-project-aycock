import argparse

from rag_pipeline import build_store_vector, retrieve_chunks, generate_results

# Default PDF used if the user does not pass a --pdf
DEFAULT_PDF_PATH = "data/raw/walmart-10K.pdf"

# Builds the vector DB from a PDF
def build_command(args):
    build_store_vector(args.pdf)

# Handles user questions from CLI and retrieves relevant chunk for LLM
def query_command(args):
    results = retrieve_chunks(args.query, n_results=args.top_k)
    retrieved_docs = results["documents"][0]

    answer = generate_results(args.query, retrieved_docs)

    print("\nAsk Question:")
    print(args.query)

    print("\nAnswer:")
    print(answer)

    if args.show_sources:
        print("\nSources:")

        for i, doc in enumerate(retrieved_docs, start=1):
            metadata = results["metadatas"][0][i - 1]

            print(f"\n----- Source {i} -----")
            print(
                f"Company Name: {metadata.get('company')} | "
                f"Company Filing: {metadata.get('filing_type')} | "
                f"Year: {metadata.get('year')}"
            )

            print(doc[:args.source_chars])

# Defines CLI commands
# build: creates vector DB from PDF
# ask: ask a question against the indexed filing
def main():
    parser = argparse.ArgumentParser(
        description="RAG Financial Analyzer CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Build command
    build_parser = subparsers.add_parser(
        "build",
        help="Builds the ChromaDB vector store DB from a PDF"
    )

    build_parser.add_argument(
        "--pdf",
        default=DEFAULT_PDF_PATH,
        help="Path the financial filing PDF"

    )

    build_parser.set_defaults(func=build_command)

    # Ask command
    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask a question about the financial filing stored"
    )

    ask_parser.add_argument(
        "query",
        help="Question to ask the RAG-based system"
    )

    ask_parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of chunks to retrieve from stored DB"
    )

    ask_parser.add_argument(
        "--show-sources",
        action="store_true",
        help="Show the retrieved source chunks"
    )

    ask_parser.add_argument(
        "--source-chars",
        type=int,
        default=1000,
        help="Number of chars to show per source found"
    )

    ask_parser.set_defaults(func=query_command)
    args = parser.parse_args()
    # Calls either build_command or query_command based on user input
    args.func(args)

if __name__ == "__main__":
    main()