from process import *
from split_blocks import split_blocks
from writeCSV import writeCSV

file_dirs = ['data\\data_raw_1.txt',
             'data\\data_raw_2.txt',
             'data\\data_raw_3.txt',
             'data\\data_raw_4.txt',
             'data\\data_raw_5.txt',
             ]

sn_file = 'college_code_reversed.json'
export_file = 'export.csv'

for raw_file in file_dirs:
    print("Now we start: ", raw_file)
    with open(raw_file, 'r', encoding='utf-8') as fi:
        blocks = split_blocks(fi)
    for block in blocks:
        processBlock(block, sn_file)

for school in colleges:
    sn = school.get_sn()
    name = school.get_name()
    majors = school.get_majors()
    for major, detail in majors.items():
        # 首选科目
        if len(set(detail["首选科目"].values())) != 1:
            _首选科目 = detail["首选科目"]["2022"]
        else:
            _首选科目 = detail["首选科目"]["2021"] + " | " + detail["首选科目"]["2022"]

        # 再选科目
        if len(set(detail["再选科目"].values())) != 1:
            _再选科目 = detail["再选科目"]["2022"]
        else:
            _再选科目 = detail["再选科目"]["2021"] + " | " + detail["再选科目"]["2022"]
        
        # 录取批次
        if len(set(detail["首选科目"].values())) != 1:
            _录取批次 = detail["录取批次"]["2022"]
        else:
            _录取批次 = detail["录取批次"]["2021"] + " | " + detail["录取批次"]["2022"]
        
        # 说明
        if len(set(detail["首选科目"].values())) != 1:
            _说明 = detail["说明"]["2022"]
        else:
            _说明 = detail["说明"]["2021"] + " | " + detail["说明"]["2022"]

        # 分数
        try:
            mark_2022_max, mark_2022_min = detail["分数"]["2022"]
        except:
            mark_2022_max, mark_2022_min = "", ""
        try:
            mark_2021_max, mark_2021_min = detail["分数"]["2021"]
        except:
            mark_2021_max, mark_2021_min = "", ""

        # 排名
        try:
            rank_2022_max, rank_2022_min = detail["排名"]["2022"]
        except:
            rank_2022_max, rank_2022_min = "", ""
        try:
            rank_2021_max, rank_2021_min = detail["排名"]["2021"]
        except:
            rank_2021_max, rank_2021_min = "", ""

        writeCSV(export_file, [sn, name, major, _首选科目, _再选科目, _录取批次, _说明, mark_2022_max, rank_2022_max, mark_2022_min, rank_2022_min, mark_2021_max, rank_2021_max, mark_2021_min, rank_2021_min])

print("FINISH")