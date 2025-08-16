import os,logging
def get_logger(testcase):
    folder = os.path.join(os.path.dirname(__file__),'..','Logs',f'{testcase}')
    print(folder)
    os.makedirs(folder,exist_ok=True)
    logger = logging.getLogger(testcase)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file = os.path.join(folder,f'{testcase}.log')
        fh = logging.FileHandler(file)
        fmt = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

