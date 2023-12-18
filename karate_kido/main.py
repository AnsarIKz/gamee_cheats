from PIL import ImageGrab
import pyautogui
import numpy as np
import keyboard  

def compare_colors(color1, color2, tolerance=10):
    for c1, c2 in zip(color1, color2):
        if abs(c1 - c2) > tolerance:
            return False
    return True

def get_average_color(x, y, radius=10):
    screenshot = ImageGrab.grab(bbox=(x - radius, y - radius, x + radius, y + radius))
    image_array = np.array(screenshot)
    average_color = np.mean(image_array, axis=(0, 1)).astype(int)

    return tuple(average_color)

def init_coords():
    print("Наведите мышку на интересующий участок(ветка слева) и нажмите клавишу Пробел:")
    coordinates = []
    try:
        keyboard.wait("space")
        x, y = pyautogui.position()
        coordinates.append((x,y))
        print(f"Координаты участка: x={x}, y={y}")
        print("Выбирете второй участок(ветка справа)")
        keyboard.wait("space")
        x, y = pyautogui.position()
        coordinates.append((x,y))
        print(coordinates)
        return True, coordinates
    except KeyboardInterrupt:
        print("Программа прервана пользователем.")
        return False, None

def start_game(coordinates):
    position = 0  # 0: left, 1: right
    left_coords, right_coords = coordinates
    
    while True:
        left_color = get_average_color(left_coords[0], left_coords[1])
        right_color = get_average_color(right_coords[0], right_coords[1])

        if position == 0:
            # Проверяем изменение цвета на левом участке
            pyautogui.press('left')
            if not compare_colors(left_color, get_average_color(left_coords[0], left_coords[1])):
                position = 1
                print("Переход на правый участок")
        else:
            # Проверяем изменение цвета на правом участке
            pyautogui.press('right')
            if not compare_colors(right_color, get_average_color(right_coords[0], right_coords[1])):
                position = 0
                print("Переход на левый участок")


def main():
    coordinates = None
    is_ready = False
    while not is_ready:
        is_ready, coordinates = init_coords()
    start_game(coordinates)
    pass

if __name__ == "__main__":
    main()
