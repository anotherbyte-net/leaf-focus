import logging
import pathlib
import typing

from leaf_focus.pdf import model

logger = logging.getLogger("leaf_focus.app")


class App:
    """The main application."""

    def __init__(self, exe_dir: pathlib.Path):
        """
        Create a new instance of the application.

        :param exe_dir: path to the directory containing the executable files
        """

        self._exe_dir = exe_dir

    def run(self, input_pdf: pathlib.Path, output_dir: pathlib.Path) -> bool:
        """
        Run the application.

        :param input_pdf: path to the pdf file
        :param output_dir: path to the output directory to save text files
        :return: return true if the text extraction succeeded, otherwise false
        :rtype: bool
        """

        logger.info("Starting leaf-focus")
        input_pdf, output_dir = self.validate(input_pdf, output_dir)

        # create the output directory
        if not output_dir.is_dir():
            logger.warning(f"Creating output directory '{output_dir}'.")
            output_dir.mkdir(exist_ok=True, parents=True)
        else:
            logger.info(f"Using output directory '{output_dir}'.")

        # TODO: implement the text extraction

        logger.info("Finished")
        return True

    def validate(
        self, input_pdf: pathlib.Path, output_dir: pathlib.Path
    ) -> typing.Tuple[pathlib.Path, pathlib.Path]:
        """
        Validate the input and output paths.

        :param input_pdf: path to the pdf file
        :param output_dir: path to the output directory to save text files
        :return: returns the normalised input and output paths
        :rtype: typing.Tuple[pathlib.Path, pathlib.Path]
        """

        if not self._exe_dir or not self._exe_dir.exists():
            raise model.LeafFocusException(
                f"Could not find the exe dir: '{self._exe_dir}'."
            )
        self._exe_dir = self._exe_dir.resolve()

        if not input_pdf or not input_pdf.exists():
            raise model.LeafFocusException(
                f"Could not find the input pdf file: '{input_pdf}'."
            )
        input_pdf = input_pdf.resolve()

        if not output_dir:
            raise model.LeafFocusException("Must provide the output directory.")

        output_dir = output_dir.absolute()

        return input_pdf, output_dir
