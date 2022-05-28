# encoding = utf-8
import requests
from query import *

url = "https://web.traceint.com/index.php/graphql/"


def get_session(wechat_sess_id: str, authorization: str) -> requests.Session:
    s = requests.Session()
    s.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                              "Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1326.400 QQBrowser/9.0.2524.400 " \
                              "Mozilla/5.0 (" \
                              "Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 " \
                              "Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(" \
                              "0x63010200) "
    s.cookies["wechatSessioId"] = wechat_sess_id
    s.cookies["Authorization"] = authorization
    # s.headers["wechatSESS_ID"] = wechat_sess_id
    # s.headers["Authorization"] = authorization
    return s


# to do
def get_idle_seats(s: requests.Session):
    data = {"operationName": "libLayout",
            "query": "query libLayout($libId: Int, $libType: Int) {\n userAuth {\n reserve {\n libs(libType: $libType, "
                     "libId: $libId) {\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n lib_layout {\n "
                     "seats_total\n seats_booking\n seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n type\n name\n "
                     "seat_status\n status\n }\n }\n }\n }\n }\n} ", "variables": {"libId": 23}}
    res = s.post(url=url, json=data)
    try:
        lib_layout = res.json()["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]
    except Exception as e:
        return None


def post_index(s: requests.Session) -> dict:
    data = {"operationName": "index", "variables": {"pos": "App-首页"},
            "query": index_query
            }
    res = s.post(url=url, json=data)
    # print(res)
    # print(res.headers)
    return res.json()


def need_often_send(s: requests.Session):
    data = {"operationName": "getUserCancleConfig",
            "query": often_send_query}
    s.post(url=url, json=data)


def book(s: requests.Session, seat_key: list) -> dict:
    # seat_key:[seat_key, lib_info]
    data = {"operationName": "reserveSeat",
            "query": book_query,
            "variables": {"seatKey": seat_key[0], "libId": seat_key[1], "captchaCode": "", "captcha": ""}}
    res = s.post(url=url, json=data)
    return res.json()
