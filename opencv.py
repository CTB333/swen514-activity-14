import cv2 as cv
import numpy as np
import os
import shutil

OPEN_IMG = "assets/open.png"
CLOSED_IMG = "assets/closed.png"
NEEDLE_IMG = "assets/chat.png"
VIDEO_PATH = "assets/video.mkv"
VIDEO_DIRECTORY = "video_clips"


# Clears the folder that holds video segments
def reset_video_analysis(path=VIDEO_DIRECTORY):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)


# Cuts video into segments keeping every nth_frame value
def save_video_frames(video_path, nth_frame=30):
    paths = list()

    current_frame = 0
    video = cv.VideoCapture(video_path)

    while video.isOpened():
        success, frame = video.read()

        if not success:
            video.release()
            cv.destroyAllWindows()
            break

        if current_frame % nth_frame == 0:
            name = f"{VIDEO_DIRECTORY}/{str(current_frame)}_frame.png"
            cv.imwrite(name, cv.cvtColor(frame, cv.COLOR_RGBA2BGRA))
            paths.append(name)
            print(f"Created: {name}")

        current_frame += 1

    return paths


# Attempts object detection on a video, first cutting into frames then attempting to match the needle to each frame¸
def analyze_video(video_path, needle_path):
    reset_video_analysis()
    paths = save_video_frames(video_path, 30)

    print()

    for path in paths:
        haystack, needle, result = matchTemplate(path, needle_path)
        top_left, bottom_right, confidence, valid_match = get_best_match(result, needle)

        title = f"Valid {confidence}"

        if not valid_match:
            print(f"Invalid Match: {path} {confidence}")
            title = f"Invalid {confidence}"
            os.remove(path)

        else:
            print(f"Valid Match: {path}")
            box_needle(haystack, top_left, bottom_right, "Gold")

        print(f"Confidence: {confidence}")
        print()

        cv.imshow(title, haystack)
        # cv.imshow("R-" + title, result)
        cv.waitKey(1250)
        cv.destroyAllWindows()


# Read the file names into computer vision files and look for needle in the haystack
def matchTemplate(haystack, needle):
    haystack_image = cv.imread(haystack, cv.IMREAD_UNCHANGED)
    needle_image = cv.imread(needle, cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(
        haystack_image,
        needle_image,
        # cv.TM_CCOEFF,  # Bad
        # cv.TM_CCOEFF_NORMED, Bad
        # cv.TM_CCORR,  # Bad
        # cv.TM_CCORR_NORMED,  # Bad
        # cv.TM_SQDIFF,  # Better ish
        cv.TM_SQDIFF_NORMED,  # Bad
    )
    return haystack_image, needle_image, result


# Get the coordinates and confidence of the Best Match for the needle in the haystack
def get_best_match(result, needle_image, threshold=0.8):
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    needle_w = needle_image.shape[1]
    needle_h = needle_image.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
    return top_left, bottom_right, max_val, max_val > threshold


# Looks for an image inside another image (needle in a haystack) draws a rectangle around the best match if there is one
def needle_in_haystack(haystack, needle, delay=7500, threshold=0.8):
    haystack_image, needle_image, result = matchTemplate(haystack, needle)

    top_left, bottom_right, confidence, valid_match = get_best_match(
        result, needle_image
    )

    print(f"Best match top left corner position {str(top_left)}")
    print(f"Best match confidence {str(confidence)}")
    if not valid_match:
        print("Needle not found")
    else:
        print("Needle Found")
    print()

    if valid_match:
        box_needle(haystack_image, top_left, bottom_right, "Gold")

    cv.imshow("Result", haystack_image)
    cv.waitKey(delay)


# Draw a box around a cv image to highlight a particular portion of the image
def box_needle(haystack, top_left, bottom_right, color="Green"):
    colors = dict(
        {
            "Green": (0, 255, 0),
            "Red": (0, 0, 255),
            "Blue": (255, 0, 0),
            "Gold": (24, 202, 247),
        }
    )

    cv.rectangle(
        haystack,
        top_left,
        bottom_right,
        thickness=2,
        lineType=cv.LINE_4,
        color=colors[color],
    )


def main():
    analyze_video(VIDEO_PATH, NEEDLE_IMG)
    # needle_in_haystack(OPEN_IMG, NEEDLE_IMG)
    # needle_in_haystack(CLOSED_IMG, NEEDLE_IMG)


if __name__ == "__main__":
    main()
