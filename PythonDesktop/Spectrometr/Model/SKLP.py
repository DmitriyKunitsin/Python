r""" Установка PySerial - не входит в пакет Литвинова!
- если есть инет:
%LOOCH_PYTHON_DIR%\python.exe -m pip install pyserial
- если нету инета, скачать и выполнить
https://files.pythonhosted.org/packages/07/bc/587a445451b253b285629263eb51c2d8e9bcea4fc97826266d186f96f558/pyserial-3.5-py2.py3-none-any.whl
%LOOCH_PYTHON_DIR%\python.exe -m pip install %LOOCH_PYTHON_DIR%\pyserial-3.5-py2.py3-none-any.whl
- если есть лучевский обрезанный интернет и работает заплатка на сервере:
%LOOCH_PYTHON_DIR%\python -m pip install pyserial -i http://opo.looch.ru:4040/root/pypi/+simple --trusted-host opo.looch.ru
"""

'''
Библиотека обмена с модулями СКЛ:
- SKLP                  SKLP, базовый класс интерфейса обмена
- SKLP_Serial           SKLP, транспорт через COM-порт
- SKLP_Emul             SKLP, виртуальный транспорт через очереди
Библиотека модулей СКЛ:
- SKLP_Module           Базовый класс
- SKLP_ModuleInclin     Инклинометр 173/174/РУС
- SKLP_ModuleGK         ВИКПБ.ГК
- SKLP_Module_RUSPump   РУС, электропривод насоса
- SKLP_Module_RUSTele   РУС, телеметрия
- SKLP_Module_GGP_SADC  ГГКП, счетчик гаммы
- SKLP_Module_MUP       МУП
'''

from struct import *
import serial
import serial.tools.list_ports
import queue
import struct
import threading

# Интерфейс обмена по SKLP, Master/Slave
class SKLP:
    ''' Базовый класс интерфейса обмена по SKLP. Транспорт должен быть определен в наследующем классе. '''
    __aCRC8_Table = [
    0x00,0xBC,0x01,0xBD,0x02,0xBE,0x03,0xBF,0x04,0xB8,0x05,0xB9,0x06,0xBA,0x07,0xBB,
    0x08,0xB4,0x09,0xB5,0x0A,0xB6,0x0B,0xB7,0x0C,0xB0,0x0D,0xB1,0x0E,0xB2,0x0F,0xB3,
    0x10,0xAC,0x11,0xAD,0x12,0xAE,0x13,0xAF,0x14,0xA8,0x15,0xA9,0x16,0xAA,0x17,0xAB,
    0x18,0xA4,0x19,0xA5,0x1A,0xA6,0x1B,0xA7,0x1C,0xA0,0x1D,0xA1,0x1E,0xA2,0x1F,0xA3,
    0x20,0x9C,0x21,0x9D,0x22,0x9E,0x23,0x9F,0x24,0x98,0x25,0x99,0x26,0x9A,0x27,0x9B,
    0x28,0x94,0x29,0x95,0x2A,0x96,0x2B,0x97,0x2C,0x90,0x2D,0x91,0x2E,0x92,0x2F,0x93,
    0x30,0x8C,0x31,0x8D,0x32,0x8E,0x33,0x8F,0x34,0x88,0x35,0x89,0x36,0x8A,0x37,0x8B,
    0x38,0x84,0x39,0x85,0x3A,0x86,0x3B,0x87,0x3C,0x80,0x3D,0x81,0x3E,0x82,0x3F,0x83,
    0x40,0xFC,0x41,0xFD,0x42,0xFE,0x43,0xFF,0x44,0xF8,0x45,0xF9,0x46,0xFA,0x47,0xFB,
    0x48,0xF4,0x49,0xF5,0x4A,0xF6,0x4B,0xF7,0x4C,0xF0,0x4D,0xF1,0x4E,0xF2,0x4F,0xF3,
    0x50,0xEC,0x51,0xED,0x52,0xEE,0x53,0xEF,0x54,0xE8,0x55,0xE9,0x56,0xEA,0x57,0xEB,
    0x58,0xE4,0x59,0xE5,0x5A,0xE6,0x5B,0xE7,0x5C,0xE0,0x5D,0xE1,0x5E,0xE2,0x5F,0xE3,
    0x60,0xDC,0x61,0xDD,0x62,0xDE,0x63,0xDF,0x64,0xD8,0x65,0xD9,0x66,0xDA,0x67,0xDB,
    0x68,0xD4,0x69,0xD5,0x6A,0xD6,0x6B,0xD7,0x6C,0xD0,0x6D,0xD1,0x6E,0xD2,0x6F,0xD3,
    0x70,0xCC,0x71,0xCD,0x72,0xCE,0x73,0xCF,0x74,0xC8,0x75,0xC9,0x76,0xCA,0x77,0xCB,
    0x78,0xC4,0x79,0xC5,0x7A,0xC6,0x7B,0xC7,0x7C,0xC0,0x7D,0xC1,0x7E,0xC2,0x7F,0xC3 ]
    class Signature:
        StartQuery  = 0x40
        StartAnswer = 0x23
    class AddressList:
        Broadcast   = 0x00
        MUP         = 0x62      # МУП
        NNKT        = 0x71      # ННКТ
        GGLP_SADC   = 0x88      # два µC на одном адресе, но на разных шиных
        GGLP_SADC_S = 0x89      # ближний зонд (не используется)
        GGLP_SADC_L = 0x8A      # дальний зонд (не используется)
        Inclin      = 0x99      # инклинометр Луч
        MPI         = 0xEA      # МПИ
        # Модемные
        BKS         = 0x24      # БКС
        VIKPB       = 0x55      # ВИКПБ
        VIKPB_GK    = 0x56      # ВИКПБ ГК
        NNKTe       = 0x73      # ННКТ(б)
        GGP         = 0x82      # ГГкП
        ACP_Aux     = 0xB1      # АКП(б), вспомогательный канал
        ACP         = 0xB2      # АКП(б)
        NDM_Trans   = 0xDB      # НДМ-ПП
        NDMT        = NDM_Trans
        EML         = NDMT
        # МП
        MP_18V_Broadcast    = 0xD0
        MP_18V              = 0xD1
        MP_36V_Broadcast    = 0xD2
        MP_36V              = 0xD3
        # РУС
        RUS_Tele    = 0x1A      # РУС (Теле)
        RUS_Pump    = 0x1B      # РУС контроллер электропривода (широковещательный)
        RUS_Pump0   = 0x1C      # РУС контроллер электропривода 0°
        RUS_Pump1   = 0x1D      # РУС контроллер электропривода 120°
        RUS_Pump2   = 0x1E      # РУС контроллер электропривода 240°
        RUS_GK      = VIKPB_GK
        RUS_Inclin  = Inclin

    def __init__( self, Timeout = 0.5, Name = 'SKLP' ):
        ''' Установка таймаута во время передачи пакета через модуль 'serial'
        иногда приводит к нарушению передаваемого фрейма UART, во всяком случае на плате 498_01 с чипом FTDI.
        Из-за этого установку таймаута порта необходимо производить до начала передачи запроса.
        Оказалось удобнее исключить аргумент 'Timeout' из функции __RecFrame(), и передавать таймаут через поле класса.
        '''
        self.Timeout = Timeout  
        self.Name = Name

    def CalcCRC8( Packet ) -> int:
        CRC8 = 0
        PacketLen = len( Packet )
        for i in range( 0, PacketLen ):
            CRC8 = SKLP.__aCRC8_Table[ CRC8 ^ Packet[i] ]
        return CRC8
    
    def Calc_CRC16( Packet: bytearray, Size, CRC16 ):
        CRC16 %= 65536
        h_12 = 255
        h_1 = 255
        hh_5 = 255
        hl_5 = 255
        temp = 65535
        i = 0
        while(Size > 0):
            h_12 = (CRC16 >> 8) % 256
            h_1 = (h_12) % 256
            h_12 = ((h_12 >> 4)|(h_12 << 4)) % 256
            hh_5 = (h_12) % 256
            h_12 ^= (h_1) % 256
            h_12 &= (0xF0) % 256
            hh_5 &= (0x0F) % 256
            h_1 ^= (hh_5) % 256
            hl_5 = (h_12) % 256
            temp = ( (hh_5 << 8) | hl_5 ) % 65536
            temp <<= 1
            temp %= 65536
            hh_5 = (temp >> 8) % 256
            hl_5 = (temp) % 256
            h_1 ^= (hl_5) % 256
            h_12 ^= (hh_5) % 256
            hl_5 = (CRC16) % 256
            h_1 ^= (Packet[i]) % 256
            h_12 ^= (hl_5) % 256
            CRC16 = ( (h_12 << 8) | h_1 ) % 65536
            Size = Size - 1
            i += 1
        return CRC16
        
#   Транспортные функции должны быть определены в наследующих классах
#    def __SendFrame( self, Frame :bytearray ):
#    def __RecFrame( self, Timeout = None ) -> ( bytearray, int ):

    def __SendPacket( self, Signature :Signature, Packet :bytearray ) -> None:
        PacketSize = len( Packet )
        if PacketSize > 0xFF:
            PacketSize = 0xFF
        Frame = bytearray( [ Signature, PacketSize ] ) + Packet
        CRC = SKLP.CalcCRC8( Frame )
        Frame = Frame + bytearray( [ CRC ] )
        self.__SendFrame( Frame )

    def __SendQuery( self, Address, Function, Data = bytearray() ) -> None:
        self.__SendPacket( SKLP.Signature.StartQuery, bytearray( [ Address, Function ] ) + Data )
           
    def Answer( self, Data ) -> None:
        self.__SendPacket( SKLP.Signature.StartAnswer, Data )

    def Query( self, Address, Function, Data = bytearray(), RecAnswer = True, Timeout = None ) -> bytearray:
        '''Формирует запрос на плату и она же возвращает ответ в виде bytearray() '''
        if Timeout != None:
            self.Timeout = Timeout
        self.__SendQuery( Address, Function, Data )
        if RecAnswer:
            Frame, Signature = self.__RecFrame( Timeout = None )
            if Signature != SKLP.Signature.StartAnswer:
                Frame = bytearray()
            return Frame

    def RecQuery( self, Timeout = None ) -> ( int, int, bytearray ):   # Address, Command, Data
        Frame, Signature = self.__RecFrame( Timeout )
        if ( Frame == None ) or ( Signature != SKLP.Signature.StartQuery ):
            return None
        FrameSize = len ( Frame )
        if FrameSize < 2:
            return None
        return ( Frame[0], Frame[1], Frame[2:FrameSize] )

    def RecQueryAnswer( self, Timeout = None ) -> ( str, int, int, bytearray ):   # ( 'Query', ( Address, Command, Data ) ) or ( 'Answer', Data )
        Frame, Signature = self.__RecFrame( Timeout )
        if ( Frame == None ) or ( Signature not in ( SKLP.Signature.StartQuery, SKLP.Signature.StartAnswer ) ):
            return None
        FrameSize = len( Frame )
        if Signature == SKLP.Signature.StartQuery:
            if FrameSize < 2:
                return None
            return ( 'Query', ( Frame[0], Frame[1], Frame[2:FrameSize] ) )
        elif Signature == SKLP.Signature.StartAnswer:
            if FrameSize < 1:
                return None
            return ( 'Answer', Frame[0:FrameSize] )
        return None

