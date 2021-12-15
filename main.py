import os
from utils import hfuter

if __name__ == '__main__':
    env_dist = os.environ

    stu = hfuter(username=env_dist['username'], password=env_dist['password'])
    stu.daily_checkin(env_dist['address'])
