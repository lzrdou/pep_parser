# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

# useful for handling different item types with a single interface

BASE_DIR = Path(__file__).parent.parent
results_dir = BASE_DIR / "results"
results_dir.mkdir(exist_ok=True)
now = dt.datetime.now()
now_formatted = now.strftime("%Y-%m-%dT%H-%M-%S")
file_name = f"status_summary_{now_formatted}.csv"
file_path = results_dir / file_name


class PepParsePipeline:
    def open_spider(self, spider):
        self.counter = defaultdict(int)

    def process_item(self, item, spider):
        self.counter[''.join(item['status'])] += 1
        return item

    def close_spider(self, spider):
        result = [("Статус", "Количество")]
        result.extend(self.counter.items())
        total = sum(self.counter.values())
        result.append(("Total", total))
        with open(file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, dialect="unix")
            writer.writerows(result)
        self.counter.clear()
