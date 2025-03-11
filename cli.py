import argparse
from papers.fetch import fetch_paper_ids, fetch_paper_details, save_to_csv


def main():
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results")

    args = parser.parse_args()

    if args.debug:
        print(f"Query: {args.query}")

    paper_ids = fetch_paper_ids(args.query)
    if args.debug:
        print(f"Fetched IDs: {paper_ids}")

    papers = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            papers.append(details)

    if args.file:
        save_to_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)


if __name__ == "__main__":
    main()
