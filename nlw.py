import simplejson as json
import unicodecsv as csv
import requests
from collections import OrderedDict


def get_manifests_from_file(filename):
    manifest_list = []
    with open('manifests.txt', 'r') as manifest_file:
        [manifest_list.append(line.strip()) for line in manifest_file.readlines()]
        return manifest_list


def manifest_test(manifest, dict_w):
    """
    Very crude dump to file logging.
    :param manifest:
    :param good_log:
    :param bad_log:
    :return:
    """
    r = requests.get(manifest)
    result = {'Type': 'Manifest', 'URI': manifest, 'Status': r.status_code}
    dict_w.writerow(result)
    if r.status_code == requests.codes.ok:
        images_test(manifest_json=r.json(), dict_w=dict_w)


def images_test(manifest_json, dict_w, repeats=5):
    canvases = manifest_json['sequences'][0]['canvases']
    for canvas in canvases:
        image_service = canvas['images'][0]['resource']['service']['@id']
        info_json = image_service + '/info.json'
        thumbnail = image_service + '/full/100,/0/native.jpg'
        tiles = [image_service + '/0,0,100,100/100,/0/native.jpg', image_service + '/100,100,200,200/100,/0/native.jpg']
        for x in range(0, repeats):
            r = requests.get(info_json)
            result = {'Type': 'Info.json', 'URI': info_json, 'Status': r.status_code,
                      'Elapsed Seconds': r.elapsed.total_seconds()}
            print(result)
            dict_w.writerow(result)
            r = requests.get(thumbnail)
            result = {'Type': 'Thumbnail', 'URI': thumbnail, 'Status': r.status_code}
            print(result)
            dict_w.writerow(result)
            for tile in tiles:
                r = requests.get(tile)
                result = {'Type': 'Tile', 'URI': tile, 'Status': r.status_code}
                print(result)
                dict_w.writerow(result)


if __name__ == "__main__":
    manifests = get_manifests_from_file('manifests.txt')
    f = 'output_repeats.csv'
    fieldnames = OrderedDict([('Type', None), ('URI', None), ('Status', None), ('Elapsed Seconds', None)])
    with open(f, 'wb') as output_csv:
        dw = csv.DictWriter(output_csv, delimiter='\t', fieldnames=fieldnames)
        dw.writeheader()
        for manifest in manifests:
            manifest_test(manifest, dict_w=dw)
