import json
from abc import ABC, abstractmethod

class Revertable(ABC):
    @abstractmethod
    def snapshot(self):
        pass

    @abstractmethod
    def revert(self):
        pass

    @abstractmethod
    def commit(self):
        pass

class User:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

class AccountSnapshot:
    def __init__(self, balance: float):
        self.balance = balance

class Account(Revertable):
    def __init__(self, id, owner, balance=0.0):
        self.__id = id
        self.__owner = owner
        self.__balance = balance
        self.snap = None

    def get_id(self):
        return self.__id
    
    def get_owner(self):
        return self.__owner

    def get_balance(self):
        return self.__balance
    
    def withdraw(self, amount) -> bool:
        if amount <= 0:
            return False
        if self.__balance < amount:
            return False
        self.__balance -= amount
        return True

    def deposit(self, amount) -> bool:
        if amount <= 0:
            return False
        self.__balance += amount 
        return True

    def snapshot(self):
        if self.snap is not None:
            raise Exception("a snapshot is already instantiated")
        self.snap = AccountSnapshot(self.__balance)

    def revert(self):
        if self.snap is None:
            raise Exception("can not revert a snapshot not made before")
        self.__balance = self.snap.balance
        self.snap = None

    def commit(self):
        if self.snap is None:
            raise Exception("can not commit a snapshot not made before")
        self.snap = None

def execute_transaction(transaction_data) -> tuple[bool, list[Account]]:
    users = {
        u["id"]: User(u["id"], u["name"])
        for u in transaction_data["users"]
    }

    accounts_dict = {}
    instances: list[Account] = []
    
    for acc in transaction_data["accounts"]:
        owner = users[acc["owner_id"]]
        account = Account(acc["id"], owner, acc["balance"])
        accounts_dict[acc["id"]] = account
        instances.append(account)

    try:
        for obj in instances:
            obj.snapshot()

        for action in transaction_data["actions"]:
            acc_id = action["id"]
            method_name = action["method"]["name"]
            args = action["method"]["input"]

            target_obj = accounts_dict[acc_id]
            method = getattr(target_obj, method_name)

            success = method(*args)

            if not success:
                raise Exception(f"Method {method_name} returned False on account {acc_id}")
        
        for obj in instances:
            obj.commit()
        return True, instances

    except Exception as e:
        print(f"    [!] Error during transaction: {e}")
        for obj in instances:
            obj.revert()
        return False, instances

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def execute_transactions_from_file(file_path):
    data = load_json(file_path)

    for tx_index, transaction in enumerate(data["transactions"], start=1):
        print(f"\n--- Executing Transaction #{tx_index} ---")
        
        success, instances = execute_transaction(transaction)

        if success:
            print(f"Transaction #{tx_index} COMPLETE. Balances:")
        else:
            print(f"Transaction #{tx_index} FAILED. Rollback executed. Balances:")
        
        for acc in instances:
            print(f" Account {acc.get_id()} (Owner: {acc.get_owner().get_name()}): ${acc.get_balance():.2f}")

if __name__ == "__main__":
    execute_transactions_from_file("transactions.json")