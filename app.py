import sys
import grpc
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import QThread, QTimer, Signal, Slot
from PySide6.QtGui import QIcon

from QuickChatUI import Ui_QuickChat
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

    def __init__(self, port, name, parent=None):
        super(QuickChatServerThread, self).__init__(parent)
        self.port = port
        self.server = None
        self.ip = get_ip_addresses().get('Tailscale')
        self.name = name

    def run(self):
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_QuickChatServiceServicer_to_server(QuickChatServer(self), self.server)
        self.server.add_insecure_port(f'0.0.0.0:{self.port}')
        self.server.start()
        print(f"Server started on port {self.port}")
        print(f"Host ip: (Tailscale){self.ip}")
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

    def __init__(self, name, port):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"QuickChat - {name}")
        self.setWindowIcon(QIcon('resource/icon.ico'))

        self.serverThread = QuickChatServerThread(port=port, name=name)
        self.serverThread.start()

        self.ip = get_ip_addresses().get('Tailscale')
        self.port = port
        self.name = name
        self.members = {}
        self.stubs = {}
        self.inviter = None
        self.local_idx = None
        self.vclock = None
        self.message_queue = []
        self.db = SQLiteDatabase('data/chat.db')
        self.chat_id = None

        self.timer = QTimer(self)
        self.timer.setInterval(0)

        """ 信号函数绑定"""
        self.sendButton.clicked.connect(self.send_message)
        self.inviteButton.clicked.connect(self.invite)
        self.chatCreatedSignal.connect(self.chat_created)
        self.serverThread.chatJoinSignal.connect(self.chat_join)
        self.serverThread.chatInvitedSignal.connect(self.chat_invited)
        self.serverThread.messageReceiveSignal.connect(self.receive_message)
        self.timer.timeout.connect(self.check_message_queue)

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
        self.inviteBox.hide()
        self.inviteButton.hide()
        self.label_2.hide()

        """ 初始化向量时钟 """
        for i, name in enumerate(sorted(self.members)):
            if self.members[name] == f'{self.ip}:{self.port}':
                self.local_idx = i
                break
        self.vclock = VectorClock(self.local_idx, self.members)
        self.timer.start()

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

        self.inviteBox.clear()
        for name in sorted(members):
            self.memberBox.append(f"{name}({members[name]})")
        self.inviteBox.hide()
        self.inviteButton.hide()
        self.label_2.hide()

        """ 初始化向量时钟 """
        for i, name in enumerate(sorted(self.members)):
            if self.members[name] == f'{self.ip}:{self.port}':
                self.local_idx = i
                break
        self.vclock = VectorClock(self.local_idx, self.members)
        self.timer.start()

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
            request = service_pb2.ChatMessageRequest(sender_ip=f'{self.ip}:{self.port}',
                                                     message=message, vclock=message_vector)
            self.stubs[name].SendChatMessage(request)
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


def main():
    """
    程序入口
    :return:
    """
    app = QApplication(sys.argv)
    if len(sys.argv) > 2:
        name = str(sys.argv[1])
        port = int(sys.argv[2])
        app_ui = QuickChat(name, port)
        app_ui.show()
        sys.exit(app.exec())
    else:
        print("Missing argument")


if __name__ == '__main__':
    main()
