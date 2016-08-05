# encoding:utf-8
import json
import urllib.request
import urllib.parse
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


def get_baidu_gps(poi):
    ak = 'og6twr6AIxoj1XMARgaepweY'
    host_url = 'http://api.map.baidu.com/geocoder/v2/?address=ADDRESS_NAME&output=json&ak=%s&callback=showLocation' % ak
    print(poi)
    address_name = poi['address']
    address = urllib.parse.quote(address_name)
    tmp_url = host_url.replace('ADDRESS_NAME', address)
    req = urllib.request.Request(tmp_url)
    try:
        data = urllib.request.urlopen(req)
    except:
        data = urllib.request.urlopen(req)
    rs = data.read()
    print(rs)

    text = rs.decode('utf-8')

    re_pattern = re.compile('showLocation&&showLocation\((.*)\)')
    match = re_pattern.search(text)

    poi['gis_x'] = ''
    poi['gis_y'] = ''
    if match:
        try:
            tmp = json.loads(match.group(1))
            poi['gis_x'] = tmp['result']['location']['lng']
            poi['gis_y'] = tmp['result']['location']['lat']
            return poi
        except:
            return poi

    else:
        return poi


def poi_gis(filename):
    data = read_csv(filename)
    temp = []
    for addr in data:
        item = get_baidu_gps(addr)
        temp.append(item)
    save_csv(r'result_1.csv', temp)
    print('Done')


if __name__ == "__main__":
    poi_gis('yixian_2.csv')
