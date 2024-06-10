
import asyncio
from collections import OrderedDict
import inspect
import os
import sys
from pydoc import cli
import papermill
import click
from loguru import logger
from paperless.paperless import Paperless

@click.group()
def cli():
    """
    This is the main command line interface for the Paperless application.
    """



def PaperlessExecuter(*args, **kwargs):
    """
    Executes the Paperless application with the given arguments and keyword arguments.

    Args:
        *args: Positional arguments passed to the Paperless application.
        **kwargs: Keyword arguments passed to the Paperless application.

    Returns:
        The result of executing the Paperless application.
    """
    template_name = os.getenv("TEMPLATE_NAME", "")
    logger.info("paperless execution started! with template_name: {template_name}", template_name=template_name)

    loop = asyncio.get_event_loop()
    paperless = loop.run_until_complete(Paperless(notebookPath=kwargs['input_path'], \
                     templateName=template_name).\
        configure())

    return paperless.\
        build_session().\
        verify().\
        execute(args,kwargs).\
        shutdown()
    

# replace the execute_notebook function with the PaperlessExecuter
module = sys.modules["papermill.execute"]
module.execute_notebook =  PaperlessExecuter
from papermill.cli import papermill

# export defualt command of papermill
papermill()