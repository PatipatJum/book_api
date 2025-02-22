from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb+srv://admin:admin123@cluster0.sp43h.mongodb.net/mydatabase"
client = MongoClient(MONGO_URI)
db = client["bookDB"]
books_collection = db["book"]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Create (POST) operation
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    last_book = books_collection.find_one(sort=[("id", -1)])
    new_id = last_book["id"] + 1 if last_book else 1
    new_book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "image_url": data["image_url"]
    }
    books_collection.insert_one(new_book)
    return jsonify(new_book), 201

# Read (GET) operation - Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = list(books_collection.find({}, {"_id": 0}))  # ไม่ส่งคืน _id
    return jsonify({"books": books})

# Read (GET) operation - Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = books_collection.find_one({"id": book_id}, {"_id": 0})
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Update (PUT) operation
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    updated_book = {
        "title": data["title"],
        "author": data["author"],
        "image_url": data["image_url"]
    }
    result = books_collection.update_one({"id": book_id}, {"$set": updated_book})
    if result.modified_count > 0:
        return jsonify({"message": "Book updated successfully"})
    return jsonify({"error": "Book not found"}), 404

# Delete operation
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books_collection.delete_one({"id": book_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
