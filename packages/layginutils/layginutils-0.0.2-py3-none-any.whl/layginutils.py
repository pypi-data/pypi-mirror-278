# -*- coding: utf-8 -*-
# '''
# @date: 4/12/2024
#
# @author: laygin
#
# '''
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import math
import time
import logging
from PIL import Image, ImageDraw
from PIL import Image
import imutils
import pyclipper
import pycocotools.mask
from shapely.geometry import Polygon


def plot_boxes(img, bboxes, color=(0, 0, 255), show=True):
    if isinstance(img, Image.Image):
        img = np.asarray(img.convert('RGB'))[..., ::-1]

    bboxes = [b.astype(int) for b in bboxes]
    img = cv2.drawContours(img.astype(np.uint8), bboxes, -1, color, 2)
    if show:
        cv2.imshow('img', img)
        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
    return img


def plot_img(img, name='img', x=40, y=30):
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)
    cv2.imshow(name, img)
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()


def load_txt(txt_file):
    res = []
    with open(txt_file, 'r', encoding='utf-8') as f:
        for i in f:
            res.append(i.strip())
    return res


def to_txt(cnt, txt_file):
    with open(txt_file, 'w', encoding='utf-8') as f:
        for i in cnt:
            f.write(f'{i}\n')


def shape_to_mask(img_shape, points, shape_type=None, line_width=10, point_size=5):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = Image.fromarray(mask)
    draw = ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]
    if shape_type == "circle":
        assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
    elif shape_type == "rectangle":
        assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
        draw.rectangle(xy, outline=1, fill=1)
    elif shape_type == "line":
        assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == "linestrip":
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == "point":
        assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
    else:
        assert len(xy) > 2, "Polygon must have points more than 2"
        draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def plot_img_plt(img, fig_size=(15, 10), title='', cmap=None):
    plt.figure(figsize=fig_size)
    plt.imshow(img, cmap=cmap)
    plt.title(title)
    plt.tight_layout()
    plt.show(block=True)


def load_jsn(jsnfile):
    with open(jsnfile, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump_jsn(cnt, jsn_file):
    with open(jsn_file, 'w', encoding='utf-8') as f:
        json.dump(cnt, f, indent=2)


def is_image_ext(file: str) -> bool:
    IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')
    for i in IMG_EXTENSIONS:
        if file.endswith(i):
            return True
    else:
        return False


def get_hierarchical_files(data_dir, ext='jpg'):
    files = []
    for r, d, fs in os.walk(data_dir):
        for i in fs:
            if i.endswith(ext):
                files.append(os.path.join(r, i))

    return files


def get_hierarchical_images(data_dir):
    files = []
    for r, d, fs in os.walk(data_dir):
        for i in fs:
            if is_image_ext(i):
                files.append(os.path.join(r, i))

    return files


def cv_imread(imgpath, flag=1):
    img = cv2.imread(imgpath, flag)
    if os.path.exists(imgpath) and img is None:
        img = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), flag)

    return img


def cv_imwrite(img, path, ext='jpg'):
    cv2.imencode(f'.{ext}', img)[1].tofile(path)


def image_wall(imgs, h=128, w=128, nh=1):
    num_imgs = len(imgs)
    # nh = 1  # math.ceil(num_imgs ** (1/2))
    nw = math.ceil(num_imgs/nh)

    wall = np.zeros((nh*h, nw*w, 3), dtype=np.uint8)
    rects = []
    for i in range(nh):
        for j in range(nw):
            wall[i*h:(i+1)*h, j*w:(j+1)*w] = imgs[i*nw+j]
            rects.append((i*h, j*w))
    # for pt in rects:
    #     pt = pt[::-1]
    #     wall = cv2.rectangle(wall, pt, (pt[0]+h, pt[1]+w), (255,0,0),2)

    return wall


def get_stride_and_kernel_wrt_planes(in_planes, out_planes):
    s = in_planes // out_planes
    k = in_planes - (out_planes - 1) * s

    return s, k


