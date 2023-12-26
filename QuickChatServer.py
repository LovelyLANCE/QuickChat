import service_pb2
import service_pb2_grpc


class QuickChatServer(service_pb2_grpc.QuickChatServiceServicer):
    def __init__(self, thread):
        """
        初始化
        :param message_signal_emitter:
        """
        self.name = thread.name
        self.thread = thread

    def SendChatInvite(self, request, context):
        """
        发送聊天邀请
        :param request:
        :param context:
        :return:
        """
        self.thread.chatInvitedSignal.emit(request.inviter_ip)
        return service_pb2.ChatInviteResponse(accepted=True, name=self.name)

    def SendChatMemberInfo(self, request, context):
        """
        发送聊天成员信息
        :param request:
        :param context:
        :return:
        """
        members_dict = {k: v for k, v in request.members.items()}
        timestamp = request.timestamp
        self.thread.chatJoinSignal.emit(members_dict, timestamp)
        return service_pb2.ChatMemberInfoResponse(confirmed=True)

    def SendChatMessage(self, request, context):
        """
        发送聊天消息
        :param request:
        :param context:
        :return:
        """
        sender_ip = request.sender_ip
        message = request.message
        message_clock = request.vclock
        self.thread.messageReceiveSignal.emit(sender_ip, message, message_clock)
        return service_pb2.ChatMessageResponse(success=True)

    def SendChatQuit(self, request, context):
        """
        接收其他聊天者的退出消息
        :param request:
        :param context:
        :return:
        """
        sender_ip = request.sender_ip
        self.thread.memberQuitSignal.emit(sender_ip)
        return service_pb2.ChatQuitResponse(confirmed=True)

    def SendChatDetect(self, request, context):
        """
        发送探测其他成员在线情况的请求
        :param request:
        :param context:
        :return:
        """
        return service_pb2.ChatDetectResponse(confirmed=True)
