import tensorflow as tf
import imgaug.augmenters as iaa
import imgaug as ia
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D,GlobalMaxPooling2D, Input
from tensorflow.keras.optimizers import Adam
import numpy as np
import json
import cv2
import os
from tensorflow.keras.losses import MeanSquaredError

def greet(name):
    return f"Hello, {name}!"


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def crop_image(image, left, right, top, bottom):
    # Получаем размеры изображения
    height, width = image.shape[:2]

    # Вычисляем новые границы после обрезки
    new_left = left
    new_right = width - right
    new_top = top
    new_bottom = height - bottom

    # Обрезаем изображение с новыми границами
    cropped_image = image[new_top:new_bottom, new_left:new_right]

    return cropped_image


def adjust_image(image, white_threshold=200, black_threshold=50):
    # Конвертирование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение порогового значения для создания двоичного изображения
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # Применение морфологических операций для устранения шума
    kernel = np.ones((5, 5), np.uint8)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    # Создание маски для белых пикселей
    white_mask = cv2.inRange(gray_image, white_threshold, 255)

    # Создание маски для черных пикселей
    black_mask = cv2.inRange(gray_image, 0, black_threshold)

    # Применение маски к изображению
    white_pixels = cv2.bitwise_and(image, image, mask=white_mask)
    black_pixels = cv2.bitwise_and(image, image, mask=black_mask)

    # Замена белых пикселей на абсолютно белые
    white_pixels[white_pixels > 0] = 255

    # Замена черных пикселей на абсолютно черные
    black_pixels[black_pixels > 0] = 0

    # Объединение изображений
    result_image = cv2.add(white_pixels, black_pixels)

    return result_image


def straighten_image(image):
    data = straighten_image_data(image)
    center = data['center']
    skew_angle = data['skew_angle']
    original_size_0 = data['original_size'][0]
    original_size_1 = data['original_size'][1]
    M = cv2.getRotationMatrix2D(center, skew_angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (original_size_0, original_size_1), flags=cv2.INTER_CUBIC,
                                   borderMode=cv2.BORDER_REPLICATE)
    return rotated_image


def straighten_image_data(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines using Probabilistic Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if lines is not None:
        # Calculate the angle of each line
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angles.append(angle)

        # Convert angles to a numpy array
        angles = np.array(angles)

        # Compute the median angle
        median_angle = np.median(angles)

        # Filter out angles that deviate too much from the median
        diff = np.abs(angles - median_angle)
        filtered_angles = angles[diff < 10]  # Filtering threshold can be adjusted

        if len(filtered_angles) > 0:
            # Calculate the robust mean angle of the filtered angles
            skew_angle = np.mean(filtered_angles)

            # Calculate the new bounding box after rotation
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, skew_angle, 1.0)

            # Compute the new bounding box dimensions
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            new_w = int(h * sin + w * cos)
            new_h = int(h * cos + w * sin)

            # Compute the changes in dimensions
            left_diff = (new_w - w) // 2
            right_diff = (new_w - w) - left_diff
            top_diff = (new_h - h) // 2
            bottom_diff = (new_h - h) - top_diff

            # Return the results
            return {
                'skew_angle': skew_angle,
                'left_diff': left_diff,
                'right_diff': right_diff,
                'top_diff': top_diff,
                'bottom_diff': bottom_diff,
                'original_size': (w, h),
                'new_size': (new_w, new_h),
                'center': center
            }
        else:
            raise Exception("No valid angles detected after filtering.")
    else:
        raise Exception("No lines detected. The image might be too noisy or not contain clear edges.")


def crop_image_without_background_data(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Create a binary mask using adaptive thresholding
    binary_mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)

    # Apply median blur to remove small noise
    binary_mask = cv2.medianBlur(binary_mask, 5)

    # Apply morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=2)

    # Remove small noise by filtering small contours
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 1000  # Minimum area threshold to consider a contour as part of the document

    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    if filtered_contours:
        # Initialize variables to hold the minimum and maximum coordinates
        x_min = float('inf')
        y_min = float('inf')
        x_max = float('-inf')
        y_max = float('-inf')

        # Iterate over filtered contours to find the overall bounding box
        for contour in filtered_contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        # Ensure the coordinates are within the image bounds
        x_min = int(max(x_min, 0))
        y_min = int(max(y_min, 0))
        x_max = int(min(x_max, image.shape[1]))
        y_max = int(min(y_max, image.shape[0]))

        # Adjust the top, bottom, left, and right bounds to include more content
        y_min = max(y_min - 10, 0)
        y_max = min(y_max + 10, image.shape[0])
        x_min = max(x_min - 10, 0)
        x_max = min(x_max + 10, image.shape[1])

        # Crop the image using the bounding box
        cropped_image = image[y_min:y_max, x_min:x_max]

        # Calculate original and cropped sizes
        original_height, original_width = image.shape[:2]
        cropped_height, cropped_width = cropped_image.shape[:2]

        # Calculate the number of pixels cropped from each side
        left_crop = x_min
        right_crop = original_width - x_max
        top_crop = y_min
        bottom_crop = original_height - y_max

        return {
            'original_size': (original_width, original_height),
            'cropped_size': (cropped_width, cropped_height),
            'left_crop': left_crop,
            'right_crop': right_crop,
            'top_crop': top_crop,
            'bottom_crop': bottom_crop,
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'contours': filtered_contours
        }
    else:
        raise Exception("No contours found. The image might be completely white or empty.")


def crop_image_without_background(image):
    data = crop_image_without_background_data(image)
    contours = data['contours']
    y_min = data['y_min']
    y_max = data['y_max']
    x_min = data['x_min']
    x_max = data['x_max']
    if contours:
        # Crop the image using the bounding box
        cropped_image = image[y_min:y_max, x_min:x_max]
        return cropped_image
    else:
        raise Exception("No contours found. The image might be completely white or empty.")


