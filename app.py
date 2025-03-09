from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time

app = Flask(__name__)

# Blockchain Class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.transactions = []  # Reset transactions after mining
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.get_previous_block()['index'] + 1

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                return new_proof
            new_proof += 1

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

blockchain = Blockchain()

# HTML + CSS + JS (Frontend)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Blockchain</title>
    <style>
        body {
            background: linear-gradient(to right, #141E30, #243B55);
            font-family: Arial, sans-serif;
            text-align: center;
            color: white;
        }
        .container {
            width: 50%;
            margin: auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-top: 50px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            border: none;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #45a049;
        }
        input {
            padding: 10px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Simple Blockchain</h1>
        <h3>Pending Transactions: <span id="pending">0</span></h3>

        <h2>Add Transaction</h2>
        <input type="text" id="sender" placeholder="Sender">
        <input type="text" id="recipient" placeholder="Recipient">
        <input type="number" id="amount" placeholder="Amount">
        <button onclick="addTransaction()">Add Transaction</button>

        <h3>Transactions</h3>
        <pre id="transactions"></pre>

        <button onclick="mineBlock()">Mine Block</button>
        
        <h3>Blockchain</h3>
        <pre id="blockchain"></pre>
    </div>

    <script>
        function updateBlockchain() {
            fetch('/get_chain')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('blockchain').textContent = JSON.stringify(data.chain, null, 4);
                    document.getElementById('transactions').textContent = JSON.stringify(data.pending, null, 4);
                    document.getElementById('pending').textContent = data.pending.length;
                });
        }

        function addTransaction() {
            let sender = document.getElementById("sender").value;
            let recipient = document.getElementById("recipient").value;
            let amount = document.getElementById("amount").value;
            if (!sender || !recipient || !amount) {
                alert("Please enter all transaction details!");
                return;
            }
            fetch('/add_transaction', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sender, recipient, amount})
            }).then(response => response.json())
              .then(() => updateBlockchain());
        }

        function mineBlock() {
            fetch('/mine_block', { method: 'GET' })
                .then(response => response.json())
                .then(() => updateBlockchain());
        }

        updateBlockchain();
    </script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not sender or not recipient or not amount:
        return jsonify({'message': 'Missing transaction data'}), 400

    index = blockchain.add_transaction(sender, recipient, amount)
    return jsonify({'message': f'Transaction added to block {index}'})

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    return jsonify({'message': 'Block mined!', 'block': block})

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain, 'pending': blockchain.transactions})

if __name__ == '__main__':
    app.run(debug=True)
