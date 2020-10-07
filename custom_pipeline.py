import scrapy
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class ArtspiderPipeline:
    def process_item(self, item, spider):
        return item

class CsvPipeline(object):
    def __init__(self):
        self.file = open("/home/pi/Documents/Programs/art_finder_env/all_data/freshly_scraped_info.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item