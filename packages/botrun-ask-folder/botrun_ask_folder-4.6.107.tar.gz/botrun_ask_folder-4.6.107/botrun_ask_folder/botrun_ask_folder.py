import asyncio
import os

from botrun_ask_folder.botrun_drive_manager import botrun_drive_manager
from botrun_ask_folder.drive_download import drive_download
from botrun_ask_folder.embeddings_to_qdrant import embeddings_to_qdrant
from botrun_ask_folder.run_split_txts import run_split_txts


def botrun_ask_folder(google_drive_folder_id: str) -> None:
    google_service_account_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS",
                                                "/app/keys/google_service_account_key.json")
    drive_download(
        google_service_account_key_path,
        google_drive_folder_id,
        9999999,
        output_folder=f"./data/{google_drive_folder_id}")

    run_split_txts(
        f"./data/{google_drive_folder_id}",
        2000,
        False)

    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_port = os.getenv("QDRANT_PORT", 6333)
    asyncio.run(embeddings_to_qdrant(
        f"./data/{google_drive_folder_id}",
        "openai/text-embedding-3-large",
        3072,
        30,
        f"{google_drive_folder_id}",
        qdrant_host,
        qdrant_port))

    botrun_drive_manager(f"波{google_drive_folder_id}", f"{google_drive_folder_id}")
