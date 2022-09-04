import logging
import os
import pathlib
import typing

import numpy as np

from leaf_focus.ocr import model
from leaf_focus import utils

logger = logging.getLogger(__name__)


class OpticalCharacterRecognition:
    def __init__(self):
        self._pipeline = None

    def create_engine(self):
        if self._pipeline is not None:
            return

        logger.warning("Creating keras ocr processing engine.")

        log_level = logger.getEffectiveLevel()

        # set TF_CPP_MIN_LOG_LEVEL before importing tensorflow
        # this allows changing the logging printed by tensorflow
        tf_log_level_map = {
            logging.DEBUG: "0",
            logging.INFO: "1",
            logging.WARNING: "2",
            logging.ERROR: "3",
        }
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = tf_log_level_map.get(log_level)

        import tensorflow as tf

        # also set the tf logger level

        tf.get_logger().setLevel(log_level)

        import keras_ocr

        # TODO: allow using local weights files for detector
        # detector_weights_path = ""
        # detector = keras_ocr.detection.Detector(weights=None)
        # detector.model = keras_ocr.detection.build_keras_model(
        #     weights_path=detector_weights_path, backbone_name="vgg"
        # )
        # detector.model.compile(loss="mse", optimizer="adam")
        detector = None

        # TODO: allow using local weights files for recogniser
        # recognizer_weights_path = ""
        # recognizer = keras_ocr.recognition.Recognizer(
        #     alphabet=keras_ocr.recognition.DEFAULT_ALPHABET, weights=None
        # )
        # recognizer.model.load_weights(recognizer_weights_path)
        recognizer = None

        # see: https://github.com/faustomorales/keras-ocr
        # keras-ocr will automatically download pretrained
        # weights for the detector and recognizer.
        self._pipeline = keras_ocr.pipeline.Pipeline(
            detector=detector, recognizer=recognizer
        )

    def recognise_text(
        self, image_file: pathlib.Path, output_dir: pathlib.Path
    ) -> model.KerasOcrResult:

        if not image_file:
            raise utils.LeafFocusException("Must supply image file.")
        if not output_dir:
            raise utils.LeafFocusException("Must supply output directory.")
        if not image_file.exists():
            msg = f"Image file does not exist '{image_file}'."
            raise utils.LeafFocusException(msg) from FileNotFoundError(image_file)

        # check if output files already exist
        annotations_file = utils.output_root(image_file, "annotations", output_dir)
        annotations_file = annotations_file.with_suffix(".png")

        predictions_file = utils.output_root(image_file, "predictions", output_dir)
        predictions_file = predictions_file.with_suffix(".csv")

        result = model.KerasOcrResult(
            output_dir=output_dir,
            annotations_file=annotations_file,
            predictions_file=predictions_file,
            items=[],
        )

        if annotations_file.exists() and predictions_file.exists():
            logger.debug(
                "Predictions and annotations files already exist "
                f"for '{image_file.stem}'."
            )
            items = list(model.TextItem.load(predictions_file))
            result.items = model.TextItem.order_text_lines(items)
            return result

        # read in the image
        logger.debug(
            f"Creating predictions and annotations files for '{image_file.stem}'."
        )
        import keras_ocr

        self.create_engine()

        images = [
            keras_ocr.tools.read(str(image_file)),
        ]

        # Each list of predictions in prediction_groups is a list of
        # (word, box) tuples.
        prediction_groups = self._pipeline.recognize(images)

        # Plot and save the predictions
        for image, predictions in zip(images, prediction_groups):
            self.save_figure(annotations_file, image, predictions)

            items = list(self.convert_predictions(predictions))
            self.save_items(predictions_file, [item for line in items for item in line])
            result.items = items

        return result

    def save_figure(
        self,
        annotation_file: pathlib.Path,
        image: typing.Optional[np.ndarray],
        predictions: typing.List[typing.Tuple[typing.Any, typing.Any]],
    ):
        """Save the annotated image."""

        if not annotation_file:
            raise utils.LeafFocusException("Must supply annotation file.")
        if image is None or image.size < 1 or len(image.shape) != 3:
            msg_image = image.shape if image is not None else None
            raise utils.LeafFocusException(
                f"Must supply valid image data, not '{msg_image}'."
            )
        if not predictions:
            predictions = []

        logger.info(f"Saving OCR image to '{annotation_file}'.")

        import matplotlib.pyplot as plt

        annotation_file.parent.mkdir(exist_ok=True, parents=True)

        fig, ax = plt.subplots(figsize=(20, 20))
        import keras_ocr

        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
        fig.savefig(str(annotation_file))
        plt.close(fig)

    def convert_predictions(
        self, predictions: typing.List[typing.Tuple[typing.Any, typing.Any]]
    ) -> typing.List[typing.List[model.TextItem]]:
        """Convert predictions to items."""
        if not predictions:
            predictions = []

        items = []
        for prediction in predictions:
            items.append(model.TextItem.from_prediction(prediction))

        # order_text_lines sets the line number and line order
        line_items = model.TextItem.order_text_lines(items)

        return line_items

    def save_items(
        self,
        items_file: pathlib.Path,
        items: typing.Iterable[model.TextItem],
    ):
        """Save items to csv file."""
        if not items_file:
            raise utils.LeafFocusException("Must supply predictions file.")
        if not items:
            raise utils.LeafFocusException("Must supply predictions data.")

        logger.info(f"Saving OCR predictions to '{items_file}'.")

        items_list = list(items)
        model.TextItem.save(items_file, items_list)

    def _build_name(self, prefix: str, middle: str, suffix: str):
        prefix = prefix.strip("-")
        middle = middle.strip("-")
        suffix = suffix if suffix.startswith(".") else "." + suffix
        return "-".join([prefix, middle]) + suffix
