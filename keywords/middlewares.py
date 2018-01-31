import re

from scrapy.exceptions import IgnoreRequest


class IgnoreExtensions(object):
    IGNORED_EXTENSIONS = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf',
        'wmv', 'm4a', 'm4v',

        # other
        'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar', 'ppsx',
        'pptx', 'xml', 'tar'
    ]

    def process_request(self, request, spider):
        pattern = r'\.(%s)' % '|'.join(self.IGNORED_EXTENSIONS)

        url = request.url
        if re.findall(pattern, url, re.IGNORECASE) != []:
            raise IgnoreRequest('denied extension')
        else:
            return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        return None
