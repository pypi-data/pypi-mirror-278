import io
import multiprocessing
from typing import Any

import cv2
import numpy as np
from PIL import Image

if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.image_utils import Rect, ImgConv, Img, ImgDraw

img_tmp_dir = tmp_dir / 'image'
img_tmp_dir.mkdir(exist_ok=True)
cat_png_path = rc_dir / 'cat.png'


def test_Rect():
    rect = Rect([100.1, 100.9, 200.0, 200 * 1.001], rect_format=Rect.LTRB)
    assert Rect([(100.1, 100.9), (200.0, 200 * 1.001)], rect_format=Rect.LT_RB) == rect
    assert Rect([100.1, 100.9, 100, 100], rect_format=Rect.LTWH) == rect
    assert Rect([150, 150, 50, 50], rect_format=Rect.CENTER_RECT) == rect
    assert Rect(((100, 100), (200, 100), (200, 200), (100, 200)), rect_format=Rect.LT_RT_RB_LB) == rect

    assert rect.to_lt_rb() == ((100, 100), (200, 200)), rect.to_lt_rb()
    assert rect.to_ltwh() == (100, 100, 100, 100), rect.to_ltwh()
    assert rect.to_ltrb() == (100, 100, 200, 200), rect.to_ltrb()
    assert rect.to_lt_rt_rb_lt() == ((100, 100), (200, 100), (200, 200), (100, 200)), rect.to_lt_rt_rb_lt()
    assert rect.to_center() == (150, 150), rect.to_center()
    assert rect.to_center_rect() == (150, 150, 50, 50), rect.to_center_rect()


def test_ImgConv():
    path_img = ImgConv(cat_png_path)
    img_list = [path_img, ImgConv(Image.open(cat_png_path)), ImgConv(path_img.to_numpy()),
                ImgConv(cv2.imread(str(cat_png_path)), from_opencv=True),
                ImgConv(path_img.to_bytesio()), ImgConv(path_img.to_bytes()), ImgConv(path_img.to_bytearray())]

    def _test(img: Any, i: int) -> None:
        assert isinstance(img.to_pil(), Image.Image), i
        assert isinstance(img.to_numpy(), np.ndarray), i
        assert isinstance(img.to_opencv(), np.ndarray), i
        assert isinstance(img.to_bytesio(), io.BytesIO), i
        assert isinstance(img.to_bytes(), bytes), i
        assert isinstance(img.to_bytearray(), bytearray), i
        path = img_tmp_dir / f'cat{i}.png'
        assert img.to_path(path) == path, i

    for i, img in enumerate(img_list):
        multiprocessing.Process(target=_test, args=(img, i)).start()


def test_Img():
    img = Img(cat_png_path)
    img.resize(ratio=0.5).to_path(img_tmp_dir / 'cat_resize.png')
    img = Img(cat_png_path)
    img.contrast(2).to_path(img_tmp_dir / 'cat_contrast.png')
    img = Img(cat_png_path)
    img.brightness(2).to_path(img_tmp_dir / 'cat_brightness.png')
    img = Img(cat_png_path)
    img.sharpness(2).to_path(img_tmp_dir / 'cat_sharp.png')
    img = Img(cat_png_path)
    img.grayscale().to_path(img_tmp_dir / 'cat_grayscale.png')
    img = Img(cat_png_path)
    img.invert().to_path(img_tmp_dir / 'cat_invert.png')
    img = Img(cat_png_path)
    img.rotate(120).to_path(img_tmp_dir / 'cat_rotate.png')
    img = Img(cat_png_path)
    img.binaryzation(128).to_path(img_tmp_dir / 'cat_binaryzation.png')
    img = Img(cat_png_path)
    img.crop(Rect([0, 0, *img.image.size]).resize(0.5)).to_path(img_tmp_dir / 'cat_crop.png')
    img = Img(cat_png_path)
    img.dpi(1000).to_path(img_tmp_dir / 'cat_dpi.png')
    img = Img(cat_png_path)
    img.resize(ratio=0.5).contrast(2).brightness(2).sharpness(2).to_path(img_tmp_dir / 'cat_combination.png')


def test_ImgDraw():
    img_draw = ImgDraw(cat_png_path)
    rects = [Rect([0, 0, *img_draw.image.size]).resize(0.5),
             Rect([300, 300, 50, 50])]
    img_draw.rectangles(rects).to_path(img_tmp_dir / 'cat_rectangle.png')

    img_draw = ImgDraw(cat_png_path)
    polygons = [[(50, 50), (75, 75), (60, 90)],
                [(100, 100), (150, 105), (130, 150), (145, 200), (95, 250)]]
    img_draw.polygons(polygons).to_path(img_tmp_dir / 'cat_polygon.png')

    img_draw = ImgDraw(cat_png_path)
    text = 'Hello,\n 我來自北方中國大陆，\n一個城市名字是北京，\n作为中國的首都'
    img_draw.text(text, left_top_point=(100, 200)).to_path(img_tmp_dir / 'cat_text.png')

    img_draw = ImgDraw(cat_png_path)
    text = 'Hello, 我來自北方中國大陆，\n一個城市名字是北京，作为中國的首都'
    rect = Rect([100, 100, 1000, 250], rect_format=Rect.LTRB)
    img_draw.rectangles([rect])
    img_draw.text_in_rect(text, rect, fill='yellow').to_path(img_tmp_dir / 'cat_text_in_rect.png')


def tests():
    print('test image utils')
    test_Rect()
    test_ImgConv()
    test_Img()
    test_ImgDraw()


if __name__ == '__main__':
    tests()
