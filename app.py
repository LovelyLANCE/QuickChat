import sys
import grpc
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import QThread, QTimer, Signal, Slot
from PySide6.QtGui import QIcon, QFont, Qt

from QuickChatUI import Ui_QuickChat
from QuickChatSetupUI import Ui_QuickChatSetup
from QuickChatServer import QuickChatServer
import service_pb2
import service_pb2_grpc
from utils import get_ip_addresses, VectorClock, Message, get_chat_id
from database import SQLiteDatabase


class QuickChatServerThread(QThread):
    """
    QuickChat服务器线程
    """

    """ 信号 """
    chatInvitedSignal = Signal(str)
    chatJoinSignal = Signal(dict, str)
    messageReceiveSignal = Signal(str, str, list)
    memberQuitSignal = Signal(str)

    def __init__(self, ip, port, name, parent=None):
        super(QuickChatServerThread, self).__init__(parent)
        self.port = port
        self.server = None
        self.ip = ip
        self.name = name

    def run(self):
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_QuickChatServiceServicer_to_server(QuickChatServer(self), self.server)
        self.server.add_insecure_port(f'0.0.0.0:{self.port}')
        self.server.start()
        print(f"Server started on port {self.port}")
        self.server.wait_for_termination()

    def stop(self):
        if self.server:
            self.server.stop(0)


