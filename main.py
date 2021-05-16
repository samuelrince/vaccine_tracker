import time

from datetime import datetime

from vaccine_tracker.doctolib import get_available_slots
from vaccine_tracker.utils import notify


DEFAULT_SLEEP_TIME = 60 * 10    # 10 minutes
URL = 'https://www.doctolib.fr/vaccination-covid-19/orsay?force_max_limit=2&ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005'


if __name__ == '__main__':
    slots_ids = set()

    while True:
        if 15 <= datetime.now().hour <= 23:
            new_slots = get_available_slots(URL)

            if new_slots:
                notify('New vaccination slots available', f'Found {len(new_slots)} new slots on Doctolib')

                for slot in new_slots:
                    if slot.id not in slots_ids:
                        slots_ids.add(slot.id)
                        print(slot)

        time.sleep(DEFAULT_SLEEP_TIME)
