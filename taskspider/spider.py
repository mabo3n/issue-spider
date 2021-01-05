from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta as date_delta


class TaskSpider():

    activity_selector = ('.timeline-entry '
                         '.timeline-content '
                         '.note-header-info ')

    def __init__(self, html):
        self.html = html

    def __get_activity_formatted_time(self, activity_node):
        activity_time_text = activity_node.find('time').get('datetime')
        activity_time_gmt_0 = date_parser.parse(activity_time_text)
        activity_time = activity_time_gmt_0 + date_delta(hours=-3)
        formatted_time = activity_time.strftime('%d/%m/%Y %H:%M')

        return formatted_time

    def __remove_amiss_stage_updates(self, stage_updates):
        stage_names = []
        update_times = {}
        for stage, time in stage_updates:
            already_went_to_stage = stage in stage_names
            if already_went_to_stage:
                stage_index = stage_names.index(stage)
                stage_names = stage_names[:stage_index + 1]
            else:
                stage_names.append(stage)
                update_times[stage] = time

        return [(stage, update_times[stage])
                for stage in stage_names]

    def scrap_metrics(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        stage_updates = []

        for activity_node in soup.select(self.activity_selector):
            activity_time = self.__get_activity_formatted_time(activity_node)

            message_node = activity_node.find('span',
                                              class_='system-note-message')
            message = message_node.text

            if (message.startswith('closed')
                    and 'via merge request' not in message):
                stage_updates.append(('DONE', activity_time))

            elif (message.startswith('added')):
                for message_item in message_node.find('span').children:

                    if 'and removed' in str(message_item):
                        break

                    if ('DELIVERY SERVICE' in str(message_item)
                            or 'UPSTREAM' in str(message_item)):

                        stage_updates.append((message_item.text,
                                             activity_time))
                        break

        return self.__remove_amiss_stage_updates(stage_updates)


if __name__ == "__main__":
    import sys
    import json
    from os import path

    current_dir = path.dirname(path.abspath(__file__))
    settings_file_path = path.join(current_dir, 'settings.json')

    with open(settings_file_path, 'r') as settings:
        settings = json.load(settings)

    downloads_dir = path.expanduser(settings['downloadsDirectory'])
    task_number = sys.argv[1]
    task_file_path = f'{downloads_dir}/{task_number}.html'

    with open(task_file_path, 'r') as task_file:
        spider = TaskSpider(task_file)
        spider.scrap_metrics()

    stage_names, update_times = zip(*spider.stage_updates)
    print('')
    print('\t'.join(stage_names))
    print('\t'.join(update_times))
