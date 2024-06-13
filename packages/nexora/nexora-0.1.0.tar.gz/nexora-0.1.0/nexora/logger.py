import logging


shandler = logging.StreamHandler()
shandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
fhandler = logging.FileHandler("/tmp/autotuna.log")
fhandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger = logging.getLogger("nexora")
logger.addHandler(shandler)
logger.addHandler(fhandler)
logger.setLevel(logging.INFO)
