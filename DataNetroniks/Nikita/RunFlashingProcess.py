from SKLP import *


board_adressed_list = [0x1C, 0x1D, 0x1E]
angle_list = ['0°', '120°', '240°']

Interface = None
print( 'COM ports list:' )
ports = sorted( serial.tools.list_ports.comports() )
i = 1
for ( port, desc, hwid ) in ports:
    print(port)
    print(desc)
    print(hwid)
    
    # port_one = "{}.  {}:\t{:30}\t{}".format(i, port, desc, hwid )
    # print(port_one)
    # i+=1 

# index = input('Введите index нужного порта...\n')


    # SerialPortHWID = port_one.split(' ')
#     for i in range(len(SerialPortHWID)):
#         for j in range(len(SerialPortHWID[i]) - 2):
#             if( (SerialPortHWID[i][j] == 'P') and (SerialPortHWID[i][j+1] == 'I') and (SerialPortHWID[i][j+2] == 'D') ):
#                 Interface = SKLP_Serial( Baud = 115200, Timeout = 0.1, PortAutoHwid = SerialPortHWID[i], Name = 'SKLPM' )

# for i in range(len(board_adressed_list)):
#     if(SKLP_Module_RUS_Regul(Address = board_adressed_list[i], Interface = Interface).Query_GetID()):
#         print(f'Регулятор {angle_list[i]} на шине!')

# print(f'Выберите регулятор, который необходимо прошить\nРегулятор 0°\t= 0\nРегулятор 120°\t= 1\nРегулятор 240°\t= 2')

