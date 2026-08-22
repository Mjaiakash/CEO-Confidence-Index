from database.database import engine
from database.schema import initialize_database
from config import REPORT_DIR, TRANSCRIPT_DIR, PROCESSED_DIR, OUTPUT_DIR


def main():
    initialize_database(engine)
    for directory in (REPORT_DIR, TRANSCRIPT_DIR, PROCESSED_DIR, OUTPUT_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    print("CEO Confidence Index initialized successfully.")


if __name__ == "__main__":
    main()
