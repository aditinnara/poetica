from django import template

register = template.Library()

@register.filter(name='get_title')
def get_title(poems, index):
    return (poems[index])['Title']


@register.filter(name='get_poem')
def get_poem(poems, index):
    return (poems[index])['Poem']


@register.filter(name='get_poet')
def get_poet(poems, index):
    return (poems[index])['Poet']