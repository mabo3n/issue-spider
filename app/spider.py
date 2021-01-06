from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta as date_delta


class IssueSpider():

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
    from os import path, walk

    current_dir = path.dirname(path.abspath(__file__))
    html_dir = path.join(current_dir, 'html')

    def load_html_files():
        for dir_path, _, file_names in walk(html_dir):
            for file_name in file_names:
                if file_name.endswith('.html'):
                    file_path = path.join(dir_path, file_name)
                    with open(file_path, 'r') as html:
                        yield file_name, html

    print()
    for name, html in load_html_files():
        print(f'>>> Scraping metrics for "{name[:50]}"...\n')

        try:
            metrics = IssueSpider(html).scrap_metrics()
            stage_names, update_times = zip(*metrics)
            print('\t'.join(stage_names))
            print('\t'.join(update_times))

        except Exception:
            print('An error ocurred! Gotta do this one manually')

        print('\n<<<')

    print('Done!')
