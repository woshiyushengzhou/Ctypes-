from ctypes import *
import enum

class nm_domain_id_t(enum.Enum):
    PLATFORM = 0
    CPU = 1
    MEMORY = 2
    HW_PROTECTION = 3
    HIGH_POWER_IO = 4
    LAST_DOMAIN = HIGH_POWER_IO

class nm_policy_enable_disable_t(enum.Enum):
    GLOBAL_DISABLE = 0
    GLOBAL_ENABLE = 1
    DOMAIN_DISABLE = 2
    DOMAIN_ENABLE = 3
    POLICY_DISABLE = 4
    POLICY_ENABLE = 5

class nm_policy_trigger_type_t(enum.Enum):
    NO_POLICY_TRIGGER = 0
    INLET_TEMPERATURE_TRIGGER = 1
    MISSING_POWER_READING_TIMEOUT_TRIGGER =2
    TIME_AFTER_HOST_RESET_TRIGGER  =3
    BOOT_TIME_TRIGGER  = 4

class nm_aggressive_cpu_power_correction_t(enum.Enum):
    DEFAULT = 0
    T_STATES_NOT_ALLOWED = 1
    T_STATES_ALLOWED = 2

class nm_suspend_period_recurrence_pattern_t(enum.Enum):
    MONDAY = 0x01
    TUESDAY = 0x02
    WEDNESDAY = 0x04
    THURSDAY = 0x08
    FRIDAY = 0x10
    SATURDAY = 0x20
    SUNDAY = 0x40

class nm_reset_statistics_mode_t(enum.Enum):
    RESET_GLOBAL_POWER_TEMP = 0x00
    RESET_POLICY_POWER_TEMP = 0x01
    RESET_GLOBAL_HOST_UNHANDLED_REQ = 0x1B
    RESET_GLOBAL_HOST_RESPONSE_TIME = 0x1C
    RESET_GLOBAL_CPU_THROTTLING = 0x1D
    RESET_GLOBAL_MEMORY_THROTTLING = 0x1E
    RESET_GLOBAL_HOST_COMMUNICATION_FAILURE = 0x1F

class nm_get_statistics_mode_t(enum.Enum):
    GET_GLOBAL_POWER = 0X01
    GET_GLOBAL_TEMPERATURE = 0x02
    GET_GLOBAL_THROTTLING = 0x03
    GET_GLOBAL_VOLUMETRIC_AIRFLOW = 0x04
    GET_GLOBAL_OUTLET_AIRFLOW_TEMPERATURE = 0x05
    GET_GLOBAL_CHASSIS_POWER = 0x06
    GET_POLICY_POWER = 0x11
    GET_POLICY_TEMPERATURE = 0x12
    GET_POLICY_THROTTLING = 0x13
    GET_GLOBAL_HOST_UNHANDLED_REQ = 0x1B
    GET_GLOBAL_HOST_RESPONSE_TIME = 0x1C
    GET_GLOBAL_CPU_THROTTLING = 0x1D
    GET_GLOBAL_MEMORY_THROTTLING = 0x1E
    GET_GLOBAL_HOST_COMMUNICATION_FAILURE = 0x1F

class nm_ptu_launch_power_characterization_on_hw_change_t(enum.Enum):
    DONT_LAUNCH_OR_CANCEL_PREV_LAUNCH = 0x00
    LAUNCH_NODE_MANAGER_CHARACTERIZATION = 0x01
    LAUNCH_NODE_MANAGER_CHARACTERIZATION_ON_HW_CHANGE = 0x02

class nm_ptu_bmc_table_config_phase_action_t(enum.Enum):
    BMC_TABLE_NO_ACTION = 0x00
    BMC_TABLE_CLEAR_ALL = 0x01
    BMC_TABLE_WRITE = 0x02

class nm_ptu_bmc_phase_state_machine_action_t(enum.Enum):
    BMC_PHASE_NO_ACTION = 0x00
    BMC_PHASE_RESTART = 0x01
    BMC_PHASE_SKIP_TO_THE_NEXT_TABLE_ENTRY = 0x02
    BMC_PHASE_EXIT = 0x03

