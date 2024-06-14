.. image:: https://img.shields.io/pypi/v/fancylogging
   :alt: PyPI - Version

Fancy Logging
=============

Introduction
------------

This Python module provides an advanced logging setup using `rich` for 
console logging and `python-json-logger` for file logging. It allows for
detailed and formatted logging, ideal for applications requiring high-level
logging capabilities.

Installation
------------
This module requires the following dependencies:

* `rich <https://pypi.org/project/rich/>`_
* `python-json-logger <https://pypi.org/project/python-json-logger/>`_

Usage
-----
Import ``setup_fancy_logging`` from the module and configure your logging setup
by specifying parameters like `base_logger_name`, `console_log_level`,
`file_log_level`, `log_file_path`, and others.

Example:


.. code-block:: python

  import logging
  from fancylogging import setup_fancy_logging

  log = logging.getLogger("test")

  if __name__ == "__main__":
      setup_fancy_logging(
          "test",
          console_log_level=logging.INFO,
          file_log_level=logging.DEBUG,
          file_log_path="logs/test.json",
          file_mode="w",
      )

      log.info("Info message")
      log.debug("Debug message")
      log.warning("Warning message")
      log.error("Error message")
      log.critical("Critical message")
      try:
          raise Exception("Raising a test exception")
      except Exception:
          log.exception("Exception message")
