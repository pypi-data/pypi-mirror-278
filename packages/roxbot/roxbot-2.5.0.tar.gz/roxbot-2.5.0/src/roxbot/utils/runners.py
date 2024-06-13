#!/usr/bin/env python3
"""
utility functions

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import asyncio
import logging
import os
from typing import Any, Coroutine

import coloredlogs

from roxbot import LOG_FORMAT


def run_main_async(coro: Coroutine[Any, Any, None]) -> None:
    """convenience function to avoid code duplication"""
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    coloredlogs.install(level=loglevel, fmt=LOG_FORMAT)
    logging.info(f"Log level set to {loglevel}")

    try:
        asyncio.run(coro)
    except KeyboardInterrupt:
        pass
    except ExceptionGroup as group:
        logging.error("ExceptionGroup caught")
        for e in group.exceptions:
            logging.exception(f"Caught exception: {e}", exc_info=e)
    except asyncio.CancelledError:
        logging.error("Cancelled")

    except Exception as e:
        logging.error(f"Crashed with {e},  type: {type(e)}")
