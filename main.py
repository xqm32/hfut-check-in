import argparse
import os

from utils import HFUTer, log

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("username", type=str, help="Your student ID")
    arg_parser.add_argument("password", type=str,
                            help="Password for one.hfut.edu.cn")
    arg_parser.add_argument("address", type=str, help="Check in address")
    args = arg_parser.parse_args()

    if args == []:
        env_dist = os.environ
    else:
        env_dist = vars(args)

    stu = HFUTer(username=env_dist['username'], password=env_dist['password'])
    if (stu.daily_checkin(env_dist['address'])):
        log.info("签到成功")
    else:
        log.error("签到失败")