def sort_poly(p):
    if not isinstance(p, np.ndarray):
        p = np.array(p, dtype='float32')
    min_axis = np.argmin(np.sum(p, axis=1))
    p = p[[min_axis, (min_axis + 1) % 4, (min_axis + 2) % 4, (min_axis + 3) % 4]]
    if abs(p[0, 0] - p[1, 0]) > abs(p[0, 1] - p[1, 1]):
        return p
    else:
        return np.array(p[[0, 3, 2, 1]], dtype='float32')


def warp_img(image, pts):
    if not isinstance(pts, np.ndarray):
        pts = np.array(pts, dtype='float32')
    pts_rect = cv2.minAreaRect(pts)
    pts_rect = cv2.boxPoints(pts_rect).astype(np.int32)

    rect = sort_poly(pts_rect)
    tl, tr, br, bl = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
    rect = rect.astype('float32')

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def pointsorted(box):
    '''for warp_img1'''
    points = sorted(box, key=lambda x: x[0])
    if points[1][1] > points[0][1]:
        indexFirt = 0
        indexFour = 1
    else:
        indexFirt = 1
        indexFour = 0
    if points[3][1] > points[2][1]:
        indexSecond = 2
        indexThirt = 3
    else:
        indexSecond = 3
        indexThirt = 2
    new_box = [points[indexFirt], points[indexSecond], points[indexThirt], points[indexFour]]

    return new_box


def warp_img1(img, box):
    # box = pointsorted(box)
    dest_width1 = np.sqrt(((box[0][0] - box[1][0]) ** 2) + ((box[0][1] - box[1][1]) ** 2))
    dest_width2 = np.sqrt(((box[3][0] - box[2][0]) ** 2) + ((box[3][1] - box[2][1]) ** 2))
    maxWidth = int(max(dest_width1, dest_width2))
    dest_height1 = np.sqrt(((box[0][0] - box[3][0]) ** 2) + ((box[0][1] - box[3][1]) ** 2))
    dest_height2 = np.sqrt(((box[1][0] - box[2][0]) ** 2) + ((box[1][1] - box[2][1]) ** 2))
    maxHeight = int(max(dest_height1, dest_height2))
    ratio = maxHeight / maxWidth
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
    rect = np.array(box, dtype="float32")
    Matrix = cv2.getPerspectiveTransform(rect, dst)
    warped_img = cv2.warpPerspective(img, Matrix, (maxWidth, maxHeight))
    if ratio > 1.8:
        warped_img = imutils.rotate_bound(warped_img, 90)

    return warped_img


def get_rect_from_pts(pts):
    if pts is None:
        return None
    pts = np.array(pts)
    ys, xs = pts[:, 1], pts[:, 0]
    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    return np.array([xmin, ymin, xmax, ymax]).tolist()


