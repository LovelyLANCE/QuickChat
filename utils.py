import socket
import psutil
import hashlib


def get_ip_addresses():
    """
    获取本机ip
    :return:
    """
    host_ip_addresses = {}
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                host_ip_addresses[interface] = addr.address
    return host_ip_addresses


def get_chat_id(members_dict):
    """
    根据输入的用户信息生成一个对应的SHA-256哈希值，以十六进制字符串形式存储
    :param members_dict:
    :return:
    """
    input_string = ""
    for name in sorted(members_dict):
        input_string += name
        input_string += members_dict[name]
    return hashlib.sha256(input_string.encode()).hexdigest()


class Message:
    def __init__(self, sender_idx, message, vclock):
        self.sender_idx = sender_idx
        self.message = message
        self.vclock = vclock


class VectorClock:
    """
    向量时钟
    """
    def __init__(self, local_idx, members):
        """
        初始化向量时钟
        :param members:
        """
        self.local_idx = local_idx
        self.members = members
        self.vector = []
        for name in sorted(self.members):
            self.vector.append(0)
        print(self.local_idx)
        print(self.vector)

    def local_event(self):
        """
        本地事件时钟计数增加，返回增加后的时钟信息
        :return:
        """
        self.vector[self.local_idx] += 1
        return self.vector[:]

    def external_event(self, sender_idx, message_clock):
        """
        外部事件到来，比较消息附带时钟与本地时钟来决定当前是否接受该事件
        :return:
        """
        for i in range(len(message_clock)):
            if i == sender_idx:
                if message_clock[i] != self.vector[i] + 1:
                    return False
            else:
                if message_clock[i] > self.vector[i]:
                    return False

        for i in range(len(message_clock)):
            self.vector[i] = max(self.vector[i], message_clock[i])
        return True


if __name__ == '__main__':
    # 获取所有适配器的IP地址
    ip_addresses = get_ip_addresses()
    print("所有适配器的IP地址:", ip_addresses)

    eth0_ip = ip_addresses.get('Tailscale')
    if eth0_ip:
        print("Tailscale的IP地址:", eth0_ip)
    else:
        print("未找到Tailscale的IP地址")
