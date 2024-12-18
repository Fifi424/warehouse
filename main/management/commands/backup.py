from django.core.management.base import BaseCommand
from main.backup_to_yandex import backup_and_upload

class Command(BaseCommand):
    help = "Создаёт резервную копию базы данных и загружает её на Яндекс.Диск."

    def handle(self, *args, **options):
        self.stdout.write("Начало резервного копирования базы данных...")
        try:
            backup_and_upload()
            self.stdout.write(self.style.SUCCESS("Резервное копирование успешно завершено!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка резервного копирования: {e}"))
