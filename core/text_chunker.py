def chunk_text(text, chunk_size):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)

        if len(" ".join(current_chunk)) > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
