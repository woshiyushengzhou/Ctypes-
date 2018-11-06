from pynmprk import BaseNMPRK
from ctypes import c_ushort
import re
import subprocess
from ctypes import cdll
from nmtype import *
from df_error import *
from time import sleep
from sel_parsing_table import *
import time
import sys
from ctypes import c_byte

file_path ='/mnt/hgfs/shareTolinux/from_Sara_Last/libnmprkc.so'
dh = cdll.LoadLibrary(file_path)
nm = BaseNMPRK(dh)

def check_network(ip):
    ''' '''
    try:
        #cmd = 'ping -c 2 -w 1 %s'%ip
        cmd = 'ipmiping -c 2 %s'%ip
        p = subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout= subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        result = p.stdout.read()
        regex = re.findall(b'100.0% packet loss',result)
        if regex:
            return False
        else:
            return True
    except:
        return False


def connect_nmprk(host,usr,pwd):
    ''' return h -- the handle of connect'''

    status = check_network(host)
    if status:
        try:
            h = nm.connect_remote(host,usr,pwd)
            return h
        except :
            raise ConnectError("NM connect error")
    else:
        raise ConnectError("Network not available")

def disconnect(h):
    ''' disconnect the handle'''
    nm.disconnect(h)

def get_nm_version(h):
    ''' get NM version'''
    output = nm.get_version(h)
    if output.version == 5:
        return 'Intel NM 3.0'
    elif output.version == 4:
        return 'Intel NM 2.5'
    elif output.version == 3:
        return 'Intel NM 2.0'
    elif output.version == 2:
        return 'Intel NM 1.5'
    elif output.vetsioin ==1:
        return 'Intel NM 1.0'
    else:
        return ' '
    
def get_cups_data_util(h):
    ''' get the cups utilization average data'''
    parameter = nm_get_cups_data_parameter_t.CUPS_PARAMETER_UTILIZATION
    output = nm.get_cups_data(h,parameter)
    return output.data.util.cpu, output.data.util.memory, output.data.util.io


def get_global_power_platform(h):
    mode = nm_get_statistics_mode_t.GET_GLOBAL_POWER
    domain = nm_domain_id_t.PLATFORM
    policy = 0x00
    nm_output = nm.get_statistics(h,mode,domain,policy)
    #print nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue
    return nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue


def get_global_power_cup(h):
    mode = nm_get_statistics_mode_t.GET_GLOBAL_POWER
    domain = nm_domain_id_t.CPU
    policy = 0x00
    nm_output = nm.get_statistics(h,mode,domain,policy)
    #print nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue
    return nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue

def get_global_power_memory(h):
    mode = nm_get_statistics_mode_t.GET_GLOBAL_POWER
    domain = nm_domain_id_t.MEMORY
    policy = 0x00
    nm_output = nm.get_statistics(h,mode,domain,policy)
    #print nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue
    return nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue

def get_global_temperature_platform(h):
    mode = nm_get_statistics_mode_t.GET_GLOBAL_TEMPERATURE
    domain = nm_domain_id_t.PLATFORM
    policy = 0x00
    nm_output = nm.get_statistics(h,mode,domain,policy)
    print nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue
    return nm_output.currentValue,nm_output.minimumValue,nm_output.maximumValue

def reset_statistics_global_power(h):
    status = nm.reset_statistics(h,0,0,0)
    return status

def reset_statistics_inlet_temperature(h):
    status = nm.reset_statistics(h,1,0,0)
    return status

def power_limit(h, switch=1):
    '''
        Emergency power limit, 
        usage policy 0x01,
        target limit 0,
    '''
    try:
        nm.enable_disable_policy_control(h, 0, 0x01, 4)
    except:
        nm.set_policy(h,policyId=0x01,policyTriggerType=0,policyTargetLimit=0,correctionTimeLimit=0)
    if switch == 1:
        nm.enable_disable_policy_control(h, 0, 0x01, 5)
    else:
        nm.enable_disable_policy_control(h, 0, 0x01, 4) 

def sel_parsing(h,entryId):
    try:
        nm_output_entry = nm.ipmi_get_sel_entry(h,entryId)
    except:
        raise ConnectError("sel_parsing faild")

    #get sel entry id
    selEntryIdByte1 = nm_output_entry[1].data[0]
    selEntryIdByte2 = nm_output_entry[1].data[1]<<8
    selEntryId = hex(selEntryIdByte1 | selEntryIdByte2)

    #get record type
    record_type = nm_output_entry[1].data[2]

    #get sel entry timestamp  
    selEntryTimestampByte1 = nm_output_entry[1].data[3]
    selEntryTimestampByte2 = nm_output_entry[1].data[4]<<8
    selEntryTimestampByte3 = nm_output_entry[1].data[5]<<16
    selEntryTimestampByte4 = nm_output_entry[1].data[6]<<24
    selEntryTimestamp = (selEntryTimestampByte1 | selEntryTimestampByte2 | selEntryTimestampByte3 | selEntryTimestampByte4)

    #get generator id 2 bytes
    generatorbit1 = nm_output_entry[1].data[7]
    generatorbit2 = nm_output_entry[1].data[8]

    #get event version
    eventVersion = nm_output_entry[1].data[9]

    #get sensor type
    selEntrySensorType = nm_output_entry[1].data[10]

    #get sensor number
    selEntrySensorNumber = nm_output_entry[1].data[11]

    #get event type 
    selEntryEventType = nm_output_entry[1].data[12]
    #get event dir
    eventDirCode = (selEntryEventType >> 7) & 0x01
    eventTypeCode = selEntryEventType & 0x7f


    #get sensor datas 
    eventData1 = nm_output_entry[1].data[13]
    eventData2 = nm_output_entry[1].data[14]
    eventData3 = nm_output_entry[1].data[15]

    eventdata_all = (
            selEntryId,
            record_type,
            selEntryTimestamp,
            generatorbit1,
            generatorbit2,
            eventVersion,
            selEntrySensorType,
            selEntrySensorNumber,
            selEntryEventType,
            eventData1,
            eventData2,
            eventData3,
        )
    return eventdata_all 

def get_sensortype_str_desc(sensortype):
    return SENSOR_TYPE[sensortype-1][1]

#gen sensor class Used to confirm which data to use
def get_sensorClass(selEntryEventType):
    '''
    sensor class:
            0 threshold
            1 discrete
            2 OEM
            3 unknow
    '''
    eventtype = selEntryEventType & 0x7f
    if eventtype == 0x01:
        sensorclass = 0 
    elif 0x02<= eventtype <=0x0c:
        sensorclass = 1
    elif eventtype == 0x6f:
        sensorclass = 1
    elif 0x70<= eventtype <=0x7f:
        sensorclass = 2
    else:
        sensorclass = 3 
    return sensorclass

def get_offset_str_desc(typecode,offset,sensortype):
    '''
        typecode: event type code
        offset: description offset
        sensortype: sensor type(0x01---0x2c)
    '''
    event_offset_str_desc = "unknow"
    #typecode 0x01
    if typecode == 0x01:
        for tempdata in EVENT_TYPE_CODE_threshold:
            if tempdata[0] == typecode:
                for offset_i in tempdata[1]:
                    if offset == offset_i[0]:
                        event_offset_str_desc = offset_i[1] 
    #typecode 0x02-0x0c
    if 0x02<= typecode <=0x0c :
        for tempdata in EVENT_TYPE_CODE_generic:
            if tempdata[0] == typecode:
                for offset_i in tempdata[1]:
                    if offset == offset_i[0]:
                        event_offset_str_desc = offset_i[1] 
    #typecode 6F
    if typecode == 0x6F:
        for tempdata in EVENT_TYPE_CODE_sensorSpecific:
            if tempdata[0] == sensortype:
                for offset_i in tempdata[1]:
                    if offset == offset_i[0]:
                        event_offset_str_desc = offset_i[1] 
    if 0x70<= typecode <=0x7F:
        event_offset_str_desc = "unknow"
    return event_offset_str_desc

def get_event_dir_str_desc(eventDircode):
    if eventDircode == 1:
        eventDir = "Deasserted"
    elif eventDircode == 0:
        eventDir = "Asserted"
    else:
        eventDir = ""
    return eventDir
    
def get_event_severity(typecodep,offset,sensortype):
    '''
    sensorclass:
        0 normal/ok
        1 warning
        2 error
    only have Threshold,power supply,processor severity
    '''
    typecode = typecodep & 0x7F
    eventdir = (typecodep >> 7) & 0x01

    if typecode == 0x01:
        if offset==0x00 and eventdir == 0x00:
            return EVENT_SEVERITY_WARNING
        if offset==0x02 and eventdir == 0x00:
            return EVENT_SEVERITY_ERROR
        if offset==0x02 and eventdir == 0x01:
            return EVENT_SEVERITY_WARNING
    if typecode == 0x6F:
        if sensortype == 0x07:
            if offset == 0x0a and eventdir == 0x00:
                return EVENT_SEVERITY_WARNING
        if sensortype == 0x08:
            if offset == 0x03 and eventdir == 0x00:
                return EVENT_SEVERITY_ERROR
    return EVENT_SEVERITY_NORMAL       

def get_all_sel(h):
    #Store all log information
    sel_list = []
    #Gets the log number
    output = nm.ipmi_get_sel_info(h)
    total_sel = output.repoEntries

    for entryid in range(1,total_sel+1):
        tempdata = sel_parsing(h,entryid)
        tempdict = {
            "severity":"unknow",
            "timestamp":"unknow",
            "description":"unknow",
            "sensortype":"unknow"
        }
        #if record type is not 2 or sel version is not 4 back unknow
        if tempdata[1]!=2 or tempdata[5]!=4:
            sel_list.append(tempdict)
            continue

        #unknow sensor type
        if not (0x01<= tempdata[6] <=0x2c):
            sel_list.append(tempdict)
            continue

        #get sensor str description
        sensortype_str_desc = get_sensortype_str_desc(tempdata[6])

        #get event detail description
        typecode = tempdata[8] & 0x7F
        offset = tempdata[9] & 0x0F
        sensortype = tempdata[6]
        event_offset_str_desc = get_offset_str_desc(typecode,offset,sensortype)

        #get event dir
        eventdircode = (tempdata[8] >> 7) & 0x01
        event_dir_str_desc = get_event_dir_str_desc(eventdircode)

        #get timestamp(int)
        timestamp_str_desc = tempdata[2] 
        
        #get event severity
        offset = tempdata[9] & 0x0F
        event_severity_str_desc = get_event_severity(tempdata[8],offset,tempdata[6])

        tempdict["timestamp"] = timestamp_str_desc
        tempdict["sensortype"] = sensortype_str_desc
        #add rpm
        if tempdata[6] == 0x04:
            tempdict["description"] = "{0} | {1} {2}RPM".format(event_offset_str_desc,event_dir_str_desc,tempdata[-2]*100)
        else:
            tempdict["description"] = "{0} | {1}".format(event_offset_str_desc,event_dir_str_desc)

        tempdict["severity"] = event_severity_str_desc

        sel_list.append(tempdict)
        
    return sel_list

def get_device_model():
    '''NMPRK_IPMI_GetDeviceId Bytes 8:10 Manufacturer ID
       https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers
    '''
    try:
        nm_output = nm.ipmi_get_device_id(h)
    except:
        raise ConnectError("get device id faild")
    print "version :",nm_output.ipmiVersion

    ManufacturerIdByte1 = nm_output.manufId[0]
    ManufacturerIdByte2 = nm_output.manufId[1] << 8 
    ManufacturerIdByte3 = nm_output.manufId[2] << 16
    ManufacturerId = ManufacturerIdByte1 | ManufacturerIdByte2 | ManufacturerIdByte3
    Manufacturer = "None"
    for i in Manufacturer_ID:
        if ManufacturerId == i[0]:
            Manufacturer = i[1]
            break
    print "Product Manufacturer :",Manufacturer

