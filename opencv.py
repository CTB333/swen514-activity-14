import cv2 as cv
import numpy as np

OPEN_IMG = "assets/open.png"
CLOSED_IMG = "assets/closed.png"
NEEDLE_IMG = "assets/chat.png"


def needle_in_haystack(haystack_image, needle_image, delay=5000, threshold=0.8):
    haystack_image = cv.imread(haystack_image, cv.IMREAD_UNCHANGED)
    needle_image = cv.imread(needle_image, cv.IMREAD_UNCHANGED)
    result = cv.matchTemplate(haystack_image, needle_image, cv.TM_CCOEFF_NORMED)

    # Best Match Values
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    print(f"Best match top left corner position {str(max_loc)}")
    print(f"Best match confidence {str(max_val)}")
    if threshold > max_val:
        print("Needle not found")
    else:
        print("Needle Found")
    print()

    needle_w = needle_image.shape[1]
    needle_h = needle_image.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv.rectangle(
        haystack_image,
        top_left,
        bottom_right,
        color=(0, 0, 255),
        thickness=2,
        lineType=cv.LINE_4,
    )

    cv.imshow("Result", haystack_image)
    cv.waitKey(delay)


def main():
    needle_in_haystack(OPEN_IMG, NEEDLE_IMG)
    needle_in_haystack(CLOSED_IMG, NEEDLE_IMG)


if __name__ == "__main__":
    main()
