from django import template

register = template.Library()


@register.filter("img_detail")
def img_detail(lst_details, position):
    return lst_details[position]


@register.filter("see_index")
def see_index(counter, number):
    return counter == number


@register.filter("range_days")
def range_days():
    lst_days = list(range(1, 32))
    return lst_days


@register.filter("range_months")
def range_months():
    lst_months = list(range(1, 13))
    return lst_months


@register.filter("range_years")
def range_years():
    lst_years = list(range(1970, 2025))
    return lst_years


@register.filter("to_int")
def to_int(num):
    try:
        num_to_int = int(num)
        return num_to_int
    except ValueError:
        return num


@register.filter("filter_dict")
def filter_dict(dictionary: dict):
    dictionary.pop(__key="link_video")
    return dictionary


@register.filter("list_item_by_index")
def list_item_by_index(dictionary, idx, key):
    for _key, value in dictionary.items():
        if int(_key) == int(key):
            return value[idx]


@register.filter("retrieve_element")
def retrieve_element(lst, idx):
    return lst[idx]