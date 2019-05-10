import cv2
from imutils.video import VideoStream
import imutils
import dlib


def draw_dlib_rect(frame, rect):
    x, y = rect.left(), rect.top()
    w, h = rect.right() - x, rect.bottom() - y
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


def main():
    detector = dlib.get_frontal_face_detector()
    # predictor = dlib.shape_predictor(
    #     './shape_predictor_68_face_landmarks.dat')

    vs = VideoStream(src=0, resolution=(1280, 960)).start()
    fileStream = False

    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', 1000, 800)

    prev_face = None
    prev_idx = 0
    PREV_MAX = 100

    mask = cv2.imread('./mask.png')
    mask_h, mask_w, _ = mask.shape
    mask_x, mask_y = mask_w / 2, mask_h / 2

    while True:
        if fileStream and not vs.more():
            break

        frame = vs.read()
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

            draw_dlib_rect(frame, rect)
            frame_x, frame_y = int(
                (rect.right() + rect.left()) / 2), int(rect.top() + rect.bottom() / 2)
            cv2.circle(frame, (frame_x, frame_y), 5, (0, 255, 0), -1)
            dx = (frame_x - mask_x)
            dy = (frame_y - mask_y)

            frame[int(dy):int(dy + mask_h), int(dx):int(dx + mask_w)] = mask

        cv2.imshow("Frame", frame)  # 프레임 표시

        # q 키를 눌러 종료
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()


if __name__ == '__main__':
    main()
