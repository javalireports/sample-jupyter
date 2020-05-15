import Evtx.Evtx as evtx
import argparse


def main():
    parser = argparse.ArgumentParser(description="Dump a binary EVTX file into XML.")
    parser.add_argument("inputfile", type=str, help="Path to the Windows EVTX event log file")
    parser.add_argument("outputfile", type=str, help="Path to the output XML file")
    args = parser.parse_args()

    newfilename = args.outputfile
    file = open(newfilename, "w")
    print("Writing output to " + newfilename)

    error_count = 0

    output_interval = 10000
    output_count = 0
    file.write("<Events>")
    with evtx.Evtx(args.inputfile) as log:
        for chunk in log.chunks():
            for record in chunk.records():
                try:
                    s = record.xml()
                    file.write(s)
                    # root = ET.fromstring(s)
                    # print root.findall('EventData')
                    # print root.find('{http://schemas.microsoft.com/win/2004/08/events/event}EventID')
                    output_count = output_count + 1

                    if output_count % output_interval == 0:
                        print("[Working] %d records written to file." % output_count)

                except UnicodeDecodeError:
                    error_count = error_count + 1
                    print("UnicodeDecode Error encountered skipping entry Errors[%d]" % error_count)
                    continue
    file.write("</Events>")
    # print norm_count, error_count
    file.close()


if __name__ == "__main__":
    main()
