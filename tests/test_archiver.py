import json
import time
import unittest
from random import randint
from mock import MagicMock

import config
from archiver.archiver import IngestArchiver, AssayBundle
from archiver.converter import Converter
from archiver.ingestapi import IngestAPI
from archiver.usiapi import USIAPI


class TestIngestArchiver(unittest.TestCase):
    def setUp(self):
        self.archiver = IngestArchiver(exclude_types=['project', 'study', 'sequencing_experiment', 'sequencing_run'])
        self.converter = Converter()
        self.ingest_api = IngestAPI()
        self.usi_api = USIAPI()

        with open(config.JSON_DIR + 'hca/biomaterials.json', encoding=config.ENCODING) as data_file:
            biomaterials = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/project.json', encoding=config.ENCODING) as data_file:
            project = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/process.json', encoding=config.ENCODING) as data_file:
            assay = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/biomaterial.json', encoding=config.ENCODING) as data_file:
            input_biomaterial = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/library_preparation_protocol.json', encoding=config.ENCODING) as data_file:
            library_preparation_protocol = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/sequencing_protocol.json', encoding=config.ENCODING) as data_file:
            sequencing_protocol = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/sequencing_protocol.json', encoding=config.ENCODING) as data_file:
            sequencing_protocol = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/library_preparation_protocol.json', encoding=config.ENCODING) as data_file:
            sequencing_protocol = json.loads(data_file.read())

        with open(config.JSON_DIR + 'hca/sequencing_file.json', encoding=config.ENCODING) as data_file:
            sequencing_file = json.loads(data_file.read())

        for biomaterial in biomaterials:
            # TODO decide what to use for alias, assign random no for now
            biomaterial['uuid']['uuid'] = 'hca' + str(randint(0, 1000)) + str(randint(0, 1000))

        self.bundle = {
            'biomaterials': biomaterials,
            'project': project,
            'files': [sequencing_file],
            'assay': assay,
            'library_preparation_protocol': library_preparation_protocol,
            'sequencing_protocol': sequencing_protocol,
            'input_biomaterial': input_biomaterial
        }

        pass

    def test_get_archivable_entities(self):
        assay_bundle = self._mock_assay_bundle(self.bundle)
        entities_by_type = self.archiver.get_archivable_entities(assay_bundle)
        self.assertTrue(entities_by_type['sample'])

    @unittest.skip
    def test_is_submittable(self):
        assay_bundle = self._mock_assay_bundle(self.bundle)
        entities_dict_by_type = self.archiver.get_archivable_entities(assay_bundle)
        converted_entities = self.archiver._get_converted_entities(entities_dict_by_type)

        usi_submission = self.usi_api.create_submission()

        self.archiver.add_entities_to_submission(usi_submission, converted_entities)

        time.sleep(3)
        is_submittable = self.archiver.is_submittable(usi_submission)

        self.archiver.delete_submission(usi_submission)

        self.assertTrue(is_submittable)

    @unittest.skip
    def test_is_validated(self):
        assay_bundle = self._mock_assay_bundle(self.bundle)
        entities_dict_by_type = self.archiver.get_archivable_entities(assay_bundle)
        converted_entities = self.archiver._get_converted_entities(entities_dict_by_type)

        usi_submission = self.usi_api.create_submission()

        self.archiver.add_entities_to_submission(usi_submission, converted_entities)

        time.sleep(3)
        is_validated = self.archiver.is_validated(usi_submission)

        self.archiver.delete_submission(usi_submission)

        self.assertTrue(is_validated)

    @unittest.skip
    def test_is_validated_and_submittable(self):
        assay_bundle = self._mock_assay_bundle(self.bundle)
        entities_dict_by_type = self.archiver.get_archivable_entities(assay_bundle)
        converted_entities =  self.archiver._get_converted_entities(entities_dict_by_type)

        usi_submission = self.usi_api.create_submission()

        self.archiver.add_entities_to_submission(usi_submission, converted_entities)

        time.sleep(3)
        is_validated_and_submittable = self.archiver.is_validated_and_submittable(usi_submission)

        self.archiver.delete_submission(usi_submission)

        self.assertTrue(is_validated_and_submittable)

    # @unittest.skip('submitted submissions cannot be deleted, skipping this')
    def test_archive(self):
        assay_bundle = self._mock_assay_bundle(self.bundle)
        entities_dict_by_type = self.archiver.get_archivable_entities(assay_bundle)
        archive_submission = self.archiver.archive(entities_dict_by_type)
        print(archive_submission.generate_report())
        self.assertTrue(archive_submission.is_completed)
        self.assertTrue(archive_submission.processing_result)

    def _mock_assay_bundle(self, bundle):
        assay_bundle = MagicMock('assay_bundle')
        assay_bundle.get_biomaterials = MagicMock(
            return_value=bundle.get('biomaterials'))
        assay_bundle.get_project = MagicMock(
            return_value=bundle.get('project'))
        assay_bundle.get_assay_process = MagicMock(
            return_value=bundle.get('assay'))
        assay_bundle.get_library_preparation_protocol = MagicMock(
            return_value=bundle.get('library_preparation_protocol'))
        assay_bundle.get_sequencing_protocol = MagicMock(
            return_value=bundle.get('sequencing_protocol'))
        assay_bundle.get_input_biomaterial = MagicMock(
            return_value=bundle.get('input_biomaterial'))
        assay_bundle.get_files = MagicMock(
            return_value=bundle.get('files'))
        return assay_bundle

    def test_archive_skip_metadata_with_accessions(self):
        with open(config.JSON_DIR + 'hca/biomaterial_with_accessions.json', encoding=config.ENCODING) as data_file:
            biomaterials = json.loads(data_file.read())
        bundle = {'biomaterials': biomaterials}
        assay_bundle = self._mock_assay_bundle(bundle)
        entities_dict_by_type = self.archiver.get_archivable_entities(assay_bundle)
        archive_submission = self.archiver.archive(entities_dict_by_type)
        print(archive_submission.generate_report())
        self.assertTrue(archive_submission.is_completed)
        self.assertTrue(archive_submission.errors)
        self.assertFalse(archive_submission.processing_result)
