# -*- coding: utf-8 -*-

__original_author__ = "Rolando Espinoza"
__author__ = "Gie"
__email__ = "593443714@qq.com"
__version__ = "2.0.0"

from iaar_tools.iaarLog import iaarLoguru
from iaar_tools.inner_ip import get_inner_ip

inner_ip = get_inner_ip()

# PRODUCTION_ENV_TAG = '10.90'
# # 不是以10.90开头的，认为是非生产环境
# if inner_ip.startswith(PRODUCTION_ENV_TAG):
#     iaar_log = iaarLoguru(deep=2, log_file='/data/logs/crawler/crawler.log.es')
# else:
#     iaar_log = iaarLoguru()
#     inner_ip = "127.0.0.1"
