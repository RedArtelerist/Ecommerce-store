import copy
from EcommerceStore import settings
from store.models import Product


class WishList(object):
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            # save an empty cart in the session
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def __iter__(self):
        product_ids = self.wishlist.keys()
        # получение объектов product и добавление их в wishlist
        products = Product.objects.filter(id__in=product_ids)
        wishlist = copy.deepcopy(self.wishlist)
        for product in products:
            wishlist[str(product.id)]['product'] = product

        for item in wishlist.values():
            yield item

    def __len__(self):
        return len(self.wishlist.values())

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {}
            self.save()
        else:
            self.remove(product)

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def save(self):
        # Обновление сессии wishlist
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def clear(self):
        # удаление wishlist из сессии
        del self.session[settings.WISHLIST_SESSION_ID]
        self.session.modified = True