def resize_objects(image, new_width, new_height):
    # Уменьшение масштаба объектов на изображении
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Создание нового изображения с теми же размерами, что и исходное
    height, width = image.shape[:2]
    new_image = np.full((height, width, 3), 255, dtype=np.uint8)

    # Рассчитываем смещение, чтобы поместить уменьшенное изображение по центру
    x_offset = (width - new_width) // 2
    y_offset = (height - new_height) // 2

    # Помещение уменьшенного изображения на новое изображение
    new_image[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image

    return new_image


def resize_image(image, new_width, new_height):
    # Изменение размера изображения
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_image


def resize_image_data(image, new_width, new_height):
    # Get original dimensions
    original_height, original_width = image.shape[:2]
    return {
        'original_height': original_height,
        'original_width': original_width,
        'new_width': new_width,
        'new_height': new_height
    }


def show_img(img, title):
    plt.figure()
    plt.imshow(img)
    plt.title(title)
    # plt.axis('off')
    plt.show()


def increase_contrast(image, alpha, beta):
    """
    Увеличивает контраст изображения.

    Параметры:
        image: numpy.ndarray
            Изображение в формате numpy.ndarray.
        alpha: float
            Множитель контраста. Значение alpha > 1 увеличит контраст, alpha < 1 уменьшит контраст.
        beta: int
            Сдвиг контраста. Значение beta добавляется к каждому пикселю изображения.

    Возвращает:
        numpy.ndarray: Изображение с увеличенным контрастом.
    """
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image


def remove_noise(image, kernel_size=3):
    # Применяем медианный фильтр для удаления шума
    denoised_image = cv2.medianBlur(image, kernel_size)

    return denoised_image


def crop_image_by_percentages(image, left_percent, right_percent, top_percent, bottom_percent):
    # Получение размеров изображения
    height, width = image.shape[:2]

    # Вычисление числа пикселей для каждой стороны, которые нужно обрезать
    top_pixels = int(height * top_percent / 100)
    bottom_pixels = int(height * bottom_percent / 100)
    left_pixels = int(width * left_percent / 100)
    right_pixels = int(width * right_percent / 100)

    # Обрезка изображения
    cropped_image = image[top_pixels:height - bottom_pixels, left_pixels:width - right_pixels]

    return cropped_image


def draw_polygon_on_image(input_image, polygon_coords, color=(0, 255, 0)):
    # Преобразование координат в целые числа
    polygon_coords = np.array(polygon_coords, np.int32)

    # Преобразование формы координат
    polygon_coords = polygon_coords.reshape((-1, 1, 2))

    # Копирование изображения для сохранения оригинала неизмененным
    image_with_polygon = input_image.copy()

    # Рисование полигона на изображении
    cv2.polylines(image_with_polygon, [polygon_coords], isClosed=True, color=color, thickness=2)

    return image_with_polygon


def math_rotate_coordinates(x, y, angle):
    # Поворот координат на заданный угол
    radians = np.deg2rad(angle)
    new_x = x * np.cos(radians) - y * np.sin(radians)
    new_y = x * np.sin(radians) + y * np.cos(radians)
    return new_x, new_y


def coco_transform_to_x_y_format(coco_segmentation_item_poly):
    return np.array(coco_segmentation_item_poly).reshape((-1, 2))


def coco_transform_bbox_to_coordinates_numpy(coco_bbox):
    """
    Преобразует координаты ограничивающей рамки из формата COCO в формат (x_min, y_min), (x_max, y_max) с использованием numpy.

    :param coco_bbox: Список координат в формате COCO [x, y, width, height]
    :return: Массив numpy с двумя точками [[x_min, y_min], [x_max, y_max]]
    """
    x_min, y_min, width, height = coco_bbox
    x_max = x_min + width
    y_max = y_min + height
    return np.array([[x_min, y_min], [x_max, y_max]])


def change_angle_poly_x_y_format(x_y_poly_items, angle):
    data = []
    for index, item in enumerate(x_y_poly_items):
        x = item[0]
        y = item[1]
        changed_item = math_rotate_coordinates(x, y, angle)
        new_x, new_y = changed_item
        data.append([new_x, new_y])
    return np.array(data)


def correct_polygon_coords_straighten(old_coords, straighten_results):
    skew_angle = straighten_results['skew_angle']
    center = straighten_results['center']
    left_diff = straighten_results['left_diff']
    right_diff = straighten_results['right_diff']
    top_diff = straighten_results['top_diff']
    bottom_diff = straighten_results['bottom_diff']
    original_size = straighten_results['original_size']
    new_size = straighten_results['new_size']

    # Convert skew angle to radians
    skew_angle_rad = np.radians(skew_angle)  # Positive angle for reverse transformation

    # Define the rotation matrix for reverse transformation
    reverse_rotation_matrix = np.array([
        [np.cos(skew_angle_rad), np.sin(skew_angle_rad)],
        [-np.sin(skew_angle_rad), np.cos(skew_angle_rad)]
    ])

    corrected_coords = []
    for x, y in old_coords:
        # Translate the point to the origin
        x_translated = x - center[0]
        y_translated = y - center[1]

        # Apply the reverse rotation
        x_rotated, y_rotated = np.dot(reverse_rotation_matrix, [x_translated, y_translated])

        # Translate the point back from the origin
        x_corrected = x_rotated + center[0] + left_diff - right_diff
        y_corrected = y_rotated + center[1] + top_diff - bottom_diff

        corrected_coords.append((x_corrected, y_corrected))

    return corrected_coords


def correct_polygon_coords_crop(polygon_coords, crop_data):
    left_crop = crop_data['left_crop']
    top_crop = crop_data['top_crop']

    corrected_coords = []
    for x, y in polygon_coords:
        x_corrected = x - left_crop
        y_corrected = y - top_crop
        corrected_coords.append((x_corrected, y_corrected))

    return corrected_coords


def x_y_format_to_coco_format(coords):
    # Преобразование массива NumPy в одномерный список
    coco_format = np.array(coords).flatten().tolist()
    return coco_format


def correct_polygon_coords_resize(polygon_coords, resize_data):
    # Calculate scale factors
    x_scale = resize_data['new_width'] / resize_data['original_width']
    y_scale = resize_data['new_height'] / resize_data['original_height']

    corrected_coords = []
    for x, y in polygon_coords:
        x_corrected = x * x_scale
        y_corrected = y * y_scale
        corrected_coords.append((x_corrected, y_corrected))

    return corrected_coords


def polygon_to_bbox(polygon):
    """
    Преобразует список точек полигона в bounding box в формате, удобном для использования с OpenCV.

    Args:
    polygon (list): Список координат точек полигона в формате [[x1, y1], [x2, y2], ..., [xn, yn]]

    Returns:
    tuple: Кортеж координат bounding box в формате ((x_min, y_min), (x_max, y_max))
    """
    x_coords = [point[0] for point in polygon]
    y_coords = [point[1] for point in polygon]

    x_min = min(x_coords)
    y_min = min(y_coords)
    x_max = max(x_coords)
    y_max = max(y_coords)

    return ((x_min, y_min), (x_max, y_max))


def bbox_to_polygon(bbox):
    """
    Преобразует bounding box в полигон и возвращает его в формате [[x1, y1], [x2, y2], [x3, y3], [x4, y4]].

    Args:
    bbox (tuple): Кортеж координат bounding box в формате ((x_min, y_min), (x_max, y_max))

    Returns:
    np.ndarray: Массив координат точек полигона в формате [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    """
    (x_min, y_min), (x_max, y_max) = bbox

    polygon = [x_min, y_min, x_max, y_min, x_max, y_max, x_min, y_max]
    return np.array(polygon).reshape((-1, 2))


def draw_bbox(image, bbox, color=(0, 255, 0), thickness=2):
    """
    Рисует bounding box на изображении.

    Args:
    image (np.ndarray): Исходное изображение.
    bbox (tuple): Кортеж координат bounding box в формате ((x_min, y_min), (x_max, y_max)).
    color (tuple): Цвет линии bounding box в формате (B, G, R).
    thickness (int): Толщина линии bounding box.

    Returns:
    np.ndarray: Изображение с нарисованным bounding box.
    """
    # Преобразуем координаты в целые числа
    (x_min, y_min), (x_max, y_max) = bbox
    x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

    # Рисуем прямоугольник
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
    return image


def rotate_image_within_bounds_data(image, angle, keep_bounds=True):
    """
    Получает данные для поворота изображения на заданный угол.

    :param image: Изображение в формате numpy массива
    :param angle: Угол поворота (в градусах)
    :param keep_bounds: Если True, поворот будет в пределах исходных размеров изображения.
                        Если False, изображение может быть расширено.
    :return: Словарь с данными для корректировки координат полигонов
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    # Получение матрицы поворота
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    if not keep_bounds:
        # Вычисление новых границ изображения
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        # Корректировка матрицы поворота для центра нового изображения
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        return {
            "rotation_matrix": M,
            "image_shape": (new_h, new_w)
        }
    else:
        return {
            "rotation_matrix": M,
            "image_shape": (h, w)
        }


def correct_polygons_rotate(coords, rotation_data):
    """
    Корректирует координаты полигонов при повороте изображения.

    :param coords: Список координат полигонов [(x1, y1), (x2, y2), ...]
    :param rotation_data: Словарь с матрицей поворота и размерами изображения
    :return: Список скорректированных координат полигонов
    """
    M = rotation_data["rotation_matrix"]
    (h, w) = rotation_data["image_shape"]

    # Преобразование координат полигонов в массив numpy
    coords = np.array(coords)

    # Добавление единиц для использования матрицы поворота
    ones = np.ones(shape=(len(coords), 1))
    coords_ones = np.hstack([coords, ones])

    # Применение матрицы поворота к координатам
    rotated_coords = M.dot(coords_ones.T).T

    return rotated_coords[:, :2]


def rotate_image(image, angle, keep_bounds=True, fill_color=(255, 255, 255)):
    """
    Поворачивает изображение на заданный угол и возвращает повернутое изображение.

    :param image: Изображение в формате numpy массива
    :param angle: Угол поворота (в градусах)
    :param keep_bounds: Если True, поворот будет в пределах исходных размеров изображения.
                        Если False, изображение может быть расширено.
    :param fill_color: Цвет для заполнения добавленных пикселей (по умолчанию белый)
    :return: Повернутое изображение
    """
    # Получаем данные поворота
    rotation_data = rotate_image_within_bounds_data(image, angle, keep_bounds)

    # Получаем матрицу поворота и размеры изображения
    M = rotation_data["rotation_matrix"]
    (h, w) = rotation_data["image_shape"]

    # Выполнение поворота изображения с заданным цветом границ
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=fill_color)
    return rotated


def zoom_image_data(image, scale_x, scale_y):
    """
    Получает данные для масштабирования изображения на заданное количество пикселей в пределах исходных размеров.

    :param image: Изображение в формате numpy массива
    :param scale_x: Количество пикселей для масштабирования по горизонтали (может быть отрицательным)
    :param scale_y: Количество пикселей для масштабирования по вертикали (может быть отрицательным)
    :return: Словарь с данными для корректировки координат полигонов
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    # Вычисление коэффициентов масштабирования
    scale_x_factor = (w + scale_x) / w
    scale_y_factor = (h + scale_y) / h

    # Применение масштабирования в пределах исходных размеров
    M = np.array([
        [scale_x_factor, 0, center[0] * (1 - scale_x_factor)],
        [0, scale_y_factor, center[1] * (1 - scale_y_factor)]
    ])
    return {
        "scale_matrix": M,
        "image_shape": (h, w)
    }


def correct_polygons_zoom(coords, scale_data):
    """
    Корректирует координаты полигонов при масштабировании изображения.

    :param coords: Список координат полигонов [(x1, y1), (x2, y2), ...]
    :param scale_data: Словарь с матрицей масштабирования и размерами изображения
    :return: Список скорректированных координат полигонов
    """
    M = scale_data["scale_matrix"]
    (h, w) = scale_data["image_shape"]

    # Преобразование координат полигонов в массив numpy
    coords = np.array(coords)

    # Добавление единиц для использования матрицы масштабирования
    ones = np.ones(shape=(len(coords), 1))
    coords_ones = np.hstack([coords, ones])

    # Применение матрицы масштабирования к координатам
    zoomed_coords = M.dot(coords_ones.T).T

    return zoomed_coords[:, :2]


def zoom_image(image, scale_x, scale_y, fill_color=(255, 255, 255)):
    """
    Масштабирует изображение на заданное количество пикселей в пределах исходных размеров и возвращает масштабированное изображение.

    :param image: Изображение в формате numpy массива
    :param scale_x: Количество пикселей для масштабирования по горизонтали (может быть отрицательным)
    :param scale_y: Количество пикселей для масштабирования по вертикали (может быть отрицательным)
    :param fill_color: Цвет для заполнения добавленных пикселей (по умолчанию белый)
    :return: Масштабированное изображение
    """
    # Получаем данные масштабирования
    scale_data = zoom_image_data(image, scale_x, scale_y)

    # Получаем матрицу масштабирования и размеры изображения
    M = scale_data["scale_matrix"]
    (h, w) = scale_data["image_shape"]

    # Выполнение масштабирования изображения с заданным цветом границ
    zoomed = cv2.warpAffine(image, M, (w, h), borderValue=fill_color)

    return zoomed


def flip_image_data(image, flip_code):
    """
    Получает данные для отражения изображения.

    :param image: Изображение в формате numpy массива
    :param flip_code: Код отражения: 1 для горизонтального, 0 для вертикального
    :return: Словарь с данными для корректировки координат полигонов
    """
    (h, w) = image.shape[:2]

    if flip_code == 1:  # Horizontal flip
        M = np.array([[-1, 0, w], [0, 1, 0]], dtype=np.float32)
    elif flip_code == 0:  # Vertical flip
        M = np.array([[1, 0, 0], [0, -1, h]], dtype=np.float32)
    else:
        raise ValueError("Invalid flip code. Use 1 for horizontal and 0 for vertical flipping.")

    return {
        "flip_matrix": M,
        "image_shape": (h, w)
    }


def correct_polygons_flip(coords, flip_data):
    """
    Корректирует координаты полигонов при отражении изображения.

    :param coords: Список координат полигонов [(x1, y1), (x2, y2), ...]
    :param flip_data: Словарь с матрицей отражения и размерами изображения
    :return: Список скорректированных координат полигонов
    """
    M = flip_data["flip_matrix"]
    (h, w) = flip_data["image_shape"]

    # Преобразование координат полигонов в массив numpy
    coords = np.array(coords)

    # Добавление единиц для использования матрицы отражения
    ones = np.ones(shape=(len(coords), 1))
    coords_ones = np.hstack([coords, ones])

    # Применение матрицы отражения к координатам
    flipped_coords = M.dot(coords_ones.T).T

    return flipped_coords[:, :2]


def flip_image(image, flip_code, fill_color=(255, 255, 255)):
    """
    Отражает изображение на заданный угол и возвращает отраженное изображение.

    :param image: Изображение в формате numpy массива
    :param flip_code: Код отражения: 1 для горизонтального, 0 для вертикального
    :param fill_color: Цвет для заполнения добавленных пикселей (по умолчанию белый)
    :return: Отраженное изображение
    """
    # Получаем данные отражения
    flip_data = flip_image_data(image, flip_code)

    # Получаем матрицу отражения и размеры изображения
    M = flip_data["flip_matrix"]
    (h, w) = flip_data["image_shape"]

    # Выполнение отражения изображения с заданным цветом границ
    flipped = cv2.warpAffine(image, M, (w, h), borderValue=fill_color)
    return flipped


def translate_image_data(image, tx, ty):
    """
    Получает данные для сдвига изображения на заданное количество пикселей.

    :param image: Изображение в формате numpy массива
    :param tx: Количество пикселей для сдвига по горизонтали (может быть отрицательным)
    :param ty: Количество пикселей для сдвига по вертикали (может быть отрицательным)
    :return: Словарь с данными для корректировки координат полигонов
    """
    (h, w) = image.shape[:2]

    # Применение сдвига
    M = np.array([
        [1, 0, tx],
        [0, 1, ty]
    ], dtype=np.float32)

    return {
        "translation_matrix": M,
        "image_shape": (h, w)
    }


def correct_polygons_translation(coords, translation_data):
    """
    Корректирует координаты полигонов при сдвиге изображения.

    :param coords: Список координат полигонов [(x1, y1), (x2, y2), ...]
    :param translation_data: Словарь с матрицей сдвига и размерами изображения
    :return: Список скорректированных координат полигонов
    """
    M = translation_data["translation_matrix"]
    (h, w) = translation_data["image_shape"]

    # Преобразование координат полигонов в массив numpy
    coords = np.array(coords)

    # Добавление единиц для использования матрицы сдвига
    ones = np.ones(shape=(len(coords), 1))
    coords_ones = np.hstack([coords, ones])

    # Применение матрицы сдвига к координатам
    translated_coords = M.dot(coords_ones.T).T

    return translated_coords[:, :2]


def translate_image(image, tx, ty, fill_color=(255, 255, 255)):
    """
    Сдвигает изображение на заданное количество пикселей и возвращает сдвинутое изображение.

    :param image: Изображение в формате numpy массива
    :param tx: Количество пикселей для сдвига по горизонтали (может быть отрицательным)
    :param ty: Количество пикселей для сдвига по вертикали (может быть отрицательным)
    :param fill_color: Цвет для заполнения добавленных пикселей (по умолчанию белый)
    :return: Сдвинутое изображение
    """
    # Получаем данные сдвига
    translation_data = translate_image_data(image, tx, ty)

    # Получаем матрицу сдвига и размеры изображения
    M = translation_data["translation_matrix"]
    (h, w) = translation_data["image_shape"]

    # Выполнение сдвига изображения с заданным цветом границ
    translated = cv2.warpAffine(image, M, (w, h), borderValue=fill_color)
    return translated


def resize_with_padding_data(image, target_width, target_height, fill_color=(255, 255, 255)):
    """
    Получает данные для изменения размера изображения с добавлением padding.

    :param image: Изображение в формате numpy массива
    :param target_width: Ширина целевого изображения
    :param target_height: Высота целевого изображения
    :param fill_color: Цвет для заполнения добавленных пикселей (по умолчанию белый)
    :return: Словарь с данными для корректировки координат полигонов
    """
    (h, w) = image.shape[:2]

    # Вычисление смещения для центрирования изображения
    x_offset = (target_width - w) // 2
    y_offset = (target_height - h) // 2

    return {
        "target_width": target_width,
        "target_height": target_height,
        "x_offset": x_offset,
        "y_offset": y_offset,
        "fill_color": fill_color
    }


def correct_polygons_resize_padding(coords, resize_data):
    """
    Корректирует координаты полигонов при изменении размера изображения с добавлением padding.

    :param coords: Список координат полигонов [(x1, y1), (x2, y2), ...]
    :param resize_data: Словарь с данными изменения размера и добавления padding
    :return: Список скорректированных координат полигонов
    """
    x_offset = resize_data["x_offset"]
    y_offset = resize_data["y_offset"]

    # Применение смещения к координатам полигонов
    corrected_coords = [(int(x + x_offset), int(y + y_offset)) for (x, y) in coords]

    return corrected_coords


def resize_with_padding(image, target_width, target_height, fill_color=(255, 255, 255)):
    """
    Изменяет размер изображения с добавлением padding и возвращает новое изображение.

    :param image: Изображение в формате numpy массива
    :param target_width: Ширина целевого изображения
    :param target_height: Высота целевого изображения
    :param fill_color: Цвет для заполнения добавленных пикселей (по умолчанию белый)
    :return: Изображение с добавленным padding
    """
    # Получаем данные для изменения размера и добавления padding
    resize_data = resize_with_padding_data(image, target_width, target_height, fill_color)

    # Получаем параметры изменения размера и добавления padding
    x_offset = resize_data["x_offset"]
    y_offset = resize_data["y_offset"]
    target_width = resize_data["target_width"]
    target_height = resize_data["target_height"]
    fill_color = resize_data["fill_color"]

    # Создание нового изображения с заполнением цветом
    new_image = np.full((target_height, target_width, 3), fill_color, dtype=np.uint8)

    # Вставка исходного изображения в центр нового изображения
    new_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]] = image

    return new_image


