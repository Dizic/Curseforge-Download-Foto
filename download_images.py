import json
import os
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('mod_image_download.log'),
        logging.StreamHandler()
    ]
)

def sanitize_filename(filename):
    """
    Очищает имя файла от недопустимых символов
    """
    # Удаляем все символы, кроме букв, цифр, дефисов и подчеркиваний
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    # Ограничиваем длину имени файла
    return filename[:255]

def download_image(url, save_path):
    """
    Скачивает изображение по URL и сохраняет в указанный путь
    """
    try:
        # Проверяем, что URL не пустой
        if not url:
            logging.warning(f"Пустой URL для {save_path}")
            return False

        # Загрузка изображения
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Сохраняем изображение
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        logging.info(f"Скачано изображение: {url}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при скачивании {url}: {e}")
        return False

def process_mods_data(json_path='mods_data.json', images_dir='mods'): # mods нужно указать путь
    """
    Обработка JSON с модами и скачивание их изображений
    """
    # Загружаем данные о модах
    with open(json_path, 'r', encoding='utf-8') as f:
        mods_data = json.load(f)

    # Счетчики
    total_mods = len(mods_data)
    downloaded_mods = 0
    failed_mods = 0

    # Многопоточная загрузка изображений
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Список задач на скачивание
        futures = []
        for mod in mods_data:
            if mod.get('imageUrl'):
                # Генерируем имя файла из URL
                parsed_url = urlparse(mod['imageUrl'])
                filename = os.path.basename(parsed_url.path)
                
                # Очищаем и ограничиваем имя файла
                safe_mod_name = sanitize_filename(mod['name'])
                save_filename = f"{safe_mod_name}_{filename}"
                save_path = os.path.join(images_dir, save_filename)

                # Создаем задачу на скачивание
                future = executor.submit(download_image, mod['imageUrl'], save_path)
                futures.append((future, mod['name']))

        # Обработка результатов
        for future, mod_name in futures:
            try:
                result = future.result()
                if result:
                    downloaded_mods += 1
                else:
                    failed_mods += 1
            except Exception as e:
                logging.error(f"Ошибка при обработке мода {mod_name}: {e}")
                failed_mods += 1

    # Итоговая статистика
    logging.info(f"\nВсего модов: {total_mods}")
    logging.info(f"Скачано изображений: {downloaded_mods}")
    logging.info(f"Не удалось скачать: {failed_mods}")

if __name__ == '__main__':
    process_mods_data()
