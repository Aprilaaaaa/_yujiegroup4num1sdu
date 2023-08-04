import hashlib
import json
import socket
from typing import List, Dict


class MerkleTree:
    def __init__(self, data: List[str]):
        self.data = data
        self.tree = self._build_tree(self.data)

    @staticmethod
    def hash_fn(data: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(data.encode('utf-8'))
        return sha256.hexdigest()

    def _build_tree(self, data_list: List[str]) -> str:
        if len(data_list) == 1:
            return data_list[0]

        next_level = []
        for i in range(0, len(data_list), 2):
            if i + 1 < len(data_list):
                next_level.append(self.hash_fn(data_list[i] + data_list[i + 1]))
            else:
                next_level.append(self.hash_fn(data_list[i]))

        return self._build_tree(next_level)

    def get_root(self) -> str:
        return self.tree

    def verify(self, data: str, root_hash: str) -> bool:
        return self.tree == root_hash


def send_data(data: List[str], root_hash: str, receiver_address: str, receiver_port: int) -> None:
    data_to_send = {
        'data': data,
        'root_hash': root_hash
    }
    data_json = json.dumps(data_to_send).encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((receiver_address, receiver_port))
        client_socket.sendall(data_json)


def process_received_data(received_data: Dict[str, str], root_hash: str) -> None:
    data = received_data['data']

    merkle_tree = MerkleTree(data)
    is_valid = merkle_tree.verify(data, root_hash)

    if is_valid:
        print("Data is valid. Accepting the received data.")
        # 执行接收到的数据的相应操作
    else:
        print("Data is invalid. Rejecting the received data.")


def receive_data(sender_port: int, root_hash: str) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', sender_port))
            server_socket.listen(1)

            while True:
                conn, addr = server_socket.accept()
                received_data = conn.recv(1024)

                if not received_data:
                    break

                data_to_verify = json.loads(received_data.decode('utf-8'))
                process_received_data(data_to_verify, root_hash)

    finally:
        conn.close()


# 示例用法
if __name__ == '__main__':
    data = ['block1', 'block2', 'block3', 'block4']
    merkle_tree = MerkleTree(data)
    root_hash = merkle_tree.get_root()
    print(f"Root Hash: {root_hash}")

    receiver_address = '127.0.0.1'  # 接收方的IP地址
    receiver_port = 8888  # 接收方的端口号
    send_data(data, root_hash, receiver_address, receiver_port)

    sender_port = 8888  # 发送方的监听端口
    receive_data(sender_port, root_hash)
