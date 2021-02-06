from .wishlist import WishList


def wishlist(request):
    return {'wishlist': WishList(request)}