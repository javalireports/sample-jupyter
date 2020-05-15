"""
XML Parser to CSV

Events.Event.System.TimeCreated SystemTime - время создания DATETIME
Events.Event.UserData.DocumentPrinted.
Param2 - имя документа DOCUMENT
Param3 - пользователь USERNAME
Param4 - имя компьютера COMPUTER
Param5 - имя принтера PRINTER
Param8 - количество распечатаных страниц COUNT = Message
Events-Event-RenderingInfo Culture
Message-"Страниц напечатано: 1." COUNT - (Param8)
"""
from lxml import etree
import csv
import argparse


def split(arr, size):
    """
    Функция разделения списка на части по вхождению

    :param arr:
    :param size:
    :return:
    """
    array = []
    while len(arr) > size:
        resizer = arr[:size]
        array.append(resizer)
        arr = arr[size:]
    array.append(arr)
    return array


parser = argparse.ArgumentParser(description="Converter XML event Windows log to CSV.")
parser.add_argument("inputfile", type=str, help="Path to the XML event log file")
parser.add_argument("outputfile", type=str, help="Path to the output CSV file")
args = parser.parse_args()

outputfile_filename = args.outputfile
inputfile_filename = args.inputfile

# открываем файл для записи
file_out = open(outputfile_filename, 'w', newline='')
csv_writer = csv.writer(file_out, delimiter=';')

# оформляем шапку
header = ['DATETIME', 'DOCUMENT', 'USERNAME', 'COMPUTER', 'PRINTER', 'COUNT']
csv_writer.writerow(header)

# определяем список необходимых элементов
head = ['SystemTime', 'Param2', 'Param3', 'Param4', 'Param5', 'Param8']
letter_message = 'Страниц напечатано: '
# объявляем переменную глобально
_ROW = []

with open(inputfile_filename, 'br') as f:
    for event, element in etree.iterparse(f):
        for x in element.attrib:
            if 'SystemTime' in x:
                _ROW.append(element.attrib[x])
        for params in head:
            if params in element.tag:
                _ROW.append(element.text)

# распакуем построчно и перенаправим stdout в файл
for x in split(_ROW, 6):
    print(*x, sep=';', file=file_out)

# закрываем файл
file_out.close()
