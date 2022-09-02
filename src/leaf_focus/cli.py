import argparse
import logging
import pathlib
import sys
import typing

from leaf_focus import app, model

"""Command line for leaf focus."""


def main(args: typing.Optional[typing.List[str]] = None) -> int:
    """
    Run as a command line program.

    :param args: The program arguements.
    :return: Program exit code.
    :rtype: int
    """

    if args is None:
        args = sys.argv[1:]

    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s:] %(message)s", level=logging.INFO
    )
    logger = logging.getLogger("leaf_focus")

    parser = argparse.ArgumentParser(
        prog="leaf-focus",
        description="Extract structured text from a pdf file.",
    )
    parser.add_argument(
        "exe_dir",
        type=pathlib.Path,
        help="path to the directory containing xpdf executable files",
    )
    parser.add_argument(
        "input_pdf",
        type=pathlib.Path,
        help="path to the pdf file to read",
    )
    parser.add_argument(
        "output_dir",
        type=pathlib.Path,
        help="path to the directory to save the extracted text files",
    )
    parsed_args = parser.parse_args(args)

    app_inst = app.App(exe_dir=parsed_args.exe_dir)

    try:
        result = app_inst.run(
            input_pdf=parsed_args.input_pdf,
            output_dir=parsed_args.output_dir,
        )
        return 0 if result else 1

    except model.LeafFocusException as e:
        logger.error(f"Error: {e.__class__.__name__} - {str(e)}")
        return 1

    except Exception as e:
        logger.error(f"Error: {e.__class__.__name__} - {str(e)}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