class nm_ptu_power_domain_id_t(enum.Enum):
    POWER_DOMAIN_PLATFORM = 0x00
    POWER_DOMAIN_CPU_SUBSYSTEM = 0x01
    POWER_DOMAIN_MEMORY_SUBSYSTEM = 0x02

class nm_ptu_power_draw_characterization_point_t(enum.Enum):
    POWER_DRAW_CHARACTERIZATION_POINT_MAX = 0x00
    POWER_DRAW_CHARACTERIZATION_POINT_MIN = 0x01
    POWER_DRAW_CHARACTERIZATION_POINT_EFF = 0x02

class nm_get_cups_data_parameter_t(enum.Enum):
    CUPS_PARAMETER_INDEX = 0x01
    CUPS_PARAMETER_DYNAMIC = 0x02
    CUPS_PARAMETER_BASE = 0x03
    CUPS_PARAMETER_AGGREGATE = 0x04
    CUPS_PARAMETER_UTILIZATION = 0X05

class nm_cups_policy_id_t(enum.Enum):
    CUPS_CORE_DOMAIN = 0x01
    CUPS_MEMORY_DOMAIN = 0x02
    CUPS_IO_DOMAIN = 0x04

class nm_cups_target_identifier_t(enum.Enum):
    CUPS_TARGET_BMC = 0x00
    CUPS_TARGET_REMOTE_CONSOLE = 0x01

class ipmi_cipher_suite_t(enum.Enum):
    CIPHER_SUITE_0 = 0
    CIPHER_SUITE_1 = 1
    CIPHER_SUITE_2 = 2
    CIPHER_SUITE_3 = 3
    CIPHER_SUITE_6 = 6
    CIPHER_SUITE_7 = 7
    CIPHER_SUITE_8 = 8
    CIPHER_SUITE_11 = 11
    CIPHER_SUITE_12 = 12

class ipmi_acpi_system_power_state_t(enum.Enum):
    ACPI_POWER_STATE_SYS_S0G0 = 0x00
    ACPI_POWER_STATE_SYS_S1 = 0x01
    ACPI_POWER_STATE_SYS_S2 = 0x02
    ACPI_POWER_STATE_SYS_S3 = 0x03
    ACPI_POWER_STATE_SYS_S4 = 0x04
    ACPI_POWER_STATE_SYS_S5G2 = 0x05
    ACPI_POWER_STATE_SYS_S4S5 = 0x06
    ACPI_POWER_STATE_SYS_G3 = 0x07
    ACPI_POWER_STATE_SYS_SLEEPING = 0x08
    ACPI_POWER_STATE_SYS_G1_SLEEP = 0x09
    ACPI_POWER_STATE_SYS_OVERRIDE = 0x0A
    ACPI_POWER_STATE_SYS_LEGACY_ON = 0x20 
    ACPI_POWER_STATE_SYS_LEGACY_OFF = 0x21
    ACPI_POWER_STATE_SYS_UNKNOWN = 0x2A
    ACPI_POWER_STATE_SYS_NO_CHANGE = 0x7f 



class ipmi_acpi_device_power_state_t(enum.Enum):
    '''IPMI ACPI Device Power States
    '''
    ACPI_POWER_STATE_DEV_D0 = 0x00
    ACPI_POWER_STATE_DEV_D1 = 0x01
    ACPI_POWER_STATE_DEV_D2 = 0x02
    ACPI_POWER_STATE_DEV_D3 = 0x03
    ACPI_POWER_STATE_DEV_UNKNOWN = 0x2a
    ACPI_POWER_STATE_DEV_NO_CHANGE = 0x7f

#Parameters passed to the NMPRK_ConnectRemote function
class nmprk_conn_remote_parameters_t (Structure):
    _fields_ =[("ipOrHostname",c_char_p),
               ("username",c_char_p),
               ("password",c_char_p),
               ("useCustomCipherSuite",c_int),
               ("customCipherSuite",c_int)
              ]

