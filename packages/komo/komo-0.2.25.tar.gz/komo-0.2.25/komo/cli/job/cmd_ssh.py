import click

from komo import printing
from komo.cli.utils import handle_errors
from komo.core import get_job, ssh_job
from komo.types import JobStatus


@click.command("ssh")
@click.argument(
    "job_id",
    type=str,
)
@handle_errors
def cmd_ssh(job_id: str):
    job = get_job(job_id)
    if job.status != JobStatus.RUNNING:
        printing.error(f"Job {job_id} is not running")
        exit(1)

    ssh_job(job_id)
