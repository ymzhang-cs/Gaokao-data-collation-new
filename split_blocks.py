def split_blocks(file):
    '''给定raw数据文件，返回按块处理过的列表，每个元素为列表，元素为一行
    '''
    blocks = []
    cnt = -1
    for line in file:
        line = line.replace("\n", "")
        if "各专业录取分数" in line:
            cnt += 1
            blocks.append([line])
        else:
            blocks[cnt].append(line)
    
    return blocks

if __name__ == "__main__":
    f = open('data\\data_raw_1.txt', 'r', encoding='utf-8')
    print(split_blocks(f))