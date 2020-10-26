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

html = open('/home/marcelbornancin/Downloads/2974.html', 'r')
soup = BeautifulSoup(html, 'html.parser')

activity_selector = '.timeline-entry .timeline-content .note-headline-light'

stage_updates = []

for activity in soup.select(activity_selector):
    activity_message_node = activity.find('span', class_='system-note-message')

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
        stage_updates.append((added_tag, formatted_time))
    # print(f'-{removed_tag}a', '\t\t', f'+{added_tag}', '  \tat', formatted_time)

stage_names, update_times = zip(*stage_updates)

print('')
print('\t'.join(stage_names))
print('\t'.join(update_times))
