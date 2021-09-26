from django import template

register = template.Library()


@register.simple_tag
def table_row_index(page, forloop_counter0):
    """

    :param page: 페이지 객체
    :param forloop_counter0: 장고 템플릿 태그 forloop_counter0 값
    :return: 페이지네이션 시의 row 인덱스 번호
    """
    return page.start_index() + forloop_counter0
