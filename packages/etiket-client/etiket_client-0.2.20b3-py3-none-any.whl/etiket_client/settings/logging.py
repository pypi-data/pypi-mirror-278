from etiket_client.settings.folders import get_log_dir
import logging, logging.handlers, os
import datetime, sys

def set_up_logging(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    log_file = os.path.join(get_log_dir(), f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_etiket_client.{os.getpid()}.log')
    handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount=10)
    handler.suffix = "%Y%m%d"
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("Logging started, using python version: %s", sys.version)

def set_up_sync_logger(name):
    log_file = os.path.join(get_log_dir(), f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_etiket_sync.{os.getpid()}.log')
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    # little bit hackey but it works...
    if len(logger.handlers) == 1:
        f_name = logger.handlers[0].baseFilename
        logger.handlers[0].flush()
        logger.handlers[0].close()
        logger.handlers.clear()

        os.rename(os.path.join(get_log_dir(), f_name), log_file)
    else:
        logger.handlers.clear()
    
    handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount=10)
    handler.suffix = "%Y%m%d"
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger