from Parsers import parser_dat
from Parsers.Writer import FileSplitWriter
from Struct.Header import PacketHeader
import datetime
import os
from construct import Struct,Byte

input_file = r'Files_to_read\Solkinskoe_70BIS_2109\bytes_2026-05-15_22-31-03-2330.dat'

def main():
    parser = parser_dat.FormatDatParser(
        "Парсер формата .dat",
        input_file
    )
    
        # Создаём писатель с порогом 300 МБ (300 * 1024 * 1024)
    writer = FileSplitWriter(
        base_dir=os.path.dirname(input_file),
        base_name="output",
        bytes_per_file=300 * 1024 * 1024,
        ext= "json"
    )
    
    records = parser.read_file(show_progress_bar= True, writer=writer)
    print(f'Успешно записано записей : {len(records)}, В файл : {writer.get_count_record()}')
    # temp_cnt_data = 0
    # cnt = 0
    # for item_ts, item_data in records:
    #     temp_cnt_data+=len(item_data)
    #     cnt +=1
    #     try:
    #         dt = datetime.datetime(1,1,1) + datetime.timedelta(microseconds=item_ts/10)
    #     except:
    #         continue
    #     print(f'{cnt})TimeStamp: {item_ts} , Size : {len(item_data)} bytes, Sum({temp_cnt_data}) , Data : {dt}')
    #     if cnt > 15:
    #         break
    print(f'Всего байт в файле : {parser.file_size()} ({parser_dat.FormatDatParser.get_format_size(parser.file_size())})')
    
        
if __name__ == '__main__':
    main()