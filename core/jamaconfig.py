import logging


class JamaConfig:
    def __init__(self):
        self.username = "username"
        self.password = "password"
        self.auth = (self.username, self.password)
        self.base_url = "https://base_url.jamacloud.com"
        self.rest_url = self.base_url + "/rest/latest/"
        self.itemType = 115
        self.projectId = 299
        self.verify_ssl = True
        self.LOG_FILENAME = 'logs.out'
        logging.basicConfig(filename=self.LOG_FILENAME, level=logging.DEBUG)
        self.logger = logging.getLogger("post-process")
        self.urllib3_logger = logging.getLogger('requests')
        self.urllib3_logger.setLevel(logging.CRITICAL)
