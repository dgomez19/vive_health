from django.conf import settings


def get_work_schedule():
    list_hours = []
    for i in range(settings.START_ATTENTION_HOURS, settings.END_ATTENTION_HOURS):

        if len(str(i)) == 1:
            list_hours.append(f'0{i}:00')
            list_hours.append(f'0{i}:30')
        else:
            list_hours.append(f'{i}:00')

            if f'{i}:30' != '15:30':
                list_hours.append(f'{i}:30')

    return list_hours
