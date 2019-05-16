# The OpenPower Message Registry

This document describes the fields in the OpenPower message registry.

At this moment, it is a work in progress, but shows the general idea.

This registry is used to enable creating OpenPower Platform Event Logs and
Redfish event logs from OpenBMC event logs.

This registry will be installed on the BMC, and tentatively the format will be
JSON.  A future decision is whether this will be spread over single or multiple
files, and which repositories these will reside in.

When a new OpenBMC event log is sent to the PEL daemon, it will look up that
log in the message registry to find the fields required to construct a PEL.
Note that some fields in a PEL may need to be looked up on the system itself,
like the Machine Type/Model or firmware version.

When PELs are sent down from the host, the PLDM handler will create an OpenBMC
event log for them and pass in the PEL data somehow, so a new PEL does not need
to be created.  However, a Redfish log is still needed, so the Redfish section
is still required.  There will most likely be very few types of OpenBMC event
log messages to cover all host PELs, so there will only need to be a few
entries that are like this.  If the Redfish log needs to display the SRC, it
can get it straight from the PEL.

## General Fields

### Name
* The openBMC event log 'Message' property,
* For example:  "xyz.openbmc_project.Power.Error.PGOODFault"
* Used to find an entrybased on the OpenBMC event log.

### Notes

* As JSON doesn't allow comments, this is just for anything extra a developer
    would like to add in this entry.  It is not used by any software.

## User Header fields

### Severity
* String name that converts to the 1B Event Severity field in the User Header
    section
* Example: "recovered"
* Could allow this to be optional, in which case it would use the OpenBMC event
    log severity, which is a lot less granular but may work in most cases.

### Subsystem
* String name that converts to the 1B Subsystem ID field in the User Header
    section
* For example: "processor"

### EventType
* String name that converts to 1B Event Type field in the User Header section.
* Optional.  Only required when Event Severity is 0x00 = NonError Event
* Exampe: "tracing"

### EventScope
* String name that converts to the 1B Event Scope field in the User Header
    section
* Optional. Defaults to "platform"

### ProblemDomain
* String name that translates to the 1B Problem Domain field in the User Header
    section
* This is subsystem dependent. Right now only "Cec Hardware" domains are
    defined.
* Optional.  Defaults to 0 = Reserved.

### ProblemVector
* String name that translates to the 1B Problem Vector field in the User Header
    section
* This is also subsystem dependent.
* Optional. Defaults to 0 = Reserved.

### ActionFlags
* Array of string names that translate to the 2B Event Action Flags bitmask in
    the User Header Section
* Example: ["report", "hidden", "call_home"]
* Optional?  Default could be "report"

## SRC Fields

### ReasonCode
* The 2B SRC reason code.  Must be unique.
* For example: 0x2525

### There are probably more


## Redfish/REST Fields

We could probably generate the Redfish message registry files from these.
These could also be used in any on-BMC PEL parsers that would like to display
some text.  Translation would happen in the bmcweb/web UI side of things.

### Description
* A short description of the error.
* For example: Indicates that a threshold sensor has crossed a critical low
    threshold going low.

### Message
* The message that is displayed to the user.  If a %integer is included in part
    of the string, it shall be used to represent a string substitution for any
    MessageArgs accompanying the message, in order.
* Example: "%1 sensor crossed a critical low threshold going low. Reading=%2
    Threshold=%3."
* Must have these values in either
  * AdditionalData "MESSAGE_ARG0=ambient, MESSAGE_ARG1=20, MESSAGE_ARG2=30" or
      "MESSAGE_ARGS=ambient,20,30"
  * or in the OEMJson
  * "MessageArgs": ["ambient", 20, 30]

### MessageArgTypes
* The types for the Message args, in order (needed for Redfish msg registry)
* array of strings
* for example: ["string", "number", "number"]
* Or maybe we could imply them somehow.

### Resolution
* Optional, can use for the 'Resolution' Redfish message property, otherwise
    the daemon can make up a generic one, like "Check the service
    documentation"

## Host PELs

### HostPEL
* Boolean. Indicates a PEL is part of the OpenBMC log so the PEL fields related
    fields are not required.
* Optional. Defaults to false.
* Not sure though if a schema validator could handle this.  If not, may need to
    just put in dummy values for these or think of something else.

## Notes

* We could allow the PEL related fields to be overridden at creation time by
    allowing the user to pass in their own values via the OEM JSON.
* These can be validated using a JSON schema validator at build time, like
    https://github.com/Julian/jsonschema (python)
