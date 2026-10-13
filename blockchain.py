
import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, product_id, status, location, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.product_id = product_id
        self.status = status
        self.location = location
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "product_id": self.product_id,
            "status": self.status,
            "location": self.location,
            "previous_hash": self.previous_hash
        }

        encoded_data = json.dumps(
            block_data, sort_keys=True
        ).encode()

        return hashlib.sha256(encoded_data).hexdigest()


class SupplyChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.products = {}

    def create_genesis_block(self):
        return Block(
            0,
            time.time(),
            "SYSTEM",
            "Blockchain Created",
            "BlockTrace Network",
            "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def register_product(self, product_id, name, category, manufacturer, origin):
        if product_id in self.products:
            return False, "Product ID already exists."

        self.products[product_id] = {
            "product_id": product_id,
            "name": name,
            "category": category,
            "manufacturer": manufacturer,
            "origin": origin
        }

        self.add_update(
            product_id,
            "Product Registered",
            origin
        )

        return True, "Product registered successfully!"

    def add_update(self, product_id, status, location):
        if product_id not in self.products:
            return False, "Product not found."

        previous_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            time.time(),
            product_id,
            status,
            location,
            previous_block.hash
        )

        self.chain.append(new_block)
        return True, "Supply chain status updated successfully!"

    def get_product_history(self, product_id):
        return [
            block for block in self.chain
            if block.product_id == product_id
        ]

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True


supply_chain = SupplyChain()