def get_all_fru_area(h):
    '''
        NMPRK_IPMI_ReadFruData,poll read all data
    '''
    try:
        nm_output_info = nm.ipmi_get_fru_info(h)
    except:
        raise ConnectError("get fru info faild")
    #get fru area size
    fru_size = nm_output_info.fruSize
    #storage all fru data
    all_fru_area_data = []
    for offset in range(0,fru_size,8):
        if (fru_size - offset) < 8:
            read_once_data = nm.ipmi_read_fru_data(h,offset,fru_size-offset)
        else:
            read_once_data = nm.ipmi_read_fru_data(h,offset,8)
        all_fru_area_data.extend(read_once_data)

    return tuple(all_fru_area_data)

def get_str(offset,all_fru_area_data):
    typecode = (all_fru_area_data[offset] & 0xC0) >> 6
    #8-bit ASCII 
    if typecode == 3:
        area_len = all_fru_area_data[offset] & 0x3f
        orgstr = ""
        if area_len > 0:
            for i in range(area_len):
                #ascii trans to number
                orgstr += chr(all_fru_area_data[offset+1+i])
        offset = offset + area_len + 1
        return (orgstr,offset)
    #6-bit ASCII,BCD plus
    else:
        pass

def read_fru_main(h):
    FRU_DESC_ALL_AREA = {
        "chsassis":{
            "Chassis Type":"",
            "Chassis Part Number":"",
            "Chassis Serial":"",
            "Chassis Extra":""
        },
        "board":{
            "Board Mfg Date":"",
            "Board Mfg":"",
            "Board Product":"",
            "Board Serial":"",
            "Board Part Number":"",
            "Board FRU ID":"",
            "Board Extra":""
        },
        "product":{
            "Product Manufacturer":"",
            "Product Name":"",
            "Product Part Number":"",
            "Product Version":"",
            "Product Serial":"",
            "Product Asset Tag":"",
            "Product FRU ID":"",
            "Product Extra":"",
        }
    }
    #is fru device ?
    deviceSupport = nm.ipmi_get_device_id(h)     
    if(deviceSupport.isFruInvDev):
        all_fru_area_data = get_all_fru_area(h)
        #fro version is 0x01?   
        if all_fru_area_data[0] != 1:
            return "Unknow fru version"

        #internal area
        if all_fru_area_data[1] > 0:
            pass

        #chassis area
        if all_fru_area_data[2] > 0:
            chassis_start_offset = 8 * all_fru_area_data[2]
            offset = chassis_start_offset

            #get chassis type str
            if all_fru_area_data[offset+2] > len(Chassis_Type) - 1:
                FRU_DESC_ALL_AREA["chsassis"]["Chassis Type"] = Chassis_Type[2]
            else:
                FRU_DESC_ALL_AREA["chsassis"]["Chassis Type"] = Chassis_Type[all_fru_area_data[offset+2]]
            offset = offset + 3
            #get chassis Part Number str
            FRU_DESC_ALL_AREA["chsassis"]["Chassis Part Number"],offset = get_str(offset,all_fru_area_data)
            #get Chassis Serial str
            FRU_DESC_ALL_AREA["chsassis"]["Chassis Serial"],offset = get_str(offset,all_fru_area_data)
            #get Chassis Extra str
            if all_fru_area_data[offset] == 0xc1:
                del FRU_DESC_ALL_AREA["chsassis"]["Chassis Extra"]
            else:
                FRU_DESC_ALL_AREA["chsassis"]["Chassis Extra"],offset = get_str(offset,all_fru_area_data)

        #board area
        if all_fru_area_data[3] > 0:
            board_start_offset = 8 * all_fru_area_data[3] 
            offset = board_start_offset

            #get Board Mfg Date str
            tavltime = all_fru_area_data[offset+3] | (all_fru_area_data[offset+4]<<8) | (all_fru_area_data[offset+5]<<16)
            tavltime *= 60
            tavltime += 820454400
            time_local = time.localtime(tavltime)
            FRU_DESC_ALL_AREA["board"]["Board Mfg Date"] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            offset = offset + 3 + 3
            #get Board Mfg str
            FRU_DESC_ALL_AREA["board"]["Board Mfg"],offset = get_str(offset,all_fru_area_data)
            #get Board Product str
            FRU_DESC_ALL_AREA["board"]["Board Product"],offset = get_str(offset,all_fru_area_data)
            #get Board Serial str
            FRU_DESC_ALL_AREA["board"]["Board Serial"],offset = get_str(offset,all_fru_area_data)
            #get Board Part Number str
            FRU_DESC_ALL_AREA["board"]["Board Part Number"],offset = get_str(offset,all_fru_area_data)
            #get Board FRU ID str
            FRU_DESC_ALL_AREA["board"]["Board FRU ID"],offset = get_str(offset,all_fru_area_data)
            #get Board Extra str
            if all_fru_area_data[offset] == 0xc1:
                del FRU_DESC_ALL_AREA["board"]["Board Extra"]
            else:
                FRU_DESC_ALL_AREA["board"]["Board Extra"],offset = get_str(offset,all_fru_area_data)

        #product area
        if all_fru_area_data[4] > 0:
            product_start_offset = 8 * all_fru_area_data[4] 
            offset = product_start_offset
            offset = offset + 3
            #get Product Manufacturer str
            FRU_DESC_ALL_AREA["product"]["Product Manufacturer"],offset = get_str(offset,all_fru_area_data)
            #get Product Name str
            FRU_DESC_ALL_AREA["product"]["Product Name"],offset = get_str(offset,all_fru_area_data)
            #get Product Part Number str
            FRU_DESC_ALL_AREA["product"]["Product Part Number"],offset = get_str(offset,all_fru_area_data)
            #get Product Version str
            FRU_DESC_ALL_AREA["product"]["Product Version"],offset = get_str(offset,all_fru_area_data)
            #get Product Serial str
            FRU_DESC_ALL_AREA["product"]["Product Serial"],offset = get_str(offset,all_fru_area_data)
            #get Product Asset Tag str
            FRU_DESC_ALL_AREA["product"]["Product Asset Tag"],offset = get_str(offset,all_fru_area_data)
            #get Product FRU ID str
            FRU_DESC_ALL_AREA["product"]["Product FRU ID"],offset = get_str(offset,all_fru_area_data)
            #get Product Extra str
            if all_fru_area_data[offset] == 0xc1:
                del FRU_DESC_ALL_AREA["product"]["Product Extra"]
            else:
                FRU_DESC_ALL_AREA["product"]["Product Extra"],offset = get_str(offset,all_fru_area_data)
            
        #multi area
        if all_fru_area_data[5] > 0:
            pass
        return FRU_DESC_ALL_AREA
    else:
        return "Unsupport fru" 
    return FRU_DESC_ALL_AREA


