from datetime import datetime, timezone
from typing import Annotated
import typer

from pcli import PerianTyper
from pcli.api.billing import generate_bill
from pcli.responses import (
    BillingTimeOrderException,
    BothBillingTimesNeededException,
    DefaultApiException,
    ExceptionLevel,
    handle_exception,
)
from pcli.util.formatter import print_billing_information

billing_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Managed and interact with billing information",
)


@billing_command.command("get", help="Get billing information for a given time")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(BillingTimeOrderException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(BothBillingTimesNeededException, exit=True, level=ExceptionLevel.WARNING)
def get_bill(
    start_time: Annotated[datetime, typer.Option(
        help="Start time for the billing information. Defaults to the beginning of the last month")] = None,
    end_time: Annotated[datetime, typer.Option(
        help="End time for the billing information. Defaults to the end of the last month")] = None,
):
    """Get billing information for a given time. If no time is provided, the billing information for the last month is returned."""
    if start_time and not end_time:
        raise BothBillingTimesNeededException()

    # adding timezone information to the datetime objects
    if start_time:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
    if end_time:
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

    billing_information = generate_bill(start_time, end_time)

    print_billing_information(billing_information)