#Parameters to pass to the ::NMPRK_EnableDisablePolicyControl function
class nm_enable_disable_policy_control_input_t(Structure):
    '''Parameters to pass to the :nmEnableDisablePolicyControl function
    '''
    _fields_=[("flags",c_int),
              ("domain",c_int),
              ("policy",c_ubyte),
             ]

#Parameters that represent a Node Manager Policy
class nm_policy_info_t(Structure):
    '''Parameters that represent a Node Manager Policy.
    Used with the following functions: nmSetPolicy; nmGetPolicy; nmGetAllPolicies.
    '''
    _fields_=[("domain",c_int),
              ("policyId",c_ubyte),
              ("policyEnabled",c_int),
              ("policyTriggerType",c_int),
              ("aggressiveCpuPowerCorrection",c_int),
              ("policyExceptionActionShutdown",c_int),
              ("policyExceptionActionSendAlert",c_int),
              ("secondaryPowerDomain",c_int),
              ("policyTargetLimit",c_ushort),
              ("correctionTimeLimit",c_uint),
              ("policyTriggerLimit",c_ushort),
              ("statisticsReportingPeriod",c_ushort),
             ]

#Parameters to pass to the ::NMPRK_SetPolicy function
class nm_set_policy_input_t(Structure):
    #_fields_=[("info",POINTER(nm_policy_info_t)),
    _fields_=[("info",nm_policy_info_t),
              ("removePolicy",c_int),
             ]

#Parameters to pass to the ::NMPRK_GetPolicy function
class nm_get_policy_input_t(Structure):
    _fields_=[("domain",c_int),
              ("policy",c_ubyte),
             ]
# 00h - standard; 80h - policy_id_invalid; 81h - domain_id_invalid
#class standard(Structure):
#    _fields_=[("info",POINTER(nm_policy_info_t)),
#              ("perDomainPolicyControlEnabled",c_int),
#              ("globalPolicyControlEnabled",c_int),
#              ("policyCreatedByOtherClient",c_int),
#             ]
#class policy_id_invalid(Structure):
#    _fields_=[("valid",c_int),
#              ("nextValidPolicyId",c_ubyte),
#              ("numberOfDefinedPoliciesForDomain",c_ubyte),
#             ]
#class domain_id_invalid(Structure):
#    _fields_=[("valid",c_int),
#              ("nextValidDomainId",c_ubyte),
#              ("numberOfAvailableDomains",c_ubyte),
#             ]
#class u(Union):
#    _fields_=[("standard",POINTER(standard)),
#              ("policy_id_invalid",policy_id_invalid),
#              ("domain_id_invalid",domain_id_invalid),
#             ]
##Parameters returned from the ::NMPRK_GetPolicy function
#class nm_get_policy_output_t(Structure):
#    #_fields_=[("u",POINTER(u)),]
#    _fields_=[("u",u)]
#
class standard(Structure):
    _fields_=[("info",nm_policy_info_t),
              ("perDomainPolicyControlEnabled",c_int),
              ("globalPolicyControlEnabled",c_int),
              ("policyCreatedByOtherClient",c_int),
             ]
class policy_id_invalid(Structure):
    _fields_=[("valid",c_int),
              ("nextValidPolicyId",c_ubyte),
              ("numberOfDefinedPoliciesForDomain",c_ubyte),
             ]
class domain_id_invalid(Structure):
    _fields_=[("valid",c_int),
              ("nextValidDomainId",c_ubyte),
              ("numberOfAvailableDomains",c_ubyte),
             ]
class u(Union):
    _fields_=[("standard",standard),
              ("policy_id_invalid",policy_id_invalid),
              ("domain_id_invalid",domain_id_invalid),
             ]
#Parameters returned from the ::NMPRK_GetPolicy function
class nm_get_policy_output_t(Structure):
    _fields_=[("u",u)]
