from django.template.defaulttags import register


@register.filter
def joiner(l):
    return (', ').join(l.strip('],[').split(','))

@register.filter
def range_(count):
    return range(1,count+1)


if __name__=="__main__":
    print(joiner(['a','b','c']))