class QuickChat(QWidget, Ui_QuickChat):
    """
    QuickChat应用程序
    """

    """ 信号 """
    chatCreatedSignal = Signal(str)

    def __init__(self, name, ip, port):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"QuickChat - {name}({ip}:{port})")
        self.setWindowIcon(QIcon("resource/icon.ico"))
        self.stackedWidget.setCurrentIndex(0)

        self.serverThread = QuickChatServerThread(port=port, name=name, ip=ip)
        self.serverThread.start()

        self.ip = ip
        self.port = port
        self.name = name
        self.members = {}
        self.status = {}
        self.stubs = {}
        self.inviter = None
        self.local_idx = None
        self.vclock = None
        self.message_queue = []
        self.db = SQLiteDatabase('data/chat.db')
        self.chat_id = None

        self.message_timer = QTimer(self)
        self.message_timer.setInterval(0)
        self.detect_timer = QTimer(self)
        self.detect_timer.setInterval(3000)

        """ 信号函数绑定"""
        self.sendButton.clicked.connect(self.send_message)
        self.inviteButton.clicked.connect(self.invite)
        self.loadButton.clicked.connect(self.load_chat_history)
        self.quitButton.clicked.connect(self.quit)
        self.chatCreatedSignal.connect(self.chat_created)
        self.serverThread.chatJoinSignal.connect(self.chat_join)
        self.serverThread.chatInvitedSignal.connect(self.chat_invited)
        self.serverThread.messageReceiveSignal.connect(self.receive_message)
        self.serverThread.memberQuitSignal.connect(self.member_quit)
        self.message_timer.timeout.connect(self.check_message_queue)
        self.detect_timer.timeout.connect(self.detect_members_status)

    """ 槽与事件 """

    @Slot()
    def invite(self):
        """
        邀请用户加入聊天
        :return:
        """
        self.inviter = f'{self.ip}:{self.port}'
        addresses = self.inviteBox.toPlainText()
        addresses = addresses.split('\n')
        addresses = [address for address in addresses if address.strip()]
        self.members[self.name] = f"{self.ip}:{self.port}"
        for address in addresses:
            channel = grpc.insecure_channel(address)
            stub = service_pb2_grpc.QuickChatServiceStub(channel)
            request = service_pb2.ChatInviteRequest(inviter_ip=f"{self.ip}:{self.port}")
            response = stub.SendChatInvite(request)
            if response.accepted:
                self.members[response.name] = address
                self.stubs[response.name] = stub
                self.status[response.name] = True

        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp)
        for name in self.members.keys():
            if name == self.name:
                continue
            request = service_pb2.ChatMemberInfoRequest(members=self.members, timestamp=timestamp)
            self.stubs[name].SendChatMemberInfo(request)

        self.chatCreatedSignal.emit(timestamp)

    @Slot(str)
    def chat_created(self, timestamp):
        """
        聊天成功创建
        :return:
        """
        self.inviteBox.clear()
        for name in sorted(self.members):
            self.memberBox.append(f"{name}({self.members[name]})")

        self.stackedWidget.setCurrentIndex(1)

        """ 初始化向量时钟 """
        for i, name in enumerate(sorted(self.members)):
            if self.members[name] == f'{self.ip}:{self.port}':
                self.local_idx = i
                break
        self.vclock = VectorClock(self.local_idx, self.members)
        self.message_timer.start()
        self.detect_timer.start()

        """ 在数据库中初始化本次聊天信息 """
        identifier = get_chat_id(self.members)
        self.chat_id = self.db.create_chat(identifier, timestamp)

        QMessageBox.information(self, "消息", "聊天创建成功！")

    @Slot(str)
    def chat_invited(self, inviter):
        """
        登记聊天创建者信息
        :param inviter:
        :return:
        """
        self.inviter = inviter

    @Slot(dict, str)
    def chat_join(self, members, timestamp):
        """
        成功加入某个聊天室
        :return:
        """
        self.members = members
        for name, address in self.members.items():
            if name == self.name:
                continue
            channel = grpc.insecure_channel(address)
            stub = service_pb2_grpc.QuickChatServiceStub(channel)
            self.stubs[name] = stub
            self.status[name] = True

        self.inviteBox.clear()
        for name in sorted(members):
            self.memberBox.append(f"{name}({members[name]})")

        self.stackedWidget.setCurrentIndex(1)

        """ 初始化向量时钟 """
        for i, name in enumerate(sorted(self.members)):
            if self.members[name] == f'{self.ip}:{self.port}':
                self.local_idx = i
                break
        self.vclock = VectorClock(self.local_idx, self.members)
        self.message_timer.start()
        self.detect_timer.start()

        """ 在数据库中初始化本次聊天信息 """
        identifier = get_chat_id(self.members)
        self.chat_id = self.db.create_chat(identifier, timestamp)

        QMessageBox.information(self, "消息", f"您已加入由{self.inviter}创建的聊天！")

    @Slot()
    def send_message(self):
        """
        发送信息至聊天室
        :return:
        """
        message = self.editBox.toPlainText()
        message_vector = self.vclock.local_event()
        for name in self.stubs.keys():
            if not self.status[name]:
                continue
            request = service_pb2.ChatMessageRequest(sender_ip=f'{self.ip}:{self.port}',
                                                     message=message, vclock=message_vector)
            try:
                # 加入超时检测避免阻塞
                response = self.stubs[name].SendChatMessage(request, timeout=1)
            except grpc.RpcError as e:
                pass

        msg = Message(self.local_idx, message, message_vector)
        self.message_queue.append(msg)
        print(msg.message)
        self.editBox.clear()

    @Slot(str, str, list)
    def receive_message(self, sender_ip, message, vclock):
        """
        接收其他用户发来的消息
        :return:
        """
        sender_idx = None
        for i, name in enumerate(sorted(self.members)):
            if self.members[name] == sender_ip:
                sender_idx = i
                break
        msg = Message(sender_idx, message, vclock)
        print(msg.message)
        self.message_queue.append(msg)

    @Slot()
    def check_message_queue(self):
        """
        定期检查消息队列，根据向量时钟判断当前可接受的消息
        :return:
        """
        if self.message_queue is not None:
            for i in range(len(self.message_queue) - 1, -1, -1):
                if self.message_queue[i].sender_idx == self.local_idx or \
                        self.vclock.external_event(self.message_queue[i].sender_idx, self.message_queue[i].vclock):
                    name = sorted(self.members.keys())[self.message_queue[i].sender_idx]
                    self.db.save_message(self.chat_id, name, self.members[name], self.message_queue[i].message)
                    if name == self.name:
                        name = '我'
                    self.messageBox.append(f'{name} : {self.message_queue[i].message}')
                    print(self.vclock.vector)
                    del self.message_queue[i]

    @Slot()
    def load_chat_history(self):
        """
        加载历史聊天记录
        :return:
        """
        identifier = get_chat_id(self.members)
        history_chats = self.db.load_chat_history(identifier)
        self.messageBox.append("")
        self.messageBox.append(f"<span style='color: gray;'>--------------------历史聊天记录--------------------</span>")
        for chat in history_chats:
            self.messageBox.append(f"<span style='color: gray;'>-----{chat['time']}-----</span>")
            chat = sorted(chat['content'], key=lambda x: x[0])
            for message in chat:
                self.messageBox.append(f"<span style='color: gray;'>{message[1]}({message[2]}) : {message[3]}</span>")
            self.messageBox.append("")

    @Slot(str)
    def member_quit(self, sender_ip):
        """
        接受并处理其他成员的退出聊天请求
        :return:
        """
        for name in self.stubs.keys():
            if self.members[name] == sender_ip:
                self.status[name] = False
                text = f"系统消息 : {name}({sender_ip})已退出聊天"
                message = f"<span style='color: red;'>{text}</span>"
                self.messageBox.append(message)
                break

    @Slot()
    def detect_members_status(self):
        """
        定期检查其他成员的在线情况
        :return:
        """
        for name in self.stubs.keys():
            if self.status[name]:
                print(self.status)
                request = service_pb2.ChatDetectRequest(detect=True)
                try:
                    # 超时检测
                    self.stubs[name].SendChatDetect(request, timeout=3)
                except grpc.RpcError as e:
                    self.status[name] = False
                    for n in self.stubs.keys():
                        if self.status[n]:
                            try:
                                request = service_pb2.ChatQuitRequest(sender_ip=self.members[name])
                                self.stubs[n].SendChatQuit(request, timeout=3)
                            except grpc.RpcError as e:
                                print(e)

    @Slot()
    def quit(self):
        """
        退出聊天
        :return:
        """
        for name in self.stubs.keys():
            if self.status[name]:
                request = service_pb2.ChatQuitRequest(sender_ip=f'{self.ip}:{self.port}')
                try:
                    # 超时检测
                    self.stubs[name].SendChatQuit(request, timeout=1)
                except grpc.RpcError as e:
                    pass
        self.close()

    def closeEvent(self, event):
        """
        关闭程序
        :param event:
        :return:
        """
        self.serverThread.stop()
        self.serverThread.quit()
        self.serverThread.wait()
        super().closeEvent(event)


class QuickChatSetup(QWidget, Ui_QuickChatSetup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("resource/icon.ico"))
        self.chatWindow = None

        self.ip_addresses = get_ip_addresses()
        adapters = self.ip_addresses.keys()
        for adapter in adapters:
            self.adapterBox.addItem(adapter)
        font = QFont()
        font.setPointSize(9)
        for index in range(self.adapterBox.count()):
            self.adapterBox.setItemData(index, font, Qt.FontRole)
        self.adapterBox.setFont(font)
        self.nameBox.setFont(font)
        self.portBox.setFont(font)

        self.setupButton.clicked.connect(self.setup)

    @Slot()
    def setup(self):
        """
        根据选择的适配器何端口启动QuickChat
        :return:
        """
        name = self.nameBox.text()
        adapter = self.adapterBox.currentText()
        port = self.portBox.text()
        ip = self.ip_addresses[adapter]
        self.close()
        self.chatWindow = QuickChat(name, ip, port)
        self.chatWindow.show()


def main():
    """
    程序入口
    :return:
    """
    app = QApplication()
    setup = QuickChatSetup()
    setup.show()
    app.exec()


if __name__ == '__main__':
    main()
