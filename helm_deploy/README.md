## How to deploy this project to Cloud Platform
To deploy this to the MOJ Cloud Platform you will need to follow the [Cloud Platform documentation](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/deploying-an-app/deploying-an-example-application.html).

To see an example of a Cloud Platform environment namespace configured for this project take a look at the `laa-civil-legal-aid` namespaces [here](https://github.com/ministryofjustice/cloud-platform-environments/tree/main/namespaces/live.cloud-platform.service.justice.gov.uk/laa-civil-case-api-production).

___

This example Helm Chart is set up to deploy to four environments:
- Dev (Where a new app will be deployed for each feature branch)
- UAT
- Staging
- Production

By default only the dev environment has an enabled ingress.

**You will want to rename every occurrence of `moj-fastapi-skeleton` with the name of your project.**

If you are using the included GitHub Actions workflow this is configured to set the ingress whitelist to the IP Ranges
given in the [Shared LAA IP Allowlist](https://github.com/ministryofjustice/laa-ip-allowlist).

If you run into any issues with the Helm Chart or the GitHub actions pipeline please reach out to us in [#laa-cla-dev](https://moj.enterprise.slack.com/archives/CFUESB43G).