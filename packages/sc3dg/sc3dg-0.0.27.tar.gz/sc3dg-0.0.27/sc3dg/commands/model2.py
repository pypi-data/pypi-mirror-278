from sc3dg.model.generate_cif import generate_cif
from time import time
import click



@click.command('model2')
@click.option('--pair', required=True, type=click.Path(exists=True), help='Path to the pair file.')
@click.option('--name', required=True, type=click.Path(), help='Path to the output pdb file.')
@click.option('--output', default=5, type=int, help='Number of models to generate.')
@click.option('--res', default=10, type=int, help='Number of iteration steps.')
@click.option('--max_iter', default=400, help='Comma-separated list of iteration resolutions.')
def model2(pair, name, output, res):
    """Model command to run the specified model with the config file."""

    generate_cif(pair, name, output, res, max_iter=400)