# Chunk Creation
def chunk_by_lines(text: str, max_lines: int = 3) -> list[str]:
    lines = text.split("\n")
    chunks = []

    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i:i + max_lines]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks
