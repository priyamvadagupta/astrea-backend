import chromadb

chroma_client = chromadb.PersistentClient(path="vector_db")
collection = chroma_client.get_or_create_collection("vedic_knowledge")


def retrieve_knowledge(query, n_results=12):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results.get("distances", [[]])[0]

    combined_chunks = []
    source_rows = []

    for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        source = meta.get("source", "Unknown source")
        distance = distances[i - 1] if distances else None

        combined_chunks.append(
            f"Chunk {i}\nSource: {source}\n{doc}"
        )

        source_rows.append({
            "Rank": i,
            "Source": source,
            "Distance": round(distance, 4) if distance is not None else "-",
            "Preview": doc[:300]
        })

    knowledge = "\n\n---\n\n".join(combined_chunks)

    return knowledge, source_rows