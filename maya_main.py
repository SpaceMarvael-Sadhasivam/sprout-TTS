import os
from config import *
from core.pdf_extractor import extract_text
from core.text_chunker import chunk_text
from core.text_optimizer import optimize_for_tts
from core.pause_injector import inject_pauses
from core.maya_tts_engine import synthesize_speech


RAW_LOG_DIR = "raw_text_logs"
OPTIMIZED_LOG_DIR = "optimized_text_logs"


def save_text(directory, filename, content):

    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def process_pdf(pdf_path, pdf_name):

    print(f"\nProcessing: {pdf_name}")
    print(f"Extracting text from: {pdf_path}")

    raw_text = extract_text(pdf_path)

    if not raw_text.strip():
        print("❌ No text extracted → Skipping")
        return

    # ✅ Save RAW extraction
    raw_log_file = save_text(
        RAW_LOG_DIR,
        f"{pdf_name}_raw.txt",
        raw_text
    )

    print(f"✔ Raw text saved → {raw_log_file}")

    print("Optimizing text via Gemini...")
    clean_text = optimize_for_tts(raw_text)

    if not clean_text.strip():
        print("❌ Gemini returned empty text → Skipping")
        return

    # ✅ Save OPTIMIZED text
    optimized_log_file = save_text(
        OPTIMIZED_LOG_DIR,
        f"{pdf_name}_optimized.txt",
        clean_text
    )

    print(f"✔ Optimized text saved → {optimized_log_file}")

    print("Injecting natural pauses...")
    paused_text = inject_pauses(clean_text)

    chunks = chunk_text(paused_text, CHUNK_SIZE)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        if not chunk.strip():
            print(f"⚠ Empty chunk {i} → Skipping")
            continue

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{pdf_name}_part_{i}.wav"
        )

        print(f"Generating: {output_file}")

        try:
            synthesize_speech(
                text=chunk,
                output_file=output_file,
                description=VOICE_DESCRIPTION
            )
        except Exception as e:
            print(f"⚠ Maya1 failed for chunk {i}: {e}")

    print("✅ Done.")


if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    if not pdf_files:
        raise RuntimeError("No PDF files found.")

    print(f"Found {len(pdf_files)} PDF(s)")

    for pdf_file in pdf_files:

        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]

        process_pdf(pdf_path, pdf_name)