#Parameters to pass to the ::NMPRK_SetPolicyAlertThresholds function
class nm_set_policy_alert_thresholds_input_t(Structure):
    _fields_=[("domain",c_int),
              ("policy",c_ubyte),
              ("numberOfAlertThresholds",c_ubyte),
              ("alertThresholdsArray",c_ushort*3),
             ]

#Parameters to pass to the ::NMPRK_GetPolicyAlertThresholds function
class nm_get_policy_alert_thresholds_input_t(Structure):
    _fields_=[("domain",c_int),
              ("policy",c_ubyte),
             ]

#Parameters returned from the ::NMPRK_GetPolicyAlertThresholds function
class nm_get_policy_alert_thresholds_output_t(Structure):
    _fields_=[("numberOfAlertThresholds",c_ubyte),
              ("alertThresholdsArray",c_ushort*3),
             ]

#Represents a Node Manager Policy Suspend Period
class nm_policy_suspend_period_t(Structure):
    _fields_=[("startTime",c_ubyte),
              ("stopTime",c_ubyte),
              #("recurrencePattern",POINTER(nm_suspend_period_recurrence_pattern_t)),
              ("recurrencePattern",c_int),
             ]

#Parameters to pass to the ::NMPRK_SetPolicySuspendPeriods function
class nm_set_policy_suspend_periods_input_t(Structure):
    _fields_=[("domain",c_int),
              ("policy",c_ubyte),
              ("numberOfSuspendPeriods",c_ubyte),
              #change
              #("suspendPeriods",POINTER(nm_policy_suspend_period_t)*5),
              ("suspendPeriods",nm_policy_suspend_period_t*5),
             ]

#Parameters to pass to the ::NMPRK_GetPolicySuspendPeriods function
class nm_get_policy_suspend_periods_input_t(Structure):
    _fields_=[("domain",c_int),
              ("policy",c_ubyte),
             ]

#Parameters returned from the ::NMPRK_GetPolicySuspendPeriods function
class nm_get_policy_suspend_periods_output_t(Structure):
    _fields_=[("numberOfSuspendPeriods",c_ubyte),
              ("suspendPeriods",POINTER(nm_policy_suspend_period_t)*5),
             ]

#Parameters to pass to the ::NMPRK_ResetStatistics function
class nm_reset_statistics_input_t(Structure):
    _fields_=[("mode",c_int),
              #("mode",POINTER(nm_reset_statistics_mode_t)),
              ("domain",c_int),
              ("policy",c_ubyte),
             ]

#Parameters to pass to the ::NMPRK_GetStatistics function
class nm_get_statistics_input_t(Structure):
    _fields_=[("mode",c_int),
              #("mode",POINTER(nm_get_statistics_mode_t)),
              ("domain",c_int),
              ("policy",c_ubyte),
             ]

#Parameters returned from the ::NMPRK_GetStatistics function
class nm_get_statistics_output_t(Structure):
    _fields_=[("currentValue",c_ushort),
              ("minimumValue",c_ushort),
              ("maximumValue",c_ushort),
              ("averageValue",c_ushort),
              ("timestamp",c_uint),
              ("statisticsReportingPeriod",c_uint),
              ("domain",c_int),
              ("policyGlobalAdministrativeState",c_int),
              ("policyOperationalState",c_int),
              ("measurementsState",c_int),
              ("policyActivationState",c_int),
             ]

#Parameters to pass to the ::NMPRK_GetCapabilities function
class nm_get_capabilities_input_t(Structure):
    _fields_=[("domain",c_int),
              ("policyTriggerType",c_int),
             ]

#Parameters returned from the ::NMPRK_GetCapabilities function
class nm_get_capabilities_output_t(Structure):
    _fields_=[("maxConcurrentSettings",c_ubyte),
              ("maxValue",c_ushort),
              ("minValue",c_ushort),
              ("minCorrectionTime",c_uint),
              ("maxCorrectionTime",c_uint),
              ("minStatisticsReportingPeriod",c_ushort),
              ("maxStatisticsReportingPeriod",c_ushort),
              ("domainLimitingScope",c_int),
              ("limitingBasedOn",c_int),
             ]

