import json
import schedule
import time
from send_request import *
from manager import Manager
import argparse

manager = Manager()


def read_json():
    with open("./configure.json", 'r') as f:
        configure = json.load(f)
        users = configure['users']
        for user in users:
            name = user['name']
            wechatSESS_ID = user['wechatSESS_ID']
            Authorization = user['Authorization']
            s = get_session(wechatSESS_ID, Authorization)
            res = post_index(s)
            if "errors" not in res.keys():
                manager.add_session(s)
                print(name + "添加session成功")


def go(s: requests.Session):
    res = post_index(s)
    often_seat = res['data']['userAuth']['oftenseat']["list"]
    often_seat_key = []
    for seat in often_seat:
        often_seat_key.append([seat['seat_key'], seat['lib_id']])
    for key in often_seat_key:
        for i in range(3):
            res = book(s, key)
            print(res)
            status = res['data']['userAuth']['reserve']['reserveSeat']
            if status is not None and status:
                print("预约成功")
                return
            time.sleep(10)
    print("预约失败")


def job():
    for s in manager.get_sessions():
        go(s)


def job_thread(threadName):
    schedule.every().day.at("06:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)
        for s in manager.get_sessions():
            post_index(s)
            need_often_send(s)
            # print(s.cookies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--run-once", type=bool, help="run once to test", default=False)
    read_json()
    if len(manager.get_sessions()) == 0:
        print("没有可用的session")
        exit()
    if not parser.parse_args().run_once:
        job_thread("job_thread")
    else:
        job()
