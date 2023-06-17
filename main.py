from matplotlib import pyplot as plt
import cv2
from search import LocationSearch
from stream import StreamController
import time
import config


def track():
    searcher = LocationSearch()
    stream = StreamController(config.FILENAME_IN, config.FILENAME_OUT)

    total_frames = 0

    while True:
        #t = time.time()
        frame = stream.get_frame()
        if frame is None:
            break

        if total_frames % 5 == 0:
            source_img = frame
            target_img = plt.imread(config.FILENAME_MAP)
            h, w = target_img.shape[:2]
            target_img = cv2.resize(target_img, (int(0.75 * w), int(0.75 * h)))
            try:
                output_image = searcher.search(source_img, target_img)
            except Exception as e:
                searcher.is_focus = False
                pass
        #print(f'{time.time() - t}')
        output_image = cv2.resize(output_image, (1920,1080))
        stream.write_and_show(output_image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        total_frames += 1

    stream.destroy()

if __name__ == "__main__":
    track()