def normalize_image(image, is_show=False):
    increase_contrast_result = increase_contrast(image, 1, 20)
    adjust_image_result = adjust_image(increase_contrast_result)
    straighten_image_result = straighten_image(adjust_image_result)
    # remove_noise_result = remove_noise(straighten_image_result,3)
    # crop_image_result = crop_image_by_percentages(straighten_image_result,7,7,5,5)
    crop_image_without_background_result = crop_image_without_background(straighten_image_result)

    result = crop_image_without_background_result
    if is_show == True:
        show_img(image, 'original')
        show_img(increase_contrast_result, 'increase_contrast')
        show_img(adjust_image_result, 'adjust_image')
        show_img(straighten_image_result, 'straighten_image')
        # show_img(remove_noise_result,'remove_noise')
        # show_img(crop_image_result,'crop_image')
        show_img(crop_image_without_background_result, 'crop_image_without_background')
    return result


def remove_noise_from_image(image):
    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение медианного фильтра для удаления мелких шумов
    denoised_image = cv2.medianBlur(gray_image, 3)

    # Применение метода адаптивной бинаризации для улучшения контраста
    cleaned_image = cv2.adaptiveThreshold(
        denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    # Преобразование обработанного изображения в формат RGB
    rgb_image = cv2.cvtColor(cleaned_image, cv2.COLOR_GRAY2RGB)

    return rgb_image


def crop_img(image, x, y, width, height):
    """
    Обрезает изображение по заданным координатам и размерам.

    :param image: исходное изображение
    :param x: координата x верхнего левого угла области обрезки
    :param y: координата y верхнего левого угла области обрезки
    :param width: ширина области обрезки
    :param height: высота области обрезки
    :return: обрезанное изображение
    """
    cropped_image = image[y:y + height, x:x + width]
    return cropped_image


def convert_polygon_to_coco_format(polygon):
    """
    Преобразует координаты полигона в формат COCO.

    :param polygon: Список координат полигона [(x1, y1), (x2, y2), (x3, y3), ...]
    :return: Список координат в формате COCO [x1, y1, x2, y2, x3, y3, ...]
    """
    polygon_flat = [coord for point in polygon for coord in point]
    return polygon_flat


def convert_bbox_to_coco_format(bbox):
    """
    Преобразует координаты ограничивающей рамки в формат COCO.

    :param bbox: Кортеж с двумя точками ((x_min, y_min), (x_max, y_max))
    :return: Список координат в формате COCO [x, y, width, height]
    """
    (x_min, y_min), (x_max, y_max) = bbox
    width = x_max - x_min
    height = y_max - y_min
    return [x_min, y_min, width, height]


def procceced_image(image, polygon_cords, is_show=False, is_resize=False, resizeWidth=1240, resizeHeight=1754,
                    is_crop=False, cropWidth=1240, cropHeight=1754):
    result_image = increase_contrast(image, 1, 20)
    result_image = adjust_image(result_image)

    straighten_image_data_result = straighten_image_data(result_image)
    result_image = straighten_image(result_image)

    crop_image_without_background_data_result = crop_image_without_background_data(result_image)
    result_image = crop_image_without_background(result_image)

    if is_resize == True:
        resize_image_img_data = resize_image_data(result_image, resizeWidth, resizeHeight);
        result_image = resize_image(result_image, resizeWidth, resizeHeight);
    if is_crop == True:
        cropped_image = crop_img(result_image, 0, 0, cropWidth, cropHeight)
        result_image = cropped_image

    result_polygon_cords = polygon_cords

    # correction cords poly
    correct_polygon_coords_straighten_result = correct_polygon_coords_straighten(result_polygon_cords,
                                                                                 straighten_image_data_result)
    result_polygon_cords = correct_polygon_coords_straighten_result

    correct_polygon_coords_crop_result = correct_polygon_coords_crop(result_polygon_cords,
                                                                     crop_image_without_background_data_result)
    result_polygon_cords = correct_polygon_coords_crop_result

    if is_resize == True:
        correct_polygon_coords_resize_result = correct_polygon_coords_resize(result_polygon_cords,
                                                                             resize_image_img_data)
        result_polygon_cords = correct_polygon_coords_resize_result

    # bbox
    result_bbox_cords = polygon_to_bbox(result_polygon_cords)
    result_polygon_cords_coco = convert_polygon_to_coco_format(result_polygon_cords)
    result_bbox_cords_coco = convert_bbox_to_coco_format(result_bbox_cords)

    if is_show == True:
        show_img(image, 'original')
        show_img(result_image, 'result_image')
        print('polygon_cords: ')
        print(polygon_cords)
        print('result_polygon_cords: ')
        print(result_polygon_cords)
        print('result_bbox_cords: ')
        print(result_bbox_cords)
        print('image shape')
        print(result_image.shape)
        draw_polygon_on_image_r3 = draw_polygon_on_image(result_image, result_polygon_cords, (255, 0, 255))
        show_img(draw_polygon_on_image_r3, 'draw_polygon_on_image_r3')

        bbox_img = draw_bbox(result_image, result_bbox_cords)
        show_img(bbox_img, 'bbox_img')
    return {
        'result_image': result_image,
        'result_polygon_cords': result_polygon_cords,
        'result_bbox_cords': result_bbox_cords,
        'result_image_shape': result_image.shape,
        'result_polygon_cords_coco': result_polygon_cords_coco,
        'result_bbox_cords_coco': result_bbox_cords_coco
    }


def procceced_image_clean(image, polygon_cords, is_show=False, width=1024, height=1448):
    result_image = image
    resize_image_img_data = resize_image_data(result_image, width, height);
    result_image = resize_image(result_image, width, height);

    result_polygon_cords = polygon_cords
    correct_polygon_coords_resize_result = correct_polygon_coords_resize(result_polygon_cords, resize_image_img_data)
    result_polygon_cords = correct_polygon_coords_resize_result

    # bbox
    result_bbox_cords = polygon_to_bbox(result_polygon_cords)
    result_polygon_cords_coco = convert_polygon_to_coco_format(result_polygon_cords)
    result_bbox_cords_coco = convert_bbox_to_coco_format(result_bbox_cords)

    if is_show == True:
        show_img(image, 'original')
        show_img(result_image, 'result_image')
        print('polygon_cords: ')
        print(polygon_cords)
        print('result_polygon_cords: ')
        print(result_polygon_cords)
        print('result_bbox_cords: ')
        print(result_bbox_cords)
        print('image shape')
        print(result_image.shape)
        draw_polygon_on_image_r3 = draw_polygon_on_image(result_image, result_polygon_cords, (255, 0, 255))
        show_img(draw_polygon_on_image_r3, 'draw_polygon_on_image_r3')

        bbox_img = draw_bbox(result_image, result_bbox_cords)
        show_img(bbox_img, 'bbox_img')
    return {
        'result_image': result_image,
        'result_polygon_cords': result_polygon_cords,
        'result_bbox_cords': result_bbox_cords,
        'result_image_shape': result_image.shape,
        'result_polygon_cords_coco': result_polygon_cords_coco,
        'result_bbox_cords_coco': result_bbox_cords_coco
    }


def convert_coco_to_custom_format(coco_data):
    """
    Преобразует данные COCO в указанный формат и добавляет соответствующие file_name, width и height для каждой аннотации.

    :param coco_data: Словарь с данными в формате COCO
    :return: Список аннотаций в новом формате
    """
    # Создание словаря для быстрого поиска file_name, width и height по image_id
    image_info = {image["id"]: (image["file_name"], image["width"], image["height"]) for image in coco_data["images"]}

    # Преобразование аннотаций в нужный формат и добавление соответствующих данных
    formatted_annotations = []
    for annotation in coco_data["annotations"]:
        annotation_with_info = annotation.copy()
        image_id = annotation_with_info["image_id"]
        if image_id in image_info:
            file_name, width, height = image_info[image_id]
            annotation_with_info["file_name"] = file_name
            annotation_with_info["width"] = width
            annotation_with_info["height"] = height
        annotation_with_info['polygon'] = annotation_with_info['segmentation'][0]
        formatted_annotations.append(annotation_with_info)

    return formatted_annotations


def procced_all_images(json_path, images_folder_path, images_output_procced_folder_path, procced_data_file_save):
    with open(json_path, 'r') as f:
        # Read the file contents
        prepare_merged_json_string = f.read()
    prepare_merged_json_data = json.loads(prepare_merged_json_string)
    custom_data = convert_coco_to_custom_format(prepare_merged_json_data)
    result = []
    index = 0
    for custom_item in custom_data:
        try:
            index = index + 1
            file_name = custom_item['file_name']
            image = cv2.imread(images_folder_path + '/' + file_name)
            poly_cords = custom_item['polygon']
            poly_cords_standart = coco_transform_to_x_y_format(poly_cords)
            procceced_image_data = procceced_image(image, poly_cords_standart, False, is_crop=True, is_resize=True,
                                                   resizeWidth=1024, resizeHeight=1447, cropWidth=1024, cropHeight=1024)
            result_image = procceced_image_data['result_image']
            result_image_gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(images_output_procced_folder_path + '/' + file_name, result_image_gray)

            result_polygon_cords = procceced_image_data['result_polygon_cords']
            result_bbox_cords = procceced_image_data['result_bbox_cords']
            result_image_shape = result_image_gray.shape
            result_polygon_cords_coco = procceced_image_data['result_polygon_cords_coco']
            result_bbox_cords_coco = procceced_image_data['result_bbox_cords_coco']

            result.append({
                'result_polygon_cords': result_polygon_cords,
                'result_bbox_cords': result_bbox_cords,
                'result_image_shape': result_image_shape,
                'result_polygon_cords_coco': result_polygon_cords_coco,
                'result_bbox_cords_coco': result_bbox_cords_coco,
                'filename': file_name
            })
            print(file_name + ' - ' + str(index))
        except Exception as e:
            print(f"error {e}")

    save_to_json(result, procced_data_file_save)
    return result


def process_image2(custom_item, images_folder_path, images_output_procced_folder_path, aug_counts):
    file_name = custom_item['file_name']
    try:
        print(f"Starting {file_name}")
        image = cv2.imread(os.path.join(images_folder_path, file_name))
        poly_cords = custom_item['polygon']
        poly_cords_standart = coco_transform_to_x_y_format(poly_cords)
        procceced_image_data = procceced_image2(image, poly_cords_standart, False)
        result_image = procceced_image_data['result_image']
        result_image_gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(images_output_procced_folder_path, file_name), result_image_gray)

        result_polygon_cords = procceced_image_data['result_polygon_cords']
        result_bbox_cords = procceced_image_data['result_bbox_cords']
        result_image_shape = result_image_gray.shape
        result_polygon_cords_coco = procceced_image_data['result_polygon_cords_coco']
        result_bbox_cords_coco = procceced_image_data['result_bbox_cords_coco']

        result = [{
            'result_polygon_cords': result_polygon_cords,
            'result_bbox_cords': result_bbox_cords,
            'result_image_shape': result_image_shape,
            'result_polygon_cords_coco': result_polygon_cords_coco,
            'result_bbox_cords_coco': result_bbox_cords_coco,
            'filename': file_name
        }]

        gen_all_data = gen_data(image, poly_cords_standart, aug_counts)

        for i, gen_item_data in enumerate(gen_all_data):
            aug_file_name = f"{file_name}_aug_gen_{i}"
            aug_result_image = gen_item_data['result_image']
            aug_result_image_gray = cv2.cvtColor(aug_result_image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(images_output_procced_folder_path, aug_file_name), aug_result_image_gray)
            result.append({
                'result_polygon_cords': gen_item_data['result_polygon_cords'],
                'result_bbox_cords': gen_item_data['result_bbox_cords'],
                'result_image_shape': gen_item_data['result_image_shape'],
                'result_polygon_cords_coco': gen_item_data['result_polygon_cords_coco'],
                'result_bbox_cords_coco': gen_item_data['result_bbox_cords_coco'],
                'filename': aug_file_name
            })

        print(f'Processed {file_name}')
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

    return result


