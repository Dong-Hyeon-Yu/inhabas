def get_youtube_tag(behind_of_url):
    return  '<iframe width="560" height="315" ' \
            'src="https://www.youtube.com/embed/' + behind_of_url + '"' \
            ' title="YouTube video player"' \
            ' frameborder="0"' \
            ' allow="accelerometer; ' \
            'autoplay; ' \
            'clipboard-write; ' \
            'encrypted-media; ' \
            'gyroscope; ' \
            'picture-in-picture" allowfullscreen>' \
            '</iframe>'


def get_youtube(url: str):
    equal_idx = url.rfind('=')
    slash_idx = url.rfind('/')
    if equal_idx != -1:
        youtube_url = url[equal_idx:]
        return get_youtube_tag(youtube_url)
    if slash_idx != -1:
        youtube_url = url[slash_idx:]
        return get_youtube_tag(youtube_url)
