# Creator Defined Data in PEL Parsing

### High Level Requirements

- Redfish event logs contain an error description, which will be output on the
  web UI.
    - [Example]
    - These are customer readable.
        - Do these need to be translated?
    - Do these need to go through the Redfish message registry?
    - For BMC errors, these can come from the PEL message registry.
        - These have ability to use SRC words to fill in the message, like:
```
            Processor <SRC word 6> had <SRC word 7> errors
```
    - Design Commentary
        - Look up in data files based on creator ID from Private Header?

- Print the same customer event log description as above in peltool output.

- Print developer description of SRC with other arbitrary fields, including SRC
  user data word descriptions, in peltool output.
    - Optional.
    - These are not customer readable, though will be available to service
      personnel on the BMC in the field.
    - Choosing the description can require additional SRC words besides just
      the refcode.
    - For BMC generated SRCs, the user data definitions will be present in the
      PEL message registry.

- Print parsed UserData sections in peltool output.
    - Based on UD section header version, subtype, and compID fields.
    - Parsing must be done with python scripts called by peltool.
    - Default if no parser provided will be a hex dump like errl did.

[Example]: https://ibm.invisionapp.com/share/8ENYRVXAPFD#/screens/319141765_01-Event-Logs
