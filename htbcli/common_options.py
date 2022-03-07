import click


pager_option = click.option(
    "--force-pager/--no-pager",
    "pager",
    is_flag=True,
    default=None,
    help="Force or disable the pager on output. If not specified, application will pick.",
)
