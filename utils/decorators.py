import logging
import functools
from weblib.error import ResponseNotValid


logger = logging.getLogger('blogs')


def validate_page(validation_func,
                  validation_errors=(ResponseNotValid,),
                  skip_invalid=True):
    """
    Args:
        :param validate_func: name or reference to the validation function
    """
    def build_decorator(func):
        @functools.wraps(func)
        def func_wrapper(self, grab, task):
            try:
                if isinstance(validation_func, str):
                    getattr(self, validation_func)(grab)
                else:
                    validation_func(grab)
            except validation_errors:
                if skip_invalid:
                    logger.info(
                        "Page skipped: {}".format(grab.response.url))
                else:
                    raise
            else:
                grab.meta['page-not-valid'] = None
                result = func(self, grab, task)
                if result is not None:
                    for event in result:
                        yield event
        return func_wrapper
    return build_decorator
