import pymongo
from datetime import datetime

class Order:
    def __init__(self, order_id, email, book_id, amount):
        self.order_id = order_id
        self.email = email
        self.book_id = book_id
        self.amount = amount
        self.created_time = datetime.now()
        self.completed_time = ""
        self.status = "Initiated "

    def order_id(self):
        return self.order_id

    def order_id(self, order_id):
        self.order_id = order_id

    def email(self):
        return self.email

    def name_is(self, email):
        self.email = email

    def book_id(self):
        return self.book_id

    def book_id_is(self, book_id):
        self.book_id = book_id

    def amount(self):
        return self.amount

    def amount_is(self, amount):
        self.amount = amount

    def created_time(self):
        return self.created_time

    def created_time_is(self, created_time):
        self.created_time = created_time

    def status(self):
        return self.status

    def status_is(self, status):
        self.status = status

    def fully_populated(self):
        if not self.email:
            return False
        if not self.book_id:
            return False
        if not self.amount:
            return False
        return True


def create_order(db, order):
    # Verify that new order has all information needed
    if not order.fully_populated():
        return False
    try:
        db.orders.insert_one({'order_id': order.order_id,'email': order.email, 'book_id': order.book_id, 'amount': order.amount,
                              'created_time': order.created_time, 'status': order.status})
    except:
        return False
    return True

# Customer will order books based on the following
# - Will provide customer email
# - Will provide provide book names and quantities
# Verify this customer exists in Customer DB else fail order
#
# The API will look up books collection to find via book name
# - id of each book
# - Price of each book
#
# After this API will use id to query inventory collection
# - Check if requested quantity for each book is available
# - Decrement in book inventory if everything is available else fail order
#
# Open Items: How to charge customer ? We don't have payment info in the
# Customer table.
#
# XXX TODO Note: Some of this will change when we add AUTH because we need to
# pull user information from an authenticated session object which
# identifies an authenticated user.
def process_order(db, orders):
    books_order = []
    for order in orders:
        customer = db.customers.find_one({'email_address': order.email})
        print(customer)
        if not customer:
            return None

        db.orders.update_one({'order_id': order.order_id}, {'$set': {'status': 'in_processing'}}, upsert=False)
        try:
            book_record = db.books.find_one({'Title': order.book_id})
            print(book_record)
        except:
            continue

        book_id = book_record['_id']
        book_inventory = None
        try:
            book_inventory = db.inventory.find_one({'_id': book_id})
        except:
            continue

        inv_qty = book_inventory['quantity']
        req_qty = int(order.amount)
        if req_qty <= 0 or inv_qty < req_qty:
            db.orders.update_one({'order_id': order.order_id},
                                 {'$set': {'status': 'pending'}}, upsert=False)
        else:
            remain_qty = inv_qty - req_qty
            try:
                db.inventory.update_one({'_id': book_id}, {'$set': {'quantity': remain_qty}}, upsert=False)
                db.orders.update_one({'order_id': order.order_id},
                                     {'$set': {'status': 'completed', 'completed_time': datetime.now()}}, upsert=False)
            except:
                continue
        books_order.append(order)
    return (customer, books_order)