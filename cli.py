import json
import logging
import sys

from optparse import OptionParser

from archiver.archiver import IngestArchiver

if __name__ == '__main__':
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=format, stream=sys.stdout, level=logging.INFO)

    parser = OptionParser()
    parser.add_option("-b", "--bundle_uuid", help="Bundle UUID")
    parser.add_option("-i", "--ingest_url", help="Ingest API url")

    (options, args) = parser.parse_args()

    if not options.bundle_uuid:
        print("You must supply a Bundle UUID")
        exit(2)

    if not options.ingest_url:
        print("You must supply the Ingest API url.")
        exit(2)

    archiver = IngestArchiver(ingest_url=options.ingest_url)
    assay_bundle = archiver.get_assay_bundle(options.bundle_uuid)
    entities_dict = archiver.get_archivable_entities(assay_bundle)
    archive_submission = archiver.archive(entities_dict)

    logging.info(json.dumps(archive_submission.processing_result))
    logging.info(str(archive_submission))
    logging.info('==============================================')
    archive_submission.generate_report()

