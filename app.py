from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ToasApp'
mongo = PyMongo(app)

# create table
@app.route('/create_table', methods=['POST'])
def createTable():
    try:
        table_name = request.json['table_name']
        if table_name and request.method == 'POST':
            mongo.db.create_collection(table_name)
            resp = jsonify('table created successfully')
            return resp
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}

# delete table
@app.route('/delete_table', methods = ['POST'])
def deleteTable():
    table_name = request.json['table_name']
    if table_name and request.method == 'POST':
        coll_list = mongo.db.list_collection_names()
        if table_name in coll_list:
            mongo.db.drop_collection(table_name)
            resp = jsonify('Table delete successfully')
        else:
            resp = jsonify('Table Not found')
        return resp
    else:
        return jsonify('invalid request')        

# Add Menu item
@app.route('/add', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        for i in data:
            if 'item_name' in i and 'item_price' in i:
                id = mongo.db.menu.insert(i) 
        resp = jsonify('Item added successfully')
        return resp
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}


@app.route('/update/<id>', methods=['PUT'])
def update_item(id):
    try:
        item_name = request.json['item_name']
        item_price = request.json['item_price']
        item_discount = request.json['item_discount']
        if id and (item_name or item_price or item_discount) and request.method == 'PUT':
            mongo.db.menu.update_one({'_id':ObjectId(id)}, {'$set':{'item_name':item_name, 'item_price':item_price, 'item_discount':item_discount}})
            resp = jsonify('Item updated successfully')
            return resp
        else:
            return jsonify('invalid request') 
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}

# Delete Menu Item
@app.route('/delete/<id>', methods=['DELETE'])
def depete_item(id):
    try:
        if id and request.method == 'DELETE':
            mongo.db.menu.delete_one({'_id':ObjectId(id)})
            resp = jsonify('Record delete successfully')
            return resp
        else:
            return jsonify('invalid request') 
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}

# Placed Order
@app.route('/place_order', methods=['POST'])
def placeOrder():
    try:
        data = request.get_json()
        items = data['items']
        status = 'P'
        orderList = []
        for item in items:
            val = mongo.db.menu.find({'item_name':item},{'_id':0})      
            for v in val:
                v['final_price'] = v['item_price'] - v['item_discount']
                v['status'] = 'P'
                orderList.append(v)
        id = mongo.db.order.insert_many(orderList)
        resp = jsonify('Order Places Successfully')
        return resp
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}

# update Order status
@app.route('/update_order_status/<id>', methods=['PUT'])
def updateOrderStatus(id):
    try:
        status = request.json['status']
        if id and status and request.method == 'PUT':
            mongo.db.order.update_one({'_id':ObjectId(id)}, {'$set':{'status':status}})
            resp = jsonify('order status updated successfully')
            return resp
        else:
            return jsonify('invalid request') 
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}

# view placed order
@app.route('/view_place_order', methods=['GET'])
def viewPlaceOrder():
    resp = commonOrderFun('P')
    return resp

# view ongoing order
@app.route('/view_ongoing_order', methods=['GET'])
def viewOngoingOrder():
    resp = commonOrderFun('O')
    return resp

# view complete order
@app.route('/view_complete_order', methods=['GET'])
def viewcompleteOrder():
    resp = commonOrderFun('C')
    return resp

# common for order status
def commonOrderFun(status):
    try:
        if request.method == 'GET':
            val = mongo.db.order.find({'status':status},{'_id':0,'status':0})
            orderList = [v for v in val]
            resp = jsonify(orderList)
            return resp
    except Exception as e:
        return {'Status':'Error', 'Message':str(e)}
   

if __name__ == '__main__':
    app.run(debug=True)





