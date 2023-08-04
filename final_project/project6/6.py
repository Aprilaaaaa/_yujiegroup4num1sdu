import hashlib
import json


class MerkleTree:
    def __init__(self, data):
        self.data = data
        self.tree = self.build_tree(data)

    @staticmethod
    def hash_fn(data):
        sha256 = hashlib.sha256()
        sha256.update(data.encode('utf-8'))
        return sha256.hexdigest()

    def build_tree(self, data_list):
        if len(data_list) == 1:
            return data_list[0]

        next_level = []
        for i in range(0, len(data_list), 2):
            hash_left = self.hash_fn(data_list[i])
            if i + 1 < len(data_list):
                hash_right = self.hash_fn(data_list[i + 1])
                next_level.append(self.hash_fn(hash_left + hash_right))
            else:
                next_level.append(hash_left)

        if len(next_level) == 1:
            return next_level[0]
        else:
            return self.build_tree(next_level)

    def get_root(self):
        return self.tree

    def verify(self, data, root_hash):
        return self.tree == root_hash and data in self.data


if __name__ == '__main__':
    data = ['block1', 'block2', 'block3', 'block4']
    merkle_tree = MerkleTree(data)

    root_hash = merkle_tree.get_root()
    print(f"Root Hash: {root_hash}")

    tampered_data = 'block5'
    print(f"Is Tampered Data Valid?: {merkle_tree.verify(tampered_data, root_hash)}")

    valid_data = 'block2'
    print(f"Is Valid Data Valid?: {merkle_tree.verify(valid_data, root_hash)}")
