import json
import schedule
import time
from send_request import *
from manager import Manager

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
            status = res['data']['userAuth']['reserve']['reserveSeat']
            if status is not None and status:
                print("预约成功")
                return
    print("预约失败")


def job():
    for s in manager.get_sessions():
        go(s)


def job_thread(threadName):
    schedule.every().day.at("06:02").do(job)
    while True:
        schedule.run_pending()
        time.sleep(5)
        for s in manager.get_sessions():
            need_often_send(s)


if __name__ == '__main__':
    read_json()
    if len(manager.get_sessions()) == 0:
        print("没有可用的session")
        exit()
    job_thread("job_thread")
