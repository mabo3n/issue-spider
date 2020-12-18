from taskspider import TaskSpider
from os import path


current_dir = path.dirname(path.abspath(__file__))
fixtures_dir = path.join(current_dir, 'fixtures')


def get_task_html(task_number):
    task_file_name = f'{task_number}.html'
    task_file_path = path.join(fixtures_dir, task_file_name)

    with open(task_file_path, 'r') as task_file:
        return task_file.read()


def test_scrap_metrics():
    html = get_task_html(2974)
    spider = TaskSpider(html)
    metrics = spider.scrap_metrics()

    assert len(metrics) == 15
