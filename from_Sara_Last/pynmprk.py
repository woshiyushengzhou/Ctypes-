
from nmtype import *


class BaseNMPRK(object):
    '''NMPRK basic functions.
    '''
    def __init__(self,dll):
        self.dll = dll


    def connect_remote(self,host,usr,pwd):
        '''Function: connect to remote host.
        Parameters:host - remote hostIpOrDomainName
                   usr - the username
                   pwd - the password
        Return: handle of the connected host if success, or 'Error' if failed.
        '''
        connParams = nmprk_conn_remote_parameters_t()
        connParams.ipOrHostname = host.encode()
        connParams.username = usr.encode()
        connParams.password = pwd.encode()
        h = c_int()
        status = self.dll.NMPRK_ConnectRemote(byref(connParams),byref(h))
        params = nm_discovery_parameters_t()
        status = self.dll.NMPRK_GetDiscoveryParameters(h,byref(params))
        status = self.dll.NMPRK_SetDefaultNmCommandBridging(h,params.channel,params.address)
        assert( status == 0)
        return h
         
    def get_version(self,h):
        '''
        Return: the Node Manager version
        '''
        nm_output = nm_get_version_output_t()
        status = self.dll.NMPRK_GetVersion(h,byref(nm_output))
        assert(status == 0)
        return nm_output

    def disconnect(self,h):
        '''Function: disconnect to remote host.
        Parameters: h - hanlde of host
        Return: '' if success, or 'Error' if failed.
        '''
        status=self.dll.NMPRK_Disconnect(h)
        assert(status == 0)

            
    # need modify to perfect it!
    def get_statistics(self,h,mode,domain=0,policy=0):
        '''Function: get statistics values
        Parameters: h  - handle of the connected host
                    mode - mode value
                    domain - domain value
                    policy - policy value
        Return: output (nm_get_statistics_output_t- structure) if success, or 'Error' if failed
        '''
        nm_input = nm_get_statistics_input_t()
        nm_output = nm_get_statistics_output_t()
        nm_input.mode = mode
        nm_input.domain =domain
        nm_input.policy = policy
        status = self.dll.NMPRK_GetStatistics(h,byref(nm_input),byref(nm_output))
        print status
        assert(status == 0)
        return nm_output

    def reset_statistics(self,h,mode=0,domain=0,policy=0):
        '''Function: reset statistics
        Parameters: h  - handle of the connected host
                    mode - mode value
                    domain - domain value
                    policy - policy value
        Return: 0 if success, or -1 if failed
        '''
        nm_input = nm_reset_statistics_input_t()
        nm_input.mode = mode
        nm_input.domain = domain
        nm_input.policy = policy
        status = self.dll.NMPRK_ResetStatistics(h,byref(nm_input))
        assert(status==0)
        if status == 0:
            return 0
        else:
            return -1

    def get_all_policies(self,h):
        '''Function: get all the policies
        Parameters: h - handle of host
        Returns: policies (nm_policy_info_t - structure) if success.
        '''
        policies = nm_policy_info_t()
        policiesSize = c_int()
        status = self.dll.NMPRK_GetAllPolicies(h,byref(policies),byref(policiesSize))
        print(status)
        print('get all policies succ!')
        print(policies.policyId,policies.domain,policies.policyEnabled)
        assert(status == 0)
        return policies

    def enable_disable_policy_control(self,h,domain,policy,flags):
        nm_input = nm_enable_disable_policy_control_input_t()
        nm_input.domain = domain
        nm_input.policy = policy
        nm_input.flags = flags
        status = self.dll.NMPRK_EnableDisablePolicyControl(h,byref(nm_input))
        #print('enable,disable {}'.format(status))
    '''
    def set_policy(self,h,removePolicy=False):
        nm_input = nm_set_policy_input_t()
        info = nm_policy_info_t()
        nm_input.removePolicy = removePolicy
        nm_input.info.domain = 0
        nm_input.info.policyId = 6
        nm_input.info.policyEnabled = 1
        nm_input.info.policyTargetLimit = 1200
        nm_input.info.correctionTimeLimit = 6000
        nm_input.info.statisticsReportingPeriod = 60
      
        status = self.dll.NMPRK_SetPolicy(h,byref(nm_input))
        print(status)

    ''' 
    def set_policy(self,h,
            removePolicy=False,
            domain=0,
            policyId=200,
            policyEnabled=False,
            policyTriggerType=1,
            #aggressiveCpuPowerCorrection=0,
            #policyExceptionActionShutdown=0,
            #policyExceptionActionSendAlert=0,
            #secondaryPowerDomain=0,
            policyTargetLimit=300,
            correctionTimeLimit=600000,
            policyTriggerLimit=0,
            statisticsReportingPeriod=60):
        
        nm_input = nm_set_policy_input_t()
        nm_input.removePolicy = removePolicy
        nm_input.info.domain = domain
        nm_input.info.policyId = policyId
        nm_input.info.policyEnabled = policyEnabled
        nm_input.info.policyTriggerType = policyTriggerType
        #nm_input.info.aggressiveCpuPowerCorrection = aggressiveCpuPowerCorrection
        #nm_input.info.policyExceptionActionShutdown = policyExceptionActionShutdown
        #nm_input.info.policyExceptionActionSendAlert = policyExceptionActionSendAlert
        #nm_input.info.secondaryPowerDomain = secondaryPowerDomain
        nm_input.info.policyTargetLimit = policyTargetLimit
        nm_input.info.correctionTimeLimit = correctionTimeLimit
        nm_input.info.policyTriggerLimit = policyTriggerLimit
        nm_input.info.statisticsReportingPeriod = statisticsReportingPeriod

        print('chhhh')
        status = self.dll.NMPRK_SetPolicy(h,byref(nm_input))
        print(status)
        assert(status == 0)
    
    def get_policy(self,h,domain):
        '''can get '''
        nm_input = nm_get_policy_input_t()
        nm_input.domain = domain
        nm_input.policy = 1
        nm_output = nm_get_policy_output_t()
        status = self.dll.NMPRK_GetPolicy(h,byref(nm_input),byref(nm_output))
        print(status)
        assert(status==0)
        return nm_output
    def set_power_draw_range(self,h,domain,minimumPowerDraw=350,maximumPowerDraw=400):
        '''Function: set the Min/Max power consumption ranges.This information is preserved in the persistent storage.
        Parameters: h - handle of host
                    domain - domain value
                    minimumPowerDraw - min power value
                    maximumPowerDraw - max power value
        Returns: '' if sucess, or 'Error' if failed
        '''
        nm_input = nm_set_power_draw_range_input_t()
        nm_input.domain = domain
        nm_input.minimumPowerDraw = minimumPowerDraw
        nm_input.maximumPowerDraw = maximumPowerDraw
        status = self.dll.NMPRK_SetPowerDrawRange(h,byref(nm_input))
        assert(status == 0)

    def ipmi_get_sel_info(self,h):
	'''Function: Send the Get SEL Info command (NetFn: 0Ah Cmd: 40h) and receive the response.
        Parameter: h - the connection handle
        Returns: '' if sucess, or AssertionError if failed
	'''
	nm_output = nm_ipmi_repo_info_t()

	status = self.dll.NMPRK_IPMI_GetSelInfo(h,byref(nm_output))
        assert status == 0
        #print nm_output.repoVersion,nm_output.repoEntries,nm_output.getAllocInfoSup
        return nm_output

    def ipmi_get_sel_entry(self,h,entryId=0):
	'''Function: Send the Get SEL Entry command (NetFn: 0Ah Cmd: 43h) and receive the response.
	Parameters: h - The connection handle
		    entryId - The Entry ID
        Returns: '' if sucess, or AssertionError if failed
	'''
	nm_output_nextRecord = c_ushort()
	nm_output_entry = nm_ipmi_sel_entry_t()

	status = self.dll.NMPRK_IPMI_GetSelEntry(h,entryId,byref(nm_output_nextRecord),byref(nm_output_entry))
        assert status == 0
        return (nm_output_nextRecord,nm_output_entry)

    def ipmi_clear_sel(self,h):
        '''Function: Send the Clear SEL command (NetFn: 0Ah Cmd: 47h) and receive the response.
        Parameters: h - The connection handle
        Returns: '' if sucess, or AssertionError if failed
        '''
        status = self.dll.NMPRK_IPMI_ClearSel(h)
        assert status == 0



    def get_cups_data(self,h,parameter):
        ''' get cpu and memory values '''
        nm_input = nm_get_cups_data_input_t()
        nm_output = nm_get_cups_data_output_t()
        nm_input.parameter=parameter
        status = self.dll.NMPRK_GetCupsData(h,byref(nm_input),byref(nm_output))
        assert(status==0)
        return nm_output


    def ipmi_get_device_id(self,h):
	'''Send the Get Device ID command (NetFn: 06h Cmd: 01h) and receive the response.
        Parameter: h - the connection handle
        Returns: '' if sucess, or AssertionError if failed
        '''
	nm_output = nm_ipmi_device_id_t()

	status = self.dll.NMPRK_IPMI_GetDeviceId(h,byref(nm_output))
        assert status == 0
        return nm_output

    def ipmi_get_fru_info(self,h):
	'''Function: Send the Get FRU Inventory Area Info command (NetFn: 0Ah Cmd: 10h) and receive the response.
	Parameters: h - The connection handle
        Returns: '' if sucess, or AssertionError if failed
	'''
	nm_output = nm_ipmi_fru_info_t()	

	status = self.dll.NMPRK_IPMI_GetFruInfo(h,byref(nm_output))
        assert status == 0
        return nm_output

    def ipmi_read_fru_data(self,h,offset=0,length=8):
	'''Function: Send the Read FRU Data command (NetFn: 0Ah Cmd: 11h) and receive the response.
	Parameters: h - The connection handle
		    offset - The offset into the inventory
		    length - The number of bytes to read on input, the number of bytes returned on output
        Returns: '' if sucess, or AssertionError if failed
	'''
	nm_input_offset = c_int(offset)
	nm_inAndOut_length = c_int(length)
        #malloc area to storage data has read
	nm_output_data = (c_ubyte * length)()

	status = self.dll.NMPRK_IPMI_ReadFruData(h,nm_input_offset,byref(nm_inAndOut_length),byref(nm_output_data))
        assert status == 0
        return nm_output_data

    def ipmi_power_contrl(self,h,commandtype):
	'''Function: this function provides some method for power up,down,reset,cycle.
	Parameters: h - The connection handle
                    commandtype - the command you want implementation
        Returns: '' if sucess, or AssertionError if failed
	'''
        commandtype = c_ubyte(commandtype)
        status = self.dll.NMPRK_IPMI_PowerContrl(h,commandtype)
        assert status == 0

    def ipmi_power_status(self,h):
	'''Function: this function get chassis power status(0 off, 1 on).
	Parameters: h - The connection handle
                    commandtype - the command you want implementation
        Returns: 1 is on, 0 is off 
        '''
        chassisstatus = c_ubyte()
        status = self.dll.NMPRK_IPMI_PowerStatus(h,byref(chassisstatus))
        assert status == 0
        return chassisstatus

    def ipmi_get_sensor_reading(self,h,sensornumber):
        '''Function: this function provides a method to get sensor current value
        Parameters: h - The connection handle
                    commandtype - the command you want implementation
                    sensornumber - Unique number identifying the sensor
        Return: analog sensor value
        '''
        sensornumber = c_ubyte(sensornumber)
        output = (c_ubyte*4)()
        status = self.dll.NMPRK_IPMI_GetSensorReading(h,sensornumber,byref(output))
        return output

    def ipmi_get_sdr_record(self,h,recordId=0):
	'''Function: Send the Get SDR command (NetFn: 0Ah Cmd: 23h) and receive the response.
        Parameter: h - the connection handle
		   recordId - the record ID
        Returns: '' if sucess, or AssertionError if failed
        '''
	nm_input_recordId = c_ushort(recordId)
	nm_output_nextRecord = c_ushort()
	nm_output_record = nm_ipmi_sdr_record_t()

	status = self.dll.NMPRK_IPMI_GetSdrRecord(h,nm_input_recordId,byref(nm_output_nextRecord),byref(nm_output_record))
        assert status == 0
	return nm_output_nextRecord,nm_output_record

    def ipmi_get_sdr_info(self,h):
	'''Function: Send the Get SDR Repository Info command (NetFn: 0Ah Cmd: 20h) and receive the response.
        Parameter: h - the connection handle
        Returns: '' if sucess, or AssertionError if failed
        '''
	nm_output = nm_ipmi_repo_info_t()

	status = self.dll.NMPRK_IPMI_GetSdrInfo(h,byref(nm_output))
        assert status == 0
        return nm_output

