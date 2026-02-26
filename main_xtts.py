import os
from config import PDF_FOLDER, OUTPUT_DIR, CHUNK_SIZE

from core.pdf_extractor import extract_text
from core.text_chunker import chunk_text
from core.text_optimizer import optimize_for_tts
from core.pause_injector import inject_pauses
from core.xtts_engine import synthesize_speech

RAW_LOG_DIR = "raw_text_logs"
OPTIMIZED_LOG_DIR = "optimized_text_logs"


def save_text(directory, filename, content):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def load_text_if_exists(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def process_pdf(pdf_path, pdf_name):

    print(f"\nProcessing: {pdf_name}")

    # ---------------- RAW TEXT CACHE ----------------

    raw_path = os.path.join(RAW_LOG_DIR, f"{pdf_name}_raw.txt")
    raw_text = load_text_if_exists(raw_path)

    if raw_text and raw_text.strip():
        print("✔ Using cached raw text (PDF extraction skipped)")

    else:
        print(f"Extracting text from: {pdf_path}")

        raw_text = extract_text(pdf_path)

        if not raw_text or not raw_text.strip():
            print("❌ No text extracted → Skipping")
            return

        save_text(RAW_LOG_DIR, f"{pdf_name}_raw.txt", raw_text)
        print("✔ Raw text extracted & cached")

    # ---------------- OPTIMIZED TEXT CACHE ----------------

    optimized_path = os.path.join(
        OPTIMIZED_LOG_DIR,
        f"{pdf_name}_optimized.txt"
    )

    clean_text = load_text_if_exists(optimized_path)

    if clean_text and clean_text.strip():
        print("✔ Using cached optimized text (Gemini skipped)")

    else:
        print("Optimizing text for speech (Gemini call)...")

        try:
            clean_text = optimize_for_tts(raw_text)

            if not clean_text or not clean_text.strip():
                raise RuntimeError("Optimizer returned empty text")

            save_text(
                OPTIMIZED_LOG_DIR,
                f"{pdf_name}_optimized.txt",
                clean_text
            )

            print("✔ Optimizer succeeded & cached")

        except Exception as e:
            print(f"⚠ Optimizer failed → Using raw text | {e}")
            clean_text = raw_text

    # ---------------- PAUSE + CHUNK ----------------

    paused_text = inject_pauses(clean_text)

    if not paused_text or not paused_text.strip():
        print("❌ Pause injector returned empty text → Skipping")
        return

    chunks = chunk_text(paused_text, CHUNK_SIZE)

    if not chunks:
        print("❌ Chunker returned no chunks → Skipping")
        return

    print(f"Total chunks: {len(chunks)}")

    # ---------------- AUDIO CACHE ----------------

    for i, chunk in enumerate(chunks):

        if not chunk.strip():
            print(f"⚠ Skipping empty chunk {i}")
            continue

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{pdf_name}_part_{i}.wav"
        )

        if os.path.exists(output_file):
            print(f"✔ Audio already exists → Skipping {output_file}")
            continue

        print(f"Generating: {output_file}")

        try:
            synthesize_speech(
                text=chunk,
                output_file=output_file,
                speaker_wav=r"D:\Intern\sprouts TTS\speaker.wav"
            )

        except Exception as e:
            print(f"❌ XTTS failed for chunk {i}: {e}")
            return

    print("✅ Done.")


if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(PDF_FOLDER):
        raise RuntimeError(f"PDF folder not found: {PDF_FOLDER}")

    pdf_files = [
        f for f in os.listdir(PDF_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise RuntimeError("No PDF files found.")

    print(f"Found {len(pdf_files)} PDF(s)")

    for pdf_file in pdf_files:

        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]

        process_pdf(pdf_path, pdf_name)