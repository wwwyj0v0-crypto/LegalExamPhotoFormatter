

import cv2
import io
import numpy as np

from PIL import Image
from sklearn.cluster import KMeans

from config import *


# =========================
# 读取图片
# =========================

def load_image(image_path):

    pil_img = Image.open(image_path)

    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")

    img = np.array(pil_img)

    return img


# =========================
# 人脸检测
# =========================

def detect_face(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS
    )

    if len(faces) == 0:
        raise ValueError("未检测到人脸")

    largest_face = max(
        faces,
        key=lambda f: f[2] * f[3]
    )
    print(f"检测到 {len(faces)} 张人脸")
    print(f"最大人脸框: {faces}")

    return largest_face


# =========================
# 计算裁剪框
# =========================

def calculate_crop_box(
        img_width,
        img_height,
        face_box
):

    x, y, w, h = face_box

    # ==========================
    # Haar框补偿
    # ==========================

    # 向上补偿发顶
    head_top = y - 0.18 * h

    # 整体头部高度估计
    head_height = 1.25 * h

    # ==========================
    # 根据证件照比例反推裁剪尺寸
    # ==========================

    crop_height = (
        head_height /
        HEAD_HEIGHT_RATIO
    )

    crop_width = (
        crop_height *
        TARGET_WIDTH /
        TARGET_HEIGHT
    )

    # ==========================
    # 头顶距离顶部10%
    # ==========================

    crop_top = (
        head_top -
        crop_height *
        HEAD_TOP_RATIO
    )

    # ==========================
    # 水平居中
    # ==========================

    face_center_x = x + w / 2

    crop_left = (
        face_center_x -
        crop_width / 2
    )

    crop_bottom = crop_top + crop_height
    crop_right = crop_left + crop_width

    return (
        int(round(crop_left)),
        int(round(crop_top)),
        int(round(crop_right)),
        int(round(crop_bottom))
    )

# =========================
# 获取背景颜色
# =========================

def estimate_background_color(img):

    h, w = img.shape[:2]

    border = max(
        int(min(h, w) * 0.05),
        10
    )

    top = img[:border, :, :]
    bottom = img[-border:, :, :]
    left = img[:, :border, :]
    right = img[:, -border:, :]

    pixels = np.concatenate([
        top.reshape(-1, 3),
        bottom.reshape(-1, 3),
        left.reshape(-1, 3),
        right.reshape(-1, 3)
    ])

    kmeans = KMeans(
        n_clusters=KMEANS_CLUSTERS,
        random_state=0,
        n_init=10
    )

    labels = kmeans.fit_predict(pixels)

    counts = np.bincount(labels)

    bg_idx = np.argmax(counts)

    color = kmeans.cluster_centers_[bg_idx]

    return tuple(
        int(v)
        for v in color
    )


# =========================
# 超界补背景
# =========================

def expand_canvas_if_needed(
        img,
        crop_box
):

    h, w = img.shape[:2]

    left, top, right, bottom = crop_box

    pad_left = max(0, -left)
    pad_top = max(0, -top)

    pad_right = max(
        0,
        right - w
    )

    pad_bottom = max(
        0,
        bottom - h
    )

    if (
        pad_left == 0 and
        pad_right == 0 and
        pad_top == 0 and
        pad_bottom == 0
    ):
        return img, crop_box

    bg_color = estimate_background_color(img)

    new_h = h + pad_top + pad_bottom
    new_w = w + pad_left + pad_right

    canvas = np.full(
        (new_h, new_w, 3),
        bg_color,
        dtype=np.uint8
    )

    canvas[
        pad_top:pad_top+h,
        pad_left:pad_left+w
    ] = img

    new_crop_box = (
        left + pad_left,
        top + pad_top,
        right + pad_left,
        bottom + pad_top
    )

    return canvas, new_crop_box


# =========================
# 裁剪+缩放
# =========================

def crop_and_resize(
        img,
        crop_box
):

    left, top, right, bottom = crop_box

    crop = img[
        top:bottom,
        left:right
    ]

    result = cv2.resize(
        crop,
        (
            TARGET_WIDTH,
            TARGET_HEIGHT
        ),
        interpolation=cv2.INTER_LANCZOS4
    )

    return result


# =========================
# 压缩
# =========================

def compress_to_target_size(img):

    pil_img = Image.fromarray(img)

    low = JPEG_QUALITY_MIN
    high = JPEG_QUALITY_MAX

    best_data = None

    while low <= high:

        quality = (low + high) // 2

        buffer = io.BytesIO()

        pil_img.save(
            buffer,
            format="JPEG",
            quality=quality
        )

        data = buffer.getvalue()

        size_kb = len(data) / 1024

        if MIN_SIZE_KB <= size_kb <= MAX_SIZE_KB:

            best_data = data
            break

        elif size_kb > MAX_SIZE_KB:

            high = quality - 1

        else:

            low = quality + 1

            best_data = data

    return best_data


# =========================
# 主处理函数
# =========================

def process_image(
        input_path,
        output_path
):

    img = load_image(input_path)

    face_box = detect_face(img)

    crop_box = calculate_crop_box(
        img.shape[1],
        img.shape[0],
        face_box
    )

    img, crop_box = expand_canvas_if_needed(
        img,
        crop_box
    )

    result = crop_and_resize(
        img,
        crop_box
    )

    jpg_data = compress_to_target_size(
        result
    )

    with open(
            output_path,
            "wb"
    ) as f:

        f.write(jpg_data)

    return output_path