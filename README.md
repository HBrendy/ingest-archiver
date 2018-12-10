[![Ingest Archiver Build Status](https://travis-ci.org/HumanCellAtlas/ingest-archiver.svg?branch=master)](https://travis-ci.org/HumanCellAtlas/ingest-archiver)
[![Maintainability](https://api.codeclimate.com/v1/badges/8ce423001595db4e6de7/maintainability)](https://codeclimate.com/github/HumanCellAtlas/ingest-archiver/maintainability)
[![codecov](https://codecov.io/gh/HumanCellAtlas/ingest-archiver/branch/master/graph/badge.svg)](https://codecov.io/gh/HumanCellAtlas/ingest-archiver)

# Ingest Archiver
The archiver service is an ingest component that:
- submits metadata to the appropriate external accessioning authorities. These are currently only EBI authorities (e.g. Biosamples).
- converts metadata into the format accepted by each external authority

In the future it will:
- update HCA metadata with accessions provided by external authorities

At the moment it consists of a minimum of 2 steps.
1. A metadata archiver (MA) script (the one in this repository) which archives the metadata of a submission through the USI. This script also checks the submission of the files by the file uploader (see below).
1. A file uploader (FIU) of the archive data to the USI which runs on the EBI cluster. This will need access to the file submission JSON instructions generated by the metadata archiver.

The archiver uses the [USI Submissions API](https://submission-dev.ebi.ac.uk/api/docs/how_to_submit_data_programatically.html#_overview) to communicate with EBI external authorities.

This component is currently invoked manually after an HCA submission.

# How to run
# Run the archiver script
1. Install the script requirements
`pip3 install -r requirements.txt`

2. Get the project UUID of the project you want to archive. For example rsatija dataset `5f256182-5dfc-4070-8404-f6fa71d37c73`

3. Set environment variables
```
# If you don’t know the EBI AAP password we’re using for archiving please ask an ingest dev or another EBI wrangler
$ export AAP_API_PASSWORD=’password’
$ export INGEST_API_URL=http://api.ingest.data.humancellatlas.org/
$ export USI_API_URL=https://submission-dev.ebi.ac.uk # should point to prod

# Optional environment variables, if you want the process to run until validation and submission completed , you may have to run the metadata archiver multiple times if the following are not set

$ export VALIDATION_POLL_FOREVER=TRUE
$ export SUBMISSION_POLL_FOREVER=TRUE
```

4. Run the metadata archiver
`python3 cli.py --project_uuid="2a0faf83-e342-4b1c-bb9b-cf1d1147f3bb"`

5. Take the JSON file from AM and move to a well known location on /ebi/teams/hca
6. Login to EBI CLI
7. Run <cmd> which will 
* Download the data from HCA to /ebi/teams/hca/<project-uuid>
* Convert the data to a different format where necessary
* Upload the data from /ebi/teams/hca/<project-uuid> to USI
8. Run the metadata archiver with this switch

`python cli.py --submission_url="https://submission-dev.ebi.ac.uk/api/submissions/f0db1f2f-718a-46fe-a162-c2256850e5a1"`

Keep running or rerun until it says SUCCESSFULLY SUBMITTED

# How to run the tests

```
python -m unittest discover -s tests -t tests

```

# Deployment
See https://github.com/HumanCellAtlas/ingest-kube-deployment.

An AAP username and password is also needed to use the USI API and must be set in the config.py or as environment variable.

# Versioning

For the versions available, see the [tags on this repository](https://github.com/HumanCellAtlas/ingest-archiver/tags).

# License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details
