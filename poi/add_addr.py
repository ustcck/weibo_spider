'''
{'xzqy': '320583', 'jzdz': '千灯镇长江路东，长丰路南', 'gis_y': '31.4043035', 'gis_x': '150.9755925'}
常熟行政代码为320581 昆山行政代码为320583
if 'xzqy' == '320583' 并且'jzdz'中无昆山和昆山市
则在'jzdz'中加入'昆山市'
结果如：{'chg_dz': '昆山市千灯镇长江路东，长丰路南', 'xzqy': '320583', 'jzdz': '千灯镇长江路东，长丰路南', 'gis_y': '31.4043035', 'gis_x': '150.9755925'}
'''
import csv

def read_csv(path):
    with open(path,'r') as f:
        reader = csv.reader(f)
        reader = list(reader)
        columns = [t.lower() for t in reader[0]]
        result = [dict(zip(columns,item)) for item in reader[1:] if item != []]
        return result

def add_address(result):
    result_1 = []
    for i in range(len(result)):
        if (result[i]['xzqy'] == '320581') and ('常熟市' and '常熟' not in result[i]['dwdz']):
            result[i]['chg_dz'] = '常熟市' + result[i]['dwdz']
        elif (result[i]['xzqy'] == '320583') and ('昆山市' and '昆山' not in result[i]['dwdz']):
            result[i]['chg_dz'] = '昆山市' + result[i]['dwdz']
        else:
            result[i]['chg_dz'] = result[i]['dwdz']
        result_1.append(result[i])

    return result_1

def save_csv(path,datalist):              
    with open(path,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(list(datalist[0].keys()))
        for item in datalist:
            writer.writerow(list(item.values()))


if __name__ == "__main__":
    path='changshu.csv'
    read_result = read_csv(path)
    print(read_result[0])

    temp = add_address(read_result)
    save_csv(r'changshu_result_1.csv',temp)
