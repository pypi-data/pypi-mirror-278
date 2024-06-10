from os import getcwd
from paperless.paperless import Paperless
import pytest
from paperless.paperless import Paperless


def test_e2e_process(*args, **kwargs):
    """
    This is a test function for end-to-end processing.
    """
    Paperless(
        notebookPath=f'./tests/resources/test.ipynb').\
        configure().\
        build_session().\
        verify().\
        execute(args,kwargs).\
        shutdown()
    