from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

from keywords.config import Config


class keywordsCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        for field in Config.config['keywords']:
            fields_to_export += field['words']

        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export

        super(keywordsCsvItemExporter, self).__init__(*args, **kwargs)
