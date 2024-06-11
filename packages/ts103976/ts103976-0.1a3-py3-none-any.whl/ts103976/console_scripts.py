import argparse
import sys
import json

from .lea import LEA
from .rps import RPS


def lea_console():
    parser = argparse.ArgumentParser(
        description="Generates JSON messages for simple example requests following TS 103 976, \
                                          encapsulated in TS 103 120. This is an example implementation for testing \
                                          and demonstration purposes, and should not be used in production environments.",
    )

    parser.add_argument("-s", "--sendercc", default="XX", help="Sender Country Code used in the TS 103 120 header")
    parser.add_argument("-u", "--senderid", default="SENDER", help="Sender Unique ID used in the TS 103 120 header")
    parser.add_argument("-r", "--receivercc", default="XX", help="Receiver Country Code used in the TS 103 120 header")
    parser.add_argument("-i", "--receiverid", default="RECEIVER", help="Receiver Unique ID used in the TS 103 120 header")
    parser.add_argument("-t", "--taskref", default="XX-1-234", help="Task Reference (LDID) used in the TS 103 120 LDTaskRequest")
    parser.add_argument("-v", "--vin", default="1G9Y817H34LSP7293", help="VIN to query as a RequestValue in the TS 103 120 LDTaskRequest")
    parser.add_argument("-d", "--deliveryurl", default="https://localhost", help="Delivery URL included in the TS 103 120 LDTaskRequest, as a destination for results")

    args = parser.parse_args()

    lea = LEA(args.sendercc, args.senderid, args.deliveryurl)
    json_doc = lea.generate_vin_to_comms_id(
        args.receivercc, args.receiverid, args.taskref, args.vin
    )
    print(json.dumps(json_doc))


def rps_console():
    parser = argparse.ArgumentParser(
        description="Responds to JSON messages for simple example requests following TS 103 976, \
                     encapsulated in TS 103 120, and produces simple example responses. \
                     TS 103 120 response messages will be written to stdout. The DELIVER message \
                     containing any results will either be set to the delivery address specified in the LDTaskRequest \
                     or written to disk\
                     This is an example implementation for testing \
                     and demonstration purposes, and should not be used in production environments.",
)

    parser.add_argument("-r", "--receivercc", default="XX", help="Receiver Country Code for the TS 103 120 receiver. Messages with other Receiver Country Code values will be rejected unless the '--allowanyid' flag is set.")
    parser.add_argument("-i", "--receiverid", default="RECEIVER", help="Receiver Unique ID for the TS 103 120 receiver. Messages with other Receiver Unique ID values will be rejected unless the '--allowanyid' flag is set.")
    parser.add_argument("-a", "--allowanyid", default=False, help="Respond to messages to any Receiver ID, regardless of the values set by '--receivercc' or '--receiverid'.")
    parser.add_argument("-j", "--input", type=argparse.FileType("r"), default=sys.stdin, help="Path to input file (if absent, stdin is used)")

    args = parser.parse_args()
    instance_doc = json.loads(args.input.read())
    args.input.close()

    rps = RPS(args.receivercc, args.receiverid, args.allowanyid)
    response = rps.respond_to(instance_doc)
    print(response)
