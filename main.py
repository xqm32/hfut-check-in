import argparse
import os
import sys
import json

from utils import HFUTer, log

if __name__ == "__main__":

    if os.path.exists('config.json'):
        with open('config.json', encoding="UTF-8_SIG") as f:
            env_dist = json.load(f)
    elif len(sys.argv) == 1:
        env_dist = os.environ
    else:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("username", type=str, help="Your student ID")
        arg_parser.add_argument("password", type=str,
                                help="Password for one.hfut.edu.cn")
        arg_parser.add_argument("address", type=str, help="Check in address")
        args = arg_parser.parse_args()
        env_dist = vars(args)

    stu = HFUTer(username=env_dist['username'], password=env_dist['password'])
    if (stu.daily_checkin(env_dist['address'])):
        log.info("签到成功")
    else:
        log.error("签到失败")
