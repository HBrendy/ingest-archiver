# Archiver Operations

## Setting Up

Before operating the archiver, it is necessary to obtain proper security credentials from the AAP. The archiver works
in 2 different deployment environments, namely testing and production, and it requires different set of credentials 
for each one. By default, the archiver utility stores relevant configuration files in the `_local` directory of the 
present working directory.

### Security Credentials

#### Setting Up Production

For production, the security credentials used for archiving have been stored in the AWS secrets manager. The archiver
script requires access to this and so the local environment should be setup with the correct AWS profile that has access
to these secrets. At the time of writing, the script is hardcoded to use the AWS profile named `embl-ebi`.

The archiver utility attempts to automatically setup the credentials if they are missing by fetching the data from AWS.
Alternatively, the credentials can be set up by creating an environment file named `aap_credentials` in the 
`_local/env` directory that contains the following variables (file: `_local/env/aap_credentials`):

<a name="credentials-env"></a>
* `AAP_API_URL`
* `AAP_API_DOMAIN`
* `AAP_API_USER`
* `AAP_API_PASSWORD`

This is an option for users who do not require indefinite access to AWS but need to be able to run archiving. It is 
important to note that the credentials used for production should only be shared with trusted parties.

#### Setting Up Testing

DSP that the Ingest Archiver service uses depends on the testing deployment of the AAP for testing. At the time of 
writing, there is no shared credentials for running archival scripts for testing, so users who do not have accounts
in AAP testing need to create for themselves through their 
[registration page](https://explore.aai.ebi.ac.uk/registerUser).

**Registering Domain**. Once the registration succeeds, the user name and password need to be stored in the credentials
environment file `_local/env/aap_credentials_test` using the same names specified [above](#credentials-env) 
(i.e. `AAP_API_USER`, and `AAP_API_PASSWORD`). DSP requires that user also register a domain. If the domain was 
previously set up, it can simply be added into the `app_credentials_test` file. However, the archiver util can be used 
to register the domain given a set of credentials. This is done using the `set-domain` sub-command:

    ./archiver set-domain <preferred_centre_name>
    
If this action succeeds, it will update the credentials file with the reference to the newly registered domain. Note 
that setting the domain is currently not supported for production environment.

## Obtaining Token

The archiver utility provides an easy way to obtain security token from AAP based on the configured credentials. This
can be done using the `get-token` sub-command:

    ./archiver get-token

## Archiving

Archiver supports archival on either submission or project context, through the sub-commands `submission` and `project`.
Each command requires the UUID that identifies the archival context:

    ./archiver submission <submission_uuid>
    
or
    
    ./archiver project <project_uuid>
    
For older data sets particularly ones that were previously exported to DCP/1, archival in the project context is 
preferred. For more recent submissions, submission context is advised.

**Quiet Mode**. By default, either of these commands will print out messages about the archival process, until 
eventually it displays the DSP URL of the submission. Alternatively, they can made to only return the UUID of the
DSP submission when it succeeds; this is done by using the quiet flag, `-q`.

    ./archiver submission -q <submission_uuid>
    
To check the info about the DSP submission, the resulting UUID can be passed on to the `dsp-submission` sub-command:

    ./archiver dsp-submission <dsp_submission_uuid>

### Running in Production

In order to avoid submitting to production, the archiver utility runs in test mode by default. This can changed to 
prod by setting the environment variable `ARCHIVER_ENV` to `prod`. To preserve the default behaviour, however, it is
advised to instead use the execute flag `-x` when running any of the archival commands:

    ./archiver -q project -x <project_uuid>
