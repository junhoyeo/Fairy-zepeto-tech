import cv2
import imutils
import dlib

def _draw_rect(frame, rect):
    (x, y, w, h) = rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return rect


def draw_dlib_rect(frame, rect):
    # dlib.rectangle을 frame에 cv2 rectangle로 표시
    x, y = rect.left(), rect.top()
    return _draw_rect(frame, (x, y, rect.right() - x, rect.bottom() - y))

def get_rect_width(rect):
    return rect.right() - rect.left()

def main():
    detector = dlib.get_frontal_face_detector()
    # predictor = dlib.shape_predictor(
    #     './shape_predictor_68_face_landmarks.dat')

    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', 1000, 800)

    prev_face = None
    prev_idx = 0
    PREV_MAX = 100

    mask = cv2.imread('./mask.png', -1)

    frame = cv2.imread('./photo.jpg', -1)
    frame = imutils.resize(frame, width=960)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    try:
        rects = detector(gray, 0)
        rects = sorted(
            rects,
            key=lambda rect: rect.width() * rect.height(),
            reverse=True)
        # 면적(인식된 범위)이 가장 커다란 사각형(얼굴)을 가져옴
        rect = rects[0]

    except IndexError:
        rect = None

    if rect:
        prev_idx = 0

    if not rect:
        if prev_face is not None and prev_idx < PREV_MAX:
            rect = prev_face  # 결과가 없는 경우 적절히 오래된(PREV_MAX) 이전 결과를 사용
            prev_idx += 1

    if rect:  # 얼굴을 인식한 경우(prev_face를 사용하는 경우 포함)
        prev_face = rect  # 저장

        # shape = get_shape(predictor, gray, rect)

        mask = cv2.resize(mask, (get_rect_width(rect), get_rect_width(rect)))
        mask_h, mask_w, _ = mask.shape
        mask_x, mask_y = mask_w / 2, mask_h / 2

        locate_x, locate_y = int(
            (rect.right() + rect.left()) / 2), int(rect.top() + rect.bottom() / 2) - 100
        dx = (locate_x - mask_x)
        dy = (locate_y - mask_y)

        alpha_s = mask[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            frame[int(dy):int(dy + mask_h), int(dx):int(dx + mask_w), c] = (alpha_s * mask[:, :, c] +
                                      alpha_l * frame[int(dy):int(dy + mask_h), int(dx):int(dx + mask_w), c])

        draw_dlib_rect(frame, rect)

    cv2.imshow("Frame", frame)  # 프레임 표시
    cv2.waitKey(0)

if __name__ == '__main__':
    main()

# s_img = cv2.imread("mask.png", -1)
# l_img = cv2.imread('photo.jpg',-1)
# locate_x = 162
# locate_y = 69

# y1, y2 = locate_y, locate_y + s_img.shape[0]
# x1, x2 = locate_x, locate_x + s_img.shape[1]

# alpha_s = s_img[:, :, 3] / 255.0
# alpha_l = 1.0 - alpha_s

# for c in range(0, 3):
#     l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
#                               alpha_l * l_img[y1:y2, x1:x2, c])
# cv2.imwrite('final.png',l_img)
