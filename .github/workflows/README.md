### Using GitHub actions
In order for the build and deploy steps to run as expected you will need your Cloud Platform Service Account to export
your ECR secrets into GitHub actions.

You can find documentation on setting this up [here](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/deploying-an-app/deploying-an-example-application.html).

You can see how to use the included example Helm Chart [here](../../helm_deploy/README.md).

To use Sonar Cloud you will need to have your `SONAR_TOKEN` set in your GitHub actions secrets.

You can find our documentation for this Pipeline [here](https://dsdmoj.atlassian.net/wiki/spaces/laagetaccess/pages/4906221775/Access+Civil+Legal+Aid+CI+CD+Pipeline).

If you run into any issues please feel to reach out to us in [#laa-cla-dev](https://moj.enterprise.slack.com/archives/CFUESB43G).