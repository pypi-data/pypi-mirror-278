from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def split(string, sep):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)


@register.filter
@stringfilter
def add_br(string, num):
    """num 갯수대로 문자열을 분리하고 <br>태그를 삽입한다..

    Example usage: {{ value|add_br:"2" }} -> 문자열을 둘로 나누고 <br>첨가
    """
    quotient = int(len(string)/int(num))
    index = [0]

    for i in range(1, int(num)):
        temp_index = quotient * i
        # 공백이 나오는 곳에서 문자열을 자르기 위해
        while string[temp_index] != ' ':
            temp_index += 1
        index.append(temp_index)

    new_str = ""
    for i in range(int(num)):
        try:
            new_str += string[index[i]:index[i+1]] + "<br>"
        except IndexError:
            # 맨 마지막 문자열의 경우 indexerror 발생하기 때문에
            new_str += string[index[i]:]

    return new_str



@register.filter
@stringfilter
def underscore_to_hyphen(string):
    """문자열의 _을 -로 변환한다.

    Example usage: {{ value| underscore_to_hyphen }}
    """
    return string.replace('_', '-')