def power_contrl(h,commandtype):
    '''
    commandtype : 0  power off
    commandtype : 1  power on
    commandtype : 2  power cycle 
    commandtype : 3  hard reset 
    commandtype : 4  pulse diagnostc interrupt 
    commandtype : 5  initiate a soft-shundown of OS via ACPI by emulating a fatal overtemperature 
    '''
    if 0 <= commandtype <=5:
        nm.ipmi_power_contrl(h,commandtype)
    else:
        return "Invalid chassis power command"

def power_status(h):
    try:
        status = nm.ipmi_power_status(h)
    except:
        raise ConnectError("get power status failed")
    if status.value==0:
        return "power off"
    if status.value==1:
        return "power on"
    return "Unknow status"


def get_actual_value(number,length):
    try:
        i = number & 1<<(length-1)
    except e as ValueError:
        i = 0
    #positive
    if i == 0:
        return number
    #negative
    else:
        k = 1 
        res = 1
        while k!=length:
            res = res<<1 | 1
            k += 1
        res = number ^ res
        res += 1
        #print "res is :",res
        return -1 * res
def get_calculate_factor(output_data):
    i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
    M = get_actual_value(i,10)
    #constant ,signed,4bit
    i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
    B = get_actual_value(i,10)
    i = output_data.data[24] & 0xf
    B1 = get_actual_value(i,4)
    #accuracy ,signed,4bit
    i = (output_data.data[24] & 0xf0) >> 4
    B2 = get_actual_value(i,4)
    return (M,B,B1,B2)
    
def get_lower_non_cirtical_value(output_data):
#    if output_data.data[5] & 0x10 == 0x10 and (output_data.data[15]>>6 & 3 == 2):
    if output_data.data[5] & 0x10 == 0x10:
        if output_data.data[14] & 0x01 == 1:
            #get M,B ,signed,10bit
            i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
            M = get_actual_value(i,10)
            #constant ,signed,4bit
            i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
            B = get_actual_value(i,10)
            i = output_data.data[24] & 0xf
            B1 = get_actual_value(i,4)
            #accuracy ,signed,4bit
            i = (output_data.data[24] & 0xf0) >> 4
            B2 = get_actual_value(i,4)
            #sensor type
            #Temperature 1,Voltage 2,Current 3,Fan 4
            if output_data.data[7] in (1,2,3,4):
                #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                #return ((M*c_byte(output_data.data[36]).value)+B*pow(10,B1))*pow(10,B2)
                if output_data.data[15]>>6 & 3 == 0:
                    return ((M*output_data.data[36])+B*pow(10,B1))*pow(10,B2)
                else:
                    return ((M*c_byte(output_data.data[36]).value)+B*pow(10,B1))*pow(10,B2)

        else:
            return r"N/A"
    else:
        return r"N/A"

def get_lower_cirtical_value(output_data):
    if output_data.data[5] & 0x10 == 0x10:
        if output_data.data[14] & 0x02 == 0x02:
            #get M,B
            #get M,B ,signed,10bit
            i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
            M = get_actual_value(i,10)
            #print "M is {0}".format(M)
            
            #constant ,signed,4bit
            i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
            B = get_actual_value(i,10)
            i = output_data.data[24] & 0xf
            B1 = get_actual_value(i,4)
            #accuracy ,signed,4bit
            i = (output_data.data[24] & 0xf0) >> 4
            B2 = get_actual_value(i,4)
            #sensor type
            #Temperature
            if output_data.data[7] in (1,2,3,4):
                #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                #return ((M*c_byte(output_data.data[35]).value)+B*pow(10,B1))*pow(10,B2)
                if output_data.data[15]>>6 & 3 == 0:
                    return ((M*output_data.data[35])+B*pow(10,B1))*pow(10,B2)
                else:
                    return ((M*c_byte(output_data.data[35]).value)+B*pow(10,B1))*pow(10,B2)
                #return (M*output_data.data[35]+B*pow(10,B1))*pow(10,B2)
        else:
            return r"N/A"
    else:
        return r"N/A"

def get_lower_non_recoverable_value(output_data):
    if output_data.data[5] & 0x10 == 0x10:
        if output_data.data[14] & 0x04 == 0x04:
            #get M,B
            #get M,B ,signed,10bit
            i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
            M = get_actual_value(i,10)
            #print "M is {0}".format(M)
            
            #constant ,signed,4bit
            i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
            B = get_actual_value(i,10)
            i = output_data.data[24] & 0xf
            B1 = get_actual_value(i,4)
            #accuracy ,signed,4bit
            i = (output_data.data[24] & 0xf0) >> 4
            B2 = get_actual_value(i,4)
            #sensor type
            #Temperature
            if output_data.data[7] in (1,2,3,4):
                #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                #return ((M*c_byte(output_data.data[34]).value)+B*pow(10,B1))*pow(10,B2)
                if output_data.data[15]>>6 & 3 == 0:
                    return ((M*output_data.data[34])+B*pow(10,B1))*pow(10,B2)
                else:
                    return ((M*c_byte(output_data.data[34]).value)+B*pow(10,B1))*pow(10,B2)
                #return (M*output_data.data[34]+B*pow(10,B1))*pow(10,B2)
        else:
            return r"N/A"
    else:
        return r"N/A"

