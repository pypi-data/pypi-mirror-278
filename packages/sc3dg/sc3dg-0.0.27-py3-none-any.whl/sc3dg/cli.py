import click
from sc3dg.commands.count import count
from sc3dg.commands.model1 import model1
from sc3dg.commands.model2 import model2
from sc3dg.commands.impute import impute


@click.group()
def cli():
    pass


cli.add_command(count)
cli.add_command(model1)
cli.add_command(model2)
cli.add_command(impute)



if __name__ == '__main__':
    cli()
