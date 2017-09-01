import sys
sys.path.append('../')
from store.models import Product

from cart.models import Cart, ProductOrder

# Get Cart & ProductOrder objects

class get_cart:
    def get_cart(req):
        boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
        cart = Cart.objects.filter(user=req.user, session_id=None) if boolean else Cart.objects.filter(session_id=req.session.session_key, user=None)
        orders = ProductOrder.objects.filter(cart=cart)
        total = 0
        count = 0
        for order in orders:
            total += order.product.price * order.quantity
            count += order.quantity
        context = {
            'orders': orders,
            'total': total,
            'count': count,
        }
        return context

    def get_order(req):
        boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
        cart, created = Cart.objects.get_or_create(user=req.user, session_id=None) if boolean else Cart.objects.get_or_create(user=None, session_id=req.session.session_key)
        return cart

cart_info = get_cart()