def get_upper_non_critical_value(output_data):
    if output_data.data[5] & 0x10 == 0x10:
        if output_data.data[14] & 0x08 == 0x08:
            #get M,B
            #get M,B ,signed,10bit
            i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
            M = get_actual_value(i,10)
            #print "M is {0}".format(M)
            
            #constant ,signed,4bit
            i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
            B = get_actual_value(i,10)
            i = output_data.data[24] & 0xf
            B1 = get_actual_value(i,4)
            #accuracy ,signed,4bit
            i = (output_data.data[24] & 0xf0) >> 4
            B2 = get_actual_value(i,4)
            #sensor type
            #Temperature
            if output_data.data[7] in (1,2,3,4):
                #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                #return ((M*c_byte(output_data.data[33]).value)+B*pow(10,B1))*pow(10,B2)
                if output_data.data[15]>>6 & 3 == 0:
                    return ((M*output_data.data[33])+B*pow(10,B1))*pow(10,B2)
                else:
                    return ((M*c_byte(output_data.data[33]).value)+B*pow(10,B1))*pow(10,B2)
                #return (M*output_data.data[33]+B*pow(10,B1))*pow(10,B2)
        else:
            return r"N/A"
    else:
        return r"N/A"

def get_upper_critical_value(output_data):
    if output_data.data[5] & 0x10 == 0x10:
        if output_data.data[14] & 0x10 == 0x10:
            #get M,B
            #get M,B ,signed,10bit
            i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
            M = get_actual_value(i,10)
            #print "M is {0}".format(M)
            
            #constant ,signed,4bit
            i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
            B = get_actual_value(i,10)
            i = output_data.data[24] & 0xf
            B1 = get_actual_value(i,4)
            #accuracy ,signed,4bit
            i = (output_data.data[24] & 0xf0) >> 4
            B2 = get_actual_value(i,4)
            #sensor type
            if output_data.data[7] in (1,2,3,4):
                #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                #return ((M*c_byte(output_data.data[32]).value)+B*pow(10,B1))*pow(10,B2)
                if output_data.data[15]>>6 & 3 == 0:
                    return ((M*output_data.data[32])+B*pow(10,B1))*pow(10,B2)
                else:
                    return ((M*c_byte(output_data.data[32]).value)+B*pow(10,B1))*pow(10,B2)
                #return (M*output_data.data[32]+B*pow(10,B1))*pow(10,B2)
            #Temperature
        else:
            return r"N/A"
    else:
        return r"N/A"

def get_upper_non_recoverable_value(output_data):
    if output_data.data[5] & 0x10 == 0x10:
        if output_data.data[14] & 0x20 == 0x20:
            #get M,B
            #get M,B ,signed,10bit
            i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
            M = get_actual_value(i,10)
            #print "M is {0}".format(M)
            
            #constant ,signed,4bit
            i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
            B = get_actual_value(i,10)
            i = output_data.data[24] & 0xf
            B1 = get_actual_value(i,4)
            #accuracy ,signed,4bit
            i = (output_data.data[24] & 0xf0) >> 4
            B2 = get_actual_value(i,4)
            #sensor type
            #Temperature
            if output_data.data[7] in (1,2,3,4):
                #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                if output_data.data[15]>>6 & 3 == 0:
                    return ((M*output_data.data[31])+B*pow(10,B1))*pow(10,B2)
                else:
                    return ((M*c_byte(output_data.data[31]).value)+B*pow(10,B1))*pow(10,B2)
                #return (M*output_data.data[31]+B*pow(10,B1))*pow(10,B2)
        else:
            return r"N/A"
    else:
        return r"N/A"

def get_sensor_unit(output_data):
    #Sensor unit,is a str,list in sel_parsing_table.py
    return SENSOR_UNIT[output_data.data[16]][1]

def read_sensorvalue_and_sensorstatus(h,sensornumber):
    output = nm.ipmi_get_sensor_reading(h,sensornumber)
    value_temp,status_temp = output[0],output[1]
    return value_temp,status_temp

def get_sensor_name(output_data):
    sensor_name_str = ""
    if output_data.type == 0x01:
        sensorIdcode = output_data.data[42]
    if output_data.type == 0x02:
        sensorIdcode = output_data.data[26]
    codeformat = (sensorIdcode >> 6) & 0x03
    #unicode
    if codeformat == 0:
        pass
    #BCD Plus 
    if codeformat == 1:
        pass
    #6-bit ASCII 
    if codeformat == 2:
        pass
    #8-bit ASCII
    if codeformat == 3:
        #if (sensorIdcode & 0x1f)!=0 and (sensorIdcode & 0x1f)!=0x1f:
        sensornamestrlenth = sensorIdcode & 0x1f
        if output_data.type == 0x01:
            for i in range(43,43+sensornamestrlenth):
                sensor_name_str += chr(output_data.data[i])
        if output_data.type == 0x02:
            for i in range(27,27+sensornamestrlenth):
                sensor_name_str += chr(output_data.data[i])

    return sensor_name_str
	
