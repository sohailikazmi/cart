from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample product data
products = [
    {'id': 1, 'name': 'Laptop', 'price': 1000},
    {'id': 2, 'name': 'Smartphone', 'price': 500},
    {'id': 3, 'name': 'Headphones', 'price': 100}
]

# Home route
@app.route('/')
def home():
    return render_template('home.html', products=products)

# Add to cart route
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(product)
        session.modified = True
    return redirect(url_for('view_cart'))

# View cart route
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

# Payment route
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)  # Clear cart after payment
        return render_template('success.html')
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
