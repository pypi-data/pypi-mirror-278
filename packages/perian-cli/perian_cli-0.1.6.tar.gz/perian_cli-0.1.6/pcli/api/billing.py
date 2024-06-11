from pcli.util.organization import validate_organization, generate_organization_header
from pcli import db

from pcli.responses import (
    DefaultApiException,
    BillingTimeOrderException
)

from perian import (
    BillingApi,
    Configuration,
    ApiException,
    ApiClient
)

from pcli.settings import cli_settings


def generate_bill(start_time, end_time):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = BillingApi(api_client)

        try:
            api_response = api_instance.generate_bill(
                organization=organization_data['name'],
                start_time=start_time,
                end_time=end_time,
                currency=cli_settings.base_currency.value,
                _headers=generate_organization_header(organization_data),
            )

            return api_response

        except ApiException as e:
            if "Start date must be before end date" in str(e):
                raise BillingTimeOrderException(BillingTimeOrderException.detail + "\n\n" + "Default of start time is the beginning of the last month and the default of end time is the end of the last month.")
            raise e
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))