import os
from config import *
from core.pdf_extractor import extract_text
from core.text_chunker import chunk_text
from core.text_optimizer import optimize_for_tts
from core.tts_engine import synthesize_speech


def process_pdf(pdf_path, pdf_name):

    print(f"\nProcessing: {pdf_name}")

    raw_text = extract_text(pdf_path)

    if not raw_text.strip():
        print("❌ No text extracted → Skipping")
        return

    print("Optimizing text via Gemini...")
    clean_text = optimize_for_tts(raw_text)

    chunks = chunk_text(clean_text, CHUNK_SIZE)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{pdf_name}_part_{i}.mp3"
        )

        print(f"Generating: {output_file}")

        synthesize_speech(
            text=chunk,
            output_file=output_file,
            language_code=LANGUAGE_CODE
        )

    print("✅ Done.")


if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    print(f"Found {len(pdf_files)} PDF(s)")

    for pdf_file in pdf_files:

        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]

        process_pdf(pdf_path, pdf_name)
