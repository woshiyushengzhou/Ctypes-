import csv
from time import sleep
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

from ctypes import c_ushort, c_byte, cdll
from pynmprk import BaseNMPRK
from hl_func import *
from nmtype import *



dh = cdll.LoadLibrary(file_path)
NM = BaseNMPRK(dh)
class CustomEvent(object):
    #Severity
    EVENT_SEVERITY = (
        (0,"Custom"),
        (1,"Error"),
        (2,"Info"),
    )
    #Entity
    #Event Type
    EVENT_TYPE = (
        (0,"MAIN_MAX_POWER"),
        (1,"MAX_INLET_TEMP"),
        (2,"MIX_INLET_TEMP"),
        (3,"AVE_INLET_TEMP_GR"),
        (4,"AVE_INLET_TEMP_LE"),
        (5,"DEVICE_COMPONENT_FAULT"),
        (6,"PREDICTIVE_FAN_FAILURE"),
    )
    #Description
    desc1 = "{0} custom event. threshold:{1} type:{2} condition:{3}"
    #Time Stamp
    def __init__(self):
        pass

    def main_max_power_threshold_set_update_remove(self, entity, threshold_value, threshold_value_db):
        custom_event_change = {
            "Severity":"unknow",
            "Entity":"unknow",
            "Type":"unknow",
            "Desc":"unknow",
        }
        custom_event_change["Severity"] = self.EVENT_SEVERITY[2][1]
        custom_event_change["Entity"] = entity
        custom_event_change["Type"] = self.EVENT_TYPE[0][1]
        #set
        if threshold_value_db==-1 and threshold_value>0:
            custom_event_change["Desc"] = self.desc1.format("add", threshold_value, self.EVENT_TYPE[0][1], "GREATHER THAN")
            return custom_event_change
        #update
        if threshold_value_db!=-1 and threshold_value>0:
            custom_event_change["Desc"] = self.desc1.format("update", threshold_value, self.EVENT_TYPE[0][1], "GREATHER THAN")
            return custom_event_change
        #remove
        if threshold_value_db!=-1 and threshold_value==-1:
            custom_event_change["Desc"] = self.desc1.format("remove", threshold_value_db, self.EVENT_TYPE[0][1], "GREATHER THAN")
            return custom_event_change


    def main_max_power_threshold_judge(self,entity, value, threshold_value_db):
        custom_event_change = {
            "Severity":"unknow",
            "Entity":"unknow",
            "Type":"unknow",
            "Desc":"unknow",
        }
        if value > threshold_value_db:
            custom_event_change["Severity"] = self.EVENT_SEVERITY[1][1]
            custom_event_change["Entity"] = entity
            custom_event_change["Type"] = self.EVENT_TYPE[0][1]
            custom_event_change["Desc"] = self.desc1.format("trigger", threshold_value_db, self.EVENT_TYPE[0][1], "GREATHER THAN")
            return custom_event_change
        else:
            return {}

    def inlet_temperature_set_update_remove(self, entity, set_type, threshold_value, threshold_value_db):
        '''
            set_type: 0, max_inlet_temp
                      1, mix_inlet_temp
                      2, ave_inlet_temp_ge
                      3, ave_inlet_temp_le
        '''
        custom_event_change = {
            "Severity":"unknow",
            "Entity":"unknow",
            "Type":"unknow",
            "Desc":"unknow",
        }
        #get set type
        if set_type == 0:
            event_type_temp = self.EVENT_TYPE[1][1]
            event_desc_temp = "GREATHER THAN"
        elif set_type == 1:
            event_type_temp = self.EVENT_TYPE[2][1]
            event_desc_temp = "LESS THAN"
        elif set_type == 2:
            event_type_temp = self.EVENT_TYPE[3][1]
            event_desc_temp = "GREATHER THAN"
        elif set_type == 3:
            event_type_temp = self.EVENT_TYPE[4][1]
            event_desc_temp = "LESS THAN"
        #not generate event log
        else:
            return {}

        custom_event_change["Severity"] = self.EVENT_SEVERITY[2][1]
        custom_event_change["Entity"] = entity
        custom_event_change["Type"] = event_type_temp
        #set
        if threshold_value_db==-1 and threshold_value>0:
            custom_event_change["Desc"] = self.desc1.format("add", threshold_value, event_type_temp, event_desc_temp)
            return custom_event_change
        #update
        elif threshold_value_db!=-1 and threshold_value>0:
            custom_event_change["Desc"] = self.desc1.format("update", threshold_value, event_type_temp, event_desc_temp)
            return custom_event_change
        #remove
        elif threshold_value_db!=-1 and threshold_value==-1:
            custom_event_change["Desc"] = self.desc1.format("remove", threshold_value_db, event_type_temp, event_desc_temp)
            return custom_event_change
        else:
            return {}


    def inlet_temperature_judge(self, entity, judge_type, value, threshold_value_db):
        custom_event_change = {
            "Severity":"unknow",
            "Entity":"unknow",
            "Type":"unknow",
            "Desc":"unknow",
        }
        #get set type
        if set_type == 0:
            event_type_temp = self.EVENT_TYPE[1][1]
            event_desc_temp = "GREATHER THAN"
        elif set_type == 1:
            event_type_temp = self.EVENT_TYPE[2][1]
            event_desc_temp = "LESS THAN"
        elif set_type == 2:
            event_type_temp = self.EVENT_TYPE[3][1]
            event_desc_temp = "GREATHER THAN"
        elif set_type == 3:
            event_type_temp = self.EVENT_TYPE[4][1]
        else:
            return {}

        custom_event_change["Entity"] = entity
        custom_event_change["Type"] = event_type_temp
        custom_event_change["Severity"] = self.EVENT_SEVERITY[1][1]
        
        if threshold_value_db!=-1 and value>threshold_value_db and set_type==0:
            custom_event_change["Desc"] = self.desc1.format("trigger", threshold_value_db, event_type_temp, "GREATER THAN")
            return custom_event_change

        elif threshold_value_db!=-1 and value<threshold_value_db and set_type==1:
            custom_event_change["Desc"] = self.desc1.format("trigger", threshold_value_db, event_type_temp, "LESS THAN")
            return custom_event_change
            
        elif threshold_value_db!=-1 and value>threshold_value_db and set_type==2:
            custom_event_change["Desc"] = self.desc1.format("trigger", threshold_value_db, event_type_temp, "GREATER THAN")
            return custom_event_change

        elif threshold_value_db!=-1 and value<threshold_value_db and set_type==3:
            custom_event_change["Desc"] = self.desc1.format("trigger", threshold_value_db, event_type_temp, "LESS THAN")
            return custom_event_change
        else:
            return {}

    @classmethod
    def get_actual_sensor_value(cls, status, value, output_data):
        if status>>5&1 == 0 and status !=0:
            M,B,B1,B2 = get_calculate_factor(output_data)
            #unsigned 
            if output_data.data[15]>>6 & 3 == 0:
                return ((M*value)+B*pow(10,B1))*pow(10,B2)
            #signed
            else:
                return ((M*c_byte(value).value)+B*pow(10,B1))*pow(10,B2)
        else:
            return ""



    #if xxx_list is empty, means there is no such sensor. status is OK!
    @staticmethod
    def fan_monitor(h):
        '''
        sensor name
        sensor value
        sensor states code
                1 : Not ok
                0 : ok
        sensor states description
        '''
        fan_list = []
        record_id = c_ushort(0)
        while(record_id.value != 0xffff):
            record_id,output_data = NM.ipmi_get_sdr_record(h, record_id.value)
            if output_data.type==0x01 and output_data.data[7]==4:
                fan_list.append(output_data)

        all_fan_monitor_data = []
        if not fan_list:
            return all_fan_monitor_data
        for per_fan in fan_list:
            per_fan_data = dict(name="",value="",code=1,desc="")
            per_fan_data["name"] = get_sensor_name(per_fan)
            value,status = read_sensorvalue_and_sensorstatus(h, per_fan.data[2])
            per_fan_data["value"] = CustomEvent.get_actual_sensor_value(status, value, per_fan)

            #sensor Unavailable
            if per_fan_data["value"]=="":
                continue

            low_critical = get_lower_cirtical_value(per_fan)
            if low_critical != r"N/A" and per_fan_data["value"] > low_critical:
                per_fan_data["code"] = 0
                per_fan_data["desc"] = "ok"
                all_fan_monitor_data.append(per_fan_data)
                continue

            if low_critical != r"N/A" and per_fan_data["value"] <= low_critical:
                per_fan_data["code"] = 1
                per_fan_data["desc"] = "{0}: at or below low critical ,Not ok!".format(per_fan_data["name"])
                all_fan_monitor_data.append(per_fan_data)
                continue
        return all_fan_monitor_data

    @staticmethod
    def battery_monitor(h):
        battery_list = []
        record_id = c_ushort(0)
        while(record_id.value != 0xffff):
            record_id,output_data = NM.ipmi_get_sdr_record(h, record_id.value)
            if output_data.type==0x02 and output_data.data[7]==0x29:
                battery_list.append(output_data)
        all_battery_monitor_data = []
        if not battery_list:
            return all_battery_monitor_data
        for per_battery in battery_list:
            per_battery_data = dict(name="",value="",code=1,desc="")
            per_battery_data["name"] = get_sensor_name(per_battery)
            reading_data = NM.ipmi_get_sensor_reading(h, per_battery.data[2])
            if not (reading_data[1]>>5&1 == 0 and reading_data[1] !=0):
                continue
            if reading_data[2]&0x04==4 and reading_data[2]&0x02==2 and reading_data[2]&0x01==0:
                per_battery_data["code"] = 0
                per_battery_data["desc"] = "ok"
                all_battery_monitor_data.append(per_battery_data)
                continue
            if reading_data[2]&0x02>>1==1:
                per_battery_data["code"] = 1
                per_battery_data["desc"] = "battery failed, Not ok!"
                all_battery_monitor_data.append(per_battery_data)
                continue
            if reading_data[2]&0x01==1:
                per_battery_data["code"] = 1
                per_battery_data["desc"] = "battery low, Not ok!"
                all_battery_monitor_data.append(per_battery_data)
        return all_battery_monitor_data

    @staticmethod
    def storage_monitor(h):
        pass

    @staticmethod
    def voltage_monitor(h):
        voltage_list = []
        record_id = c_ushort(0)
        while(record_id.value != 0xffff):
            record_id,output_data = NM.ipmi_get_sdr_record(h, record_id.value)
            if output_data.type==0x01 and output_data.data[7]==2:
                voltage_list.append(output_data)

        all_voltage_monitor_data = []
        if not voltage_list:
            return all_voltage_monitor_data
        for per_voltage in voltage_list:
            per_voltage_data = dict(name="",value="",code=1,desc="")
            per_voltage_data["name"] = get_sensor_name(per_voltage)
            value,status = read_sensorvalue_and_sensorstatus(h, per_voltage.data[2])
            per_voltage_data["value"] = CustomEvent.get_actual_sensor_value(status, value, per_voltage)
            if per_voltage_data["value"]=="":
                continue

            low_critical = get_lower_cirtical_value(per_voltage)
            up_critical = get_upper_critical_value(per_voltage)
            if low_critical != r"N/A" and per_voltage_data["value"] <= low_critical:
                per_voltage_data["code"] = 1 
                per_voltage_data["desc"] = "{0}: at or below low critical, Not ok!"
                all_voltage_monitor_data.append(per_voltage_data)
                continue
            elif up_critical != r"N/A" and per_voltage_data["value"] >= up_critical:
                per_voltage_data["code"] = 1 
                per_voltage_data["desc"] = "{0}: at or over up critical, Not ok!"
                all_voltage_monitor_data.append(per_voltage_data)
                continue
            else:
                per_voltage_data["code"] = 0 
                per_voltage_data["desc"] = "ok"
                all_voltage_monitor_data.append(per_voltage_data)

        return all_voltage_monitor_data

    @staticmethod
    def tempurature_monitor(h):
        tempurature_list = []
        record_id = c_ushort(0)
        while(record_id.value != 0xffff):
            record_id,output_data = NM.ipmi_get_sdr_record(h, record_id.value)
            if output_data.type==0x01 and output_data.data[7]==1:
                tempurature_list.append(output_data)

        all_tempurature_monitor_data = []
        if not tempurature_list:
            return all_tempurature_monitor_data
        for per_tempurature in tempurature_list:
            per_tempurature_data = dict(name="",value="",code=1,desc="")
            per_tempurature_data["name"] = get_sensor_name(per_tempurature)
            value,status = read_sensorvalue_and_sensorstatus(h, per_tempurature.data[2])
            per_tempurature_data["value"] = CustomEvent.get_actual_sensor_value(status, value, per_tempurature)
            if per_tempurature_data["value"]=="":
                continue

            low_critical = get_lower_cirtical_value(per_tempurature)
            up_critical = get_upper_critical_value(per_tempurature)
            if low_critical != r"N/A" and per_tempurature_data["value"] <= low_critical:
                per_tempurature_data["code"] = 1 
                per_tempurature_data["desc"] = "{0}: at or below low critical, Not ok!"
                all_tempurature_monitor_data.append(per_tempurature_data)
                continue
            elif up_critical != r"N/A" and per_tempurature_data["value"] >= up_critical:
                per_tempurature_data["code"] = 1 
                per_tempurature_data["desc"] = "{0}: at or over up critical, Not ok!"
                all_tempurature_monitor_data.append(per_tempurature_data)
                continue
            else:
                per_tempurature_data["code"] = 0 
                per_tempurature_data["desc"] = "ok"
                all_tempurature_monitor_data.append(per_tempurature_data)

        return all_tempurature_monitor_data

    @staticmethod
    def processor_monitor(h):
        processor_list = []
        record_id = c_ushort(0)
        while(record_id.value != 0xffff):
            record_id,output_data = NM.ipmi_get_sdr_record(h, record_id.value)
            if output_data.type==0x02 and output_data.data[7]==0x07:
                processor_list.append(output_data)
        all_processor_monitor_data = []
        if not processor_list:
            return all_processor_monitor_data
        for per_processor in processor_list:
            per_processor_data = dict(name="",value="",code=1,desc="")
            per_processor_data["name"] = get_sensor_name(per_processor)
            reading_data = NM.ipmi_get_sensor_reading(h, per_processor.data[2])
            if not (reading_data[1]>>5&1 == 0 and reading_data[1] !=0):
                continue
            #reference 192.168.124.115 cup0, cup1
            if (reading_data[2]==128 or reading_data[2]==0) and reading_data[3]==128:
                per_processor_data["code"] = 0
                per_processor_data["desc"] = "ok"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x01==1:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "IERR, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x02==2:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Thermal Trip, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x04==4:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "FRB1/BIST failure, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x08==8:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "FRB2/Hang in POST failure, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x10==16:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "FRB3/Processor Startup/Initialization failure, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x20==32:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Configuration Error, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x20==32:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Configuration Error, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[2]&0x40==64:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Uncorrectable CPU-complex Error, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[3]&0x01==1:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Processor disabled, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[3]&0x02==2:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Terminator Presence Detected, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
            if reading_data[3]&0x04==4:
                per_processor_data["code"] = 1
                per_processor_data["desc"] = "Processor Automatically Throttled, Not ok!"
                all_processor_monitor_data.append(per_processor_data)
                continue
        return all_processor_monitor_data

    @staticmethod
    def memory_monitor(h):
        pass

    @staticmethod
    def power_supply_monitor(h):
        power_supply_list = []
        record_id = c_ushort(0)
        while(record_id.value != 0xffff):
            record_id,output_data = NM.ipmi_get_sdr_record(h, record_id.value)
            if output_data.type==0x02 and output_data.data[7]==0x08:
                power_supply_list.append(output_data)
        all_power_supply_monitor_data = []
        if not power_supply_list:
            return all_power_supply_monitor_data
        for per_power_supply in power_supply_list:
            per_power_supply_data = dict(name="",value="",code=1,desc="")
            per_power_supply_data["name"] = get_sensor_name(per_power_supply)
            reading_data = NM.ipmi_get_sensor_reading(h, per_power_supply.data[2])
            if not (reading_data[1]>>5&1 == 0 and reading_data[1] !=0):
                continue
            if reading_data[2]==1:
                per_power_supply_data["code"] = 0
                per_power_supply_data["desc"] = "ok"
                all_power_supply_monitor_data.append(per_power_supply_data)
                continue
            if reading_data[2]&0x02==2:
                per_power_supply_data["code"] = 1
                per_power_supply_data["desc"] = "Power Supply Failure detected, Not ok!"
                all_power_supply_monitor_data.append(per_power_supply_data)
                continue 
            if reading_data[2]&0x04==4:
                per_power_supply_data["code"] = 1
                per_power_supply_data["desc"] = "Predictive Failure, Not ok!"
                all_power_supply_monitor_data.append(per_power_supply_data)
                continue 
            if reading_data[2]&0x08==8:
                per_power_supply_data["code"] = 1
                per_power_supply_data["desc"] = "Power Supply input lost, Not ok!"
                all_power_supply_monitor_data.append(per_power_supply_data)
                continue 
            if reading_data[2]&0x10==16:
                per_power_supply_data["code"] = 1
                per_power_supply_data["desc"] = "Power Supply input lost or out-of-range, Not ok!"
                all_power_supply_monitor_data.append(per_power_supply_data)
                continue 
            if reading_data[2]&0x20==32:
                per_power_supply_data["code"] = 1
                per_power_supply_data["desc"] = "Configuration error, Not ok!"
                all_power_supply_monitor_data.append(per_power_supply_data)
        return all_power_supply_monitor_data

    @staticmethod
    def fan_relate_data_sample(h):
        #Get the number of fans
        monitor_result = CustomEvent.fan_monitor(h)
        fannumber = len(monitor_result)
        speedsum = sum([i["value"] for i in monitor_result])
        currentpower = get_global_power_platform(h)[0]  
        currenttemp = get_global_temperature_platform(h)[0]
        #zhu yi shu xue 
        return [speedsum,fannumber,currenttemp,currentpower]

    @staticmethod
    def storage_traindata(data):
        #traindata.csv use for stroage tarin data
        csvFile = open("traindata.csv", "aw")
        writer = csv.writer(csvFile)
        writer.writerow(data)
        csvFile.close()

    @staticmethod
    def storage_file_init():
        csvFile = open("traindata.csv", "w")
        writer = csv.writer(csvFile)
        #zhu yi shu xue 
        writer.writerow(["speedsum","fannumber","currenttemp","currentpower"])
        csvFile.close()

    @staticmethod
    def fan_model():
        data = pd.read_csv('traindata.csv')
        #zhu yi shu xue 
        x = data[["fannumber","currenttemp","currentpower"]]
        y = data["speedsum"]
        p1,p2,p3,p4 = train_test_split(x,y,random_state=1) 
        linreg = LinearRegression()
        model=linreg.fit(p1, p3)

        return linreg.predict

    @staticmethod
    def data_pre_process(per_data):
        p = pd.DataFrame(
            {
                'fannumber':[per_data[1]],
                'currenttemp':[per_data[2]],
                'currentpower':[per_data[3]],
            }
        )
        pp = p[["fannumber","currenttemp","currentpower"]]
        return pp

if __name__ == "__main__":
    a = CustomEvent()
    h = connect_nmprk('192.168.124.115','ADMIN','ADMIN')
    '''
    a.storage_file_init()
    for i in range(100):
        try:
            per_data = a.fan_relate_data_sample(h)
        except:
            continue
        a.storage_traindata(per_data)
    '''




    model = a.fan_model()
    per_data = a.fan_relate_data_sample(h)

    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "shijizhi: ",per_data[0]
    p = pd.DataFrame(
        {
            'fannumber':[per_data[1]],
            'currenttemp':[per_data[2]],
            'currentpower':[per_data[3]],
        }
    )
    pp = p[["fannumber","currenttemp","currentpower"]]
    y_data = model(pp)
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "yucezhi: ",y_data[0]
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print "chazhishi: ",y_data[0] - per_data[0]  
