'''
    sel parse table
'''
#Threshold
Threshold = (
    (0x00,"Lower Non-critical going low"),
    (0x01,"Lower Non-critical going high"),
    (0x02,"Lower Critical going low"),
    (0x03,"Lower Critical going high"),
    (0x04,"Lower Non-recoverable going low"),
    (0x05,"Lower Non-recoverable going high"),
    (0x06,"Upper Non-critical going low"),
    (0x07,"Upper Non-critical going high"),
    (0x08,"Upper Critical going low"),
    (0x09,"Upper Critical going high"),
    (0x0A,"Upper Non-recoverable going low"),
    (0x0B,"Upper Non-recoverable going high"),
)

EVENT_TYPE_CODE_threshold = [
    (0x01,Threshold),
]



#generic
Generic02 = (
    (0x00,"Transition to Idle"),
    (0x01,"Transition to Active"),
    (0x02,"Transition to Busy"),
) 

Generic03 = (
    (0x00,"State Deasserted"),
    (0x01,"State Asserted"),
)
Generic04 = (
    (0x00,"Predictive Failure deasserted"),
    (0x01,"Predictive Failure asserted"),
)

Generic05 = (
    (0x00,"Limit Not Exceeded"),
    (0x01,"Limit Exceeded"),
)
Generic06 = (
    (0x00,"Performance Met"),
    (0x01,"Performance Lags"),
)
Generic07 = (
    (0x00,"transition to OK"),
    (0x01,"transition to Non-Critical from OK"),
    (0x02,"transition to Critical from less severe"),
    (0x03,"transition to Non-recoverable from less severe"),
    (0x04,"transition to Non-Critical from more severe"),
    (0x05,"transition to Critical from Non-recoverable"),
    (0x06,"transition to Non-recoverable"),
    (0x07,"Monitor"),
    (0x08,"Informational"),
)
Generic08 = (
    (0x00,"Device Removed"),
    (0x01,"Device Inserted"),
)

Generic09 = (
    (0x00,"Device Disabled"),
    (0x01,"Device Enabled"),
)
Generic0a = (
    (0x00,"transition to Running"),
    (0x01,"transition to In Test"),
    (0x02,"transition to Power Off"),
    (0x03,"transition to On Line"),
    (0x04,"transition to Off Line"),
    (0x05,"transition to Off Duty"),
    (0x06,"transition to Degraded"),
    (0x07,"transition to Power Save"),
    (0x08,"Install Error"),
)

Generic0b = (
    (0x00,"Fully Redundant"),
    (0x01,"Redundancy Lost"),
    (0x02,"Redundancy Degraded"),
    (0x03,"Non-redundant"),
    (0x04,"Sufficient Resources from Insufficient Resources"),
    (0x05,"Insufficient Resources"),
    (0x06,"Redundancy Degraded from Fully Redundant"),
    (0x07,"Redundancy Degraded from Non-redundant"),
)
Generic0c = (
    (0x00,"D0 Power State"),
    (0x01,"D1 Power State"),
    (0x02,"D2 Power State"),
    (0x03,"D3 Power State"),
)

EVENT_TYPE_CODE_generic = [
	(0x02,Generic02),
	(0x03,Generic03),
	(0x04,Generic04),
	(0x05,Generic05),
	(0x06,Generic06),
	(0x07,Generic07),
	(0x08,Generic08),
	(0x09,Generic09),
	(0x0a,Generic0a),
	(0x0b,Generic0b),
	(0x0c,Generic0c),		
]



#sensor-specific
Temperature = ()
Voltage = ()
Current = ()
Fan = ()
Physical_Security = (
    (0x00,"General Chassis Intrusion"),
    (0x01,"Drive Bay intrusion"),
    (0x02,"I/O Card area intrusion"),
    (0x03,"Processor area intrusion "),
    (0x04,"LAN Leash Lost"),
    (0x05,"Unauthorized dock/undock"),
    (0x06,"FAN area intrusion"),
)

Platform_Security_Violation_Attempt = (
    (0x00,"Secure Mode(Front Panel Lockout)Violation attempt"),
    (0x01,"Pre-boot Password Violation user password"),
    (0x02,"Pre-boot Password Violation attempt setup password"),
    (0x03,"Pre-boot Password Violation network boot password"),
    (0x04,"Other pre-boot Password Violation"),
    (0x05,"Out-of-band Access Password Violation"),
)