#Parameters returned from the ::NMPRK_GetVersion function
class nm_get_version_output_t(Structure):
    _fields_=[("version",c_ubyte),
               ("ipmiVersion",c_ubyte),
               ("patchVersion",c_ubyte),
               ("majorFirmwareRevision",c_ubyte),
               ("minorFirmwareRevision",c_ubyte),
              ]

#Parameters to pass to the ::NMPRK_SetPowerDrawRange function
class nm_set_power_draw_range_input_t(Structure):
    _fields_=[("domain",c_int),
              ("minimumPowerDraw",c_ushort),
              ("maximumPowerDraw",c_ushort),
             ]

class destinationInformation(Union):
    _fields_=[("i2cSlaveAddress",c_ubyte),
              ("destinationSelector",c_ubyte),
             ]
#Parameters for a Node Manager Alert Destination
class nm_alert_destination_t(Structure):
    _fields_=[("channelNumber",c_ubyte),
              ("destinationInformationReceiver",c_int),
              ("destinationInformation",POINTER(destinationInformation)),
              ("alertStringSelector",c_ubyte),
              ("sendAlertString",c_int),
             ]

#Parameters to pass to the ::NMPRK_SetAlertDestination function
class nm_set_alert_destination_input_t(Structure):
    _fields_=[("alertDestination",nm_alert_destination_t),
            #change
            #("alertDestination",POINTER(nm_alert_destination_t)),
             ]

#Parameters returned from the ::NMPRK_GetAlertDestination function
class nm_get_alert_destination_output_t(Structure):
    _fields_=[("alertDestination",POINTER(nm_alert_destination_t)),
             ]

#Parameters to pass to the ::NMPRK_PlatformCharacterizationLaunchRequest function
class nm_platform_characterization_launch_req_input_t(Structure):
    _fields_=[("launchAction",c_int),
              #("launchAction",POINTER(nm_ptu_launch_power_characterization_on_hw_change_t))
              ("bmcTableConfigPhaseActio/n",c_int),
              #("bmcTableConfigPhaseActio/n",POINTER(nm_ptu_bmc_table_config_phase_action_t)),
              ("bmcPhaseStateMachineAction",c_int),
              #("bmcPhaseStateMachineAction",POINTER(nm_ptu_bmc_phase_state_machine_action_t)),
              ("powerDomainId",c_int),
              #("powerDomainId",POINTER(nm_ptu_power_domain_id_t)),
              ("powerDrawCharacterizationPoint",c_int),
              #("powerDrawCharacterizationPoint",POINTER(nm_ptu_power_draw_characterization_point_t)),
              ("delay",c_uint),
              ("timeToRun",c_uint),
             ]

#Parameters to pass to the ::NMPRK_GetNodeManagerPowerCharacterizationRange function
class nm_get_nm_power_characterization_range_input_t(Structure):
    _fields_=[("dominId",c_int),
             ]

#Parameters returned from the ::NMPRK_GetNodeManagerPowerCharacterizationRange function
class nm_get_nm_power_characterization_range_output_t(Structure):
    _fields_=[("timestamp",c_uint),
              ("maxPowerDraw",c_ushort),
              ("minPowerDraw",c_ushort),
              ("effPowerDraw",c_ushort),
             ]

#Parameters returned from the ::NMPRK_GetCupsCapabilities function
class nm_get_cups_capabilities_output_t(Structure):
    _fields_=[("cupsEnabled",c_int),
              ("cupsPoliciesAvailable",c_int),
              ("cupsVersion",c_ubyte),
              ("reserved",c_ubyte),
             ]
#Parameters returned from the ::NMPRK_GetCupsData function
class nm_get_cups_data_input_t(Structure):
    _fields_=[("parameter",c_int),
             ]

class index(Structure):
    _fields_=[("index",c_ushort),
             ]
