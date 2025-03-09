# Simple-Blockchain-with-Transactions-Mining-using-Flask

This program is a simple blockchain implementation with a Flask-based web interface. It allows users to create transactions and mine new blocks, demonstrating the basic workings of a blockchain.

How It Works:
Blockchain Structure – The program defines a Blockchain class that manages blocks, transactions, and proof-of-work.
Transactions – Users can create new transactions (sender, recipient, and amount), which are stored in a pending list until mined into a block.
Mining – When a block is mined, a proof-of-work algorithm is used to find a valid proof number, securing the chain.
Flask Integration – A Flask server provides API routes to interact with the blockchain, such as adding transactions and viewing the chain.
Frontend (Optional) – The web interface (HTML, CSS, and JavaScript) displays the blockchain data and allows users to interact with it.

How to Run:
Install Flask 
Run the Python script
Open a browser and go to http://127.0.0.1:5000/ to interact with the blockchain.
