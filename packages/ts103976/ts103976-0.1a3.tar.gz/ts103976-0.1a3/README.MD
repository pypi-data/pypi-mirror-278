# TS 103 976 Demonstration Implementation

This repo contains a python package for creating and parsing messages as per ETSI TS 103 976.

It is intended for test and demonstration purposes only. It should not be used for production purposes. Any use it entirely at the users risk.

## Getting Started

Install the package using pip

```
#> pip install ts103976
```

## Usage

### LEA side

TODO - BETTER DOCS

Create simple VINToCommsID messages using the following:

```
#> lea -h

usage: lea [-h] [-s SENDERCC] [-u SENDERID] [-r RECEIVERCC] [-i RECEIVERID] [-t TASKREF] [-v VIN] [-d DELIVERYURL]

Generates JSON messages for simple example requests following TS 103 976, encapsulated in TS 103 120. This is an example implementation for
testing and demonstration purposes, and should not be used in production environments.

options:
  -h, --help            show this help message and exit
  -s SENDERCC, --sendercc SENDERCC
                        Sender Country Code used in the TS 103 120 header
  -u SENDERID, --senderid SENDERID
                        Sender Unique ID used in the TS 103 120 header
  -r RECEIVERCC, --receivercc RECEIVERCC
                        Receiver Country Code used in the TS 103 120 header
  -i RECEIVERID, --receiverid RECEIVERID
                        Receiver Unique ID used in the TS 103 120 header
  -t TASKREF, --taskref TASKREF
                        Task Reference (LDID) used in the TS 103 120 LDTaskRequest
  -v VIN, --vin VIN     VIN to query as a RequestValue in the TS 103 120 LDTaskRequest
  -d DELIVERYURL, --deliveryurl DELIVERYURL
                        Delivery URL included in the TS 103 120 LDTaskRequest, as a destination for results
```

### RPS side

TODO - BETTER DOCS

Parse messages and create result sets using the following:

```
#> rps -h

usage: rps [-h] [-r RECEIVERCC] [-i RECEIVERID] [-a ALLOWANYID] [-j INPUT]

Responds to JSON messages for simple example requests following TS 103 976, encapsulated in TS 103 120, and produces simple example responses.
TS 103 120 response messages will be written to stdout. The DELIVER message containing any results will either be set to the delivery address
specified in the LDTaskRequest or written to disk This is an example implementation for testing and demonstration purposes, and should not be
used in production environments.

options:
  -h, --help            show this help message and exit
  -r RECEIVERCC, --receivercc RECEIVERCC
                        Receiver Country Code for the TS 103 120 receiver. Messages with other Receiver Country Code values will be rejected
                        unless the '--allowanyid' flag is set.
  -i RECEIVERID, --receiverid RECEIVERID
                        Receiver Unique ID for the TS 103 120 receiver. Messages with other Receiver Unique ID values will be rejected unless
                        the '--allowanyid' flag is set.
  -a ALLOWANYID, --allowanyid ALLOWANYID
                        Respond to messages to any Receiver ID, regardless of the values set by '--receivercc' or '--receiverid'.
  -j INPUT, --input INPUT
                        Path to input file (if absent, stdin is used)

```