class dynamic(Structure):
    _fields_=[("cpu",c_ushort),
              ("memory",c_ushort),
              ("io",c_ushort),
             ]
class base(Structure):
    _fields_=[("cpu",c_ulonglong),
              ("memory",c_ulonglong),
              ("io",c_ulonglong),
             ]

class aggregate(Structure):
    _fields_=[("cpu",c_ulonglong),
              ("memory",c_ulonglong),
              ("io",c_ulonglong),
             ]
class util(Structure):
    _fields_=[("cpu",c_ulonglong),
              ("memory",c_ulonglong),
              ("io",c_ulonglong),
             ]
class data(Union):
    #change
    _fields_=[("index",index),
              ("dynamic",dynamic),
              ("base",base),
              ("aggregate",aggregate),
              ("util",util),
             ]
    #_fields_=[("index",POINTER(index)),
    #          ("dynamic",POINTER(dynamic)),
    #          ("base",POINTER(base)),
    #          ("aggregate",POINTER(aggregate)),
    #         ]
#Parameters returned from the ::NMPRK_GetCupsData function
class nm_get_cups_data_output_t(Structure):
    _fields_=[("data",data),
             ]
    #_fields_=[("data",POINTER(data)),
    #         ]

#Parameters for a CUPS Configuration
class nm_cups_configuration_t(Structure):
    _fields_=[("cupsEnabled",c_int),
              ("loadFactorTypeToggle",c_int),
              ("staticCoreLoadFactor",c_ushort),
              ("staticMemoryLoadFactor",c_ushort),
              ("staticIoLoadFactor",c_ushort),
              ("sampleCount",c_ubyte),
             ]

#Parameters to pass to the ::NMPRK_SetCupsConfiguration function
class nm_set_cups_configuration_input_t(Structure):
    _fields_=[("setCoreLoadFactor",c_int),
              ("setMemoryLoadFactor",c_int),
              ("setIoLoadFactor",c_int),
              #change
              #("config",POINTER(nm_cups_configuration_t)),
              ("config",nm_cups_configuration_t),
             ]

#Parameters returned from the ::NMPRK_GetCupsConfiguration function
class nm_get_cups_configuration_output_t(Structure):
    #_fields_=[("config",POINTER(nm_cups_configuration_t)),
    #         ]
    _fields_=[("config",nm_cups_configuration_t),
             ]

#Parameters for a CUPS Policy
class nm_cups_policy_t(Structure):
    _fields_=[("policyEnabled",c_int),
              ("policyStorageVolatileMemory",c_int),
              ("sendAlertEnabled",c_int),
              ("cupsThreshold",c_ubyte),
              ("averagingWindow",c_ushort),
             ]

#Parameters to pass to the ::NMPRK_SetCupsPolicies function
class nm_set_cups_policies_input_t(Structure):
    _fields_=[("policyId",c_int),
              ("target",c_int),
              ("policy",POINTER(nm_cups_policy_t)),
             ]

#Parameters to pass to the ::NMPRK_GetCupsPolicies function
class nm_get_cups_policies_input_t(Structure):
    _fields_=[("policyId",c_int),
              ("target",c_int),
             ]
# Parameters to pass to the ::NMPRK_GetCupsPolicies function
class nm_get_cups_policies_output_t(Structure):
    _fields_=[("policy",POINTER(nm_cups_policy_t)),
             ]

# Information details contained in the Node Manager Discovery record in the SDR
class nm_discovery_parameters_t(Structure):
    _fields_=[("channel",c_ubyte),
              ("address",c_ubyte),
              ("nmHealthEvSensor",c_ubyte),
              ("nmExceptionEvSensor",c_ubyte),
              ("nmOperationalCapSensor",c_ubyte),
              ("nmAlertThresExcdSensor",c_ubyte),
             ]

