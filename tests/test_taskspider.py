from taskspider import TaskSpider
from os import path


current_dir = path.dirname(path.abspath(__file__))
fixtures_dir = path.join(current_dir, 'fixtures')


def get_task_html(task_number):
    task_file_name = f'{task_number}.html'
    task_file_path = path.join(fixtures_dir, task_file_name)

    with open(task_file_path, 'r') as task_file:
        return task_file.read()


def test__scrap_metrics__should_ignore_design_and_test_planning_stages():
    html = get_task_html(3075)
    spider = TaskSpider(html)
    metrics = spider.scrap_metrics()

    assert metrics == [
        ('READY TO DEVELOPMENT', '08/12/2020 11:23'),
        ('DEVELOPMENT', '08/12/2020 14:36'),
        ('READY TO REVIEW', '09/12/2020 10:19'),
        ('REVIEW', '09/12/2020 15:35'),
        ('READY TO TEST', '09/12/2020 16:13'),
        ('TEST', '09/12/2020 16:25'),
        ('READY TO HOMOLOGATION', '09/12/2020 17:17'),
        ('HOMOLOGATION' '09/12/2020 17:18'),
        ('DONE' '09/12/2020 17:54'),
    ]

