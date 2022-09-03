import os
import pathlib
import typing

import numpy as np

from leaf_focus.ocr import model
from leaf_focus import utils


class OpticalCharacterRecognition:
    def __init__(self):
        # set TF_CPP_MIN_LOG_LEVEL before importing tensorflow
        # this allows changing the logging printed by tensorflow
        # values:
        # 0: DEBUG: All messages are logged (default).
        # 1: INFO: INFO messages are not logged.
        # 2: WARNING: INFO and WARNING messages are not logged.
        # 3: ERROR: INFO, WARNING, and ERROR messages are not logged.
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

        import tensorflow as tf

        # also set the tf logger level
        tf.get_logger().setLevel("WARNING")

        import keras_ocr

        # see: https://github.com/faustomorales/keras-ocr
        # keras-ocr will automatically download pretrained
        # weights for the detector and recognizer.
        self._pipeline = keras_ocr.pipeline.Pipeline()

    def recognise_text(
        self, image_file: pathlib.Path, output_dir: pathlib.Path
    ) -> model.KerasOcrResult:
        if not image_file:
            raise ValueError("Must supply image file.")
        if not output_dir:
            raise ValueError("Must supply output directory.")
        # if not ocr_args:
        #     raise ValueError("Must supply ocr arguments.")
        if not image_file.exists():
            raise FileNotFoundError(f"Image file does not exist '{image_file}'.")

        # read in the image
        import keras_ocr

        images = [
            keras_ocr.tools.read(str(image_file)),
        ]

        # Each list of predictions in prediction_groups is a list of
        # (word, box) tuples.
        prediction_groups = self._pipeline.recognize(images)

        # Plot and save the predictions
        items_ordered: typing.List[typing.List[model.TextItem]] = []

        annotations_file = utils.output_root("annotations", output_dir)
        annotations_file = annotations_file.with_suffix(".png")

        predictions_file = utils.output_root("predictions", output_dir)
        predictions_file = predictions_file.with_suffix(".csv")

        for image, predictions in zip(images, prediction_groups):
            self.save_figure(annotations_file, image, predictions)
            items = list(self.convert_predictions(predictions))
            items_ordered = self.order_text_lines(items)
            self.save_items(predictions_file, items)

        return model.KerasOcrResult(
            output_dir=output_dir,
            annotations_file=annotations_file,
            predictions_file=predictions_file,
            items=items_ordered,
        )

    def save_figure(
        self,
        annotation_file: pathlib.Path,
        image: typing.Optional[np.ndarray],
        predictions: typing.List[typing.Tuple[typing.Any, typing.Any]],
    ):
        """Save the annotated image."""

        if not annotation_file:
            raise ValueError("Must supply annotation file.")
        if image is None or image.size < 1 or len(image.shape) != 3:
            msg_image = image.shape if image is not None else None
            raise ValueError(f"Must supply valid image data, not '{msg_image}'.")
        if not predictions:
            predictions = []

        self._log_info(f"Saving OCR image to '{annotation_file}'.")

        import matplotlib.pyplot as plt

        annotation_file.parent.mkdir(exist_ok=True, parents=True)

        fig, ax = plt.subplots(figsize=(20, 20))
        import keras_ocr

        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
        fig.savefig(str(annotation_file))
        plt.close(fig)

    def convert_predictions(
        self, predictions: typing.List[typing.Tuple[typing.Any, typing.Any]]
    ) -> typing.Generator[model.TextItem, typing.Any, None]:
        """Convert predictions to items."""
        if not predictions:
            predictions = []

        for prediction in predictions:
            yield model.TextItem.from_prediction(prediction)

    def save_items(
        self,
        items_file: pathlib.Path,
        items: typing.Iterable[model.TextItem],
    ):
        """Save items to csv file."""
        if not items_file:
            raise ValueError("Must supply predictions file.")
        if not items:
            raise ValueError("Must supply predictions data.")

        self._log_info(f"Saving OCR predictions to '{items_file}'.")

        items_list = list(items)

        # order_text_lines sets the line number and line order
        self.order_text_lines(items_list)
        model.TextItem.save(items_file, items_list)

    def order_text_lines(self, items: typing.Iterable[model.TextItem]):
        """Put items into lines of text (top -> bottom, left -> right)."""
        if not items:
            items = []

        self._log_debug("Arranging text into lines.")

        lines = []
        current_line = []
        for item in items:
            if not item.is_horizontal_level:
                # exclude items that are too sloped
                continue

            if len(current_line) < 1:
                current_line.append(item)

            elif any([item.is_same_line(i) for i in current_line]):
                current_line.append(item)

            elif len(current_line) > 0:
                # store current line
                current_line = sorted(current_line, key=lambda x: x.top_left)
                lines.append(current_line)

                # create new line
                current_line = [item]

        # include last items
        if len(current_line) > 0:
            lines.append(current_line)

        # update items to set line number and line order
        for line_index, line in enumerate(lines):
            for item_index, item in enumerate(line):
                item.line_number = line_index + 1
                item.line_order = item_index + 1

        return lines

    def _build_name(self, prefix: str, middle: str, suffix: str):
        prefix = prefix.strip("-")
        middle = middle.strip("-")
        suffix = suffix if suffix.startswith(".") else "." + suffix
        return "-".join([prefix, middle]) + suffix

    def _log_debug(self, message: str):
        # self._logger.debug(message)
        print(message)

    def _log_info(self, message: str):
        # self._logger.info(message)
        print(message)
