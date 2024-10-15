from flask import Flask, jsonify, request, abort
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

books = []
API_KEY = 'mysecretkey'  # هنا بنحدد الـ API key

# دي دالة للتحقق من الـ API key
def check_api_key():
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        abort(401)  # لو الـ API key مش صح، بنرجع "Unauthorized"

# 1. Endpoint لاسترجاع كل الكتب
@app.route('/books', methods=['GET'])
def get_books():
    """Get all books
    ---
    security:
      - apiKey: []
    responses:
      200:
        description: A list of books
    """
    check_api_key()  # تحقق من المفتاح قبل استرجاع البيانات
    return jsonify(books), 200

# 2. Endpoint لاسترجاع كتاب محدد باستخدام ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    """Get a book by ID
    ---
    security:
      - apiKey: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book
    responses:
      200:
        description: A book object
      404:
        description: Book not found
    """
    check_api_key()  # تحقق من المفتاح
    book = next((book for book in books if book['id'] == id), None)
    return jsonify(book) if book else ('Not Found', 404)

# 3. Endpoint لإضافة كتاب جديد
@app.route('/books', methods=['POST'])
def add_book():
    """Add a new book
    ---
    security:
      - apiKey: []
    parameters:
      - name: book
        in: body
        required: true
        schema:
          id: Book
          properties:
            id:
              type: integer
              description: The ID of the book
            title:
              type: string
              description: The title of the book
            author:
              type: string
              description: The author of the book
    responses:
      201:
        description: The created book
    """
    check_api_key()  # تحقق من المفتاح
    book = request.json
    books.append(book)
    return jsonify(book), 201

# 4. Endpoint لتحديث تفاصيل كتاب موجود
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    """Update a book by ID
    ---
    security:
      - apiKey: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book
      - name: book
        in: body
        required: true
        schema:
          id: Book
          properties:
            title:
              type: string
              description: The title of the book
            author:
              type: string
              description: The author of the book
    responses:
      200:
        description: The updated book
      404:
        description: Book not found
    """
    check_api_key()  # تحقق من المفتاح
    book = next((book for book in books if book['id'] == id), None)
    if book:
        book.update(request.json)
        return jsonify(book)
    return ('Not Found', 404)

# 5. Endpoint لحذف كتاب
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    """Delete a book by ID
    ---
    security:
      - apiKey: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book
    responses:
      204:
        description: No content
      404:
        description: Book not found
    """
    check_api_key()  # تحقق من المفتاح
    global books
    books = [book for book in books if book['id'] != id]
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