def get_pts_from_mask(mask):
    contours, _ = cv2.findContours(mask.astype('uint8'), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    area = [cv2.contourArea(i) for i in contours]
    max_idx = np.argmax(area)
    con = contours[max_idx]
    # # # fixme: rotated rectangle, not good
    # bbox = cv2.minAreaRect(con)
    # points = cv2.boxPoints(bbox)

    # # # fixme: points
    eps = 0.005 * cv2.arcLength(con, True)
    approx = cv2.approxPolyDP(con, eps, True)
    points = approx.reshape((-1, 2))
    return np.intp(points).tolist()


def get_rect_from_mask(mask):
    '''applied to only one mask'''
    h = mask.shape[0]
    w = mask.shape[1]

    nonZeroEleMask = np.nonzero(mask)
    nonZeroMaskYlist = nonZeroEleMask[0]
    nonZeroMaskXlist = nonZeroEleMask[1]
    indexStartX = np.min(nonZeroMaskXlist) - 16
    indexEndX = np.max(nonZeroMaskXlist) + 16
    indexStartY = np.min(nonZeroMaskYlist) - 16
    indexEndY = np.max(nonZeroMaskYlist) + 16
    indexStartX = indexStartX if indexStartX > 0 else 1
    indexStartY = indexStartY if indexStartY > 0 else 1
    indexEndX = indexEndX if indexEndX < w else w - 1
    indexEndY = indexEndY if indexEndY < h else h - 1

    return [[indexStartX, indexStartY], [indexEndX, indexEndY]]


def extract_image_by_mask(ori_img, mask):
    return cv2.bitwise_and(ori_img, ori_img, mask=mask.astype(np.uint8))


def boxscorefast(bitmap, _box):
    h, w = bitmap.shape[:2]
    box = _box.copy()
    xMin = np.clip(np.floor(box[:, 0].min()).astype(np.int), 0, w - 1)
    xMax = np.clip(np.ceil(box[:, 0].max()).astype(np.int), 0, w - 1)
    yMin = np.clip(np.floor(box[:, 1].min()).astype(np.int), 0, h - 1)
    yMax = np.clip(np.ceil(box[:, 1].max()).astype(np.int), 0, h - 1)

    mask = np.zeros((yMax - yMin + 1, xMax - xMin + 1), dtype=np.uint8)
    box[:, 0] = box[:, 0] - xMin
    box[:, 1] = box[:, 1] - yMin
    cv2.fillPoly(mask, box.reshape(1, -1, 2).astype(np.int32), 1)
    return round(cv2.mean(bitmap[yMin:yMax + 1, xMin:xMax + 1], mask)[0], 4)


def unclip(box, unclip_ratio=1.5):
    poly = Polygon(box)
    distance = poly.area * unclip_ratio / poly.length
    offset = pyclipper.PyclipperOffset()
    offset.AddPath(box, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    expanded = np.array(offset.Execute(distance))
    return expanded


def get_mini_boxes(contour):
    bounding_box = cv2.minAreaRect(contour)
    points = sorted(list(cv2.boxPoints(bounding_box)), key=lambda x: x[0])
    if points[1][1] > points[0][1]:
        index_1 = 0
        index_4 = 1
    else:
        index_1 = 1
        index_4 = 0
    if points[3][1] > points[2][1]:
        index_2 = 2
        index_3 = 3
    else:
        index_2 = 3
        index_3 = 2
    box = [points[index_1], points[index_2], points[index_3], points[index_4]]
    return box, min(bounding_box[1])


def polygons_from_mask(pred, mask, unclip_ratio=1.5, box_th=0.8):
    height, width = mask.shape[:2]
    boxes = []
    scores = []
    contours, _ = cv2.findContours((mask*255).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        eps = 0.005 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, eps, True)
        points = approx.reshape((-1, 2))
        if points.shape[0] < 4: continue
        score = boxscorefast(pred, contour.squeeze(1))
        if box_th > score: continue
        scores.append(score)
        if points.shape[0] > 2:
            box = unclip(points, unclip_ratio=unclip_ratio)
            if len(box) > 1:continue
        else:continue

        box = box.reshape(-1, 2)
        box[:, 0] = np.clip(box[:, 0], 0, width)
        box[:, 1] = np.clip(box[:, 1], 0, height)
        boxes.append(box.astype(int))
    return boxes, scores


def boxes_from_mask(pred, mask, unclip_ratio=1.5, max_candidates=100, min_size=5, box_th=0.8):
    height, width = mask.shape[:2]
    contours, _ = cv2.findContours((mask * 255).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    num_contours = min(len(contours), max_candidates)
    boxes = []
    scores = []

    for index in range(num_contours):
        contour = contours[index].squeeze(1)
        points, sside = get_mini_boxes(contour)
        if sside < min_size: continue
        points = np.array(points)
        score = boxscorefast(pred, contour)
        if box_th > score: continue
        scores.append(score)

        box = unclip(points, unclip_ratio=unclip_ratio).reshape(-1, 1, 2)
        box, sside = get_mini_boxes(box)
        if sside < min_size + 2: continue
        box = np.array(box)
        box[:, 0] = np.clip(box[:, 0], 0, width)
        box[:, 1] = np.clip(box[:, 1], 0, height)
        boxes.append(box.astype(int))
    return boxes, scores


def refine_mask(mask, min_area=200):
    mask = cv2.morphologyEx((mask * 255).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    contours, _ = cv2.findContours((mask * 255).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    new_mask = np.zeros_like(mask, dtype=np.uint8)
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) < min_area: continue
        new_mask = cv2.drawContours(new_mask, contours, i, 1, -1)
    return new_mask


def max_area_cc(mask):
    '''
    labels：图像标记；
    stats：[[x1, y1, width1, height1, area1], ...[xi, yi, widthi, heighti, areai]]，存放外接矩形和连通区域的面积信息；
    centroids:[cen_x, cen_y]，质心的点坐标，浮点类型. 链接：https://www.jianshu.com/p/8961ba4e151e
    :param mask:
    :return:
    '''
    ret, labels, stats, centroid = cv2.connectedComponentsWithStats(mask)
    # draw
    for i, stat in enumerate(stats):
        x0, y0 = stat[0], stat[1]
        x1, y1 = x0 + stat[2], y0 + stat[3]
        cv2.rectangle(mask, (x0, y0), (x1, y1), 255, 2)
        cv2.putText(mask, str(i+1), (x0, y0+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)

    # get maximum area
    # max_area = sorted(stats, key=lambda s: s[-1], reverse=False)[-2]
    # fixme: 22-9-29, thursday, get the second largest area, which is considered be a card mask, 0 for background
    areas = stats[:, 1:-1]
    card_idx = areas.argmax() + 1
    card_mask = (labels == card_idx).astype(np.uint8)
    return card_mask


def fill_mask_holes(mask):
    '''
    refer to: https://github.com/thanhsn/opencv-filling-holes/blob/master/imfill.py.
    container unexpected issue if card mask cross the whole image
    :param mask:
    :return:
    '''
    h, w = mask.shape
    mask_ff = mask.copy()
    msk_ = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(mask_ff, msk_, (0, 0), 255)
    mask_ff_inv = cv2.bitwise_not(mask_ff)
    mask_out = mask | mask_ff_inv
    return mask_out.astype(np.bool)


def get_mask_area(mask):
    mask = np.asfortranarray(mask.astype(np.uint8))
    return float(pycocotools.mask.area(pycocotools.mask.encode(mask)))


def get_box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def get_polygon_area(pts):
    # return cv2.contourArea(pts)
    return Polygon(pts).area


class Metric:
    @staticmethod
    def box_iou(box1, box2):
        sox = max(box1[0], box2[0])
        soy = max(box1[1], box2[1])
        eox = min(box1[2], box2[2])
        eoy = min(box1[3], box2[3])
        overlap = max(eox - sox, 0) * max(eoy - soy, 0)
        union = get_box_area(box1) + get_box_area(box2) - overlap
        return overlap / union

    @staticmethod
    def mask_iou(mask1, mask2):
        union = mask1 | mask2
        inter = mask1 & mask2
        return get_mask_area(inter) / get_mask_area(union)

    @staticmethod
    def polygon_iou(pt1, pt2):
        p1 = Polygon(pt1)
        p2 = Polygon(pt2)
        intersect = p1.intersection(p2).area
        union = p1.union(p2).area
        return intersect / union


def create_logger(output_dir, log_name):
    if not os.path.exists(output_dir):
        print('=> creating {}'.format(output_dir))
        os.makedirs(output_dir)

    time_str = time.strftime('%Y-%m-%d-%H-%M')
    log_file = '{}_{}.txt'.format(log_name, time_str)
    final_log_file = os.path.join(output_dir, log_file)
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename=str(final_log_file), format=head)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    logging.getLogger('').addHandler(console)

    return logger

