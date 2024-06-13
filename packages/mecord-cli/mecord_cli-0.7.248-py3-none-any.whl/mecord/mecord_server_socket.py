import os, time, json
from urllib.parse import *
import threading
from datetime import datetime, timedelta
import calendar
from threading import Thread, current_thread, Lock
import websocket
import uuid
import queue
import subprocess, platform

from mecord import store
from mecord import xy_pb
from mecord import task
from mecord import constant 
from mecord import utils
from mecord import taskUtils
import mecord.pb.tarsproxy_pb2 as tarsproxy_pb2

thisFileDir = os.path.dirname(os.path.abspath(__file__))
waitlastTask = os.path.join(thisFileDir, f"waitlastTask")
stop_thread_file = os.path.join(thisFileDir, "stop.thread")
refreshMessage = os.path.join(thisFileDir, "refreshMessage")
country_dict = {"test": False, "sg": False, "us": False}
def can_use_longconnect():
    def getCommandResult(cmd):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        except subprocess.CalledProcessError as e:
            print(f"getCommandResult fail {e}")
        return ""
    if platform.system() == 'Windows':
        return True
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        return len(getCommandResult("which at")) > 0 and len(getCommandResult("which atd")) > 0

class MecordTaskExecutorThread(Thread):
    THEADING_LIST = []
    max_counter = 1
    cur_counter = 0
    is_running = False
    task_queue = None
    ttt = 0
    
    def appendTask(self, data, timeout, country, callback):
        self.cur_counter+=1
        self.task_queue.put([data, timeout, country, callback])
        try:
            taskUUID = data["taskUUID"]
            taskUtils.taskPrint(taskUUID, f"{current_thread().name} === addQueue {country} task : {taskUUID}")
        except:
            pass
            
    def idlePower(self):
        return self.max_counter - self.cur_counter
    
    def isWorking(self):
        return self.cur_counter > 0
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = f"MecordTaskExecutorThread"
        self.task_queue = queue.Queue()
        self.max_counter = store.get_multithread()
        self.is_running = True
        self.THEADING_LIST = []
        self.start()

    def taskRunning(self):
        while self.is_running or not self.task_queue.empty():
            try:
                data, timeout, country, callback = self.task_queue.get()
                if data is None: 
                    break
                taskUUID = data["taskUUID"]
                try:
                    name = json.loads(data['config'])['name']
                except:
                    name = ''
                try:
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name} === receive {country} task : {taskUUID}")
                    _appendTask(taskUUID, country, name)
                    is_ok, msg, result = task.runTask(data, timeout, country)
                    if is_ok == False:
                        taskUtils.notifyTaskFail(taskUUID, country, msg)
                    self.cur_counter-=1
                    callback(taskUUID, is_ok, msg, result)
                    _removeTask(taskUUID)
                except Exception as e:
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name} === {country} task exception : {e}")
                    taskUtils.notifyScriptError(taskUUID, country)
                finally:
                    taskUtils.taskPrint(taskUUID, None)
                self.task_queue.task_done()
            except Exception as ex:
                taskUtils.taskPrint(None, f"{current_thread().name} === exception : {ex}")
                pass
        lock.acquire()
        if os.path.exists(waitlastTask):
            os.remove(waitlastTask)
        lock.release()
        print(f"   {current_thread().name} taskRunning stop")

    def run(self):
        idx = 1
        for _ in range(0, self.max_counter):
            self.THEADING_LIST.append(Thread(name=f"exector-{idx}",target=self.taskRunning))
            idx+=1
        for t in self.THEADING_LIST:
            t.start()
        while self.is_running:
            time.sleep(5)
        for t in self.THEADING_LIST:
            t.join()
        print(f"   {self.name} stop!")

    def markStop(self):
        self.is_running = False
        print(f"   {self.name} waiting stop")
        for _ in range(self.max_counter*2):
            self.task_queue.put([None, -1, None, None])
        print(f"   {self.name} stop")

