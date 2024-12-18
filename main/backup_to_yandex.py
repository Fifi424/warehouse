import os
import datetime
import yadisk
from pathlib import Path

def backup_and_upload():
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASSWORD = "14789632"
    BACKUP_DIR = Path(__file__).resolve().parent / "backups"
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    YANDEX_TOKEN = "y0_AgAAAABlCIcPAAz4oQAAAAEcnPdEAADbib-Tl_VHYKR46a1TRK2-fQMirg" 
    REMOTE_DIR = "/backups"

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"backup_{timestamp}.sql"

    print("Начало резервного копирования базы данных...")

    os.environ["PGPASSWORD"] = DB_PASSWORD

    command = f'pg_dump -U {DB_USER} -h localhost {DB_NAME} > "{backup_file}"'
    os.system(command)

    print(f"Резервная копия создана: {backup_file}")

    try:
        y = yadisk.YaDisk(token=YANDEX_TOKEN)

        if not y.exists(REMOTE_DIR):
            y.mkdir(REMOTE_DIR)

        with open(backup_file, 'rb') as file_obj:
            y.upload(file_obj, f"{REMOTE_DIR}/{backup_file.name}")

        print(f"Файл загружен на Яндекс.Диск: {REMOTE_DIR}/{backup_file.name}")
    except Exception as e:
        print(f"Ошибка загрузки на Яндекс.Диск: {e}")
    finally:
        if backup_file.exists():
            os.remove(backup_file)
            print(f"Локальный файл удалён: {backup_file}")

    print("Резервное копирование успешно завершено!")
