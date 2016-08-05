import re
import csv


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        columns = [t.lower() for t in reader[0]]
        result = [dict(zip(columns, item)) for item in reader[1:] if item != []]
        return result


def save_csv(path, datalist):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(list(datalist[0].keys()))
        for item in datalist:
            writer.writerow(list(item.values()))


def replace_re(item):
    item['content'] = item['content'].strip()
    content = item['content']
    pattern = re.compile(r'^【(.*)：')
    match = pattern.match(content)
    if match:
        town = match.group().replace('【', '').replace('：', '')
    else:
        town = ''

    item['town'] = town

    return item


def replace_2(filename):
    data = read_csv(filename)
    temp = []
    for item in data:
        item_2 = replace_re(item)
        temp.append(item_2)
    save_csv(r'result_5.csv', temp)
    print('Done')


if __name__ == "__main__":
    replace_2('result_1.csv')
