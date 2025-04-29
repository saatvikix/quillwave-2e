from django import template

register = template.Library()

@register.filter
def cart_total(books):
    return sum(book.price for book in books)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