class MecordLongConnectThread(Thread):
    
    def get_url(self):
        return {
            "test": "wss://mecord-beta.2tianxin.com/proxymsg/ws",
            "us": "wss://api.mecordai.com/proxymsg/ws",
            "sg": "wss://api-sg-gl.mecordai.com/proxymsg/ws" 
        }[self.service_country]
    ws = None
    extend_config = {}
    token = ""
    device_id = ""
    service_country = "test"
    THEADING_LIST = []
    is_running = False
    last_get_task_begin = 0
    last_get_task_end = 0
    reconnect_cnt = 0
    executor: MecordTaskExecutorThread = None
    
    def taskCallback(self, taskUUID, is_ok, msg, result):
        self.TaskNotify(taskUUID, is_ok, msg, result)
        
    def receive_unknow_func(self, body):
        pass
    def receive_GetTask(self, body):
        self.last_get_task_end = calendar.timegm(time.gmtime())
        rsp = xy_pb.aigc_ext_pb2.GetTaskRes()
        rsp.ParseFromString(body)
        for it in rsp.list:
            self.executor.appendTask({
                "taskUUID": it.taskUUID,
                "pending_count": rsp.count - rsp.limit,
                "config": it.config,
                "data": it.data,
            }, rsp.timeout, self.service_country, self.taskCallback)
        if len(rsp.list) > 0:
            for _country in country_dict:
                if self.service_country == _country:
                    continue
                else:
                    country_dict[_country] = True
            if self.executor.idlePower() > 0:
                self.GetTask()
    def receive_TaskNotify(self, body):
        rsp = xy_pb.aigc_ext_pb2.TaskNotifyRes()
        rsp.ParseFromString(body)
        if rsp.ok and len(rsp.notify_id) > 0:
            xy_pb.resetLastTaskNotify(rsp.task_uuid)
            taskUtils.taskPrint(rsp.task_uuid, f"{current_thread().name}=== task : {rsp.task_uuid} notify server success")
        else:
            taskUtils.taskPrint(rsp.task_uuid, f"{current_thread().name}=== task : {rsp.task_uuid} server fail~~ rsp={rsp}")
    def receive_TaskInfo(self, body):
        rsp = xy_pb.aigc_ext_pb2.TaskInfoRes()
        rsp.ParseFromString(body)

    def on_message(self, ws, message):
        try:
            msg = tarsproxy_pb2.Message()
            msg.ParseFromString(message)
            cases = {
                "mecord.aigc.AigcExtObj_GetTask": self.receive_GetTask,
                "mecord.aigc.AigcExtObj_TaskNotify": self.receive_TaskNotify,
                "mecord.aigc.AigcExtObj_TaskInfo": self.receive_TaskInfo,
            }
            return cases.get(f"{msg.obj}_{msg.func}", self.receive_unknow_func)(msg.body)
        except Exception as ex:
            pass
    def on_error(self, ws, error):
        print(f"Connection on_error (error: {error})")
        if "Connection to remote host was lost" in str(error):
            print(f"close socket & sleep(5)")
            self.socket_close()
            time.sleep(5)
        if self.is_running:
            self.reconnect()
        pass
    def on_close(self, ws, status_code, close_msg):
        print(f"Connection closed (status code: {status_code}, message: {close_msg})")
        time.sleep(5)
        if self.is_running:
            self.reconnect()
    def on_ping(self, ws, message):
        print(f"on_ping... {message}")
    def on_pong(self, ws, message):
        print(f"on_pong... {message}")
    def on_open(self, ws):
        self.reconnect_cnt=0
        self.GetTask()

    def __init__(self, country, executor):
        threading.Thread.__init__(self)
        self.name = f"MecordLongConnectThread-{country}"
        extInfo = store.readDeviceInfo()
        extInfo["app_version"] = constant.app_version
        extInfo["app_bulld_number"] = constant.app_bulld_number
        extInfo["app_name"] = constant.app_name
        extInfo["dts"] = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        extInfo["trace_id"] = ''.join(str(uuid.uuid4()).split('-'))
        extInfo["host_name"] = utils.get_hostname()
        self.extend_config = json.dumps(extInfo)
        self.token = xy_pb.real_token(country)
        self.device_id = utils.generate_unique_id()
        self.service_country = country
        self.executor = executor
        self.is_running = True
        self.THEADING_LIST = []
        self.last_get_task_begin = 0
        self.last_get_task_end = 0
        self.reconnect_cnt = 0
        self.socket_init()
        self.start()

    def socket_init(self):
        self.ws = websocket.WebSocketApp(self.get_url(),
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_ping=self.on_ping,
                                    on_pong=self.on_pong,
                                    header={
                                        f'deviceid:{self.device_id}'
                                    })
        self.ws.on_open = self.on_open
    def socket_start(self):
        if self.ws:
            self.ws.run_forever()
    def reconnect(self):
        print(f"{current_thread().name} === reconnect {self.reconnect_cnt}/60...")
        if self.reconnect_cnt > 60:
            print(f"{current_thread().name} === 无法连接上服务器，重启")
            self.is_running = False
            utils.begin_restart(f"the number of reconnect to {self.service_country} is more than 60 times") #reconnect
        else:
            self.reconnect_cnt+=1
            self.socket_close()
            self.socket_init()
    def send_byte(self, b):
        try:
            if self.ws:
                self.ws.send_bytes(b)
        except:
            pass
    def socket_close(self):
        if self.ws:           
            self.ws.close()
        self.ws = None

    def socket_bypass(self):
        last_heart_pts = calendar.timegm(time.gmtime())
        last_check_service_work_status_pts = calendar.timegm(time.gmtime())
        now = datetime.now()
        next_day = now.replace(hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)
        while self.is_running:
            if os.path.exists(refreshMessage):  # enable/disable后 告知服务器最新的widget
                self.GetTask()
                lock.acquire()
                if os.path.exists(refreshMessage):
                    os.remove(refreshMessage)
                lock.release()
            elif country_dict[self.service_country]:  # 接收到任务后，告知其他服务器最新的limit
                self.GetTask()
                country_dict[self.service_country] = False
            else:
                cur_pts = calendar.timegm(time.gmtime())
                if cur_pts - last_heart_pts > 10:
                    self.send_byte(self._pb_pack("", None))
                    # if 3 == random.randint(0, 5):
                    print(f"{current_thread().name}-{self.service_country} === heartbeat")
                    if self.service_country != "test":
                        #Previous tasks may have failed due to network problems, so collect and resend
                        xy_pb.retryLastTaskNotify()
                    last_heart_pts = cur_pts
                if cur_pts - last_check_service_work_status_pts > 120 and self.executor.isWorking() == False:
                    if abs(self.last_get_task_end - self.last_get_task_begin) > 180:
                        #from wuyongcong@xinyu668.com ,may be server is disconnect but client dont know
                        print(f"{current_thread().name}-{self.service_country} === 重启")
                        self.is_running = False
                        utils.begin_restart(f"did not connect to {self.service_country}") #reconnect
                    if cur_pts - self.last_get_task_end > 60:
                        #request once this device status
                        self.GetTask()
                        print(f"{current_thread().name}-{self.service_country} === trigger timeout getTask!")
                    last_check_service_work_status_pts = cur_pts
                if (datetime.now() - next_day).total_seconds() > 0:
                    taskUtils.notifyCounterIfNeed(self.service_country)
                    next_day += timedelta(days=1)
                    print(f'{current_thread().name}-{self.service_country} === publish daily report')
            time.sleep(3)
        print(f"   {current_thread().name}-{self.service_country} heartbeat stop")

    def _pb_pack(self, func, req):
        opt = {
            "lang": "zh-Hans",
            "region": "CN",
            "appid": "80",
            "application": "mecord",
            "version": "1.0",
            "X-Token": self.token,
            "uid": "1",
        }
        input_req = xy_pb.rpcinput_pb2.RPCInput(obj="mecord.aigc.AigcExtObj", func=func, req=(req.SerializeToString() if req else None), opt=opt)
        return input_req.SerializeToString()
    def GetTask(self):
        if not os.path.exists(stop_thread_file):
            req = xy_pb.aigc_ext_pb2.GetTaskReq()
            req.limit = self.executor.idlePower()
            print(f"=============== gettask {req.limit}")
            if req.limit <= 0:
                req.limit = 0  # 小于或等于则置为0，告知服务器不接任务
            req.version = xy_pb.constant.app_version
            req.DeviceKey = self.device_id
            map = store.widgetMap()
            for it in map:
                if isinstance(map[it], (dict)):
                    if map[it]["isBlock"] == False:
                        req.widgets.append(it)
                else:
                    req.widgets.append(it)
            if len(req.widgets) == 0:  # disable all 的时候则不接任务
                req.widgets.append('No_widgets') # 如果是空[],仍然会接到任务,所以给一个不存在的widget
                req.limit = 0
            req.token = self.token
            req.extend = self.extend_config
            req.apply = True
            self.last_get_task_begin = calendar.timegm(time.gmtime())
            print(f"{current_thread().name} waiting next {req.limit} task")
            self.send_byte(self._pb_pack("GetTask", req))
    def TaskInfo(self, taskUUID):
        req = xy_pb.aigc_ext_pb2.TaskInfoReq()
        req.taskUUID = taskUUID
        req.findTaskResult = True
        self.send_byte(self._pb_pack("TaskInfo", req))
    def TaskNotify(self, taskUUID, status, msg, dataStr):
        req = xy_pb.aigc_ext_pb2.TaskNotifyReq()
        req.version = constant.app_version
        req.taskUUID = taskUUID
        if status:
            req.taskStatus = xy_pb.common_ext_pb2.TaskStatus.TS_Success
        else:
            req.taskStatus = xy_pb.common_ext_pb2.TaskStatus.TS_Failure
        req.failReason = msg
        req.data = dataStr
        req.extend = self.extend_config
        xy_pb.saveTaskNotifyData(self.service_country, taskUUID, status, msg, dataStr)
        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== notify {self.service_country} task : {taskUUID}")
        self.send_byte(self._pb_pack("TaskNotify", req))
        for i in country_dict:
            country_dict[i] = True

    def run(self):
        self.THEADING_LIST.append(Thread(target=self.socket_bypass))
        for t in self.THEADING_LIST:
            t.start()
        while self.is_running:
            self.socket_start()
            print(f"   {self.name} socket stop")
            time.sleep(1)

    def markStop(self):
        self.is_running = False
        print(f"   {self.name} waiting stop")
        for t in self.THEADING_LIST:
            t.join()
        while os.path.exists(waitlastTask):
            time.sleep(1)
        if self.service_country != "test":
            xy_pb.retryLastTaskNotify()
        if self.ws:
            self.ws.close()
            self.ws = None
        print(f"   {self.name} stop")