def procced_all_images2(json_path, images_folder_path, images_output_procced_folder_path, procced_data_file_save,
                        aug_counts=3):
    with open(json_path, 'r') as f:
        prepare_merged_json_string = f.read()
    prepare_merged_json_data = json.loads(prepare_merged_json_string)
    custom_data = convert_coco_to_custom_format(prepare_merged_json_data)

    result = []

    print("Starting thread pool...")

    max_workers = 10  # Начните с небольшого количества потоков
    total_tasks = len(custom_data)
    completed_tasks = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_image2, item, images_folder_path, images_output_procced_folder_path, aug_counts) for
            item in custom_data]

        for index, future in enumerate(as_completed(futures)):
            try:
                res = future.result()
                result.extend(res)
                completed_tasks += 1
                print(f"Completed {completed_tasks}/{total_tasks} tasks")
            except Exception as e:
                print(f"Error in future: {e}")

    save_to_json(result, procced_data_file_save)
    print(f"Results saved to {procced_data_file_save}")
    return result


def save_to_json(data, output_file_path):
    """
    Сохраняет любой словарь или список в файл JSON.

    :param data: Данные для сохранения (словарь или список)
    :param output_file_path: Путь к выходному файлу JSON
    """
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {output_file_path}")


def read_json_file(json_path):
    with open(json_path, 'r') as f:
        # Read the file contents
        json_string = f.read()
    return json.loads(json_string)


