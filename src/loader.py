from pathlib import Path
import re
from typing import List

from .schemas import Document


META_PATTERN = re.compile(r"^([A-Za-z_]+):\s*(.+)$")


def load_documents(directory: str | Path) -> List[Document]:
    directory = Path(directory)
    documents = []

    for path in sorted(directory.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        metadata = {}
        body_lines = []

        in_header = True
        for line in raw.splitlines():
            if in_header:
                match = META_PATTERN.match(line.strip())
                if match and match.group(1).lower() in {"title", "url"}:
                    metadata[match.group(1).lower()] = match.group(2).strip()
                    continue
                if not line.strip():
                    continue
                in_header = False
            body_lines.append(line)

        title = metadata.get("title", path.stem.replace("-", " ").title())
        url = metadata.get("url", f"https://docs.example.local/{path.stem}")
        text = "\n".join(body_lines).strip()

        documents.append(
            Document(
                document_id=path.stem,
                title=title,
                source=path.name,
                url=url,
                text=text,
            )
        )

    if not documents:
        raise ValueError(f"No Markdown documents found in {directory}")

    return documents
