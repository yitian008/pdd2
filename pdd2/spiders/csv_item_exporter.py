# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
功能:让item按固定列顺序额输出到csv文件中
'''

from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter

class Pdd2CsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export

        super(Pdd2CsvItemExporter, self).__init__(*args, **kwargs)