class SKLP_Serial( SKLP ):
    ''' Интерфейс SKLP, транспорт через COM-порт '''
    def PrintListCOM():
        print( 'COM ports list:' )
        ports = sorted( serial.tools.list_ports.comports() )
        for ( port, desc, hwid ) in ports:
            print( "{}:\t{:30}\t{}".format( port, desc, hwid ) )

    def __init__( self, Port = 'COM17', Baud = 1000000, Timeout = 0.5, PortAutoDesc = None, PortAutoHwid = None, Name = 'SKLP_Serial' ):
        SKLP.__init__( self, Timeout, Name )
        if( ( Port == None ) and ( ( PortAutoDesc != None ) or ( PortAutoHwid != None ) ) ):
            ports = serial.tools.list_ports.comports()
            for ( port, desc, hwid ) in sorted( ports ):
                if( ( ( PortAutoDesc != None ) and ( desc.find( PortAutoDesc ) >= 0 ) ) or \
                    ( ( PortAutoHwid != None ) and ( hwid.find( PortAutoHwid ) >= 0 ) ) ):
                    Port = port
                    break
        self.SPort = None
        if( Port == None ):
            Signature = PortAutoDesc if ( PortAutoDesc != None ) else PortAutoHwid
            raise ValueError( Name + ' can\'t found COM \"{}\"!'.format( Signature ) )
        self.SPort = serial.Serial(
            port        = Port,
            baudrate    = Baud,
            parity      = serial.PARITY_NONE,
            stopbits    = serial.STOPBITS_ONE,
            bytesize    = serial.EIGHTBITS,
            timeout     = self.Timeout )
        self.Status = self.Name + ' connected to ' + self.SPort.portstr
        self.SPort.reset_input_buffer()
        self.LastRecFrame = None
        self.bLogEnable = False
        self.WriteMtx = threading.Lock()
        self.bResetInputBuffer = True       # по-умолчанию очищать приемный буфер после приема пакета. однако, это не дает нормально работать снифферу
        
    def __del__( self ):
        if self.SPort != None:
            self.SPort.close()

    def _SKLP__SendFrame( self, Frame :bytearray ):
        self.WriteMtx.acquire()
        try:
            self.SPort.reset_input_buffer()
            self.SPort.reset_output_buffer()
            self.SPort.timeout = self.Timeout  # !! Установка таймаута во время передачи пакета приводит к нарушению фрейма UART, во всяком случае на плате 498_01 с чипом FTDI, поэтому таймаут проходится устанавливать до начала передачи запроса!
            self.SPort.write( Frame )
            if self.bLogEnable:
                print( '>> {}:\t[{}]\t{}'.format( self.SPort.portstr, len( Frame ), Frame.hex() ) )
        except serial.SerialException:
            return None
        finally:
            self.WriteMtx.release()

    def _SKLP__RecFrame( self, Timeout = None ) -> ( bytearray, int ):
        ''' Реализация приема только коротких пакетов, с полем размера от 1 до 254! '''
        try:
        # if True:
            if Timeout != None:                     # Установку таймаута производить только при ожидании приема асинхронного пакета. В режиме запрос-ответ таймаут устанавливать перед началом передачи запроса!
                self.Timeout = Timeout
                self.SPort.timeout = self.Timeout
            Frame = self.SPort.read( 2 )
            if ( Frame != None ) and ( len( Frame ) == 2 ):
                PacketSize = Frame[1];

                # Frame = Frame + self.SPort.read( PacketSize + 1 )
                # if ( 0 < PacketSize < 255 ) and ( SKLP.CalcCRC8( Frame ) == 0 ) :
                    # self.SPort.reset_input_buffer()
                    # self.LastReqFrame = Frame
                    # if self.bLogEnable:
                        # print( '<< {}:\t[{}]\t{}'.format( self.SPort.portstr, len( Frame ), Frame.hex() ) )
                    # return Frame[ 2 : PacketSize+2 ], Frame[0]
                    
                if ( 0 < PacketSize < 255 ):
                    Frame = Frame + self.SPort.read( PacketSize + 1 )
                else:
                    PacketSize = 20000
                    FrameTail = self.SPort.read( PacketSize + 1 )
                    PacketSize = len( FrameTail ) - 1;
                    Frame = Frame + FrameTail
                if self.bResetInputBuffer:
                    self.SPort.reset_input_buffer()
                if ( SKLP.CalcCRC8( Frame ) == 0 ) and ( PacketSize > 0 ):
                    self.LastReqFrame = Frame
                    if self.bLogEnable:
                        print( '<< {}:\t[{}]\t{}'.format( self.SPort.portstr, len( Frame ), Frame.hex() ) )
                    return Frame[ 2 : PacketSize+2 ], Frame[0]
                    
            raise serial.SerialException
        except serial.SerialException as e:
            return None, None
        
class SKLP_Emul( SKLP ):
    ''' Интерфейс SKLP, виртуальный транспорт через очереди '''
    def __init__( self, QueTx = None, QueRx = None, Name = 'SKLP_Emul' ):
        SKLP.__init__( self, Timeout = None, Name = Name )
        if ( QueRx == None ) or ( QueTx == None ):
            raise ValueError( Name + ' can\'t connected to Queues!' )
        self.Name = Name
        self.QueTx = QueTx
        self.QueRx = QueRx
        self.Status = '{}.Rx connected to Queue at 0x{:0X}, {}.Tx connected to Queue at 0x{:0X}'.format( self.Name, id( self.QueRx ), self.Name, id( self.QueTx ) )
        self.LastRecFrame = None

    def CreatePair( Name = 'SKLP_Emul' ) -> ( 'SKLP_Emul_Master', 'SKLP_Emul_Salve' ):
        ''' Создать пару интерфейсов, соединенных через очереди '''
        QueMasterTx = queue.Queue( maxsize = 4 )
        QueMasterRx = queue.Queue( maxsize = 4 )
        SKLP_EmulMaster = SKLP_Emul( QueTx = QueMasterTx, QueRx = QueMasterRx, Name = Name + '_Master' )
        SKLP_EmulSlave = SKLP_Emul( QueTx = QueMasterRx, QueRx = QueMasterTx, Name = Name + '_Slave' )
        return ( SKLP_EmulMaster, SKLP_EmulSlave )

    def __QueClear( Que ):
        while not Que.empty():
            Que.get()

    def _SKLP__SendFrame( self, Frame :bytearray ):
        Que = self.QueTx
        if ( Que != None ) and ( Frame != None ):
            SKLP_Emul.__QueClear( Que )
            Que.put_nowait( Frame )
            self.Status = '{}.SendFrame, {} bytes'.format( self.Name, len( Frame ) )

    def _SKLP__RecFrame( self, Timeout ) -> ( bytearray, int ):
        if Timeout == None:
            Timeout = self.Timeout
        Que = self.QueRx
        while True:
            if Que == None:
                break
            self.Status = '{}.RecFrame, wait {} s for Frame...'.format( self.Name, Timeout )
            try:
                Frame = Que.get( timeout = Timeout )
            except queue.Empty:
                self.Status += ' Timeout!'
                break
            FrameSize = len( Frame )
            if( FrameSize < 3 ):
                self.Status += ' Broken frame!'
                break
            if SKLP.CalcCRC8( Frame ) == 0:
                self.Status += ' Success!'
                self.LastRecFrame = Frame
                return Frame[ 2 : FrameSize-1 ], Frame[0]
            self.Status += ' Bad CRC!'
            break
        return None, None
 
# ********************************************
# ********************************************
import time
import datetime
import numpy as np

def ParseBlock( Packet :bytearray, iStart :int, Parse :str ) -> ( int, tuple ):
    ''' Распарсить фрагмент пакета, начиная с указанного индекса.
    Вернуть индекс следующего фрагмента и кортеж из полученных тегов '''
    ParseSize = calcsize( Parse )
    tParsed = unpack( Parse, Packet[ iStart : iStart+ParseSize ] )
    return ( iStart+ParseSize, tParsed )

