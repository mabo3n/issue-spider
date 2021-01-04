from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta as date_delta


class TaskSpider():

    activity_selector = ('.timeline-entry '
                         '.timeline-content '
                         '.note-header-info ')

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

        for activity_node in soup.select(self.activity_selector):
            activity_time = self.get_activity_formatted_time(activity_node)

            message_node = activity_node.find('span',
                                              class_='system-note-message')
            message = message_node.text

            if (message.startswith('closed')
                    and 'via merge request' not in message):
                self.stage_updates.append(('DONE', activity_time))

            elif (message.startswith('added')):
                for message_item in message_node.find('span').children:

                    if 'and removed' in str(message_item):
                        break

                    if 'UPSTREAM' in str(message_item):
                        self.stage_updates.append((message_item.text,
                                                   activity_time))
                        break

                    if 'DELIVERY SERVICE' in str(message_item):
                        self.stage_updates.append((message_item.text,
                                                   activity_time))
                        break

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
