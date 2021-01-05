from taskspider import TaskSpider
from os import path


current_dir = path.dirname(path.abspath(__file__))
fixtures_dir = path.join(current_dir, 'fixtures')


def get_task_html(task_number):
    task_file_name = f'{task_number}.html'
    task_file_path = path.join(fixtures_dir, task_file_name)

    with open(task_file_path, 'r') as task_file:
        return task_file.read()


def test__scrap_metrics():
    html = get_task_html(2963)
    spider = TaskSpider(html)
    metrics = spider.scrap_metrics()

    assert metrics == [
        ('READY TO DESIGN',          '27/08/2020 10:52'),
        ('DESIGN DOING',             '11/09/2020 17:32'),
        ('READY TO TEST PLANNING',   '14/09/2020 18:19'),
        ('TEST PLANNING',            '15/09/2020 08:09'),
        ('READY TO DEVELOPMENT',     '15/09/2020 08:12'),
        ('DEVELOPMENT',              '23/10/2020 15:57'),
        ('READY TO REVIEW',          '03/11/2020 15:59'),
        ('REVIEW',                   '04/11/2020 17:36'),
        ('READY TO TEST',            '06/11/2020 08:09'),
        ('TEST',                     '06/11/2020 08:38'),
        ('READY TO HOMOLOGATION',    '06/11/2020 10:00'),
        ('HOMOLOGATION',             '09/11/2020 17:24'),
        ('DONE',                     '10/11/2020 09:33'),
    ]


def test__scrap_metrics__should_ignore_design_and_test_planning_stages():
    html = get_task_html(3075)
    spider = TaskSpider(html)
    metrics = spider.scrap_metrics()

    assert metrics == [
        ('READY TO DEVELOPMENT',     '08/12/2020 11:23'),
        ('DEVELOPMENT',              '08/12/2020 14:36'),
        ('READY TO REVIEW',          '09/12/2020 10:19'),
        ('REVIEW',                   '09/12/2020 15:35'),
        ('READY TO TEST',            '09/12/2020 16:13'),
        ('TEST',                     '09/12/2020 16:25'),
        ('READY TO HOMOLOGATION',    '09/12/2020 17:17'),
        ('HOMOLOGATION',             '09/12/2020 17:18'),
        ('DONE',                     '10/12/2020 10:02'),
    ]


def test__scrap_metrics__should_work_with_multiple_tag_additions():
    '''
    When creating a task and adding multiple tags at once,
    the first delivery service tag should be considered
    '''
    html = get_task_html(3050)
    spider = TaskSpider(html)
    metrics = spider.scrap_metrics()

    assert metrics == [
        ('READY TO DEVELOPMENT',     '19/11/2020 09:30'),
        ('DEVELOPMENT',              '19/11/2020 13:36'),
        ('READY TO REVIEW',          '24/11/2020 09:32'),
        ('REVIEW',                   '24/11/2020 10:21'),
        ('READY TO TEST',            '24/11/2020 15:02'),
        ('TEST',                     '24/11/2020 16:40'),
        ('READY TO HOMOLOGATION',    '24/11/2020 17:22'),
        ('HOMOLOGATION',             '24/11/2020 17:50'),
        ('DONE',                     '25/11/2020 08:36'),
    ]


def test__scrap_metrics__should_ignore_amiss_stage_updates():
    '''
    When a task is mistakenly moved forward in the board
    the amiss stage uptates should be ignored.
    '''
    html = get_task_html(3051)
    spider = TaskSpider(html)
    metrics = spider.scrap_metrics()

    assert metrics == [
        ('READY TO DEVELOPMENT',     '19/11/2020 10:05'),
        ('DEVELOPMENT',              '15/12/2020 16:48'),
        ('READY TO REVIEW',          '17/12/2020 16:52'),
        ('REVIEW',                   '18/12/2020 11:53'),
        ('READY TO TEST',            '18/12/2020 11:53'),
        ('TEST',                     '18/12/2020 13:38'),
        ('READY TO HOMOLOGATION',    '18/12/2020 15:03'),
        ('HOMOLOGATION',             '04/01/2021 08:49'),
        ('DONE',                     '04/01/2021 13:59'),
    ]
