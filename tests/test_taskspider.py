from taskspider import TaskSpider


def test_scrap_metrics():
    task_number = 2974
    task_file_path = f'/home/marcelbornancin/Downloads/{task_number}.html'

    with open(task_file_path, 'r') as task_file:
        spider = TaskSpider(task_file)
        metrics = spider.scrap_metrics()

    assert len(metrics) == 15
