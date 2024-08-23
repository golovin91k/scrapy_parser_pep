from collections import defaultdict
import csv
import datetime as dt

from pep_parse.settings import BASE_DIR, TIME_FORMAT


list_of_statuses = []


class PepParsePipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        list_of_statuses.append(item['status'])
        return item

    def close_spider(self, spider):
        results_dict = defaultdict(int)
        for status in list_of_statuses:
            results_dict[status] += 1
        results = []
        for key, value in results_dict.items():
            results.append((key, value))
        results.append(('Total', len(list_of_statuses)))

        now = dt.datetime.now()
        now_formatted = now.strftime(TIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = BASE_DIR / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            file_writer = csv.writer(f, delimiter=',', lineterminator='\r')
            file_writer.writerow(['Status', 'Quantity'])
            file_writer.writerows(results)
