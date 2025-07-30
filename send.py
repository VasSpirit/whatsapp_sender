import webbrowser
from urllib.parse import quote
import pyautogui
import time

# Получаем размеры экрана один раз вне цикла
screen_width, screen_height = pyautogui.size()

# Остальные переменные и логика остаются прежними
CLICK_POSITION_X = None
CLIP_ICON_POSITION = None

def find_element(image_path):
    """Ищет элемент на экране"""
    element_position = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
    return element_position

def wait_for_element(image_path, timeout=10):
    """Ждет появление элемента на экране"""
    start_time = time.time()
    while True:
        position = find_element(image_path)
        if position:
            return position
        elif time.time() - start_time > timeout:
            raise TimeoutError(f"Элемент '{image_path}' не найден.")
        else:
            time.sleep(1)

# Основной цикл отправки сообщений
with open('phones.txt', 'r', encoding='utf-8') as phones_file:
    phones_and_names_list = phones_file.readlines()

for row in phones_and_names_list:
    row_list = row.strip().split(',')
    phone = row_list[0]
    name = row_list[1]
    attachment_path = row_list[2]

    message = f'Здравствуйте, {name}! Держите ваш уникальный сертификат для оказания услуг!'
    encoded_message = quote(message.encode('utf-8'))

    # Открыть страницу WhatsApp Web с указанным номером и текстом сообщения
    webbrowser.open(f'https://web.whatsapp.com/send?phone={phone}&text={encoded_message}')
    time.sleep(15)  # Ждем, пока страница откроется

    # Центр экрана для активации окна
    CLICK_POSITION_X = screen_width // 2
    CLICK_POSITION_Y = screen_height // 2
    pyautogui.click(CLICK_POSITION_X, CLICK_POSITION_Y)

    # Затем ищем иконку прикрепления (скрепку)
    clip_icon_position = wait_for_element('clip_icon.png')
    pyautogui.click(clip_icon_position)
    time.sleep(2)  # Ждем показ выпадающего меню

    # Ищем иконку "Документы" среди возможных типов вложений
    document_icon_position = wait_for_element('document_icon.png')
    pyautogui.click(document_icon_position)
    time.sleep(2)  # Подождём, пока появится окно выбора файла

    # Вводим путь к файлу и выбираем его
    pyautogui.write(attachment_path)
    pyautogui.press('enter')
    time.sleep(15)  # Ждем окончания загрузки файла

    # Отсылаем сообщение
    pyautogui.press('enter')
    time.sleep(10)

    # Закрываем вкладку браузера
    pyautogui.hotkey('ctrl', 'w')