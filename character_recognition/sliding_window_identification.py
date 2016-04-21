import PIL.Image as Image
import numpy as np
from sklearn.preprocessing import scale
import pickle


def resize_quadratic_image(image):
    if image.size[0] <= 20:
        return image
    image = image.resize((20, 20), Image.ANTIALIAS)
    return image


def get_image_tiles_from_image(image_path="store.jpg"):
    results = []

    image = Image.open(image_path).convert("L")
    horizontal_size = image.size[0]
    vertical_size = image.size[1]
    smallest_side_size = min(horizontal_size, vertical_size)

    for frame_width in range(20, smallest_side_size, 10):
        step_size = frame_width // 2

        for vertical_start in range(0, vertical_size, step_size):
            vertical_end = vertical_start + frame_width
            if vertical_end > vertical_size:
                vertical_start = vertical_size - frame_width
                vertical_end = vertical_size
            
            for horizontal_start in range(0, horizontal_size, step_size):
                horizontal_end = horizontal_start + frame_width
                if horizontal_end > horizontal_size:
                    horizontal_start = horizontal_size - frame_width
                    horizontal_end = horizontal_size
                crop_box = (
                    horizontal_start, vertical_start, horizontal_end, vertical_end)
                examined_frame = image.crop(crop_box)
                resized_crop = resize_quadratic_image(examined_frame)
                flattened_array = np.asarray(resized_crop.getdata(), dtype=np.float64).reshape(
                    (resized_crop.size[1] * resized_crop.size[0], 1))

                flattened_array = scale(flattened_array)

                results.append(flattened_array)

    results = np.array(results)
    results = results.reshape(results.shape[:2])

    return results


if __name__ == "__main__":
    classifier = pickle.load(open("classifier.pickle", "rb"))
    inputs = get_image_tiles_from_image()
    predictions = classifier.predict(inputs)
    predictions_with_probabilities = classifier.predict_proba(inputs)
    print("Hello")
