from typing import Annotated, Optional
from typing import Annotated
from uuid import UUID

import typer

from pcli import PerianTyper
from pcli.api.instance_type import get_by_id, get_by_requirements
from pcli.responses import (
    InvalidFilterCriteriaException,
    InstanceTypeApiException,
    DefaultApiException,
    handle_exception,
    ExceptionLevel,
    InvalidInstanceTypeIdException,
    InstanceTypeNotFoundException,
    NoOrganizationException,
    CurrencyAPIException
)
from pcli.util import (
    load_instance_type_filter_from_json,
    load_instance_type_filter_from_values,
)
from pcli.util.formatter import (
    print_instance_types_list,
    print_instance_type_description,
)
from perian import (
    InstanceTyperQueryView
)

instance_type_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Find and compare instance types",
)


@instance_type_command.command("get", help="Get available instance types")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InstanceTypeApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(InvalidInstanceTypeIdException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InstanceTypeNotFoundException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(CurrencyAPIException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InvalidFilterCriteriaException, exit=True, level=ExceptionLevel.WARNING)
def get_instance_type(
    instance_type_id: Annotated[Optional[str], typer.Argument(help="ID of instance type")] = None,
    cores: Annotated[Optional[int], typer.Option(help="Number of cpu cores")] = None,
    memory: Annotated[Optional[int], typer.Option(help="Gigabyte of RAM")] = None,
    accelerators: Annotated[Optional[int], typer.Option(help="Number of Accelerators")] = None,
    accelerator_type: Annotated[
        Optional[str],
        typer.Option(
            help="Name of accelerator type. See accelerator-type command for a list of all supported ones"
        ),
    ] = None,
    country_code: Annotated[Optional[str], typer.Option(help="Country code (e.g. DE)")] = None,
    filters: Annotated[
        Optional[str],
        typer.Option(
            help="Filter criteria to select instance types. A JSON string or the path to a JSON file is expected here"
        ),
    ] = None,
    limit: Annotated[
        int, typer.Option(help="Number of instance types to display")
    ] = 25,
):
    if instance_type_id:
        try:
            instance_type_id = UUID(instance_type_id)
        except Exception:
            raise InvalidInstanceTypeIdException()

        instance_type = get_by_id(instance_type_id)
        print_instance_type_description(instance_type)

    elif not instance_type_id:
        instance_type_filters = None

        if filters:
            instance_type_filters = load_instance_type_filter_from_json(filters)
        else:
            instance_type_filters = load_instance_type_filter_from_values(
                cores=cores,
                memory=memory,
                accelerators=accelerators,
                accelerator_type=accelerator_type,
                country_code=country_code,
            )

        # creating instance type query
        instance_type_query = InstanceTyperQueryView(**instance_type_filters)

        # calling API
        instance_types = get_by_requirements(instance_type_query, limit)

        if len(instance_types) == 0:
            raise InstanceTypeNotFoundException("No instance types for given filters found.")

        print_instance_types_list(instance_types)
