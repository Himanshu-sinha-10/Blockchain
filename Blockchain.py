import datetime
import hashlib
import json
from flask import Flask, jsonify

# create block chain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1 , previous_hash = '0') #this will create the genesis block(the first block)
        
    def create_block(self, proof, previous_hash):
        block = {
              
            'index':len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            'proof':proof,
            'previous_hash': previous_hash
        }
        
        self.chain.append(block)
        
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if(hash_operation[:4] == "0000"):
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        
        while(block_index < len(self.chain)):
            curr_block = self.chain[block_index]
            
            if(self.hash(previous_block) != curr_block['previous_hash']):
                return False
        
            previous_proof = previous_block['proof']
            curr_proof = curr_block['proof']
            
            hash_operation =  hash_operation = hashlib.sha256(str(curr_proof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4] != "0000"):
                return False
            
            previous_block = curr_block
            block_index += 1
            
        return True
            
            
# mining blockchain

# set up flask web app

app = Flask(__name__)

# create an instance of Blockchain class

blockchain = Blockchain()

# mining a new block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    curr_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    
    mined_block = blockchain.create_block(curr_proof, previous_hash)
    
    response = {
        'message' : 'Congratulations, you just mined a new BLOCK',
        'index' : mined_block['index'],
        'timestamp' : mined_block['timestamp'],
        'proof' : mined_block['proof'],
        'previous_hash' : mined_block['previous_hash']
        }
    return jsonify(response),200

# getting full chain

@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
         }

    return jsonify(response),200

# check if chain is valid
@app.route('/is_valid',methods=['GET'])
def is_valid():
    
    if blockchain.is_chain_valid():
        response = {'valid' : 'True'}
    else:
        response = {'valid' : 'False'}
        
    return jsonify(response)




# running the app


app.run(host = '0.0.0.0' , port= 5000)











































   
   




            
            
            
            
            
            
            
            
            
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            