#Information returned from the ::NMPRK_IPMI_GetDeviceId
class nm_ipmi_device_id_t(Structure):
    _fields_=[("deviceId",c_ubyte),
              ("deviceRev",c_uint),
              ("deviceProvidesSdr",c_int),
              ("firmwareRev",c_uint),
              ("devNormOp",c_int),
              ("firmwareRev2",c_uint),
              ("ipmiVersion",c_ubyte),
              ("isSensorDev",c_int),
              ("isSdrRepoDev",c_int),
              ("isSelDev",c_int),
              ("isFruInvDev",c_int),
              ("isIpmbRevDev",c_int),
              ("isIpmbGenDev",c_int),
              ("isBridgeDev",c_int),
              ("isChassisDev",c_int),
              ("manufId",c_ubyte*3),
              ("productId",c_ubyte*3),
             ]

#Information in an SDR Record
class nm_ipmi_sdr_record_t(Structure):
    _fields_=[("recordId",c_ushort),
              ("version",c_ubyte),
              ("type",c_ubyte),
              ("len",c_ubyte),
              ("data",c_ubyte*1024),
             ]

#Information in an SEL Entry
class nm_ipmi_sel_entry_t(Structure):
    _fields_=[("data",c_ubyte*1024),
              ("len",c_uint),
             ]

# tm define
class tm(Structure):
    _fields_=[("tm_sec",c_int),
              ("tm_min",c_int),
              ("tm_hour",c_int),
              ("tm_mday",c_int),
              ("tm_mon",c_int),
              ("tm_year",c_int),
              ("tm_wday",c_int),
              ("tm_yday",c_int),
              ("tm_isdst",c_int),
	      ("tm_gmtoff",c_long),#add
	      ("tm_zone",c_char_p),#add
             ]

#Information about the SDR or SEL repository
class nm_ipmi_repo_info_t(Structure):
    _fields_=[("repoVersion",c_ubyte),
              ("repoEntries",c_uint),
              ("repoFreeSpace",c_uint),
              ("mostRecentAddTS",tm),
              ("mostRecentDelTS",tm),
              #("mostRecentAddTS",POINTER(tm)),
              #("mostRecentDelTS",POINTER(tm)),
              ("getAllocInfoSup",c_int),
              ("reserveSup",c_int),
              ("parAddSup",c_int),
              ("delSup",c_int),
              ("nonmodalSupported",c_int),
              ("modalSupported",c_int),
             ]

#Information about the FRU repository
class nm_ipmi_fru_info_t(Structure):
    _fields_=[("fruSize",c_ushort),
              ("accessByWord",c_int),
             ]
# Information about the ACPI Power State
class ipmi_acpi_power_state_t(Structure):
    _fields_=[("setSystemState",c_int),
              ("setDeviceState",c_int),
              ("systemState",c_int),
              ("deviceState",c_int),
             ]

#class nm_get_policy_output_t(Structure):
#    _fields_ =[(""),
#              ]


class nm_discovery_parameters_t(Structure):
    _fields_=[("channel",c_ubyte),
              ("address",c_ubyte),
              ("nmHealthEvSensor",c_ubyte),
              ("nmExceptionEvSensor",c_ubyte),
              ("nmOperationalCapSensor",c_ubyte),
              ("nmAlertThresExcdSensor",c_ubyte),
             ]
class nm_get_statistics_input_t(Structure):
    _fields_=[("mode",c_int),
              ("domain",c_int),
              ("policy",c_ubyte),
             ]
class ipmi_req_t(Structure):
    _fields_=[("netFun",c_ubyte),
	      ("cmd",c_ubyte),
	      ("data",c_ubyte*490),
              ("len",c_uint),
              ("rsAddr",c_ubyte),
	      ("rsLun",c_ubyte),
             ]
class ipmi_rsp_t(Structure):
    _fields_=[("compCode",c_ubyte),
              ("data",c_ubyte*490),
              ("len",c_uint),
             ]
class ipmi_capture_req_t(Structure):
    _fields_=[("count",c_int),
	      ("data",c_ubyte*490),
	     ]
class ipmi_capture_rsp_t(Structure):
    _fields_=[("count",c_int),
	      ("data",c_ubyte*490),
	     ]
