import argparse
from .rag import RAGSystem


def main():
    parser = argparse.ArgumentParser(description="Ask the local RAG system a question.")
    parser.add_argument("question")
    parser.add_argument(
        "--strategy",
        choices=["lexical", "semantic", "hybrid"],
        default="hybrid",
    )
    args = parser.parse_args()

    rag = RAGSystem.from_config("config.yaml")
    result = rag.ask(args.question, strategy=args.strategy)

    print("\nAnswer")
    print("------")
    print(result["answer"])

    print("\nSources")
    print("-------")
    for source in result["sources"]:
        print(
            f"{source['rank']}. {source['title']} "
            f"({source['url']}) score={source['score']:.4f}"
        )


if __name__ == "__main__":
    main()