lock = Lock()
task_config_file = os.path.join(thisFileDir, f"task_config.txt")
def _readTaskConfig():
    if os.path.exists(task_config_file) == False:
        with open(task_config_file, 'w') as f:
            json.dump({
                "last_task_pts": 0
            }, f)
    with open(task_config_file, 'r') as f:
        data = json.load(f)
    return data
def _saveTaskConfig(data):
    with open(task_config_file, 'w') as f:
        json.dump(data, f)
def _appendTask(taskUUID, country, name):
    lock.acquire()
    task_config = _readTaskConfig()
    task_config[taskUUID] = {
        "country": country,
        "pts": calendar.timegm(time.gmtime()),
        "name": name
    }
    task_config["last_task_pts"] = task_config[taskUUID]["pts"]
    _saveTaskConfig(task_config)
    lock.release() 
def _clearTask():
    lock.acquire()
    task_config = {
        "last_task_pts": 0
    }
    _saveTaskConfig(task_config)
    lock.release() 
def _removeTask(taskUUID):
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        del task_config[taskUUID]
    _saveTaskConfig(task_config)
    lock.release() 
def _taskCreateTime(taskUUID):
    pts = 0
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        pts = task_config[taskUUID]["pts"]
    lock.release()
    return pts 
def _getTaskConfig():
    lock.acquire()
    task_config = _readTaskConfig()
    lock.release() 
    return task_config

class MecordShortConnectThread(Thread):
    is_running = False
    service_country = "sg"
    executor: MecordTaskExecutorThread = None

    def __init__(self, country, executor):
        super().__init__()
        self.name = f"MecordShortConnectThread-{country}"
        self.is_running = True
        self.service_country = country
        self.executor = executor
        self.start()
    
    def taskCallback(self, taskUUID, is_ok, msg, result):
        xy_pb.TaskNotify(self.service_country, taskUUID, is_ok, msg, result)

    def run(self):
        print(f"   {self.name} start")
        what_time = 2 if self.service_country != "sg" else 5
        while (self.is_running):
            try:
                datas, timeout = xy_pb.GetTask(self.service_country)
                for it in datas:
                    self.executor.appendTask(it, timeout, self.service_country, self.taskCallback)
            except Exception as ex:
                taskUtils.taskPrint(None, f"{self.name} === exception : {ex}")
            time.sleep(what_time)
        print(f"   {self.name} stop")

    def markStop(self):
        print(f"   {self.name} waiting stop")
        self.is_running = False