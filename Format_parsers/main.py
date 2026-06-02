from Parsers import parser_dat
import datetime

def main():
    parser = parser_dat.FormatDatParser(
        "Парсер формата .dat",
        r'Files_to_read\Solkinskoe_70BIS_2109\bytes_2026-05-15_22-31-03-2330.dat'
    )
    records = parser.read_file()
    print(f'Успешно записано записей : {len(records)}')
    temp_cnt_data = 0
    cnt = 0
    for item_ts, item_data in records:
        temp_cnt_data+=len(item_data)
        cnt +=1
        try:
            dt = datetime.datetime(1,1,1) + datetime.timedelta(microseconds=item_ts/10)
        except:
            continue
        print(f'{cnt})TimeStamp: {item_ts} , Size : {len(item_data)} bytes, Sum({temp_cnt_data}) , Data : {dt}')
        if cnt > 15:
            break
    print(f'Всего байт в файле : {parser.file_size()}')
        
if __name__ == '__main__':
    main()