Processor = (
	(0x00,"IERR"),
	(0x01,"Thermal Trip"),
	(0x02,"FRB1/BIST failure"),
	(0x03,"FRB2/Hang in POST failure"),
	(0x04,"FRB3/Processor Startup/Initialization failure"),
	(0x05,"Configuration Error"),
	(0x06,"SM BIOS Uncorrectable CPU-complex Error"),
	(0x07,"Processor Presence detected"),
	(0x08,"Processor disabled"),
	(0x09,"Terminator Presence Detected"),
	(0x0A,"Processor Automatically Throttled"),
)

Power_Supply = (
	(0x00,"Presence detected"),
	(0x01,"Power Supply Failure detected"),
	(0x02,"Predictive Failure"),
	(0x03,"Power Supply input lost(AC/DC)"),
	(0x04,"Power Supply input lost or out-of-range"),
	(0x05,"Power Supply input out-of-range, but present"),
	(0x06,"Configuration error"),
)

Power_Unit = (
	(0x00,"Power Off/Power Down"),
	(0x01,"Power Cycle"),
	(0x02,"240VA Power Down"),
	(0x03,"Interlock Power Down"),
	(0x04,"AC lost"),
	(0x05,"Soft Power Control Failure"),
	(0x06,"Power Unit Failure detected"),
	(0x07,"Predictive Failure"),
)

Cooling_Device = ()

Memory = (
	(0x00,"Correctable ECC/other correctable memory error"),
	(0x01,"Uncorrectable ECC/other uncorrectable memory error"),
	(0x02,"Parity"),
	(0x03,"Memory Scrub Failed"),
	(0x04,"Memory Device Disabled"),
	(0x05,"Correctable ECC/other correctable memory error logging limit reached"),
	(0x06,"Presence detected"),
	(0x07,"Configuration error"),
	(0x08,"Spare"),
)

Drive_Slot = (
	(0x00,"Drive Present"),
)

Other_Units_based_Sensor = ()

POST_Memory_Resize = ()

System_Firmware_Progress = (
	(0x00,"System Firmware Error"),
	(0x01,"System Firmware Hang"),
	(0x02,"System Firmware Progress"),
)

Event_Logging_Disabled = (
	(0x00,"Correctable Memory Error Logging Disabled"),
	(0x01,"Event Type Logging Disabled"),
	(0x02,"Log Area Reset/Cleared"),
	(0x03,"All Event Logging Disabled"),
	(0x04,"SEL Full"),
	(0x05,"SEL Almost Full"),
)

Watchdog_1 = (
	(0x00,"BIOS Watchdog Reset"),
	(0x01,"OS Watchdog Reset"),
	(0x02,"OS Watchdog Shut Down"),
	(0x03,"OS Watchdog Power Down"),
	(0x04,"OS Watchdog Power Cycle"),
	(0x05,"OS Watchdog NMI/Diagnostic Interrupt"),
	(0x06,"OS Watchdog Expired,status only"),
	(0x07,"OS Watchdog pre-timeout Interrupt,non-NMI"),
)

System_Event = (
	(0x00,"System Reconfigured"),
	(0x01,"OEM System Boot Event"),
	(0x02,"Undetermined system hardware failure"),
	(0x03,"Entry added to Auxiliary Log"),
	(0x04,"PEF Action"),
	(0x05,"Timestamp Clock Sync"),
)

Critical_Interrupt = (
	(0x00,"Front Panel NMI/Diagnostic Interrupt"),
	(0x01,"Bus Timeout"),
	(0x02,"I/O channel check NMI"),
	(0x03,"Software NMI"),
	(0x04,"PCI PERR"),
	(0x05,"PCI SERR"),
	(0x06,"EISA Fail Safe Timeout"),
	(0x07,"Bus Correctable Error"),
	(0x08,"Bus Uncorrectable Error"),
	(0x09,"Fatal NMI"),
	(0x0A,"Bus Fatal Error"),
)

Button_Switch = (
	(0x00,"Power Button pressed"),
	(0x01,"Sleep Button pressed"),
	(0x02,"Reset Button pressed"),
	(0x03,"FRU latch open"),
	(0x04,"FRU service request button"),
)

Module_Board = ()