def gen_data(image, cords, count=200, height=2048, width=2048):
    data = [];
    image_clean = procceced_image_clean(image, cords, False)
    i = 1
    while i <= count:
        aug_gen_data = aug_gen(image_clean['result_image'], image_clean['result_polygon_cords'], False, height, width)
        aug_gen_data_result_image = aug_gen_data['result_image']
        aug_gen_data_result_polygon_cords = aug_gen_data['result_polygon_cords']

        if is_polygon_within_image(aug_gen_data_result_image, aug_gen_data_result_polygon_cords):
            data.append(aug_gen_data)
            i += 1
    return data


def aug_gen(image, polys_x_y, is_show=False, height=2048, width=2048):
    resize_with_padding_1 = resize_with_padding(image, width, height)
    resize_with_padding_data_1 = resize_with_padding_data(image, width, height)
    correct_polygons_resize_padding_1 = correct_polygons_resize_padding(polys_x_y, resize_with_padding_data_1)

    image = resize_with_padding_1
    polys_x_y = correct_polygons_resize_padding_1

    # Определение аугментаторов
    augmenters = iaa.Sequential([
        iaa.Fliplr(0.5),  # Горизонтальное отражение
        iaa.Flipud(0.5),  # Вертикальное отражение
        iaa.Affine(rotate=(-15, 15), mode="edge", cval=255),  # Поворот на угол от -30 до 30 градусов
        iaa.Affine(scale=(0.8, 1.2), mode="edge", cval=255),  # Масштабирование от 80% до 120%
        iaa.Multiply((0.8, 1.2)),  # Изменение яркости от 80% до 120%
        iaa.LinearContrast((0.75, 1.5)),  # Изменение контраста
        iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)),  # Добавление гауссовского шума
        iaa.CropAndPad(percent=(-0.2, 0.2), pad_mode="edge", pad_cval=255)  # Случайное обрезание и дополнение
    ])
    images_aug_polygons_on_image = ia.PolygonsOnImage([polys_x_y], shape=image.shape)
    image_augs, polygons_aug_instances = augmenters(images=[image], polygons=np.array([images_aug_polygons_on_image]))
    image_aug = image_augs[0]
    polygons_aug_instance = polygons_aug_instances[0]
    polygons_aug = polygons_aug_instances[0][0]
    correct_crods_auth_1 = [(int(x), int(y)) for x, y in polygons_aug]
    height, width = image_aug.shape[:2]

    resize_aug = iaa.Resize({"height": height, "width": width})
    image_aug = resize_aug(image=image_aug)

    # Масштабирование координат полигонов до нового размера
    scale_x = 2048 / width
    scale_y = 2048 / height
    correct_crods_auth_1 = [(int(x * scale_x), int(y * scale_y)) for x, y in correct_crods_auth_1]

    if is_show == True:
        aug_gen_data_draw_poly_to_image = draw_polygon_on_image(image_aug, correct_crods_auth_1, (0, 255, 0))
        show_img(aug_gen_data_draw_poly_to_image, 'image_aug')

    result_bbox_cords = polygon_to_bbox(correct_crods_auth_1)
    result_polygon_cords_coco = convert_polygon_to_coco_format(correct_crods_auth_1)
    result_bbox_cords_coco = convert_bbox_to_coco_format(result_bbox_cords)

    return {
        'result_image': image_aug,
        'result_polygon_cords': correct_crods_auth_1,
        'result_bbox_cords': result_bbox_cords,
        'result_image_shape': image_aug.shape,
        'result_polygon_cords_coco': result_polygon_cords_coco,
        'result_bbox_cords_coco': result_bbox_cords_coco
    }


