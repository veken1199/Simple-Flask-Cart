

def get_cart(session):
    if 'cart' not in session:
        session['cart'] = dict()
    return session['cart']