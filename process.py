import re, json

colleges = {}

def merge_dict(dict1, dict2):
    '''
    将作为值的字典融合 用到了递归 ChatGPT写的
    '''
    # 遍历dict2中的键值对，将其合并到dict1中
    for key, value in dict2.items():
        # 如果dict1中已经存在相同的键，则递归合并两个字典
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dict(dict1[key], value)
        # 否则直接将dict2中的键值对添加到dict1中
        else:
            dict1[key] = value
    return dict1

class College:
    '''A college'''
    # 基本信息：学校代码与学校名称
    _sn = ""
    _name = ""
    # _majors = {"计算机科学与技术": {"首选科目": {"2022": "物理", "2021": "物理"}, "再选科目": {"2022": "不限", "2021": "化学"}, "录取批次": {"2022":"本科批次", "2021": "本科批次"}, "说明": {"2022":"", "2021":""}, "分数": {"2022": (666, 633), "2021": (655, 634)}, "排名": {"2022": (4022, 1525), "2021": (2141, 2114)}}}
    _majors = {}

    def __init__(self, sn, name):
        self._sn = sn
        self._name = name

    def get_sn(self):
        return self._sn
    
    def get_name(self):
        return self._name
    
    def get_majors(self):
        return self._majors

    def add_entry(self, year, majorInfo):
        '''add a major entry to the college
        year = "2022"
        majorInfo = {"专业名称": "计算机科学与技术",
                     "录取批次": "本科批次",
                     "首选科目": "物理",
                     "再选科目": "不限",
                     "分数": (666, 633),
                     "排名": (4022, 1525),
                     "说明": "报考该科目有色觉要求"}
        '''

        _专业名称 = majorInfo["专业名称"]
        _录取批次 = majorInfo["录取批次"]
        _首选科目 = majorInfo["首选科目"]
        _再选科目 = majorInfo["再选科目"]
        _说明 = majorInfo["说明"]
        _分数 = majorInfo["分数"]
        _排名 = majorInfo["排名"]
        
        entry_dict = {"首选科目": {year: _首选科目}, "再选科目": {year: _再选科目}, "录取批次": {year: _录取批次}, "说明": {year: _说明}, "分数": {year: _分数}, "排名": {year: _排名}}

        if _专业名称 in self._majors:
            self._majors[_专业名称] = merge_dict(self._majors[_专业名称], entry_dict)
        else:
            self._majors[_专业名称] = entry_dict

def get_college_sn(name, file):
    '''给定大学名称，输出大学代码
    name: 大学名称
    file: 将大学名称与代码对应的json形式字典
    '''
    with open(file, 'r') as code:
    #TEST with open(college_code_reversed.json, 'r') as code:
        college_sn = json.loads(code.read())
    return college_sn[name]

def processBlock(block, sn_file):
    
    block = [string.rstrip('\n') for string in block]
    line_num = 0
    major_is_coming = False
    
    while True:
        if line_num == len(block):
            break

        if "各专业录取分数" in block[line_num]:
            college_name = re.search(r"^(.*?)(?=[0-9])", block[line_num]).group(1)
            sn = get_college_sn(college_name, sn_file)
            year = re.search(r"([0-9]{4})", block[line_num]).group(1)
            colleges[sn] = College(sn, college_name)
        
        elif "等科目类" in block[line_num]:
            major_is_coming = False
            __首选科目 = block[line_num].split("（")[1][0:2]
            line_num += 1
            __录取批次 = block[line_num]
            line_num += 1
            __再选科目 = block[line_num].split(r"(")[1].split(r")")[0]
            line_num += 1
            if "专业代号" in block[line_num+2]:
                __说明 = block[line_num]
                line_num += 1
            else:
                __说明 = ""
                line_num += 1
            major_is_coming = True

        if major_is_coming:
            __专业名称 = block[line_num]
            line_num += 2
            data = block[line_num].split("\t")
            __分数 = (data[0], data[2])
            __排名 = (data[1], data[3])
            majorInfo = {"专业名称": __专业名称,
                     "录取批次": __录取批次,
                     "首选科目": __首选科目,
                     "再选科目": __再选科目,
                     "分数": __分数,
                     "排名": __排名,
                     "说明": __说明}
            
            colleges[sn].add_entry(year, majorInfo)
            
        line_num += 1
        print(line_num)        
        continue

if __name__ == "__main__":
    test_string1 = "北京大学医学部2022年各专业录取分数\n院校专业组\n专业\n最高分\n最高分位次\n最低分\n最低分位次\n普通类（历史等科目类）\n本科批次\n北京大学医学部01专业组(不限)\n报考该专业组有色觉要求，具体请查阅院校招生章程\n英语(医学英语)(只招英语考生)\n专业代号：01\n630\t前107\t629\t前107\n普通类（物理等科目类）\n本科批次\n北京大学医学部02专业组(不限)\n报考该专业组有色觉要求，具体请查阅院校招生章程\n英语(医学英语)(只招英语考生)\n专业代号：02\n664\t175\t661\t243\n普通类（物理等科目类）\n本科批次\n北京大学医学部03专业组(化学)\n报考该专业组有色觉要求，具体请查阅院校招生章程\n基础医学\n专业代号：03\n668\t115\t665\t157\n临床医学\n专业代号：04\n679\t前101\t673\t前101\n临床医学\n专业代号：05\n672\t前101\t669\t102\n口腔医学\n专业代号：06\n681\t前101\t681\t前101\n口腔医学\n专业代号：07\n671\t前101\t668\t115\n预防医学\n专业代号：08\n668\t115\t668\t115\n药学\n专业代号：09\n673\t前101\t665\t157".split("\n")
    test_string2 = "北京大学医学部2021年各专业录取分数\n院校专业组\n专业\n最高分\n最高分位次\n最低分\n最低分位次\n普通类（历史等科目类）\n本科批次\n北京大学医学部01专业组(不限)\n报考该专业组有色觉要求,具体请查阅院校招生章程\n英语(医学英语)(只招英语考生)\n专业代号：01\n632\t前101\t630\t116\n普通类（物理等科目类）\n本科批次\n北京大学医学部02专业组(不限)\n报考该专业组有色觉要求,具体请查阅院校招生章程\n英语(医学英语)(只招英语考生)\n专业代号：02\n651\t262\t647\t372\n普通类（物理等科目类）\n本科批次\n北京大学医学部03专业组(化学)\n报考该专业组有色觉要求,具体请查阅院校招生章程\n基础医学\n专业代号：03\n653\t212\t649\t313\n临床医学\n专业代号：04\n662\t前101\t656\t160\n临床医学\n专业代号：05\n655\t182\t652\t238\n口腔医学\n专业代号：06\n673\t前101\t673\t前101\n口腔医学\n专业代号：07\n648\t348\t646\t406\n预防医学\n专业代号：08\n646\t406\t646\t406\n药学\n专业代号：09\n652\t238\t648\t348".split("\n")
    college_code_reversed = "college_code_reversed.json"
    processBlock(test_string1, college_code_reversed)
    processBlock(test_string2, college_code_reversed)
    for key in colleges:
        i = colleges[key]
        print(i.get_name())
        print(i.get_sn())
        print(i.get_majors())
