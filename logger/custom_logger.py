import logging,os
from datetime import datetime
class CustomLogger:
    def __init__(self,log_dir="logs"):
        self.log_dirs=os.path.join(os.getcwd(),log_dir)
        os.makedirs(self.log_dirs,exist_ok=True)
        #creation of log file

        log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        LOG_FILE_PATH=os.path.join(self.log_dirs,log_file)

        #logger config
        logging.basicConfig(
            filename=LOG_FILE_PATH,
            format='[%(asctime)s] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s',
            level=logging.INFO
        )
    def get_Logger(self,name=__file__):
        return logging.getLogger(os.path.basename(name))
    
if __name__=="__main__":
    logger=CustomLogger()
    logger=logger.get_Logger(__file__)
    logger.info('Custom Logger Initialised')