if True:    # Примочки для работы с SKLP-идентификаторами модулей. Перенести в родительский класс?
    def ParseLoochSerial( BCD :int ) -> tuple:                          # 0xNNCNCCYY -> ( YYYY, CCC, NNN )
        def BCD3_2Dec( BCD3 :int ) -> int:      # 0x3210 -> #2*100 + #1*10 + #0
            return ( BCD3//256 )*100 + ( ( BCD3%256 )//16 )*10 + ( ( BCD3%256 )%16 ) 
        Year    = BCD3_2Dec( BCD & 0xFF ) + 2000
        Decimal = BCD3_2Dec( ( ( BCD >> 4 ) & 0xFF0 ) | ( ( BCD >> 20 ) & 0x0F ) )
        Number  = BCD3_2Dec( ( ( BCD >> 8 ) & 0xF00 ) | ( ( BCD >> 24 ) & 0xFF ) )
        return ( Year, Decimal, Number )
        
    def ParseLoochSerialTxt( BCD :int ) -> str:                         # 0xNNCNCCYY -> "YY'CCC'NNN"
        ( Year, Decimal, Number ) = ParseLoochSerial( BCD )
        return f"{ Year%2000 :02d}\'{ Decimal :03d}\'{ Number :03d}"

    def CodeLoochSerial( Year :int, Decimal :int, Number :int ) -> int: # ( YYYY, CCC, NNN ) -> 0xNNCNCCYY
        Result = 0
        if ( Year < 2000 ) or ( Year > 2099 ):
            raise( ValueError( f'Year = {Year}!' ) )
        Year -= 2000
        Result |= ( ( Year // 10 ) << 4 ) | ( Year % 10 )

        if ( Decimal < 0 ) or ( Decimal > 999 ):
            raise( ValueError( f'Decimal = {Decimal}!' ) )
        Result |= ( ( Decimal // 100 ) << 12 ) | ( ( ( Decimal % 100 ) // 10 ) << 8 ) | ( ( Decimal % 10 ) << 20 )

        if ( Number < 0 ) or ( Number > 999 ):
            raise( ValueError( f'Number = {Number}!' ) )
        Result |= ( ( Number // 100 ) << 16 ) | ( ( ( Number % 100 ) // 10 ) << 28 ) | ( ( Number % 10 ) << 24 )

        return Result
            
    def ParseLoochSoftVersion( BCD :int ) -> tuple:                     # 0xYYMMDDVV -> ( YYYY, MM, DD, VV )
        Year    = ( ( BCD >> 24 ) & 0xFF ) + 2000
        Month   = ( BCD >> 16 ) & 0xFF
        Day     = ( BCD >> 8 ) & 0xFF
        Vers    = ( BCD >> 0 ) & 0xFF
        return ( Year, Month, Day, Vers )

    def ParseLoochSoftVersionTxt( BCD :int ) -> str:                    # 0xYYMMDDVV -> "YYYY.MM.DD vVV"
        ( Year, Month, Day, Vers ) = ParseLoochSoftVersion( BCD )
        return f"{ Year :04d}.{ Month :02d}.{ Day :02d} v{ Vers :02d}"

if True:    # --- Функции для работы с запакованными тетрадами
    ''' Структура байтового массива с запакованными тетрадами:
    - первый байт:          количество тетрад, 0..255;
    - последующие байты:    по две тетрады, младшая тетрада на младшей позиции;
    При нечетном количестве тетрад, старшая тетрада в последнем байте не имеет смысла.
    '''
    def NibblePacket_Pack( aNibbles :list ) -> bytearray:       # упаковать список тетрад в байтовый массив
        NibblesCount = len( aNibbles )
        if NibblesCount > 255:
            NibblesCount = 255
        aPack = bytearray( 1 + ( NibblesCount + 1 ) // 2 )
        aPack[0] = NibblesCount
        for i in range( NibblesCount ):
            if 0 == i%2:
                aPack[ 1 + i//2 ] = aNibbles[i] & 0x0F
            else:
                aPack[ 1 + i//2 ] |= ( aNibbles[i] & 0x0F ) << 4
        return aPack

    def NibblePacket_Unpack( aPack :bytearray ) -> list:        # распаковать байтовый массив в список тетрад
        NibblesCount, = unpack( '=B', aPack[0:1] )
        aNibbles = [None] * NibblesCount
        for i in range( NibblesCount ):
            Pack, = unpack( '=B', aPack[ 1 + i//2 : 1 + i//2 + 1 ] )
            if 0 == i%2:
                aNibbles[i] = Pack & 0x0F
            else:
                aNibbles[i] = ( Pack >> 4 ) & 0x0F
        return aNibbles


class SKLP_Module:      # Родительский класс для модулей на интерфейсе SKLP
    class Commands:
        GetID       = 0x01
        SetID       = 0x02
        GetWorkTime = 0x07
    class ID:
        def __init__( self, Address, Serial, DevType, Version ):
            self.Address    = Address
            self.Serial     = Serial
            self.DevType    = DevType
            self.Version    = Version
    class Parse:
        GetIDv1     = '=BLL'        # Flags, Serial, SoftVersion
        GetIDv2     = '=BLHL'       # Flags, Serial, DevType, SoftVersion
        SetID       = '=LL'         # Serial, SoftVersion
            
    def __init__( self, Address, Serial = 0, DevType = 0, Version = 0, Name = 'SKLP_Module', Interface :SKLP = None ):
        self.InterfaceDefault = Interface
        self.ID     = SKLP_Module.ID( Address, Serial, DevType, Version )
        self.Flag   = 0
        self.LogMsg = None
        self.Name   = Name
        
    def __CheckInterface( self, Interface :SKLP ) -> SKLP:
        if Interface != None:
            return Interface
        if self.InterfaceDefault != None:
            return self.InterfaceDefault
        raise ValueError( 'No Interface!' )
        
    def QueryCB( self, Address, Command, Data, Interface = None ):
        if Address != self.ID.Address:
            return
        Interface = self.__CheckInterface( Interface )
        if ( Command == self.Commands.GetID ) and ( len( Data ) == 0 ):
            Interface.Answer( pack( '=BLHL', self.Flag, self.ID.Serial, self.ID.DevType, self.ID.Version ) )
            
    def Query( self, Command, Data = bytearray( ), Interface = None, Timeout = None, RecAnswer = True ):
        Interface = self.__CheckInterface( Interface )
        self.LastQueryInterface = Interface
        return Interface.Query( self.ID.Address, Command, Data, Timeout = Timeout, RecAnswer = RecAnswer )

    '''        
    def Query_GetID( self, Interface = None, Timeout = None ):
        Interface = self.__CheckInterface( Interface )
        AnswerPacket = self.Query( self.Commands.GetID, Interface = Interface, Timeout = Timeout )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == 1+4+2+4 ):
            ( self.Flag, self.ID.Serial, self.ID.DevType, self.ID.Version ) = unpack( '=BLHL', AnswerPacket[0:1+4+2+4] )
            self.LogMsg = '{}.GetID Success at 0x{:X}: Serial=0x{:X},\tDevType=0x{:X},\tVersion=0x{:X}'\
                            .format( Interface.Name, self.ID.Address, self.ID.Serial, self.ID.DevType, self.ID.Version )
            return True
        else:
            self.LogMsg = '{}.GetID Fail at 0x{:X}'.format( Interface.Name, self.ID.Address )
            return False
    '''

    def __ParseGetSetID( self, AnswerPacket, FuncName ):
        if AnswerPacket != None:
            for Parse in SKLP_Module.Parse.GetIDv1, SKLP_Module.Parse.GetIDv2:
                if len( AnswerPacket ) == calcsize( Parse ):
                    tID = unpack( Parse, AnswerPacket )
                    self.ID.Serial = tID[1]
                    if len( AnswerPacket ) == calcsize( SKLP_Module.Parse.GetIDv2 ):
                        self.ID.DevType = tID[2]
                        self.ID.Version = tID[3]
                    else:
                        self.ID.DevType = 0
                        self.ID.Version = tID[2]
                    self.LogMsg = f'{ self.LastQueryInterface.Name }.{ FuncName } Success at 0x{self.ID.Address:X}:\n'  \
                            f'Serial\t= 0x{ self.ID.Serial :08X} ({ ParseLoochSerialTxt( self.ID.Serial ) })\n'         \
                            f'DevType\t= 0x{ self.ID.DevType :04X}\n'                                                   \
                            f'Version\t= 0x{ self.ID.Version :08X} ({ ParseLoochSoftVersionTxt( self.ID.Version ) })'
                    return True
        self.LogMsg = f'{ self.LastQueryInterface.Name }.{ FuncName } Fail at 0x{ self.ID.Address:X}'
        return False

    def Query_GetID( self, Interface = None, Timeout = None ):
        AnswerPacket = self.Query( SKLP_Module.Commands.GetID, Interface = Interface, Timeout = Timeout )
        return self.__ParseGetSetID( AnswerPacket, 'GetID' )

    def Query_SetID( self, Interface = None, Timeout = None ):
        QueryData = pack( SKLP_Module.Parse.SetID, self.ID.Serial, 0 )  # Soft Version can't set
        AnswerPacket = self.Query( SKLP_Module.Commands.SetID, Data = QueryData, Interface = Interface, Timeout = Timeout )
        return self.__ParseGetSetID( AnswerPacket, 'SetID' )

            
class SKLP_ModuleInclin( SKLP_Module ):
    class Commands:
        GetID           = 0x01
        GetDataMain     = 0x13
        GetDataCalibr   = 0x14
    class Axes:
        def __init__( self, Axes :tuple = ( 0, 0, 0, 0, 0, 0 ) ):
            ( self.BX, self.BY, self.BZ, self.GX, self.GY, self.GZ ) = Axes
            
        def ToTuple( self ) -> tuple:
            return ( self.BX, self.BY, self.BZ, self.GX, self.GY, self.GZ )
            
        def __mul__( self, Value ):
            return SKLP_ModuleInclin.Axes( ( x * Value ) for x in SKLP_ModuleInclin.Axes.ToTuple( self ) )
        
    class Angles:
        def __init__( self, Angles :tuple = ( 0, 0, 0, 0, 0 ) ):
            ( self.TFG, self.TFM, self.ZENI, self.ZENIGZ, self.AZIM ) = Angles
            
        def ToTuple( self ) -> tuple:
            return ( self.TFG, self.TFM, self.ZENI, self.ZENIGZ, self.AZIM )
            
        def __mul__( self, Value ):
            return SKLP_ModuleInclin.Angles( ( x * Value ) for x in SKLP_ModuleInclin.Angles.ToTuple( self ) )
        
    def __init__( self, Interface, Serial = 0, Version = 0 ):
        SKLP_Module.__init__( self, SKLP.AddressList.Inclin, Serial, 0x1710, Version, Name = 'Inclin', Interface = Interface )
        self.DIP = 0
        self.TOTB, self.TOTG, self.TMCU = ( 0, 0, 0 )   # [x/16+56->°C]
        self.Angles = self.Angles() # [x0.01->°]
        self.IAxes = self.Axes()    # [?,?]                     после АЦП
        self.TAxes = self.Axes()    # [?,?]                     после температурной калибровки
        self.GAxes = self.Axes()    # [x0.01?->uT, x0.0001->G]  после геометрической калибровки
        
    def QueryCB( self, Address, Command, Data ):
        if Address != self.ID.Address:
            return
        Interface = self.InterfaceDefault
        if ( Command == self.Commands.GetDataMain ) and ( len( Data ) == 0 ):
            Interface.Answer( pack( '5H', *self.Angles.ToTuple() ) + pack( '3H', self.DIP, self.TOTB, self.TOTG ) )
        elif ( Command == self.Commands.GetDataCalibr ) and ( len( Data ) == 0 ):
            Interface.Answer(
                    pack( '6h', *self.IAxes.ToTuple() ) +
                    pack( '6h', *self.TAxes.ToTuple() ) +
                    pack( '6h', *self.GAxes.ToTuple() ) +
                    pack( '3H', 0, 0, self.TMCU ) )
        else:
            SKLP_Module.QueryCB( self, Address, Command, Data )

    def Query_GetDataMain( self, Timeout = None ):
        AnswerPacket = self.Query( self.Commands.GetDataMain, Timeout = Timeout )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == 8*2 ):
            self.Angles = SKLP_ModuleInclin.Angles( unpack( '5H', AnswerPacket[0:5*2] ) )
            ( self.DIP, self.TOTB, self.TOTG ) = unpack( '3H', AnswerPacket[5*2:8*2] )
            return True
        return False

    def Query_GetDataCalibr( self, Timeout = None ):
        AnswerPacket = self.Query( self.Commands.GetDataCalibr, Timeout = Timeout )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == 3*6*2+3*2 ):
            Axes = SKLP_ModuleInclin.Axes
            self.IAxes = Axes( unpack( '6h', AnswerPacket[0*6*2:1*6*2] ) )
            self.TAxes = Axes( unpack( '6h', AnswerPacket[1*6*2:2*6*2] ) )
            self.GAxes = Axes( unpack( '6h', AnswerPacket[2*6*2:3*6*2] ) )
            ( self.TA, self.TM, self.TMCU ) = unpack( '3H', AnswerPacket[3*6*2:3*6*2+3*2] )
            return True
        return False

class SKLP_ModuleGK( SKLP_Module ):
    class Commands:
        GetID           = 0x01
        GetBlockMain    = 0x13
        GetBlockTech    = 0x14
        GetBlockAux     = 0x15
    ParseGetBlockMain = '=B3B2fHHlh'
        
    def __init__( self, Interface, Serial = 0, Version = 0 ):
        SKLP_Module.__init__( self, SKLP.AddressList.VIKPB_GK, Serial, 0xF000, Version, Name = 'Gamma', Interface = Interface )
        self.GRC = 0        # [pps]     счет приведенный ко времени накоплениЯ
        self.GR = 0         # [µR/h]    мгновенное значение естественной радиоактивности
        self.dt = 0         # [ms]      интервал времени измерениЯ
        self.UHV = 0        # [V]       напряжение высоковольтника
        self.Press_kPa = 0  # [kPa]     давление затрубное
        self.Temp = 0       # [°C]      температура
        
    def QueryCB( self, Address, Command, Data ):
        if Address != self.ID.Address:
            return
        Interface = self.InterfaceDefault
        if ( Command == self.Commands.GetBlockMain ) and ( len( Data ) == 0 ):
            Interface.Answer( pack( self.ParseGetBlockMain, 0, 0, 0, 0, self.GRC, self.GR, int( self.dt ), int( self.UHV ), int( self.Press_kPa ), int( self.Temp ) ) )
        else:
            SKLP_Module.QueryCB( self, Address, Command, Data )

    def Query_GetBlockMain( self, Timeout = None ):
        AnswerPacket = self.Query( self.Commands.GetBlockMain, Timeout = Timeout )
        PacketSize = calcsize( self.ParseGetBlockMain )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( f0, id, f1, f2, self.GRC, self.GR, self.dt, self.UHV, self.Press_kPa, self.Temp ) = unpack( self.ParseGetBlockMain, AnswerPacket[0:PacketSize] )
            return True
        return False

class SKLP_Module_RUSPump( SKLP_Module ):
    class Commands:
        GetID       = 0x01
        ModeSet     = 0x11
        DataGet     = 0x13
    class Parse:
        AnDataGet       = '=BBffffffh'      # Flags, iMode, VBus, Power, MotorSpeedSet, MotorSpeed, PressSet, Press, DriveTemp
        QuModeSet       = '=B'              # iMode
        QuModeSetArg    = '=Bf'             # iMode, Argument (Speed, Press)
    dPumpModes = { 'Off': 0, 'Idle': 1, 'HoldSpeed': 2, 'HoldPress': 3 }
    class Constraints:
        PressMax                    = 1.5   # [МПа]
        MotorSpeedMin               = 1500  # [Об/мин]
        MotorSpeedMax               = 9000  # [Об/мин]
    class Data:                             # Data Packet from Command.DataGet
        def __init__( self ):
            self.Flags              = 0     # reserved
            self.iMode              = 0     # dPumpModes.values()
            self.VBus               = 0.0   # [В]
            self.MotorPower         = 0.0   # [Вт]
            self.MotorSpeedSetup    = 0.0   # [Об/мин]
            self.MotorSpeedCurrent  = 0.0   # [Об/мин]
            self.PressSetup         = 0.0   # [МПа]
            self.PressCurrent       = 0.0   # [МПа]
            self.TempDrive          = 0.0   # [°C]
        def PackForDataGet( self ):
            return pack( SKLP_Module_RUSPump.Parse.AnDataGet, self.Flags, self.iMode, self.VBus, self.MotorPower, self.MotorSpeedSetup, self.MotorSpeedCurrent, self.PressSetup, self.PressCurrent, self.TempDrive )
        def UnPackFromDataGet( self, Packet ):
            ( self.Flags, self.iMode, self.VBus, self.MotorPower, self.MotorSpeedSetup, self.MotorSpeedCurrent, self.PressSetup, self.PressCurrent, self.TempDrive ) = unpack( SKLP_Module_RUSPump.Parse.AnDataGet, Packet )

    def __init__( self, Interface, Order, Serial = 0, Version = 0 ):
        if Order == 0:      # TF = 0°
            Address = SKLP.AddressList.RUS_Pump0
            Name    = 'Pump   0°'
        elif Order == 1:    # TF = 120°
            Address = SKLP.AddressList.RUS_Pump1
            Name    = 'Pump 120°'
        elif Order == 2:    # TF = 240°
            Address = SKLP.AddressList.RUS_Pump2
            Name    = 'Pump 240°'
        elif Order == -1:   # Single Pump on Bus
            Address = SKLP.AddressList.RUS_Pump
            Name    = 'Pump Single'
        else:
            raise ValueError( 'Set order to -1, 0, 1 or 2!' )
        self.Order = Order
        self.Data = SKLP_Module_RUSPump.Data()
        SKLP_Module.__init__( self, Address, Serial, 0xF000, Version, Name = Name, Interface = Interface )

    def QueryCB( self, Address, Command, QueryPacket ):
        if Address != self.ID.Address:
            return
        Interface = self.InterfaceDefault
        if ( Command == self.Commands.DataGet ) and ( len( QueryPacket ) == 0 ):
            Interface.Answer( self.Data.PackForDataGet() )
        elif Command == self.Commands.ModeSet:
            if len( QueryPacket ) == calcsize( self.Parse.QuModeSet ):
                self.Data.iMode, = unpack( self.Parse.QuModeSet, QueryPacket[0:calcsize( self.Parse.QuModeSet )] )
                if self.Data.iMode == self.dPumpModes['Off']:
                    self.Data.PressSetup = 0
                    self.Data.MotorSpeedSetup = 0
            elif len( QueryPacket ) == calcsize( self.Parse.QuModeSetArg ):
                iMode, Arg = unpack( self.Parse.QuModeSetArg, QueryPacket[0:calcsize( self.Parse.QuModeSetArg )] )
                if iMode == self.dPumpModes['HoldSpeed']:
                    self.Data.MotorSpeedSetup = Arg
                    self.Data.iMode = iMode
                elif iMode == self.dPumpModes['HoldPress']:
                    self.Data.PressSetup = Arg
                    self.Data.iMode = iMode
        else:
            SKLP_Module.QueryCB( self, Address, Command, QueryPacket )

    def Query_DataGet( self, Timeout = None ):
        AnswerPacket = self.Query( self.Commands.DataGet, Timeout = Timeout )
        PacketSize = calcsize( self.Parse.AnDataGet )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            self.Data.UnPackFromDataGet( AnswerPacket[0:PacketSize] )
            return True
        return False

    def Query_ModeSet( self, Mode, Arg = None, Timeout = None ):
        LogStr = f'{self.Name} set to Mode \"{Mode}\"'
        if Mode in ( 'Off', 'Idle' ):
            QueryPacket = pack( self.Parse.QuModeSet, self.dPumpModes[Mode] )
        elif Mode in ( 'HoldSpeed', 'HoldPress' ):
            QueryPacket = pack( self.Parse.QuModeSetArg, self.dPumpModes[Mode], Arg )
            LogStr += f', Arg = {Arg}'
        else:
            raise ValueError( f'Set Mode to { list( self.dPumpModes.keys() ) }!' )
        print( LogStr )
        self.Query( self.Commands.ModeSet, Data = QueryPacket, Timeout = Timeout, RecAnswer = False )
        return True

class SKLP_Module_RUSTele( SKLP_Module ): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    class Commands:
        GetID           = 0x01
        GetData         = 0x13      # считать основные данные
        SetHydro        = 0x60      # установить параметры через гидроканал
        AnalogIGet      = 0x99
    ParseGetData = '=2B4Hh2B3BH'    # ответ на [0x13]
    ParseSetHydro = '=BB2H2BH'      # запрос [0x60], ответ как на [0x13]
    ParseAnalogInGet = '9f'

    class AnalogInputs:
        def __init__(self):
            self.VT     = 0
            self.VSTD   = 0
            self.VBAT   = 0
            self.VGEN   = 0
            self.VDDA   = 0
            self.Temp   = 0
            self.IPWR   = 0
            self.IBAT   = 0
            self.QBAT   = 0


    def __init__( self, Address, Interface, Serial = 0, Version = 0, GateEnable = False):
        # SKLP_Module.__init__( self, Address, Interface, Serial, Version, Name = 'RUS_Tele' )
        SKLP_Module.__init__( self, Address, Serial, 0x3500, Version, Name = 'RUS_Tele', Interface=Interface )
        self.Flags1 = 0
        self.Flags2 = 0
        self.InclZENI = 0       # [x0.01->°]    зенитный угол от инклина
        self.InclTF = 0         # [x0.01->°]    угол отклонителя от инклина
        self.TarZENI = 0        # [x0.01->°]    целевой зенитный угол
        self.TarTF = 0          # [x0.01->°]    целевой угол отклонителя
        self.GenRate = 0        # [об/мин]      обороты генератора
        self.TarForceStatic = 0 # [0..1->0..FF] целевая сила распирания
        self.TarForceCurve = 0  # [0..1->0..FF] целевая сила кривления
        self.Force = ( 0, 0, 0 )# [0..1->0..FF] расчетные усилия на лапах
        self.GR = 0             # [pps]         счет модуля гаммы
        self.GuidanceMode = 0   # []            режим наведения
        self.PipeCurrent = 0    # []            номер текущей свечки
        self.AnalogInputsData = SKLP_Module_RUSTele.AnalogInputs()
        if( GateEnable ):
            self.GateQueM2S = queue.Queue( maxsize = 1 )
            self.GateQueS2M = queue.Queue( maxsize = 1 )
            self.GateBuzy = False

    def QueryCB( self, Address, Command, Data, Interface :SKLP ):
        if Address != self.ID.Address:
            return
        if ( Command == self.Commands.GetData ) and ( len( Data ) == 0 ):
            Forces = ( ( int( f * 256 ) if f < 0.9999 else 255 ) for f in ( self.TarForceStatic, self.TarForceCurve, *self.Force ) )
            DataToPack = ( self.Flags1, self.Flags2, self.InclZENI, self.InclTF, self.TarZENI, self.TarTF, self.GenRate, *Forces, self.GR )
            try:
                Interface.Answer( pack( SKLP_Module_RUSTele.ParseGetData, *DataToPack ) )
            except struct.error as ex:
                print( 'Exception \"{}\" while packing {}'.format( ex, DataToPack ) )
        else:
            SKLP_Module.QueryCB( self, Address, Command, Data, Interface = Interface )

    def Query_GetData( self, Interface :SKLP, Timeout = None ):
        AnswerPacket = self.Query( self.Commands.GetData, Interface = Interface, Timeout = Timeout )
        PacketSize = calcsize( self.ParseGetData )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            Forces = (0,)*5
            ( self.Flags1, self.Flags2, self.InclZENI, self.InclTF, self.TarZENI, self.TarTF, self.GenRate, *Forces, self.GR ) = unpack( self.ParseGetData, AnswerPacket[0:PacketSize] )
            self.TarForceStatic, self.TarForceCurve, *self.Force = ( f / 256 for f in Forces )
            return True
        return False

    def Query_SetHydro( self, Interface :SKLP, Timeout = None ):
        try:
            Forces = tuple( ( int( f * 256 ) if f < 0.9999 else 255 ) for f in ( self.TarForceStatic, self.TarForceCurve, *self.Force ) )
            DataToPack = ( 0xFF, self.GuidanceMode, self.TarZENI, self.TarTF, Forces[0], Forces[1], self.PipeCurrent )
            QueryPacket = pack( self.ParseSetHydro, *DataToPack )
        except struct.error as ex:
            print( 'Exception \"{}\" while packing {}'.format( ex, DataToPack ) )
        AnswerPacket = self.Query( self.Commands.SetHydro, Data = QueryPacket, Interface = Interface, Timeout = Timeout )
        PacketSize = calcsize( self.ParseGetData )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            Forces = (0,)*5
            ( self.Flags1, self.Flags2, self.InclZENI, self.InclTF, self.TarZENI, self.TarTF, self.GenRate, *Forces, self.GR ) = unpack( self.ParseGetData, AnswerPacket[0:PacketSize] )
            self.TarForceStatic, self.TarForceCurve, *self.Force = ( f / 256 for f in Forces )
            return True
        return False

    def Query_Analog_Signal_Get(self, Timeout = 0.2):
        AnswerPacket = self.Query(self.Commands.AnalogIGet, Timeout = Timeout)
        PacketSize = calcsize(self.ParseAnalogInGet)
        if( ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ) ):
            (self.AnalogInputsData.VT, self.AnalogInputsData.VSTD, self.AnalogInputsData.VBAT,
             self.AnalogInputsData.VGEN, self.AnalogInputsData.VDDA, self.AnalogInputsData.Temp,
             self.AnalogInputsData.IPWR, self.AnalogInputsData.IBAT, self.AnalogInputsData.QBAT) = unpack(self.ParseAnalogInGet, AnswerPacket)
        
            self.AnalogInputsData.IBAT *= 1000
            self.AnalogInputsData.IPWR *= 1000

        else:
            print("No answer from Tele!")


class SKLP_Module_GGP_SADC( SKLP_Module ):
    ''' Протокол 0x6381 одноканального спектрометрического АЦП для ГГЛП
        Обмен по внутренней шине (без драйверов) с платой телеметрии на 460800,
        две платы подключены к разным интерфейсам и не разнесены по адресам.
        !! Добавлен тестовый протокол 0x6370 двухканальной платы без АЦП, только интегральные счета.
        !! Протокол вероятно будет пересмотрен.
        !! Реализация класса именно под 0x6370!
    '''
    class Commands:
        GetID           = 0x01
        SetMode         = 0x11
        GetDataMain     = 0x13
        GetDataTech     = 0x14
        GetSpectrum     = 0x15
        SetMode6370     = 0x21      # !! Test for 0x6370 protocol
        GetDataMain6370 = 0x23      # !! Test for 0x6370 protocol
    ParseGetDataMain6370    = '=BHHHBHH'
    ParseSetMode6370_Query  = '=BHH'
    ParseSetMode6370_Answer = '=B'
    Baud = 460800
        
    def __init__( self, Interface, Serial = 0, Version = 0 ):
        # !! Test for 0x6370 protocol
        SKLP_Module.__init__( self, SKLP.AddressList.GGLP_SADC, Serial, 0xF000, Version, Name = 'GGLP_SADC', Interface = Interface )
        self.Flag = 0           #       флаги
        self.dCntS = 0          # [p]   мгновенный счет по ближнему зонду за единицу времени
        self.dCntL = 0          # [p]   мгновенный счет по дальнему зонду за единицу времени
        self.dt = 0             # [ms]  дельта времени, за которую были накоплены мгновенные счета
        self.Temp = 0           # [°C]  температура
        self.RSD = 0            # [pps] счет по ближнему зонду за 1 с
        self.RLD = 0            # [pps] счет по дальнему зонду за 1 с
        self.Mode = 1           #       режим работы, 1 - разрешение
        self.VCompS = 0xFFFF    # [mV]  напряжение порога по ближнему зонду, 0xFFFF - Auto
        self.VCompL = 0xFFFF    # [mV]  напряжение порога по дальнему зонду, 0xFFFF - Auto
        self.GetDataMainTS = 0  # [s]   отметка времени последнего опроса
        self.Dispersion = 50    # [??]  дисперсия при эмуляции счета
        
    # Интерфес опроса слейва
    def Query_GetDataMain6370( self, Timeout = None ):
        AnswerPacket = self.Query( self.Commands.GetDataMain6370, Timeout = Timeout )
        PacketSize = calcsize( self.ParseGetDataMain6370 )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            Temp = 0
            ( self.Flag, self.dt, self.dCntS, self.dCntL, Temp, self.VCompS, self.VCompL ) = unpack( self.ParseGetDataMain6370, AnswerPacket[0:PacketSize] )
            self.Temp = Temp - 55.0
            return True
        return False

    def Query_SetMode6370( self, Timeout = None ):
        QueryPacket = pack( ParseSetMode6370_Query, self.Mode, self.VCompS, self.VCompSL )
        AnswerPacket = self.Query( self.Commands.SetMode6370, Data = QueryPacket, Timeout = Timeout )
        PacketSize = calcsize( self.ParseSetMode6370_Answer )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.Flag, ) = unpack( self.ParseSetMode6370_Answer, AnswerPacket[0:PacketSize] )
            return True
        return False

    # Интерфес ответов виртуального слейва
    def QueryCB( self, Address, Command, Data ):
        if Address != self.ID.Address:
            return
        if ( Command == self.Commands.GetDataMain6370 ) and ( len( Data ) == 0 ):
            Timestamp = time.time()
            dt = ( Timestamp - self.GetDataMainTS ) if ( self.GetDataMainTS != 0 ) else 0
            self.GetDataMainTS = Timestamp
            self.dt     = int( dt * 1000 )
            self.dCntS  = int( np.random.normal( self.RSD, self.Dispersion ) * dt )
            self.dCntL  = int( np.random.normal( self.RLD, self.Dispersion ) * dt )
            if self.dCntS < 0:
                self.dCntS = 0
            if self.dCntL < 0:
                self.dCntL = 0
            Temp = self.Temp + 55
            DataToPack = ( self.Flag, self.dt, self.dCntS, self.dCntL, Temp, self.VCompS, self.VCompL )
            Interface = self.InterfaceDefault
            try:
                Interface.Answer( pack( self.ParseGetDataMain6370, *DataToPack ) )
            except struct.error as ex:
                print( 'Exception \"{}\" while packing {}'.format( ex, DataToPack ) )
        else:
            SKLP_Module.QueryCB( self, Address, Command, Data, Interface = Interface )

class SKLP_Module_MUP( SKLP_Module ):
    SectorsCount = 16
    HydroSectorsCount = 4
    BlockAzimSizeSD = 512           # размер азимутального блока на SD-карте
    class Commands:
        Reset           = 0x00
        GetID           = 0x01
        DataGet         = 0x13      # запросить данные
        DataMainSend    = 0x18      # отправить блок основных данных
        DataAzimSend    = 0x19      # отправить блок азимутальных данных
    class Parse:
        # Answers
        DataGet         = '=BLHBBhHBBBB'
        # DataMainSend    = DataGet
        DataAzimSend    = '=B'
        DataAzimSendTest    = '=B4B'            # Flag, RHOB[4]
        DataAzimSendTest2   = '=B4f4B'          # Flag, RHO[4], RHOB[4]
        # Queries
        DataMainSend    = '=B7B16BBHBB191B'     # ID, Time, ModulesFlags, FlagsAux, FlagsInfo, Mode, Protocol, Data
        DataAzimSign    = '=5B'                 # 'START'
        DataAzimHeader  = '=B7BLHB'             # ID, Time, ModulesCurrent, FlagsInfo, Mode
        DataAzimModHeader   = '=BH'             # Address, Size
        DataAzimACP     = '=BB64B14B'           # Flag1, Flag2, DataIntg, DataInst
        DataAzimGGP     = '=B136BHB'            # Flag, GammaDataTable, TF, Temp
        DataAzimGGPSect = '=HHBBH'              # RSD, RLD, RHOB, R, dT
        DataAzimBKS     = '=BBBB96B8B8B6BHlh'   # Flag, ID, Flag1, Flag2, ResistivityTbl, ElectroData, ButtonData, GenCoil, TF, Press, Temp
        DataAzimBKSSect = '=fH'                 # Rho, dT
    class AzimGGP:
        def __init__( self ):
            self.TF         = 0
            self.Temp       = 0
            self.aRLD       = [0]*SKLP_Module_MUP.SectorsCount
            self.aRSD       = [0]*SKLP_Module_MUP.SectorsCount
            self.aRHOB      = [0]*SKLP_Module_MUP.SectorsCount
            self.adT        = [0]*SKLP_Module_MUP.SectorsCount
            self.aRHOB_Hydro= [0]*SKLP_Module_MUP.HydroSectorsCount
            AzimModHeaderSize = calcsize( SKLP_Module_MUP.Parse.DataAzimModHeader )
            self.Packet     = bytearray( calcsize( SKLP_Module_MUP.Parse.DataAzimGGP ) + AzimModHeaderSize )
            self.Packet[0:AzimModHeaderSize] = pack( SKLP_Module_MUP.Parse.DataAzimModHeader, SKLP.AddressList.GGP, calcsize( SKLP_Module_MUP.Parse.DataAzimGGP ) )
    class AzimBKS:
        def __init__( self ):
            self.aRho       = [0]*SKLP_Module_MUP.SectorsCount
            self.adT        = [0]*SKLP_Module_MUP.SectorsCount
            self.aRho_Hydro = [0]*SKLP_Module_MUP.HydroSectorsCount
            AzimModHeaderSize = calcsize( SKLP_Module_MUP.Parse.DataAzimModHeader )
            self.Packet     = bytearray( calcsize( SKLP_Module_MUP.Parse.DataAzimBKS ) + AzimModHeaderSize )
            self.Packet[0:AzimModHeaderSize] = pack( SKLP_Module_MUP.Parse.DataAzimModHeader, SKLP.AddressList.BKS, calcsize( SKLP_Module_MUP.Parse.DataAzimBKS ) )

    def __init__( self, Interface, Serial = 0, Version = 0, Name = 'MUP' ):
        SKLP_Module.__init__( self, SKLP.AddressList.MUP, Serial, 0xF000, Version, Name = Name, Interface = Interface )
        AzimModHeaderSize = calcsize( self.Parse.DataAzimModHeader )
        # Default data
        self.Time       = (0,0,0,0,0,0,0)
        self.ModFlags   = (0xFF,0xFF,0xFF,0xFF)*4
        self.FlagsInfo  = 0x0301     # Reserved0, Flow1, Flow2???
        # Azim blocks
        self.AzimGGP = SKLP_Module_MUP.AzimGGP()
        self.AzimBKS = SKLP_Module_MUP.AzimBKS()

    def QueryCB( self, Address, Command, Data ):
        if Address != self.ID.Address:
            return
        SKLP_Module.QueryCB( self, Address, Command, Data )

    def Query_Reset( self, Interface :SKLP, Timeout = None ):                       # Выполнить команду сброса модуля
        print( f'{self.Name} Reset!' )
        self.Query( self.Commands.Reset, Interface = Interface, Timeout = Timeout )

    def Query_DataGet( self, Interface :SKLP, Timeout = None ):                     # Принять блок данных от МУП
        AnswerPacket = self.Query( self.Commands.DataGet, Interface = Interface, Timeout = Timeout )
        PacketSize = calcsize( self.Parse.DataGet )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.Flags, self.Modules, self.FInfo, self.Mode, self.Protocol, self.IPRS, self.FGen, self.VGen, self.VibroAP, self.VibroAS, self.Temp ) = unpack( self.Parse.DataGet, AnswerPacket[0:PacketSize] )
            return True
        return False

    def Query_DataMainSend( self, Interface :SKLP, Timeout = None ):                # Отправить основной блок в МУП (тест, устанавливаются только флаги модулей и режим работы)
        PacketSize = calcsize( self.Parse.DataMainSend )
        DataToSend = bytearray( PacketSize )
        DataToSend = pack( self.Parse.DataMainSend, 0, *self.Time, *self.ModFlags, 0, self.FlagsInfo, 6, 0, *((0,)*191) )
        
        AnswerPacket = self.Query( self.Commands.DataMainSend, Data = DataToSend, Interface = Interface, Timeout = Timeout )
        PacketSize = calcsize( self.Parse.DataGet )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.Flags, self.Modules, self.FInfo, self.Mode, self.Protocol, self.IPRS, self.FGen, self.VGen, self.VibroAP, self.VibroAS, self.Temp ) = unpack( self.Parse.DataGet, AnswerPacket[0:PacketSize] )
            return True
        return False

    def Query_DataAzimSendImage( self, Image, Interface :SKLP, Timeout = None ):    # Отправить азимутальный блок в МУП
        AnswerPacket = self.Query( self.Commands.DataAzimSend, Data = Image, Interface = Interface, Timeout = Timeout )
        PacketSize = calcsize( self.Parse.DataAzimSendTest2 )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.Flags, self.AzimBKS.aRho_Hydro[0], self.AzimBKS.aRho_Hydro[1], self.AzimBKS.aRho_Hydro[2], self.AzimBKS.aRho_Hydro[3], self.AzimGGP.aRHOB_Hydro[0], self.AzimGGP.aRHOB_Hydro[1], self.AzimGGP.aRHOB_Hydro[2], self.AzimGGP.aRHOB_Hydro[3] ) = unpack( self.Parse.DataAzimSendTest2, AnswerPacket[0:PacketSize] )
            return True
        return False

    def Query_DataAzimSend( self, Interface :SKLP, Timeout = None ):                # заполнить азимутальный блок по данным из self.AzimGGP, self.AzimBKS и т.п., отправить в МУП
        DataToSend = bytearray(512-5)
        AzimModHeaderSize = calcsize( self.Parse.DataAzimModHeader )
        # Fill AzimGGP
        Pos = calcsize( self.Parse.DataAzimHeader )
        Pos += AzimModHeaderSize + calcsize( self.Parse.DataAzimACP )
        SectorSize = calcsize( self.Parse.DataAzimGGPSect )
        for i in range( SKLP_Module_MUP.SectorsCount ):
            self.AzimGGP.Packet[ AzimModHeaderSize+1+i*SectorSize :] = pack( self.Parse.DataAzimGGPSect, int( self.AzimGGP.aRLD[i] ), int( self.AzimGGP.aRSD[i] ), int( self.AzimGGP.aRHOB[i] ), i*17, self.AzimGGP.adT[i] )   # replace 0x1111 -> RSD, 0x2222 -> RLD, ii -> R
        DataToSend[Pos:Pos+len(self.AzimGGP.Packet)] = self.AzimGGP.Packet
        # Fill AzimBKS
        Pos = calcsize( self.Parse.DataAzimHeader )
        Pos += AzimModHeaderSize + calcsize( self.Parse.DataAzimACP )
        Pos += AzimModHeaderSize + calcsize( self.Parse.DataAzimGGP )
        SectorSize = calcsize( self.Parse.DataAzimBKSSect )
        for i in range( SKLP_Module_MUP.SectorsCount ):
            self.AzimBKS.Packet[ AzimModHeaderSize+4+i*SectorSize :] = pack( self.Parse.DataAzimBKSSect, self.AzimBKS.aRho[i], self.AzimBKS.adT[i] )
        DataToSend[Pos:Pos+len(self.AzimBKS.Packet)] = self.AzimBKS.Packet

        return self.Query_DataAzimSendImage( Image = DataToSend, Interface = Interface, Timeout = Timeout )

    def ParseAzimBlock( self, BlockSD ):    # Распарсить азимутальный блок в данные ГГП, БКС и т.п.
        BlockLenReq = SKLP_Module_MUP.BlockAzimSizeSD
        BlockLenInput = len( BlockSD )
        if( BlockLenInput != BlockLenReq ):
            raise ValueError( f'Block size must be {BlockLenReq} B, not {BlockLenInput} B!' )
        SignatureReq = b'START'
        SignatureInput = BlockSD[0:5]
        if SignatureInput != SignatureReq:
            raise ValueError( f'Block signature must be \"{SignatureReq}\", not {SignatureInput}!' )
            

        Parse = SKLP_Module_MUP.Parse
        AzimModHeaderSize = calcsize( Parse.DataAzimModHeader )
        AzimHeaderSize  = calcsize( Parse.DataAzimHeader )
        AzimOffsetHeader= calcsize( Parse.DataAzimSign )
        AzimOffsetAKP   = AzimOffsetHeader + AzimHeaderSize
        AzimOffsetGGP   = AzimOffsetAKP + AzimModHeaderSize + calcsize( Parse.DataAzimACP )
        AzimOffsetBKS   = AzimOffsetGGP + AzimModHeaderSize + calcsize( Parse.DataAzimGGP )
        AzimOffsetGK    = AzimOffsetGGP + AzimModHeaderSize + calcsize( Parse.DataAzimBKS )

        aDT = [0]*7     # YY,MM,DD,hh,mm,ss,zz
        ( ID, *aDT, ModulesCurrent, FlagsInfo, Mode ) = unpack( Parse.DataAzimHeader, BlockSD[AzimOffsetHeader:AzimOffsetHeader+AzimHeaderSize] )
        self.AzimDateTime = datetime.datetime( aDT[0]+2000, aDT[1], aDT[2], aDT[3], aDT[4], aDT[5], aDT[6]*10000 )

        for ( Address, Size, Offset ) in [
                ( SKLP.AddressList.GGP, calcsize( Parse.DataAzimGGP ), AzimOffsetGGP ),
                ( SKLP.AddressList.BKS, calcsize( Parse.DataAzimBKS ), AzimOffsetBKS ) ]:
            ( PackAddress, PackSize ) = unpack( Parse.DataAzimModHeader, BlockSD[Offset:Offset+AzimModHeaderSize] )
            if PackAddress == 0xFF and PackSize == 0xFFFF:
                raise ValueError( f'Address = 0x{PackAddress:02X}, Size = 0x{PackSize:04X}' )
            if PackAddress == Address and PackSize == Size:
                if Address == SKLP.AddressList.GGP:
                    Dest = self.AzimGGP
                    Packet = BlockSD[Offset+AzimModHeaderSize:Offset+AzimModHeaderSize+Size]
                    DataTable = []
                    ( Flag, *DataTable, Dest.TF, Dest.Temp ) = unpack( Parse.DataAzimGGP, Packet )
                    SectorSize = calcsize( Parse.DataAzimGGPSect )
                    for i in range( SKLP_Module_MUP.SectorsCount ):
                        ( Dest.aRSD[i], Dest.aRLD[i], Dest.aRHOB[i], R, Dest.adT[i] ) = unpack( Parse.DataAzimGGPSect, Packet[1+i*SectorSize:1+(i+1)*SectorSize] )
                    print( f'TF = {Dest.TF}°\tRHOB = {Dest.aRHOB}\tdT = {Dest.adT}' )
                elif Address == SKLP.AddressList.BKS:
                    Dest = self.AzimBKS
                    Packet = BlockSD[Offset+AzimModHeaderSize:Offset+AzimModHeaderSize+Size]
                    SectorSize = calcsize( Parse.DataAzimBKSSect )
                    for i in range( SKLP_Module_MUP.SectorsCount ):
                        ( Dest.aRho[i], Dest.adT[i] ) = unpack( Parse.DataAzimBKSSect, Packet[4+i*SectorSize:4+(i+1)*SectorSize] )
                    print( f'TF = {0}°\tRho = {Dest.aRho}\tdT = {Dest.adT}' )
            else:
                if Address == SKLP.AddressList.GGP:
                    self.AzimGGP = SKLP_Module_MUP.AzimGGP()
                elif Address == SKLP.AddressList.BKS:
                    self.AzimBKS = SKLP_Module_MUP.AzimBKS()
            
class SKLP_ModuleMP( SKLP_Module ):
    class Commands:
        GetID           = 0x01
        SetID           = 0x02
        GetWorkTime     = 0x07
        GetData         = 0x13
        GetTech         = 0x14
        WriteTech       = 0x15
        GetData2        = 0xF0
        Control         = 0x44
        TestEEPROM      = 0x46
    class Parse:
        GetID           = '=HBLL'       # Num, Flags1, Serial, SoftVersion
        GetWorkTime     = '=HBBHH'      # Num, Flags1, Sign, WorkTime, CRC
        GetData         = '=HBBBBBB'    # Num, Flags1, Flags2, SpentCap, Voltage, Current, WorkMode
        GetTech         = '=HB2B6HL'    # Num, Flags1, CanCharge, ID, K_I, K_U, K_Q, IMax, UNom, QNom, Date
        TestEEPROM      = '=HLHL'       # Num, EE_AddressNext, EE_WrittenElements, WorkTimeTicks
        qSimple         = '=H'          # Num
        qSetID          = '=HLL'        # Num, Serial, SoftVersion
        qWriteTech      = '=H2B6HL'     # Num, CanCharge, ID, K_I, K_U, K_Q, IMax, UNom, QNom, Date
        qControl        = '=HBB'        # Num, Cmd, Arg
    class Data:
        def __init__( self ):
            self.SpentCap   = 0         # [0.2 Ah]  [Ah]
            self.Voltage    = 0         # [0.1 V]   [V]
            self.Current    = 0         # [0.02 A]  [A]
    class DataTech:
        def __init__( self ):
            self.CanCharge  = 0         # [bool]
            self.ID         = 0         # [0..4]
            self.K_I        = 0         #
            self.K_U        = 0         #
            self.K_Q        = 0         #
            self.IMax       = 0         # [0.001 A]
            self.UNom       = 0         # [0.01 V]
            self.QNom       = 0         # [0.001 Ah]
            self.Date       = 0         # [DDMMYYYY]???
        def GetAll( self ):
            return ( self.CanCharge, self.ID, self.K_I, self.K_U, self.K_Q, self.IMax, self.UNom, self.QNom, self.Date )

    class Timeouts:
        Default = 0.05
        Search  = 2.0
        Write   = 0.25
        
    def __init__( self, Interface, Serial = 0, Version = 0 ):
        # SKLP_Module.__init__( self, SKLP.AddressList.MP_18V_Broadcast, Serial, 0xF000, Version, Name = 'МП18', Interface = Interface )
        SKLP_Module.__init__( self, SKLP.AddressList.MP_18V, Serial, 0xF000, Version, Name = 'МП18', Interface = Interface )
        self.DataRaw    = SKLP_ModuleMP.Data()
        self.DataNorm   = SKLP_ModuleMP.Data()
        self.Tech       = SKLP_ModuleMP.DataTech()
        
    def __ParseGetID__( self, AnswerPacket, ApplyNewNum = False ):
        Parse = self.Parse.GetID
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( Num, self.Flags1, self.SerialBCD, self.SoftVersionBCD ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            if ApplyNewNum:
                self.ID.Num = Num
            if Num == self.ID.Num:
                return True
        return False
    
    def __ParseGetData__( self, AnswerPacket ):
        Parse = self.Parse.GetData
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( Num, self.Flags1, self.Flags2, self.DataRaw.SpentCap, self.DataRaw.Voltage, self.DataRaw.Current, self.WorkMode ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            self.DataNorm.SpentCap  = 0.2 * self.DataRaw.SpentCap
            self.DataNorm.Voltage   = 0.1 * self.DataRaw.Voltage
            self.DataNorm.Current   = 0.02 * self.DataRaw.Current
            if Num == self.ID.Num:
                return True
        return False
    
    def __ParseGetTech__( self, AnswerPacket ):
        Parse = self.Parse.GetTech
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( Num, self.Flags1, self.Tech.CanCharge, self.Tech.ID, self.Tech.K_I, self.Tech.K_U, self.Tech.K_Q, self.Tech.IMax, self.Tech.UNom, self.Tech.QNom, self.Tech.Date ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            if Num == self.ID.Num:
                return True
        return False

    def Query_SearchSingle( self ):
        self.ID.Address = SKLP.AddressList.MP_18V_Broadcast
        AnswerPacket = self.Query( self.Commands.GetID, Timeout = self.Timeouts.Search )
        if self.__ParseGetID__( AnswerPacket, ApplyNewNum = True ):
            self.ID.Address = SKLP.AddressList.MP_18V
            return True
        return False

    def Query_GetID( self ):
        AnswerPacket = self.Query( self.Commands.GetID, pack( self.Parse.qSimple, self.ID.Num ), Timeout = self.Timeouts.Default )
        return self.__ParseGetID__( AnswerPacket )

    def Query_SetID( self, NewSerial, NewSoftVersion ):
        ( NewYear, NewDecimal, NewNumber ) = ParseLoochSerial( NewSerial )
        AnswerPacket = self.Query( self.Commands.SetID, pack( self.Parse.qSetID, self.ID.Num, NewSerial, NewSoftVersion ), Timeout = self.Timeouts.Write )
        if self.__ParseGetID__( AnswerPacket, ApplyNewNum = True ):
            if NewNumber == self.ID.Num:
                return True
        return False

    def Query_GetWorkTime( self ):
        AnswerPacket = self.Query( self.Commands.GetWorkTime, pack( self.Parse.qSimple, self.ID.Num ), Timeout = self.Timeouts.Default )
        Parse = self.Parse.GetWorkTime
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( Num, self.Flags1, Sign, self.WorkTime, CRC ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            if Num == self.ID.Num:
                return True
        return False

    def Query_GetData( self ):
        AnswerPacket = self.Query( self.Commands.GetData, pack( self.Parse.qSimple, self.ID.Num ), Timeout = self.Timeouts.Default )
        return self.__ParseGetData__( AnswerPacket )

    def Query_GetData2( self ):
        AnswerPacket = self.Query( self.Commands.GetData2, pack( self.Parse.qSimple, self.ID.Num ), Timeout = self.Timeouts.Default )
        return self.__ParseGetData__( AnswerPacket )

    def Query_GetTech( self ):
        AnswerPacket = self.Query( self.Commands.GetTech, pack( self.Parse.qSimple, self.ID.Num ), Timeout = self.Timeouts.Default )
        return self.__ParseGetTech__( AnswerPacket )

    def Query_WriteTech( self, Tech ):          # Tech : SKLP_ModuleMP.DataTech
        AnswerPacket = self.Query( self.Commands.WriteTech, pack( self.Parse.qWriteTech, self.ID.Num, *Tech.GetAll() ), Timeout = self.Timeouts.Write )
        return self.__ParseGetTech__( AnswerPacket )

    def Query_Control( self, Command, Arg ):
        AnswerPacket = self.Query( self.Commands.Control, pack( self.Parse.qControl, self.ID.Num, Command, Arg ), Timeout = self.Timeouts.Default )
        return self.__ParseGetData__( AnswerPacket )
        
    def Query_TestEEPROM( self ):
        AnswerPacket = self.Query( self.Commands.TestEEPROM, pack( self.Parse.qSimple, self.ID.Num ), Timeout = self.Timeouts.Default )
        Parse = self.Parse.TestEEPROM
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( Num, self.EE_AddressNext, self.EE_WrittenElements, self.WorkTimeTicks ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            if Num == self.ID.Num:
                return True
        return False

class SKLP_ModuleMPI( SKLP_Module ):
    class Commands:
        GetID           = 0x01
        NVM_Get         = 0x04
        NVM_Set         = 0x05
        GetDataMain     = 0x13
        GetDataTech     = 0x14
        GetDataGamma    = 0x17
        GetDataInclin   = 0x19
        GetDataAzim     = 0x1E
        GetDataBundle   = 0x1D
        MemoryErase     = 0x20
        MemoryGetState  = 0x21
        MemoryRead      = 0x22
        EventsRead      = 0x28
        EventsClear     = 0x29
        ToolReconStart  = 0x40
        MemoryInfoGet   = 0x41
        ModeGet         = 0x43
        ModeSet         = 0x44
        ToolReconSave   = 0x49
        ToolReconGetRAM = 0x4C
        ToolReconGetNVM = 0x4D
        ToolInfoGet     = 0x4E
        
    class Parse:
        GetID           = '=BLHL'       # Flags, Serial, SoftVersion
        ModeGet         = '=BB'         # Flags, Mode
        ToolReconStart  = '=BB'         # Error, FlagsMemory
        ToolReconGet    = '=BBBLLL32L32H32BB'   # FlagsInit, FlagsMemory, Format, ModCurr, ModResp, ModRespErr, aSerials, aWorkTime, aMemFlags, CRC
        ToolReconGet_v1 = '=BBBLLL32L32H32B32H32L32B'   # FlagsInit, FlagsMemory, Format, ModCurr, ModResp, ModRespErr, aSerials, aWorkTime, aMemFlags, DevTypes, SoftVers, CmdFails
        ToolReconGetHeader      = '=BBBLLL'     # FlagsInit, FlagsMemory, Format, ModCurr, ModResp, ModRespErr
        ToolReconGetSerials     = '=32L'        # aSerials
        ToolReconGetWorkTime    = '=32H'        # aWorkTime
        ToolReconGetMemFlags    = '=32B'        # aMemFlags
        ToolReconGetDevTypes    = '=32H'        # DevType
        ToolReconGetSoftVers    = '=32L'        # Soft Versions
        ToolReconGetCmdFails    = '=32B'        # Command Fails
        qModeSet        = '=B'          # Mode
        MemoryInfo      = '=BBBBBBHHBBB10B10B12B12B4B'  # SKLP_MemInfo_t v0 без CRC8, но с двумя лидирующими флагами
        MemoryInfo_Hdr  = '=BBBBBBHHBBB'                # FlagsInit, FlagsMemory, Format, TypeBB, TypeTech, TypeData, MemSize_MB, SectorSize_B, DiskCnt, FlagsDisk0, FlagsDisk1
        MemoryInfo_Log  = '=LLH'                        # SKLP_MemInfo_StructLog_t:     iSectorFirst, iSectorLast, iLastByte
        MemoryInfo_Data = '=LL4B'                       # SKLP_MemInfo_StructData_t:    iSectorFirst, iSectorLast, Alias
    class Data:
        def __init__( self ):
            pass
    class ToolReconResult:
        def __init__( self ):
            self.ModCurr    = 0
            self.ModResp    = 0
            self.ModRespErr = 0
            self.aSerials   = [None]*32
            self.aWorkTime  = [None]*32
            self.aMemFlags  = [None]*32
            # Info v1
            self.aDevTypes  = [None]*32
            self.aSoftVers  = [None]*32
            self.aCmdFails  = [None]*32
    class MemoryInfo:
        class StuctLog:
            def __init__( self ):
                self.iSectorFirst   = 0
                self.iSectorLast    = 0
                self.iLastByte      = 0
        def __init__( self ):
            self.FlagsInit      = 0
            self.FlagsMemory    = 0
            self.Format         = 0
            self.FlagsDisk0     = 0
            self.FlagsDisk1     = 0
            self.StructBB       = StuctLog()
            self.StructTech     = StuctLog()
    class Timeouts:
        Default     = 0.05
        ToolRecon   = 10.0      # 2 с для МП-18 и МП-36; 6х1 с для опроса остальных
        GetInfo     = 0.20
        SaveInfo    = 1.0
        
    dModes = { 'NotAuto' : 0, 'Auto' : 1, 'AutoDrilling' : 6, 'AutoLogging' : 7, }
    aModuleNames = [
        'Inclin',       # 0
        'Gamma',        # 1
        'VIKPB',        # 2
        'GGKP',         # 3
        'NNKT',         # 4
        'BK',           # 5
        'AK',           # 6
        'INGK',         # 7
        'MP18_0',       # 8
        'MP18_1',       # 9
        'MP18_2',       # 10
        'MP18_3',       # 11
        'AKP',          # 12
        'NDM',          # 13
        'MPI',          # 14
        'MUP',          # 15
        'VIK_GK',       # 16
        'MP36_0',       # 17
        'MP36_1',       # 18
        'MP36_2',       # 19
        'MP36_3',       # 20
        'NNKText',      # 21
        '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ]
    # dModules = { 'Inclin' : 0, 'Gamma' : 1, }
        
    def __init__( self, Interface, Serial = 0, Version = 0 ):
        SKLP_Module.__init__( self, SKLP.AddressList.MPI, Serial, 0xF000, Version, Name = 'МПИ', Interface = Interface )
        self.ToolRecon = SKLP_ModuleMPI.ToolReconResult()
        
    def Query_GetID( self ):
        AnswerPacket = self.Query( self.Commands.GetID, Timeout = self.Timeouts.Default )
        Parse = self.Parse.GetID
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.Flags, self.SerialBCD, self.DevType, self.SoftVersionBCD ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            return True
        return False

    def __ParseModeGet__( self, AnswerPacket ):
        Parse = self.Parse.ModeGet
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.Flags, iMode ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            self.Mode = list( self.dModes.keys() )[ list( self.dModes.values() ).index( iMode ) ]
            return True
        return False

    def Query_ModeGet( self ):
        AnswerPacket = self.Query( self.Commands.ModeGet, Timeout = self.Timeouts.Default )
        return( self.__ParseModeGet__( AnswerPacket ) )

    def Query_ModeSet( self, Mode ):
        AnswerPacket = self.Query( self.Commands.ModeSet, pack( self.Parse.qModeSet, self.dModes[ Mode ] ), Timeout = self.Timeouts.Default )
        return( self.__ParseModeGet__( AnswerPacket ) )

    def Query_ToolReconStart( self ):
        AnswerPacket = self.Query( self.Commands.ToolReconStart, Timeout = self.Timeouts.Default )
        Parse = self.Parse.ToolReconStart
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            ( self.ReconStartErr, self.FlagsMemory ) = unpack( Parse, AnswerPacket[0:PacketSize] )
            return True
        return False

    def __Query_ToolReconGet_v0__( self, Command, Timeout = Timeouts.Default ):
        AnswerPacket = self.Query( Command, Timeout = Timeout )
        Parse = self.Parse.ToolReconGet
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            TR = self.ToolRecon
            iNext = 0
            # Assembling Info v0
            iNext, ( F1, F2, Format, TR.ModCurr, TR.ModResp, TR.ModRespErr ) = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetHeader )
            iNext, ( *TR.aSerials, )    = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetSerials )
            iNext, ( *TR.aWorkTime, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetWorkTime )
            iNext, ( *TR.aMemFlags, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetMemFlags )
            # Skip CRC
            return True
        return False

    def Query_ToolReconGet_FromRAM( self ):
        return self.__Query_ToolReconGet_v0__( self.Commands.ToolReconGetRAM )

    def Query_ToolReconGet_FromNVM( self ):
        return self.__Query_ToolReconGet_v0__( self.Commands.ToolReconGetNVM )

    def Query_ToolReconSave( self ):
        return self.__Query_ToolReconGet_v0__( self.Commands.ToolReconSave, Timeout = self.Timeouts.SaveInfo )

    def Query_ToolReconGet_v1( self ):
        AnswerPacket = self.Query( self.Commands.ToolInfoGet, pack( '=BB', 1, 0 ), Timeout = self.Timeouts.GetInfo )
        Parse = self.Parse.ToolReconGet_v1
        PacketSize = calcsize( Parse )
        if ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ):
            TR = self.ToolRecon
            iNext = 0
            # Assembling Info v0
            iNext, ( F1, F2, Format, TR.ModCurr, TR.ModResp, TR.ModRespErr ) = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetHeader )
            iNext, ( *TR.aSerials, )    = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetSerials )
            iNext, ( *TR.aWorkTime, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetWorkTime )
            iNext, ( *TR.aMemFlags, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetMemFlags )
            # No v0 CRC
            # Assembling Info v1 addendum
            iNext, ( *TR.aDevTypes, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetDevTypes )
            iNext, ( *TR.aSoftVers, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetSoftVers )
            iNext, ( *TR.aCmdFails, )   = ParseBlock( AnswerPacket, iNext, self.Parse.ToolReconGetCmdFails )
            return True
        return False

    def Query_MemoryInfo( self ):
        if False:   # сырье
            AnswerPacket = self.Query( self.Commands.MemoryInfoGet, Timeout = self.Timeouts.Default )
            Parse = self.Parse.MemoryInfo
            PacketSize = calcsize( Parse )
            if ( AnswerPacket != None ) and ( len( AnswerPacket ) >= PacketSize ):
                MI = self.MemoryInfo
                iNext = 0
                # Memory Info v0
                iNext, ( MI.FlagsInit, MI.FlagsMemory, MI.Format, TypeBB, TypeTech, TypeData, MemSize_MB, SectorSize_B, DiskCnt, MI.FlagsDisk0, MI.FlagsDisk1 ) = ParseBlock( AnswerPacket, iNext, self.Parse.MemoryInfo_Hdr )
                print( MI.FlagsInit )
                print( MI.FlagsMemory )
                print( MI.Format )
                print( MI.FlagsDisk0 )
                print( MI.FlagsDisk1 )
                return True
            return False




class SKLP_Module_RUS_Regul( SKLP_Module ):
    class Commands:
        GetID               = 0x01 #? Отдать ID модуля
        NVM_Set             = 0x05 #? Записать данные в NVM
        DataGet             = 0x13 #? Ответ на 0x13 команду (пустой)
        ExtDataGet          = 0x14 #? Ответ на 0x14 команду
        MotorPowerOn        = 0x60 #? Команда с параметром, 0х01 - подать питание на мотор, 0х00 - снять питания
        MaxCurentSet        = 0x61 #! Не реализовано!!!
        OverlapSet          = 0x62 #? Выставить процент перекрытия - параметр процент
        StartSyncProcess    = 0x63 #? Запустить процесс синхронизации по давлению
        StartCurCalibr      = 0x64 #? Запустить калибровку по потреблению
        StabilizePress      = 0x65 #? Запустить процесс стабилизации давления
        SpeedAngleSet       = 0x71 #? Выставить скорость и угол (знаковый, отвечает за направление вращения) поворота
        SpeedSet            = 0x72 #? Выставить скорость (знаковая, овтечает за направление вращения) вращения мотора
        

    class Parse:
        #Answers
        ExtDataGet          = '=BHBbhHHHBBhlhHBHHhhhB'  #? Полный ответ на 14 команду
        ExtDataGetFlags     = '=BH'                     #? Блок флагов из 14 команды
        ExtDataGetMotor     = '=BbhHHHBB'               #? Блок данных мотора из 14 команды
        ExtDataGetPress     = '=hlhH'                   #? Блок данных давлений из 14 команды
        ExtDataGetVoltage   = '=B'                      #? Напряжение на плате из 14 команды
        ExtDataGetSyncData  = '=HHhhH'                  #? Блок данных синхронизации из 14 команды
        ExtDataGetWorkMode  = '=B'                      #? Режим работы из 14 команды
        
        #Queries
        MotorPower          = '=B'                      #? Параметр команды 60 - управление питанием мотора
        SpeedSet            = '=f'                      #? Параметр команды 72 - выставить скорость
        SpeedAndAngleSet    = '=hf'                     #? Параметр команды 71 - выставить скорость и угол
        OverlapSet          = '=h'                      #? Параметр команды 62 - выставить процент перекрытия
        StabilizePress      = '=f'                      #? Параметр команды 72 - выставить скорость
        Eeprom_Press_Coefs  = '=BBBBBBBfffH'            #? Записать коэффициенты для калибровки ДД
    
    class Motor:
        def __init__(self):
            self.Rotation       = 0
            self.SpeedSet       = 0
            self.SpeedMeas      = 0
            self.AngleSet       = 0
            self.CurPosition    = 0
            self.TimerCNTValue  = 0
            self.Current        = 0
            self.Workstate      = 0
    
    class Pressure:
        def __init__(self):
            self.Average        = 0
            self.ADCCode        = 0
            self.Instant        = 0
            self.Target         = 0

    class Synchronization:
        def __init__(self):
            self.MinAngle       = 0
            self.MaxAngle       = 0
            self.MinPress       = 0
            self.MaxPress       = 0
            self.WorkZone       = 0


    def __init__(self, Address, Interface, Name ='Regul'):
        SKLP_Module.__init__( self, Address = Address, Name = Name, Interface = Interface )
        self.MainFlag       = 0
        self.LogicalFlag    = 0
        self.MotorData      = SKLP_Module_RUS_Regul.Motor()
        self.PressData      = SKLP_Module_RUS_Regul.Pressure()
        self.PowerSupply    = 0
        self.SyncData       = SKLP_Module_RUS_Regul.Synchronization()
        self.WorkMode       = 0
        
    def __del__(self):
        print(f'Object deleted!')

    def Query_ExDataGet(self, Timeout = 0.2):
        AnswerPacket = self.Query(self.Commands.ExtDataGet, Timeout = Timeout)
        PacketSize = calcsize(self.Parse.ExtDataGet)
        if( ( AnswerPacket != None ) and ( len( AnswerPacket ) == PacketSize ) ):
            # iNext = 0

            # iNext, (self.MainFlag, self.LogicalFlag)                          = ParseBlock(AnswerPacket, iNext, self.Parse.ExtDataGetFlags)
            
            # iNext, (self.MotorData.Rotation, self.MotorData.SpeedSet,
            #         self.MotorData.SpeedMeas, self.MotorData.AngleSet,
            #         self.MotorData.CurPosition, self.MotorData.TimerCNTValue,
            #         self.MotorData.Current, self.MotorData.Workstate)         = ParseBlock(AnswerPacket, iNext, self.Parse.ExtDataGetMotor)
                    
            # iNext, (self.PressData.Average, self.PressData.ADCCode,
            #         self.PressData.Instant, self.PressData.Target)            = ParseBlock(AnswerPacket, iNext, self.Parse.ExtDataGetPress)
       
            # iNext, (self.PowerSupply)                                         = ParseBlock(AnswerPacket, iNext, self.Parse.ExtDataGetVoltage)

            # iNext, (self.SyncData.MinAngle, self.SyncData.MaxAngle,
            #         self.SyncData.MinPress, self.SyncData.MaxAngle,
            #         self.SyncData.WorkZone)                                   = ParseBlock(AnswerPacket, iNext, self.Parse.ExtDataGetSyncData)
                    
            # iNext, (self.WorkMode)                                            = ParseBlock(AnswerPacket, iNext, self.Parse.ExtDataGetWorkMode)

            # ! При использовании Parseblock, self.PowerSupply почему-то кастуется как tuple. Решить проблему пока не удалось, оставлю большой unpack, так тоже
            # ! работает

            (self.MainFlag, self.LogicalFlag, 
             
            self.MotorData.Rotation, self.MotorData.SpeedSet,self.MotorData.SpeedMeas, self.MotorData.AngleSet, self.MotorData.CurPosition, 
            self.MotorData.TimerCNTValue, self.MotorData.Current, self.MotorData.Workstate, 

            self.PressData.Average, self.PressData.ADCCode,
            self.PressData.Instant, self.PressData.Target, 

            self.PowerSupply, 

            self.SyncData.MinAngle, self.SyncData.MaxAngle,
            self.SyncData.MinPress, self.SyncData.MaxPress,
            self.SyncData.WorkZone,

            self.WorkMode) = unpack(self.Parse.ExtDataGet, AnswerPacket)
            
            self.MotorData.SpeedMeas /= 100
            self.MotorData.AngleSet /= 10
            self.MotorData.CurPosition /= 10
            self.MotorData.Current /= 100

            self.PressData.Average /= 100
            self.PressData.Instant /= 100
            self.PressData.Target /= 100

            self.PowerSupply /= 10

            self.SyncData.MinAngle /= 10
            self.SyncData.MaxAngle /= 10
            self.SyncData.MinPress /= 100
            self.SyncData.MaxPress /= 100
            self.SyncData.WorkZone /=10
            
        else:
            print("No answer on 0x14 command!")

    #? Управление питанием мотора: 1 - подать питание, 0 - снять питание
    def Query_PowerManage(self, PowerOn: str):
        if("Power_Off" == PowerOn):
            self.Query(self.Commands.MotorPowerOn, pack(self.Parse.MotorPower, 0x00))
        elif("Power_On" == PowerOn):
            self.Query(self.Commands.MotorPowerOn, pack(self.Parse.MotorPower, 0x01))
        else:
            print("Invald param!")            

    #? Задать скорость вращения
    def Query_SetSpeed(self, speed):
        self.Query(self.Commands.SpeedSet, pack(self.Parse.SpeedSet, speed))

    #? Задать угол и скорость вращения
    def Query_Set_Speed_and_Angle(self, speed, angle):
        self.Query(self.Commands.SpeedAngleSet, pack(self.Parse.SpeedAndAngleSet, speed, angle))

    #? Запустить синхронизацию по давлению
    def Query_StartSynchronizationPress(self):          
        self.Query(self.Commands.StartSyncProcess)

    #? Запустить калибровку по току потребления
    #! Формально такая функция есть, и мотор даже выполнит калибровку, только никто не планирует использовать это в скважине
    def Query_StartSynchronizationCurrent(self):        
        self.Query(self.Commands.StartCurCalibr)
    
    #? Запустить процесс удеражния давления
    def Query_StabilizePressure(self, targetPressure):  
        self.Query(self.Commands.StabilizePress, pack(self.Parse.StabilizePress, targetPressure))

    #? Управление процентом перекрытия заслонки после калибровки
    def Query_OverlapSet(self, percent):
        if((0 <= percent) and (100 >= percent)):
            self.Query(self.Commands.OverlapSet, pack(self.Parse.OverlapSet, percent))
        else:
            print("Invalid param!")
    
    #? Записать коэффициенты датчика давления в ЕЕПРОМ
    def Query_Press_Coefs_Set(self, NVM_ID, data):
        year, month, day, hour, minute, second, C2, C1, C0 = data
        CRC16 = SKLP.Calc_CRC16(data, len(data), 0)
        self.Query(self.Commands.NVM_Set, pack(self.Parse.Eeprom_Press_Coefs, NVM_ID, year, month, day, hour, minute, second, C2, C1, C0, CRC16))

class SKLP_GGLP_Spectr ( SKLP_Module ):

    class Spectr_Command:
        GET_CONFIGURATION = 0x04
        SET_CONFIGURATION = 0x05 # Установить кофигурацию
        GET_ALL_DATA_SPECTR = 0x15 # Вернуть все накопленные значения и обнулить буфер
        GET_YOUR_SERIAL = 0x01 # Вернуть свой серийный номер
    class Spectr_Signature:
        ''' класс содержащий в себе сигнатуры команды для формирования пакета '''
        START_QUERY  = 0x40
        START_ANSWER = 0x23
    class Spectr_Size:
        '''  класс содежащий в себе работу с размером пакета '''
        @staticmethod
        def get_size_packet(packet):
            ''' Метод считает длину пакета [size]
            
            :param packet: Данные, которые необходимо посчитать

            :warning: Допустим пакет выглядит так [0x40][size][0x79][0x01][CRC8]
            то метод посчитает пакет без [0x40] и [CRC8] и вернет значение для [size]

            :return: Подсчитаный размер пакета

            '''
            size_packet = packet[1:]
            format_string = f'!{len(size_packet)}B'
            size_packet = pack(format_string,*size_packet)
            return len(size_packet)
    class Spectr_Address:
        '''  класс содержащий в себе все доступные адреса на плате '''
        GET_YOUR_SEARIAL_NUMBER = 0x79
    class Spectr_CRC8( SKLP ):
        '''  класс для подсчета CRC8 '''
        def __init__(self, Timeout=0.5, Name='SKLP'):
            super().__init__(Timeout, Name)
        @staticmethod
        def count_size( packet ):
            ''' Считает CRC8

            :param packet: Пакет, у которого необходимо подсчитать CRC8
            :type packet: List  

            :return: Подсчитанный CRC пакета
            :rtype: int 
            '''
            crc = SKLP.CalcCRC8(packet)
            return crc  # Возвращаем значение CRC
    class Spectr_Packet( ):
        ''' Класс для работы с пакетом данных 
        При инициализации указать атрибуты пакета для формирования, либо применятся дефолтные
        <h3>Атрибуты:</h3>
        Signature: по дефолту 0x40\n
        Adrress: по дефолту 0x79\n
        Command: по дефолту 0x01\n
        Packet:  по дефолту None
        '''
        def __init__(self, Signature=0x40, Adrress=0x79, Command=0x01, Packet=None):
            self.Signature = Signature
            self.Size = SKLP_GGLP_Spectr.Spectr_Size()
            self.Adress = Adrress
            self.Command = Command
            self.Packet = Packet
            self.Sig40 = SKLP_GGLP_Spectr.Spectr_Signature.START_QUERY
            self.Adr79 = SKLP_GGLP_Spectr.Spectr_Address.GET_YOUR_SEARIAL_NUMBER
            self.Com01 = SKLP_GGLP_Spectr.Spectr_Command.GET_YOUR_SERIAL
            self.CRC = SKLP_GGLP_Spectr.Spectr_CRC8()
        def Debbug_print_command(self, ful_packet):
            print('debug packet : '," ".join(f"{byte:#04x}" for byte in ful_packet))
        def get_your_serial_number(self):
            '''Формирует команду запроса на получение серийного номера устройства 
            
            :return: Сформированный пакет для отправки
            '''
            format_string = f'!B B B B B'
            packet = pack(f'!B B B ',self.Sig40 ,self.Adr79, self.Com01)
            result_packet = pack(format_string, self.Sig40, self.Size.get_size_packet(packet) ,self.Adr79, self.Com01 , self.CRC.count_size(packet))
            return result_packet
            

        def push_quere(self):
            ''' Формирует пакет для отправки из данных при инициализации класса <b>Spectr_Packet</b>
            
            :return: Сформированный пакет для отправки
            '''
            format_string = f"!B B B B {len(self.Packet)}B B"
            packet = pack(f'!B B B {len(self.Packet)}B', self.Signature, self.Adress, self.Command, *self.Packet)
            result_packet = pack(format_string, self.Signature, self.Size.get_size_packet(packet), self.Adress, self.Command, *self.Packet , self.CRC.count_size(packet))
            return result_packet

    def __init__(self, Address=0, Serial=0, DevType=0, Version=0, Name='SKLP_Module', Interface: SKLP = None):
        super().__init__(Address, Serial, DevType, Version, Name, Interface)
        self.Enum_Command = SKLP_GGLP_Spectr.Spectr_Command()
        self.Enum_Signature = SKLP_GGLP_Spectr.Spectr_Signature()
        self.Enum_Addresses = SKLP_GGLP_Spectr.Spectr_Address()
        # self.Sizers = SKLP_GGLP_Spectr.Spectr_Size()
        # self.Crc_counters = SKLP_GGLP_Spectr.Spectr_CRC8()
    def get_query_your_serial_number(self):
        ''' Создает экземпляр класса <b>Spectr_Packet</b> 
        Он инициализируется со своими дефолтными значениями \n
        И делает запрос на плату о ее серийном номере \n
        CRC8 и размер посчитает сама
        '''
        query = self.Spectr_Packet()
        push_packet = query.get_your_serial_number()
        query.Debbug_print_command(push_packet)
        ### TODO Отправка на плату и ожидание ответа, вывести ответ на плату
        try:
            x = self.Query(push_packet)
            print(x)
        except ValueError as e:
            print(f'Error : {e}')
    def query_push_new_packet(self,signature, adress, command ,data):
        '''Формирует пакет для отправки из входящих параметров

        CRC8 и размер посчитает сама

        :param signature: Команда для отправки запроса или приема ответа
        :param adress: Адресс устройства, кому направлен запрос
        :param command: Команда, что необходимо сделать
        :param data: Пакет данных, который надо посчитать 


        '''
        query = self.Spectr_Packet(signature, adress, command, data)
        new_packet = query.push_quere()
        query.Debbug_print_command(new_packet)


def main():
    port = SKLP_Serial(Baud=1000000, Port='COM17')
    sklp = SKLP_GGLP_Spectr(Address=0x79, Interface=port)
    y = sklp.Query_GetID()
    print(y)
    print(sklp.LogMsg)
    print('------------------------------------------------------------------')
    x =  sklp.Query(sklp.Enum_Command.GET_ALL_DATA_SPECTR)
    print(x)
    print('Размер входящего пакета : ',len(x))
    # # print(sklp.Commands.GetID)
    # packet_data = [255, 255, 255,255,255,255,255,255,88]
    # # sklp.Spectr_CRC8().CalcCRC8(packet)
    # # print(sklp.Spectr_Address.MY_ADDRESS)
    # packet_cla = sklp.Spectr_Packet(sklp.Spectr_Signature.START_QUERY, sklp.Spectr_Address.GET_YOUR_SEARIAL_NUMBER, sklp.Spectr_Command.GET_ALL_DATA_SPECTR, packet_data)
    # packet_cla.push_quere()
    # print(packet_cla.get_your_serial_number())
    # sklp.get_query_your_serial_number()
    # print('Ждем ответ...')
    # sklp.query_push_new_packet(sklp.Enum_Signature.START_QUERY, sklp.Enum_Addresses.GET_YOUR_SEARIAL_NUMBER, sklp.Enum_Command.GET_ALL_DATA_SPECTR,packet_data)
    
    


if __name__ == '__main__':
    main()