def is_polygon_within_image(img, polygon_points):
    # Получаем размеры изображения
    img_height, img_width = img.shape[:2]

    # Преобразуем список точек полигона в массив numpy
    polygon = np.array(polygon_points, dtype=np.int32)

    # Проверяем, находится ли каждая точка полигона внутри границ изображения
    def point_in_rect(point, img_width, img_height):
        x, y = point
        return 0 <= x <= img_width and 0 <= y <= img_height

    return all(point_in_rect(point, img_width, img_height) for point in polygon)


def procceced_image2(image, polygon_cords, is_show=False, width=1024, height=1448,target_width=2048,target_height=2048):
    procceced_image_clean_data = procceced_image_clean(image, polygon_cords, is_show, width, height)
    procceced_image_clean_data_image = procceced_image_clean_data['result_image']
    procceced_image_result_polygon_cords = procceced_image_clean_data['result_polygon_cords']

    result_image = resize_with_padding(procceced_image_clean_data_image, target_width, target_height)
    resize_with_padding_data_1 = resize_with_padding_data(procceced_image_clean_data_image, target_width, target_height)
    result_polygon_cords = correct_polygons_resize_padding(procceced_image_result_polygon_cords,
                                                           resize_with_padding_data_1)

    # bbox
    result_bbox_cords = polygon_to_bbox(result_polygon_cords)
    result_polygon_cords_coco = convert_polygon_to_coco_format(result_polygon_cords)
    result_bbox_cords_coco = convert_bbox_to_coco_format(result_bbox_cords)

    return {
        'result_image': result_image,
        'result_polygon_cords': result_polygon_cords,
        'result_bbox_cords': result_bbox_cords,
        'result_image_shape': result_image.shape,
        'result_polygon_cords_coco': result_polygon_cords_coco,
        'result_bbox_cords_coco': result_bbox_cords_coco
    }


