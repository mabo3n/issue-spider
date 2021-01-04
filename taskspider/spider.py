from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta as date_delta

DELIVERY_SERVICE_TAGS = ['BACKLOG',
                         'READY TO DESIGN',
                         'DESIGN DOING',
                         'READY TO TEST PLANNING',
                         'TEST PLANNING',
                         'READY TO DEVELOPMENT',
                         'DEVELOPMENT',
                         'READY TO REVIEW',
                         'REVIEW',
                         'READY TO TEST',
                         'TEST',
                         'READY TO HOMOLOGATION',
                         'HOMOLOGATION']


class TaskSpider():

    activity_selector = ('.timeline-entry '
                         '.timeline-content '
                         '.note-headline-light ')

    def __init__(self, html):
        self.html = html
        self.stage_updates = []

    @staticmethod
    def get_activity_formatted_time(activity_node):
        activity_time_text = activity_node.find('time').get('datetime')
        activity_time_gmt_0 = date_parser.parse(activity_time_text)
        activity_time = activity_time_gmt_0 + date_delta(hours=-3)
        formatted_time = activity_time.strftime('%d/%m/%Y %H:%M')

        return formatted_time

    def scrap_metrics(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        for activity in soup.select(TaskSpider.activity_selector):
            activity_message_node = activity.find('span',
                                                  class_='system-note-message')
            if activity_message_node is None:
                continue

            contents = [c for c in activity_message_node.find('span').children]
            if len(contents) == 0:
                continue

            activity_verb = str(contents[0]).strip()
            activity_time = self.get_activity_formatted_time(activity)

            if activity_verb == 'added':
                first_added_tag = contents[1].text
                if first_added_tag in DELIVERY_SERVICE_TAGS:
                    self.stage_updates.append((first_added_tag, activity_time))

            if activity_verb == 'closed':
                self.stage_updates.append(('DONE', activity_time))

            # print('contents:', [str(c)[:10] for c in contents])
            # print('content[1]:', str(contents[1].text))

        return self.stage_updates

    def print_metrics(self):
        stage_names, update_times = zip(*self.stage_updates)
        print('')
        print('\t'.join(stage_names))
        print('\t'.join(update_times))


if __name__ == "__main__":
    import sys
    task_number = sys.argv[1]
    task_file_path = f'/home/marcelbornancin/Downloads/{task_number}.html'

    with open(task_file_path, 'r') as task_file:
        spider = TaskSpider(task_file)
        spider.scrap_metrics()
        spider.print_metrics()
