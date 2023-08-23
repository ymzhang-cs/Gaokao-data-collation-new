import csv

def writeCSV(export_file, data=['代码', '大学名称', '专业', '首选科目要求', '再选科目要求', '录取批次', '说明', '2022年录取最高分', '2022年录取最高名次', '2022年录取最低分', '2022年录取最低名次', '2021年录取最高分', '2021年录取最高名次', '2021年录取最低分', '2021年录取最低名次']):
    with open(export_file, 'a', encoding='utf-8') as fo:
        writer = csv.writer(fo)
        writer.writerow(data)
    