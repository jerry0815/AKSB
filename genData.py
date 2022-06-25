import pandas as pd
from datetime import timedelta, date
import random
from tqdm import tqdm
day = timedelta(1)
start_date = date(2022,6,1)
end_date = date(2022,7,30)
#data = pd.DataFrame(columns = ['title', 'CR_ID', 'startDate', 'startSection', 'endDate', 'endSection', 'participant', 'B_ID', 'type'])
build = ["EA" , "EB" , "EC" , "ED" , "EE", "SA", "SB", "SC", "AC", "A", "AB", "HA", "EO"]
group = ['牛BB', '老果子', '母湯', '湯姆家族', '母湯貓', '屯屯一家','包子族']
activity = ['年終聚會','例行會議','團練','討論','派對','觀影']
ppl = [str(i) for i in range(1,21)]
records = []
for room in tqdm(range(1,261)):
    cur_date = start_date
    section = 1
    record = []
    while cur_date <= end_date:
        term = random.randrange(0,3)
        start_section = section
        if section + term  > 14:
            section = 14
        else:
            section += term
        end_section = section
        if section == 14:
            section = 1
            cur_date += day
        else:
            section += 1
        dice = random.randrange(1,11)
        if dice > 8:
            continue
        title = random.choice(group) + random.choice(activity)
        booker = random.randrange(1,21)
        random.shuffle(ppl)
        k = random.randrange(0,21)
        if k == 0:
            participant = ","
        else:
            participant = ppl[:k]
            if str(booker) in participant:
                participant.remove(str(booker))
                if len(participant) == 0:
                    participant = ","
            else:
                participant = ",".join(participant)
        records.append([title, room, cur_date, start_section, cur_date, end_section, participant,booker, 1])

        #tmp = pd.Series(record, index= data.columns)
        #data = data.append(tmp, ignore_index=True)
data = pd.DataFrame(records,columns = ['title', 'CR_ID', 'startDate', 'startSection', 'endDate', 'endSection', 'participant', 'B_ID', 'type'])
data.to_csv('random_record.csv',index=False, encoding='utf-8-sig')