Microcontroller_Coprocessor = (
        (0x00,"Device Disabled"),
        (0x01,"Device Enabled"),
)

Add_in_Card = ()

Chassis = ()

Chip_Set = (
	(0x00,"Soft Power Control Failure"),
)

Other_FRU = ()

Cable_Interconnect = ()

Terminator = ()

System_Boot_Initiated = (
	(0x00,"Initiated by power up"),
	(0x01,"Initiated by hard reset"),
	(0x02,"Initiated by warm reset"),
	(0x03,"User requested PXE boot"),
	(0x04,"Automatic boot to diagnostic"),
	(0x05,"Unknown"),
	(0x06,"Unknown"),
        (0x07,"System Restart"),
)

Boot_Error = (
	(0x00,"No bootable media"),
	(0x01,"Non-bootable diskette left in drive"),
	(0x02,"PXE Server not found"),
	(0x03,"Invalid boot sector"),
	(0x04,"Timeout waiting for user selection of boot source"),
)

OS_Boot = (
	(0x00,"A:boot completed"),
	(0x01,"C:boot completed"),
	(0x02,"PXE boot completed"),
	(0x03,"Diagnostic boot completed"),
	(0x04,"CD-ROM boot completed"),
	(0x05,"ROM boot completed"),
	(0x06,"boot completed-boot device not specified"),
)

OS_Critical_Stop = (
	(0x00,"Stop during OS load/initialization"),
	(0x01,"Run-time Stop"),
	(0x01,"Unknown"),
        (0x03,"OS graceful shutdown"),
)

Slot_Connector = (
	(0x00,"Fault Status asserted"),
	(0x01,"Identify Status asserted"),
	(0x02,"Slot/Connector Device installed/attached"),
	(0x03,"Slot/Connector Ready for Device Installation - Typically"),
	(0x04,"Slot/Connector Ready for Device Removal"),
	(0x05,"Slot Power is Off"),
	(0x06,"Slot/Connector Device Removal Request"),
	(0x07,"Interlock asserted"),
	(0x08,"Slot is Disabled"),
	(0x09,"Slot holds spare device"),
)

System_ACPI_Power_State = (
	(0x00,"S0/G0 working"),
	(0x01,"S1 sleeping with system h/w & processor context maintained"),
	(0x02,"S2 sleeping, processor context lost"),
	(0x03,"S3 sleeping, processor & h/w context lost, memory retained"),
	(0x04,"S4 non-volatile sleep / suspend-to disk"),
	(0x05,"S5/G2 soft-off"),
	(0x06,"S4/S5 soft-off,particular S4/S5 state cannot be determined"),
	(0x07,"G3/Mechanical Off"),
	(0x08,"Sleeping in an S1,S2,or S3 states"),
	(0x09,"G1 sleeping"),
	(0x0A,"S5 entered by override"),
	(0x0B,"Legacy ON state"),
	(0x0C,"Legacy OFF state"),
	(0x0E,"Unknown"),
)

Watchdog_2 = (
	(0x00,"Timer expired, status only"),
	(0x01,"Hard Reset"),
	(0x02,"Power Down"),
	(0x03,"Power Cycle"),
	(0x04,"Unknown"),
	(0x05,"Unknown"),
	(0x06,"Unknown"),
	(0x07,"Unknown"),
	(0x08,"Timer interrupt"),
)

Platform_Alert = (
	(0x00,"platform generated page"),
	(0x01,"platform generated LAN alert"),
	(0x02,"Platform Event Trap generated, formatted per IPMI PET specification"),
	(0x03,"platform generated SNMP trap, OEM format"),
)

Entity_Presence = (
	(0x00,"Entity Present"),
	(0x01,"Entity Absent"),
	(0x02,"Entity Disabled"),
)

Monitor_ASIC_IC = ()

LAN = (
	(0x00,"LAN Heartbeat Lost"),
	(0x01,"LAN Heartbeat"),
)

Management_Subsystem_Health = (
	(0x00,"sensor access degraded or unavailable"),
	(0x01,"controller access degraded or unavailable"),
	(0x02,"management controller off-line"),
	(0x03,"management controller unavailable"),
)

Battery = (
	(0x00,"battery low"),
	(0x01,"battery failed"),
	(0x02,"battery presence detected"),
)

Session_Audit = (
	(0x00,"Session Activated"),
	(0x01,"Session Deactivated"),
        (0x02,"Invalid Username of Password"),
)