def iou_loss(y_true, y_pred):
    y_true = tf.reshape(y_true, [-1, 4, 2])
    y_pred = tf.reshape(y_pred, [-1, 4, 2])

    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    y_true_min = tf.reduce_min(y_true, axis=1)
    y_true_max = tf.reduce_max(y_true, axis=1)
    y_pred_min = tf.reduce_min(y_pred, axis=1)
    y_pred_max = tf.reduce_max(y_pred, axis=1)

    inter_min = tf.maximum(y_true_min, y_pred_min)
    inter_max = tf.minimum(y_true_max, y_pred_max)
    intersection = tf.maximum(0.0, inter_max - inter_min)

    area_true = tf.reduce_prod(y_true_max - y_true_min, axis=1)
    area_pred = tf.reduce_prod(y_pred_max - y_pred_min, axis=1)
    area_intersection = tf.reduce_prod(intersection, axis=1)
    area_union = area_true + area_pred - area_intersection

    iou = area_intersection / (area_union + tf.keras.backend.epsilon())
    return 1 - iou


def iou_metric(y_true, y_pred):
    y_true = tf.reshape(y_true, [-1, 4, 2])
    y_pred = tf.reshape(y_pred, [-1, 4, 2])

    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    y_true_min = tf.reduce_min(y_true, axis=1)
    y_true_max = tf.reduce_max(y_true, axis=1)
    y_pred_min = tf.reduce_min(y_pred, axis=1)
    y_pred_max = tf.reduce_max(y_pred, axis=1)

    inter_min = tf.maximum(y_true_min, y_pred_min)
    inter_max = tf.minimum(y_true_max, y_pred_max)
    intersection = tf.maximum(0.0, inter_max - inter_min)

    area_true = tf.reduce_prod(y_true_max - y_true_min, axis=1)
    area_pred = tf.reduce_prod(y_pred_max - y_pred_min, axis=1)
    area_intersection = tf.reduce_prod(intersection, axis=1)
    area_union = area_true + area_pred - area_intersection

    iou = area_intersection / (area_union + tf.keras.backend.epsilon())
    return iou


