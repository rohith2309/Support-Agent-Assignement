import re
from pathlib import Path
from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from support_agent_assignement.config import settings

FAQ_PATH = Path(__file__).resolve().parents[1] / "Data" / "faq.md"


def load_and_chunk_faq(faq_path: str | Path = FAQ_PATH) -> list[Document]:
    """Splits faq.md into 12 atomic Document chunks (F01..F12), excluding internal support rules."""
    raw_text = Path(faq_path).read_text(encoding="utf-8")

    # Remove the internal rules section at the bottom of faq.md
    faq_body = raw_text.split("## The client's rules for the support team")[0]

    # Split right before every "## F01", "## F02", ..., "## F12" heading
    sections = re.split(r"(?=^## F\d{2}\b)", faq_body, flags=re.MULTILINE)

    documents: list[Document] = []
    for section in sections:
        section = section.strip()
        if not section.startswith("## F"):
            continue

        # Parse header: "## F02 · Adding a new employee" -> faq_id="F02"
        header_line = section.splitlines()[0]
        faq_id = header_line.split("·")[0].replace("##", "").strip()

        documents.append(
            Document(
                page_content=section,
                metadata={"faq_id": faq_id, "header": header_line.replace("## ", "").strip()},
            )
        )

    return documents


def build_faq_retriever(faq_path: str | Path = FAQ_PATH, k: int = 3):
    """Builds an in-memory Bedrock vector retriever over the 12 FAQ chunks."""
    chunks = load_and_chunk_faq(faq_path)
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",region_name=settings.aws_region_name,aws_access_key_id=settings.aws_access_key_id,aws_secret_access_key=settings.aws_secret_access_key)
    vectorstore = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})