Version_Change = (
	(0x00,"Hardware change detected with associated Entity"),
	(0x01,"Firmware or software change detected with associated Entity"),
	(0x02,"Hardware incompatibility detected with associated Entity"),
	(0x03,"Firmware or software incompatibility detected with associated Entity"),
	(0x04,"Entity is of an invalid or unsupported hardware version"),
	(0x05,"Entity contains an invalid or unsupported firmware or software version"),
	(0x06,"Hardware Change detected with associated Entity was successful"),
	(0x07,"Software or F/W Change detected with associated Entity was successful"),
)

FRU_State = (
	(0x00,"FRU Not Installed"),
	(0x01,"FRU Inactive"),
	(0x02,"FRU Activation Requested"),
	(0x03,"FRU Activation In Progress"),
	(0x04,"FRU Active"),
	(0x05,"FRU Deactivation Requested"),
	(0x06,"FRU Deactivation In Progress"),
	(0x07,"FRU Communication Lost"),
)

EVENT_TYPE_CODE_sensorSpecific = [
	(0x01,Temperature),
	(0x02,Voltage),
	(0x03,Current),
	(0x04,Fan),
	(0x05,Physical_Security),
	(0x06,Platform_Security_Violation_Attempt),
	(0x07,Processor),
	(0x08,Power_Supply),
	(0x09,Power_Unit),
	(0x0a,Cooling_Device),
	(0x0b,Memory),
	(0x0c,Drive_Slot),
	(0x0d,Other_Units_based_Sensor),
	(0x0e,POST_Memory_Resize),
	(0x0f,System_Firmware_Progress),
	(0x10,Event_Logging_Disabled),
	(0x11,Watchdog_1),
	(0x12,System_Event),
	(0x13,Critical_Interrupt),
	(0x14,Button_Switch),
	(0x15,Module_Board),
	(0x16,Microcontroller_Coprocessor),
	(0x17,Add_in_Card),
	(0x18,Chassis),
	(0x19,Chip_Set),
	(0x1a,Other_FRU),
	(0x1b,Cable_Interconnect),
	(0x1c,Terminator),
	(0x1d,System_Boot_Initiated),
	(0x1e,Boot_Error),
	(0x1f,OS_Boot),
	(0x20,OS_Critical_Stop),
	(0x21,Slot_Connector),
	(0x22,System_ACPI_Power_State),
	(0x23,Watchdog_2),
	(0x24,Platform_Alert),
	(0x25,Entity_Presence),
	(0x26,Monitor_ASIC_IC),
	(0x27,LAN),
	(0x28,Management_Subsystem_Health),
	(0x29,Battery),
	(0x2a,Session_Audit),
	(0x2b,Version_Change),
	(0x2c,FRU_State)
]

#oem
#Not implemented


SENSOR_TYPE = ( 
    (0x01,"Temperature"),
    (0x02,"Voltage"),
    (0x03,"Current"),
    (0x04,"Fan"),
    (0x05,"Physical Security"),
    (0x06,"Platform Security Violation Attempt"),
    (0x07,"Processor"),
    (0x08,"Power Supply"),
    (0x09,"Power Unit"),
    (0x0A,"Cooling Device"),
    (0x0B,"Other Units-based Sensor"),
    (0x0C,"Memory"),
    (0x0D,"Drive Slot"),
    (0x0E,"POST Memory Resize"),
    (0x0F,"System Firmware Progress"),
    (0x10,"Event Logging Disabled"),
    (0x11,"Watchdog 1"),
    (0x12,"System Event"),
    (0x13,"Critical Interrupt"),
    (0x14,"Button/Switch"),
    (0x15,"Module/Board"),
    (0x16,"Microcontroller/Coprocessor"),
    (0x17,"Add-in Card"),
    (0x18,"Chassis"),
    (0x19,"Chip Set"),
    (0x1A,"Other FRU"),
    (0x1B,"Cable/Interconnect"),
    (0x1C,"Terminator"),
    (0x1D,"System Boot Initiated"),
    (0x1E,"Boot Error"),
    (0x1F,"OS Boot"),
    (0x20,"OS Critical Stop"),
    (0x21,"Slot/Connector"),
    (0x22,"System ACPI Power State"),
    (0x23,"Watchdog 2"),
    (0x24,"Platform Alert"),
    (0x25,"Entity Presence"),
    (0x26,"Monitor ASIC/IC"),
    (0x27,"LAN"),
    (0x28,"Management Subsystem Health"),
    (0x29,"Battery"),
    (0x2A,"Session Audit"),
    (0x2B,"Version Change"),
    (0x2C,"FRU State"),
)


