import argparse

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context.
If the context does not contain the answer, say you do not
know based on the provided documents.

Context:
{context}

Question: {question}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()

    query_rag(args.query_text)


def query_rag(query_text: str):
    # Connect to the existing Chroma database.
    embedding_function = get_embedding_function()

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
    )

    # Retrieve the five most relevant document chunks.
    results = db.similarity_search_with_score(query_text, k=5)

    if not results:
        print("No relevant document chunks were found.")
        return

    context_text = "\n\n---\n\n".join(
        doc.page_content for doc, score in results
    )

    # Build the prompt.
    prompt_template = ChatPromptTemplate.from_template(
        PROMPT_TEMPLATE
    )

    prompt = prompt_template.format(
        context=context_text,
        question=query_text,
    )

    # Generate an answer using the local Ollama model.
    model = ChatOllama(
        model="mistral",
        temperature=0,
    )

    response = model.invoke(prompt)
    response_text = response.content

    # Display the answer and source references.
    sources = [
        doc.metadata.get("id", "Unknown source")
        for doc, score in results
    ]

    print(f"\nResponse:\n{response_text}")
    print(f"\nSources:\n{sources}")

    return response_text


if __name__ == "__main__":
    main()