def sensor_list(h):
    if(nm.ipmi_get_sdr_info(h).repoVersion != 0x51):
        return "This version is not supported"
    #init storage
    all_sensor_list = {}
    temperature_1 = []
    voltage_2 = []
    currents_3 = []
    fans_4 = []
    discrete_others = []
    
    #first record id 0x0000,last record id 0xffff
    next_record_id = c_ushort(0)
    while(next_record_id.value != 0xffff):
        next_record_id,output_data = nm.ipmi_get_sdr_record(h,next_record_id.value)

        #status: "Unavailable" or "ok"
        #Probename: empty str or a name str
        #Reading: a value number or "Unavailable"
        #lower_non_critical: a value number or "N/A"
        #upper_non_critical: a value number or "N/A"
        #lower_critical: a value number or "N/A"
        #upper_critical: a value number or "N/A"
        #lower_non_recoverable: a value number or "N/A"
        #upper_non_recoverable: a value number or "N/A"
        ###init end value
        default_description = {
            "status":"Unavailable",
            "Probename":"",
            "Reading":"Unavailable",
            "lower_non_critical":"N/A",
            "upper_non_critical":"N/A",
            "lower_critical":"N/A",
            "upper_critical":"N/A",
            "lower_non_recoverable":"N/A",
            "upper_non_recoverable":"N/A",
        }
        if output_data.type == 0x01:
            default_description["lower_non_critical"] = get_lower_non_cirtical_value(output_data)
            #get threshold
            if default_description["lower_non_critical"] != "N/A":
                default_description["lower_non_critical"] = "{0} {1}".format(default_description["lower_non_critical"],\
                                                                                            get_sensor_unit(output_data))

            default_description["upper_non_critical"] = get_upper_non_critical_value(output_data)
            if default_description["upper_non_critical"] != "N/A":
                default_description["upper_non_critical"] = "{0} {1}".format(default_description["upper_non_critical"],\
                                                                                            get_sensor_unit(output_data))
                
            default_description["lower_critical"] = get_lower_cirtical_value(output_data)
            if default_description["lower_critical"] != "N/A":
                default_description["lower_critical"] = "{0} {1}".format(default_description["lower_critical"],\
                                                                                            get_sensor_unit(output_data))

            default_description["upper_critical"] = get_upper_critical_value(output_data)
            if default_description["upper_critical"] != "N/A":
                default_description["upper_critical"] = "{0} {1}".format(default_description["upper_critical"],\
                                                                                            get_sensor_unit(output_data))

            default_description["lower_non_recoverable"] = get_lower_non_recoverable_value(output_data)
            if default_description["lower_non_recoverable"] != "N/A":
                default_description["lower_non_recoverable"] = "{0} {1}".format(default_description["lower_non_recoverable"],\
                                                                                            get_sensor_unit(output_data))

            default_description["upper_non_recoverable"] = get_upper_non_recoverable_value(output_data)
            if default_description["upper_non_recoverable"] != "N/A":
                default_description["upper_non_recoverable"] = "{0} {1}".format(default_description["upper_non_recoverable"],\
                                                                                            get_sensor_unit(output_data))

            #get sensor reading and status
            sensornumber = output_data.data[2]
            value_temp,status_temp = read_sensorvalue_and_sensorstatus(h,sensornumber)
            if status_temp>>5&1 == 0 and status_temp !=0:
                i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
                M = get_actual_value(i,10)
                #constant ,signed,4bit
                i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
                B = get_actual_value(i,10)
                i = output_data.data[24] & 0xf
                B1 = get_actual_value(i,4)
                #accuracy ,signed,4bit
                i = (output_data.data[24] & 0xf0) >> 4
                B2 = get_actual_value(i,4)
                #sensor type
                #Temperature 1,Voltage 2,Current 3,Fan 4
                if output_data.data[7] in (1,2,3,4):
                    #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                    #return ((M*c_byte(output_data.data[36]).value)+B*pow(10,B1))*pow(10,B2)
                    #unsigned
                    if output_data.data[15]>>6 & 3 == 0:
                        default_description["Reading"] = "{0} {1}".format(((M*value_temp)+B*pow(10,B1))*pow(10,B2),\
                                                                          get_sensor_unit(output_data))
                    #signed
                    else:
                        default_description["Reading"] = "{0} {1}".format(((M*c_byte(value_temp).value)+B*pow(10,B1))*pow(10,B2),\
                                                                          get_sensor_unit(output_data))
                    default_description["status"] = "ok"
            else:
                default_description["status"] = "Unavailable"
                default_description["Reading"] = "Unavailable"

            #get sensor name
            default_description["Probename"] = get_sensor_name(output_data)

            if output_data.data[7] == 1:
                temperature_1.append(default_description)
            if output_data.data[7] == 2:
                voltage_2.append(default_description)
            if output_data.data[7] == 3:
                currents_3.append(default_description)
            if output_data.data[7] == 4:
                fans_4.append(default_description)


        if output_data.type == 0x02 or (output_data.type == 0x01 and (output_data.data[8]==0x6f or 0x02<=output_data.data[8]<=0x0c)):
            #get sensor name
            sensornumber = output_data.data[2]
            sensor_name_str_d = get_sensor_name(output_data)
            discrete_init = {
                "name":sensor_name_str_d,
                "value":"N/A",
                "status":"",
            }
            try:
                sensor_type_discrete = EVENT_TYPE_CODE_sensorSpecific[output_data.data[7]-1][1]
                outputdata_sensor_reading = nm.ipmi_get_sensor_reading(h,sensornumber)
                if outputdata_sensor_reading[1]>>5&1 == 0 and outputdata_sensor_reading[1] != 0:
                    status_description_str = []
                    #data4
                    if outputdata_sensor_reading[2]&0x01 == 0x01:
                        sensor_type_discrete_i = sensor_type_discrete[0][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x02 == 0x02:
                        sensor_type_discrete_i = sensor_type_discrete[1][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x04 == 0x04:
                        sensor_type_discrete_i = sensor_type_discrete[2][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x08 == 0x08:
                        sensor_type_discrete_i = sensor_type_discrete[3][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x10 == 0x10:
                        sensor_type_discrete_i = sensor_type_discrete[4][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x20 == 0x20:
                        sensor_type_discrete_i = sensor_type_discrete[5][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x40 == 0x40:
                        sensor_type_discrete_i = sensor_type_discrete[6][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[2]&0x80 == 0x80:
                        sensor_type_discrete_i = sensor_type_discrete[7][1]
                        status_description_str.append(sensor_type_discrete_i)
                    #data5
                    if outputdata_sensor_reading[3]&0x01 == 0x01:
                        sensor_type_discrete_i = sensor_type_discrete[8][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[3]&0x02 == 0x02:
                        sensor_type_discrete_i = sensor_type_discrete[9][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[3]&0x04 == 0x04:
                        sensor_type_discrete_i = sensor_type_discrete[10][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[3]&0x08 == 0x08:
                        sensor_type_discrete_i = sensor_type_discrete[11][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[3]&0x10 == 0x10:
                        sensor_type_discrete_i = sensor_type_discrete[12][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[3]&0x20 == 0x20:
                        sensor_type_discrete_i = sensor_type_discrete[13][1]
                        status_description_str.append(sensor_type_discrete_i)
                    if outputdata_sensor_reading[3]&0x40 == 0x40:
                        sensor_type_discrete_i = sensor_type_discrete[14][1]
                        status_description_str.append(sensor_type_discrete_i)

                    if not status_description_str:
                        discrete_init["status"] = "ok"
                    else:
                        discrete_init["status"] = ";".join(status_description_str)

                else:
                    discrete_init["status"] = "N/A"
            except IndexError:
                discrete_init["status"] = "N/A"
            discrete_others.append(discrete_init)

    all_sensor_list["temperature_1"] = temperature_1
    all_sensor_list["voltage_2"] = voltage_2
    all_sensor_list["currents_3"] = currents_3
    all_sensor_list["fans_4"] = fans_4
    all_sensor_list["discrete_others"] = discrete_others

    return all_sensor_list

def get_health_status(h):
    #storage description about health
    #list is null ,ok
    #list not null,not ok
    temperature = []
    voltage = []
    fan = []
    processor = []
    power_supply = []
    next_record_id = c_ushort(0)
    flag_processor = 0
    flag_power_supply = 0
    while(next_record_id.value != 0xffff):
        next_record_id,output_data = nm.ipmi_get_sdr_record(h,next_record_id.value)
        #threshold sensor
        if output_data.type == 0x01:
            #get threshold
            lnc = get_lower_non_cirtical_value(output_data)
            unc = get_upper_non_critical_value(output_data)
            lc = get_lower_cirtical_value(output_data)
            uc = get_upper_critical_value(output_data)
            lnr = get_lower_non_recoverable_value(output_data)
            unr = get_upper_non_recoverable_value(output_data)

            #get sensor name
            sensor_name_str = ""
            sensorIdcode = output_data.data[42]
            codeformat = (sensorIdcode >> 6) & 0x03
            #unicode
            if codeformat == 0:
                pass
            #BCD Plus 
            if codeformat == 1:
                pass
            #6-bit ASCII 
            if codeformat == 2:
                pass
            #8-bit ASCII
            sensor_name_str = ""
            if codeformat == 3:
                #if (sensorIdcode & 0x1f)!=0 and (sensorIdcode & 0x1f)!=0x1f:
                sensornamestrlenth = sensorIdcode & 0x1f
                for i in range(43,43+sensornamestrlenth):
                        sensor_name_str += chr(output_data.data[i])

            #get sensor reading and status
            sensornumber = output_data.data[2]
            value_temp,status_temp = read_sensorvalue_and_sensorstatus(sensornumber)
            if status_temp>>5&1 == 0 and status_temp !=0:
                i = output_data.data[19] | (output_data.data[20]&0xc0 << 2)
                M = get_actual_value(i,10)
                #constant ,signed,4bit
                i = output_data.data[21] | (output_data.data[22]&0xc0 << 2)
                B = get_actual_value(i,10)
                i = output_data.data[24] & 0xf
                B1 = get_actual_value(i,4)
                #accuracy ,signed,4bit
                i = (output_data.data[24] & 0xf0) >> 4
                B2 = get_actual_value(i,4)
                #sensor type
                sensor_type_ = output_data.data[7]
                #Temperature 1,Voltage 2,Current 3,Fan 4
                if output_data.data[7] in (1,2,3,4):
                    #print "<<<<<<<<<< is {0} {1}".format(c_byte(output_data.data[36]).value,output_data.data[36])
                    #return ((M*c_byte(output_data.data[36]).value)+B*pow(10,B1))*pow(10,B2)
                    if output_data.data[15]>>6 & 3 == 0:
                        sensor_current_value = ((M*value_temp)+B*pow(10,B1))*pow(10,B2)
                    else:
                        sensor_current_value = ((M*c_byte(value_temp).value)+B*pow(10,B1))*pow(10,B2)
                    if uc != "N/A" and sensor_current_value >= uc:
                        description_str = "{0}:{1}".format(sensor_name_str,"at or above upper critical threshold")
                        if sensor_type_ == 1:
                            temperature.append(description_str)
                        if sensor_type_ == 2:
                            voltage.append(description_str)
                        if sensor_type_ == 4:
                            fan.append(description_str)
                    elif unc != "N/A" and sensor_current_value >= unc:
                        description_str = "{0}:{1}".format(sensor_name_str,"at or above upper non_critical threshold")
                        if sensor_type_ == 1:
                            temperature.append(description_str)
                        if sensor_type_ == 2:
                            voltage.append(description_str)
                        if sensor_type_ == 4:
                            fan.append(description_str)
                    elif lc != "N/A" and sensor_current_value <= lc:
                        description_str = "{0}:{1}".format(sensor_name_str,"at or blow lower critical threshold")
                        if sensor_type_ == 1:
                            temperature.append(description_str)
                        if sensor_type_ == 2:
                            voltage.append(description_str)
                        if sensor_type_ == 4:
                            fan.append(description_str)
                    elif lnc != "N/A" and sensor_current_value <= lnc:
                        description_str = "{0}:{1}".format(sensor_name_str,"at or blow lower non_critical threshold")
                        if sensor_type_ == 1:
                            temperature.append(description_str)
                        if sensor_type_ == 2:
                            voltage.append(description_str)
                        if sensor_type_ == 4:
                            fan.append(description_str)
                    else:
                        pass

        #discrete sensor
        if output_data.type == 0x02:
            #get sensor name
            sensor_name_str_d = ""
            sensorIdcode_d = output_data.data[26]
            codeformat_d = (sensorIdcode_d >> 6) & 0x03
            #unicode
            if codeformat_d == 0:
                pass
            #BCD Plus 
            if codeformat_d == 1:
                pass
            #6-bit ASCII 
            if codeformat_d == 2:
                pass
            #8-bit ASCII
            if codeformat_d == 3:
                #if (sensorIdcode & 0x1f)!=0 and (sensorIdcode & 0x1f)!=0x1f:
                sensornamestrlenth_d = sensorIdcode_d & 0x1f
                for i in range(27,27+sensornamestrlenth_d):
                        sensor_name_str_d += chr(output_data.data[i])
            if output_data.data[7] == 7:
                #exist processor sensor
                flag_processor = 1
                output_i = nm.ipmi_get_sensor_reading(h,output_data.data[2])
                if output_i[1]>>5&1 == 0 and output_i[1] !=0:
                    str_j = ""
                    if output_i[2]&0x01 == 1:
                        desc_str = "IERR"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x02 == 1:
                        desc_str = "Thermal Trip"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x04 == 1:
                        desc_str = "FRB1/BIST failure"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x08 == 1:
                        desc_str = "FRB2/Hang in POST failure"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x10 == 1:
                        desc_str = "FRB3/Processor Startup/Initialization failure"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x20 == 1:
                        desc_str = "Configuration Error"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x40 == 1:
                        desc_str = "SM BIOS Uncorrectable CPU-complex Error"
                        str_j = str_j + desc_str + ","

                    if output_i[2]&0x80 == 1:
                        desc_str = "Processor Presence detected"
                        str_j = str_j + desc_str + ","

                    if output_i[3]&0x01 == 1:
                        desc_str = "Processor disabled"
                        str_j = str_j + desc_str + ","

                    if output_i[3]&0x02 == 1:
                        desc_str = "Terminator Presence Detected"
                        str_j = str_j + desc_str + ","

                    if output_i[3]&0x04 == 1:
                        desc_str = "Processor Automatically Throttled"
                        str_j = str_j + desc_str + ","
                    if str_j:
                        processor.append("{0}:{1}".format(sensor_name_str_d,str_j))
            #power supply
            if output_data.data[7] == 8:
                flag_power_supply = 1
                output_i = nm.ipmi_get_sensor_reading(h,output_data.data[2])
                if output_i[1]>>5&1 == 0 and output_i[1] !=0:
                    str_i = ""
                    #status ok
                    if output_i[2]&0x01 == 0x01:
                        desc_str = "Presence detected"
                        str_i = str_i + desc_str + ","
                    if output_i[2]&0x02 == 0x02:
                        desc_str = "Power Supply Failure detected"
                        str_i = str_i + desc_str + ","
                        #power_supply.append("{0}:{1}".format(sensor_name_str_d,desc_str))
                    if output_i[2]&0x04 == 0x04:
                        desc_str = "Predictive Failure"
                        str_i = str_i + desc_str + ","
                        #power_supply.append("{0}:{1}".format(sensor_name_str_d,desc_str))
                    if output_i[2]&0x08 == 0x08:
                        desc_str = "Power Supply input lost AC/DC"
                        str_i = str_i + desc_str + ","
                        #power_supply.append("{0}:{1}".format(sensor_name_str_d,desc_str))
                    if output_i[2]&0x10 == 0x10:
                        desc_str = "Power Supply input lost or out-of-range"
                        str_i = str_i + desc_str + ","
                        #power_supply.append("{0}:{1}".format(sensor_name_str_d,desc_str))
                    if output_i[2]&0x20 == 0x20:
                        desc_str = "Power Supply input out-of-range,but present"
                        str_i = str_i + desc_str + ","
                        #power_supply.append("{0}:{1}".format(sensor_name_str_d,desc_str))
                    if str_i:
                        power_supply.append("{0}:{1}".format(sensor_name_str_d,str_i))

    health_status = {
        "temperature":temperature,
        "voltage":voltage,
        "fan":fan,
    }
    if flag_processor == 1:
        health_status["processor"] = processor
    if flag_power_supply == 1:
        health_status["power_supply"] = power_supply
    return health_status

if __name__ == '__main__':
#    h = connect_nmprk('192.168.124.115','ADMIN','ADMIN')
    h = connect_nmprk('192.168.124.30','ADMIN','ADMIN')
    #h = connect_nmprk('192.168.124.71','amax','amax')
    #lll = sensor_list(h)

    #for per_sonsor in lll["temperature_1"]:
    #    print per_sonsor["status"],"   ",per_sonsor["Probename"],"   ",per_sonsor["Reading"],"   ",per_sonsor["lower_non_recoverable"],"   ",\
    #            per_sonsor["lower_critical"],"   ",per_sonsor["lower_non_critical"],"   ",per_sonsor["upper_non_critical"],"   ",\
    #            per_sonsor["upper_critical"],"   ",per_sonsor["upper_non_recoverable"]
    #for per_sonsor in lll["voltage_2"]:
    #    print per_sonsor["status"],"   ",per_sonsor["Probename"],"   ",per_sonsor["Reading"],"   ",per_sonsor["lower_non_recoverable"],"   ",\
    #            per_sonsor["lower_critical"],"   ",per_sonsor["lower_non_critical"],"   ",per_sonsor["upper_non_critical"],"   ",\
    #            per_sonsor["upper_critical"],"   ",per_sonsor["upper_non_recoverable"]
    #for per_sonsor in lll["currents_3"]:
    #    print per_sonsor["status"],"   ",per_sonsor["Probename"],"   ",per_sonsor["Reading"],"   ",per_sonsor["lower_non_recoverable"],"   ",\
    #            per_sonsor["lower_critical"],"   ",per_sonsor["lower_non_critical"],"   ",per_sonsor["upper_non_critical"],"   ",\
    #            per_sonsor["upper_critical"],"   ",per_sonsor["upper_non_recoverable"]
    #for per_sonsor in lll["fans_4"]:
    #    print per_sonsor["status"],"   ",per_sonsor["Probename"],"   ",per_sonsor["Reading"],"   ",per_sonsor["lower_non_recoverable"],"   ",\
    #            per_sonsor["lower_critical"],"   ",per_sonsor["lower_non_critical"],"   ",per_sonsor["upper_non_critical"],"   ",\
    #            per_sonsor["upper_critical"],"   ",per_sonsor["upper_non_recoverable"]

    #for per_sonsor in lll["discrete_others"]:
    #    print "{0}    {1}    {2}".format(per_sonsor["name"],per_sonsor["value"],per_sonsor["status"])
    #print "*"*150
    #print "*"*150
    #print "xxxxxxxxxxxxxxxxx sensor reading xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    #xxx = nm.ipmi_get_sensor_reading(h,155)
    #print hex(xxx[0]),hex(xxx[1]),hex(xxx[2]),hex(xxx[3])
    #print "xxxxxxxxxxxxxxxxx sensor reading xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    #health_status = get_health_status(h)
    #for key in health_status:
    #    print key
    #print "x"*130


    #for key in health_status:
    #    for i in health_status[key]:
    #        print i
    #print "x"*120
    #print "x"*120
    #d =  nm.ipmi_get_sensor_reading(h,64)
    #for i in d:
    #    print i

    #power_limit(h,0)
    disconnect(h)




