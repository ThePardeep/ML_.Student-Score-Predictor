import sys
from .logger import logging

def extract_error_details(error_message, error_detail: sys):
    _, _, exc_trace_back = error_detail.exc_info()
    file_name = exc_trace_back.tb_frame.f_code.co_filename
    tb_lineno = exc_trace_back.tb_lineno
    error_meg = (
        "Error occurred in file name [{0}] line number [{1}] error message[{2}]".format(
            file_name, tb_lineno, str(error_message)
        )
    )
    return error_meg


class CustomException(Exception):

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = extract_error_details(
            error_message, error_detail=error_detail
        )
        logging.info(self.error_message)

    def __str__(self):
        return self.error_message


def a():

    try:
        b = 5 / 0
    except Exception as e:
        raise CustomException(e, sys)