def combined_iou_mse_loss(y_true, y_pred):
    iou_loss_value = iou_loss(y_true, y_pred)
    mse_loss_value = MeanSquaredError()(y_true, y_pred)
    return tf.cast(iou_loss_value, dtype=tf.float32) + tf.cast(mse_loss_value, dtype=tf.float32)

# Фильтрация данных
def filter_data_poly(data,indexName,polySize=8):
    return [item for item in data if len(item[indexName]) == polySize]


def combine_and_shuffle(x, y, x2, y2):
    """
    Объединяет и перемешивает массивы изображений и меток, сохраняя связь между ними.

    Параметры:
    images (list): Список исходных изображений.
    labels (list): Список исходных меток.
    image_with_aug (list): Список аугментированных изображений.
    label_with_aug (list): Список аугментированных меток.

    Возвращает:
    tuple: Перемешанные списки изображений и меток.
    """
    # Объединение массивов
    combined_x = x + x2
    combined_y = y + y2

    # Преобразование в numpy массивы для удобства перемешивания
    combined_x = np.array(combined_x)
    combined_y = np.array(combined_y)

    # Перемешивание массивов с сохранением связи
    indices = np.arange(len(combined_x))
    np.random.shuffle(indices)

    shuffled_x = combined_x[indices]
    shuffled_y = combined_y[indices]

    # Преобразование обратно в списки
    shuffled_x = shuffled_x.tolist()
    shuffled_y = shuffled_y.tolist()

    return shuffled_x, shuffled_y