#event severiy
EVENT_SEVERITY_NORMAL = 0
EVENT_SEVERITY_WARNING = 1
EVENT_SEVERITY_ERROR = 2

'''
   Manufacturer ID Code table
   https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers
'''
Manufacturer_ID = (
    (2,"IBM"),
    (11,"Hewlett-Packard"),
    (1092,"Hewlett-Packard"),
    (11147,"Hewlett-Packard"),
    (16401,"Hewlett-Packard"),
    (46898,"Hewlett-Packard"),
    (674,"Dell"),
    (299,"Sun"),
    (1167,"Sun"),
    (5771,"Cisco"),
    (5842,"Cisco"),
    (26484,"Cisco"),
    (46606,"Cisco"),
    (343,"Intel"),
    (111,"Oracle"),
    (37945,"Inspur"),
    (19046,"Lenovo"),
    (33024,"Lenovo"),
    (2623,"ASUS"),
    (34774,"Huawei"),
    (15370,"GIGABYTE"),
    (10876,"SuperMicro"),
    (47488,"SuperMicro"),
)



'''
  chassis type  
'''
Chassis_Type = (
    "Unspecified",
    "Other",
    "Unknown",
    "Desktop",
    "Low Profile Desktop",
    "Pizza Box",
    "Mini Tower",
    "Tower",
    "Portable",
    "LapTop",
    "Notebook",
    "Hand Held",
    "Docking Station",
    "All in One",
    "Sub Notebook",
    "Space-saving",
    "Lunch Box",
    "Main Server Chassis",
    "Expansion Chassis",
    "SubChassis",
    "Bus Expansion Chassis",
    "Peripheral Chassis",
    "RAID Chassis",
    "Rack Mount Chassis",
    "Sealed-case PC",
    "Multi-system Chassis",
    "CompactPCI",
    "AdvancedTCA",
    "Blade",
    "Blade Enclosure",
)


SENSOR_UNIT = (
    (0,"unspecified"),
    (1,"degrees C "),
    (2,"degrees F"),
    (3,"degrees K"),
    (4,"Volts"),
    (5,"Amps"),
    (6,"Watts"),
    (7,"Joules"),
    (8,"Coulombs"),
    (9,"VA"),
    (10,"Nits"),
    (11,"lumen"),
    (12,"lux"),
    (13,"Candela"),
    (14,"kPa"),
    (15,"PSI"),
    (16,"Newton"),
    (17,"CFM"),
    (18,"RPM"),
    (19,"Hz"),
    (20,"microsecond"),
    (21,"millisecond"),
    (22,"second"),
    (23,"minute"),
    (24,"hour"),
    (25,"day"),
    (26,"week"),
    (27,"mil"),
    (28,"inches"),
    (29,"feet"),
#    (30,""),
#    (31,""),
#    (32,""),
#    (33,""),
#    (34,""),
#    (35,""),
#    (36,""),
#    (37,""),
#    (38,""),
#    (39,""),
#    (40,""),
#    (41,""),
#    (42,""),
#    (43,""),
#    (44,""),
#    (45,""),
#    (46,""),
#    (47,""),
#    (48,""),
#    (49,""),
#    (50,""),
#    (51,""),
#    (52,""),
#    (53,""),
#    (54,""),
#    (55,""),
#    (56,""),
#    (57,""),
#    (58,""),
#    (59,""),
#    (60,""),
#    (61,""),
#    (62,""),
#    (63,""),
#    (64,""),
#    (65,""),
#    (66,""),
#    (67,""),
#    (68,""),
#    (69,""),
#    (70,""),
#    (71,""),
#    (72,""),
#    (73,""),
#    (74,""),
#    (75,""),
#    (76,""),
#    (77,""),
#    (78,""),
#    (79,""),
#    (80,""),
#    (81,""),
#    (82,""),
#    (83,""),
#    (84,""),
#    (85,""),
#    (86,""),
#    (87,""),
#    (88,""),
#    (89,""),
#    (90,""),
)
