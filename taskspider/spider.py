from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta as date_delta

stage_tags = ['BACKLOG',
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

    def scrap_metrics(self):

        soup = BeautifulSoup(self.html, 'html.parser')

        for activity in soup.select(TaskSpider.activity_selector):
            activity_message_node = activity.find('span',
                                                  class_='system-note-message')
            if activity_message_node is None:
                continue

            contents = [c for c in activity_message_node.find('span').children]

            is_tag_action = len(contents) in [3, 5]
            if not is_tag_action:
                continue

            if str(contents[0]).endswith('added '):
                added_tag = contents[1].text
            elif str(contents[0]).endswith('removed '):
                removed_tag = contents[1].text
            else:
                continue

            if len(contents) == 5:
                if str(contents[2]).endswith('added '):
                    added_tag = contents[3].text
                elif str(contents[2]).endswith('removed '):
                    removed_tag = contents[3].text
                else:
                    continue

            activity_time_text = activity.find('time').get('datetime')
            activity_time_gmt_0 = date_parser.parse(activity_time_text)
            activity_time = activity_time_gmt_0 + date_delta(hours=-3)
            formatted_time = activity_time.strftime('%d/%m/%Y %H:%M')

            if added_tag in stage_tags:
                self.stage_updates.append((added_tag, formatted_time))

            # print(f'-{removed_tag}a', '\t\t',
            #       f'+{added_tag}', '  \tat',
            #       formatted_time)

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
