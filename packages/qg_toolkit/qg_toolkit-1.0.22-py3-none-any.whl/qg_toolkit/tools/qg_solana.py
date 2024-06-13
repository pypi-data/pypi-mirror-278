import base64
import concurrent
import struct
from threading import Lock

from solana.rpc.api import Client
from solana.rpc.commitment import Commitment
from solana.transaction import Transaction
from solders.instruction import AccountMeta, Instruction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from qg_toolkit.tools.qg_file import QGFile


class QGSolana:
    # rpc
    endpoints = {
        "mainnet": "https://mainnet.infura.io/v3/257c5f3bdfed414b88a4908b0f999377",
        "mainnet2": "https://api.mainnet-beta.solana.com",
        "mainnet3": "https://fittest-aged-flower.solana-mainnet.quiknode.pro/e4283fb4f6347e50cd39b47d6ddff250327b79c1/",
    }
    lock = Lock()

    def __init__(self, index, address=None, private_key=None, mnemonic=None):
        # 取破解参数
        # "\u0077"
        # JSON.stringify(e)
        self.index = index
        self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic
        if private_key:
            self.address = str(Keypair.from_base58_string(self.private_key).pubkey())
        self.client = Client(self.endpoints.get("mainnet3"))
        self.get_balance()

    def sign_msg(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        signature_encode = k.sign_message(msg.encode())
        return base64.b64encode(bytes(signature_encode)).decode('utf-8')

    def sign_msg_to_hex(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        sig = k.sign_message(msg.encode())
        return bytes(sig).hex()

    def sign_msg_backpack(self, msg):
        payload = self.prepare_offchain_message(msg)
        k = Keypair.from_base58_string(self.private_key)
        signature_encode = k.sign_message(payload)
        return base64.b64encode(bytes(signature_encode)).decode('utf-8')

    @classmethod
    def prepare_offchain_message(cls, message, encoding="UTF-8", max_length=1212):
        message_bytes = message.encode(encoding)
        if len(message_bytes) > max_length:
            raise ValueError(f"Max message length ({max_length}) exceeded!")

        # 构建消息负载
        payload = bytearray([255]) + b"solana offchain" + bytes([0]) + \
                  bytes([0 if encoding == "ASCII" else (1 if max_length == 1212 else 2)]) + \
                  len(message_bytes).to_bytes(2, byteorder='little') + message_bytes

        return bytes(payload)

    def sign_msg_hex(self, msg):
        k = Keypair.from_base58_string(self.private_key)
        signature = k.sign_message(msg.encode())
        return bytes(signature).hex()

    def get_balance(self, address=None):
        try:
            address = address if address else self.address
            value = self.client.get_balance(Pubkey.from_string(address)).value
            value = value / 10 ** 9
            print(f'【{address}】余额：{value}')
            return value
        except Exception as e:
            print(e)

    def transfer(self, to_address, to_value, is_check=False, check_balance=0.1):
        if is_check:
            if self.get_balance(to_address) >= check_balance:
                print(f'【{to_address}】余额充足，跳过！')
                return
        sender_keypair = Keypair.from_base58_string(self.private_key)  # 发送人私钥
        receiver = Pubkey.from_string(to_address)
        # transfer_ix = transfer(TransferParams(from_pubkey=sender_keypair.pubkey(), to_pubkey=receiver, lamports=100_000))#sol精度9
        # print(transfer_ix)
        program_id = Pubkey.from_string('11111111111111111111111111111111')
        # amount = int(0.01 * 10 ** 9)
        amount = int(to_value * 10 ** 9)
        amount_hex = struct.pack('<Q', amount).hex()
        data = '02000000' + amount_hex
        data_bytes = bytes.fromhex(data)
        ats = [
            AccountMeta(sender_keypair.pubkey(), True, True),
            AccountMeta(receiver, False, True)
        ]
        transfer_ix = Instruction(program_id, data_bytes, ats)
        txn = Transaction().add(transfer_ix)
        hash = self.client.send_transaction(txn, sender_keypair)
        print(f'【{self.address}】转账给【{to_address}】,开始转账hash: {hash.value}')
        res_json = self.client.confirm_transaction(hash.value, Commitment("confirmed")).to_json()
        print(f'【{self.address}】转账给【{to_address}】,hash: {hash.value},转账结果：{res_json}')

    def batch_transfer(self, to_address_list, to_value, is_check=False, check_balance=0.01):
        for to_address in to_address_list:
            self.transfer(to_address, to_value, is_check, check_balance)

    def to_pri(self):
        k = Keypair.from_base58_string(self.private_key)
        global arr
        arr.append(k.to_bytes_array())
        print(f'【{self.address}】: {k.to_bytes_array()}')

    @staticmethod
    def generate_wallet(num,filename='生成的Solana钱包.txt'):
        for i in range(num):
            keypair = Keypair()
            log = f'{keypair.pubkey()}----{keypair}----{keypair.to_bytes_array()}'
            print(log)
            QGFile.save_to_file(f'{filename}', log)


def qg_task(index, addr, pk, mn):
    qg = QGSolana(index=index, address=addr, private_key=pk)
    qg.batch_transfer(recept_accounts, 0.1, is_check=True, check_balance=0.01)



if __name__ == '__main__':
    arr = []
    accounts = QGFile.txt_to_array("../wallets/solana/qg-solana.txt")
    recept_accounts = [x[0] for x in QGFile.txt_to_array("../wallets/solana/qg_sol-100.txt")][0:9]
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    results = []
    for i, account in enumerate(accounts, start=1):
        addr1 = account[0]
        pk1 = ""
        mn1 = ""
        email1 = ""
        twitter_info1 = ""
        dis_info1 = ""
        if 1 <= i <= 1:
            result = executor.submit(qg_task, i, addr1, pk1, mn1)
            results.append(result)
    concurrent.futures.wait(results)
    executor.shutdown()
    for xx in arr:
        print(xx)
