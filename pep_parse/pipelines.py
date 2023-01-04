import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.counter = defaultdict(int)

    def process_item(self, item, spider):
        self.counter[''.join(item['status'])] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime('%Y-%m-%dT%H-%M-%S')
        file_name = f'{results_dir}/status_summary_{now_formatted}.csv'
        result = [('Статус', 'Количество')]
        result.extend(self.counter.items())
        total = sum(self.counter.values())
        result.append(('Total', total))
        with open(file_name, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(result)
        self.counter.clear()