import re
import subprocess
def check_network(ip):
    '''Check the network linkness. '''
    try:
        cmd = 'ping -c 2 -w 1 %s'%ip
        p = subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout= subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        result = p.stdout.read()
        regex = re.findall(b'100% packet loss',result)
        if regex:
            return False
        else:
            return True
    except :
        return False
if __name__ == '__main__':
    file_path ='/home/sara/go_test/libnmprkc.so'
    dh = cdll.LoadLibrary(file_path)
    host = "192.168.124.191"
    usr = "ADMIN"
    pwd = "ADMIN"
    status = check_network(host)
    if status:
        print('Ping IP is OK!')
        nm = BaseNMPRK(dh)
        h=nm.connect_remote(host,usr,pwd)
        print('connect')
    else:
        print('Ping IP failed!')
    
    # get node manager version
    output = nm.get_version(h)
    #print(output.version)
    
    if output.version == 5:
        ver = 3
        print('ver=3')
    elif output.version == 4:
        ver = 2.5
        print('ver=2.5')
    elif output.version == 3:
        ver = 2
        print('ver=2')
    # set parameters
     
    mode = nm_get_statistics_mode_t.GET_GLOBAL_TEMPERATURE.value
    domain = nm_domain_id_t.PLATFORM.value
    policy = 1
    '''
    output=nm.get_statistics(h,mode,domain,policy)
    if output:
        print(output.currentValue,output.minimumValue,output.maximumValue,output.averageValue)
    '''
    parameter = nm_get_cups_data_parameter_t.CUPS_PARAMETER_UTILIZATION.value
    index_para = nm_get_cups_data_parameter_t.CUPS_PARAMETER_INDEX.value
    #try:
    n = 1000
    while n and ver==3:
    #try:
        import time
        time.sleep(10)
        n =n-1
        index_output = nm.get_cups_data(h,index_para)
        indexd = index_output.data.index.index
        print('index')
        print(index_output.data.index.index)
        #parameter = nm_get_cups_data_parameter_t.CUPS_PARAMETER_DYNAMIC.value
        output=nm.get_cups_data(h,parameter)
        print('cpu,memory,io')
        cpud = output.data.util.cpu
        memd = output.data.util.memory
        iod = output.data.util.io
        print(cpud)
        print(memd)
        print(iod)

        #output=nm.get_policy(h,domain)
        #print(output.u.standard.info.policyId)
    #except Exception as e:
    #    print(e)
    
    #output = nm.get_policy(h,domain,policy)
    

    
