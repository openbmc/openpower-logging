# Platform Event Logs (PELs)
On the BMC, PELs are created from the standard event logs provided by
phosphor-logging using a message registry that provides the PEL related fields.
A PEL plugin inside of phosphor-log-manager will use the message registry to
create and store a PEL for every OpenBMC event log.

## Contents
* [Message Registry](#message-registry-fields)

## Message Registry Fields
The message registry schema is [here](registry/schema/schema.json), and the
message registry itself is [here](registry/message_registry.json).  The schema
will be validated during a bitbake build.

In the message registry, there are fields for specifying:

### Name
This is the key into the message registry, and is the Message property
of the OpenBMC event log that the PEL is being created from.

```
"Name": "xyz.openbmc_project.Power.Fault"
```

### Notes
This is just an optional free format text field for keeping any notes for
the registry entry, as comments are not allowed in JSON.

```
"Notes": "This entry is for every type of power fault."
```

### Subsystem
This field is part of the PEL User Header section, and is used to specify
the subsystem pertaining to the error.  It is an enumeration that maps to the
actual PEL value.

```
"Subsystem": "power_supply"
```

### Severity
This field is part of the PEL User Header section, and is used to specify
the PEL severity.  It is an optional field, if it isn't specified, then the
severity of the OpenBMC event log will be converted into a PEL severity value.

In addition, the OpenBMC event log severity will override the message registry
severity if they differ (using a mapping of many PEL severity values to a
single OpenBMC severity values).

```
"Severity": "unrecoverable"
```

### Mfg Severity
This is an optional field and is used to override the Severity field when a
specific manufacturing isolation mode is enabled.

```
"MfgSeverity": "unrecoverable"
```

### Event Scope
This field is part of the PEL User Header section, and is used to specify
the event scope, as defined by the PEL spec.  It is optional and defaults to
"entire platform".

```
"EventScope": "entire_platform"
```

### Event Type
This field is part of the PEL User Header section, and is used to specify
the event type, as defined by the PEL spec.  It is optional and defaults to
"not applicable".

```
"EventType": "na"
```

### Action Flags
This field is part of the PEL User Header section, and is used to specify the
PEL action flags, as defined by the PEL spec.  It is an array of enumerations.

```
"ActionFlags": ["service_action", "report", "call_home"]
```

### Mfg Action Flags
This is an optional field and is used to override the Action Flags field when a
specific manufacturing isolation mode is enabled.

```
"MfgActionFlags": ["service_action", "report", "call_home"]
```

### SRC Type
This specifies the type of SRC to create.  The type is the first 2 characters
of the 8 character ASCII string field of the PEL.  The SRC types to use are
still in discussion.  It is optional and if not specified will default to the
standard OpenBMC error type.

Note: The ASCII string normally looks like: "AABBCCCC", where:
* AA = SRC type
* BB = PEL subsystem as mentioned above
* CCCC SRC reason code

```
"Type": "11"
```

### SRC Reason Code
This is the 4 character value in the latter half of the SRC ASCII string.  It
is treated as a 2 byte hex value, such as 0x5678.  The first byte is also
typically the same as the component ID field as in the Private Header that
represents the creator's component ID.

```
"ReasonCode": "0x5544"
```

### SRC Symptom ID Fields
The symptom ID is in the Extended User Header section and is defined in the PEL
spec as the unique event signature string.  It always starts with the ASCII
string.  This field in the message registry allows one to choose which SRC words
to use in addition to the ASCII string field to form the symptom ID. All words
are separated by underscores.

For example: ["SRCWord3", "SRCWord9"] would be:
`<ASCII_STRING>_<SRCWord3>_<SRCWord9>`, which could look like:
`B181320_00000050_49000000`.  If not specified, the code will choose a default
format, which may depend on the SRC type.

```
"SymptomIDFields": ["SRCWord3", "SRCWord9"]
```

### SRC words 6 to 9
In a PEL, these SRC words are free format and can be filled in by the user as
desired.  On the BMC, the source of these words is the AdditionalData fields in
the event log.  The message registry provides a way for the log creator to
specify which AdditionalData field to get the data from, and also to define
what the SRC word means.  If not specified, these SRC words will be set to zero
in the PEL.

```
"Words6to9":
{
    "6":
    {
        "description": "Failing unit number",
        "AdditionalDataPropSource": "PS_NUM"
    }
}
```

### SRC Power Fault flag
The SRC has a bit in it to indicate if the error is a power fault.  This is an
optional field in the message registry and defaults to false.

```
"PowerFault: false
```

### SRC Callouts
The message registry provides a way for the creator to specify any number of
`Procedure` and `Symbolic FRU` callouts, along with their priorities.  This
field is optional.

```
"Callouts":
[
    {
        "Procedure": "bmc_code",
        "Priority": "high"
    },
    {
        "SymbolicFRU": "cable"
        "Priority": "medium"
    }
]
```

### Redfish Message Registry Fields
The message registry is intended to also be the source for the Redfish message
registry entries that involve PELs.  How this will be done is still TBD, but to
facilitate it the following fields that will be required by the Redfish message
registry are defined here:

#### RedfishDesc
A short description of the error.  This field is not part of a Redfish message
response.

```
"RedfishDesc": "A power fault"
```

#### RedfishMessage
This field represents the Message field in the Redfish message registry.  As
such, it supports the same message argument substitution using %1, %2, etc as
Redfish does, with the source of these arguments coming from the AdditionalData
property as specified in the RedfishMessageArgs field.

```
"RedfishMessage": "Processor %1 had %2 errors"
```

#### RedfishMessageArgs
This optional field is required when the RedfishMessage field above contains
the %X positional arguments.  This field contains the type of the argument,
either a string or a number, a description of the argument, and which
AdditionalData field to get this argument from.

```
"RedfishMessageArgs":
[
    {
        "ArgType": "number", "ArgDesc": "Processor Number",
        "ArgSource": {"AdditionalDataProp": "PROC_NUM"}
    },
    {
        "ArgType": "number", "ArgDesc": "Number of errors",
        "ArgSource": {"AdditionalDataProp": "NUM_ERRORS" }
    }
]
```

