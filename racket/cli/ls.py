import click

from racket.operations.schema import list_models
from racket.utils import dict_tabulate


@click.command()
@click.option('--name', '-n', help='List available models with a specific name', default=None)
@click.option('--version', '-v', help='Retrieve models of only a specific version, e.g. '
                                      'M1, m2, or p1 (M: Major, m: minor, p: patch', default=None)
@click.option('--type', '-t', 'm_type', help='Filter on model type', is_flag=False)
@click.option('--active', '-a', help='Returns currently active model', is_flag=True)
@click.option('--id', 'model_id', help='Filters on model id', default=None)
@click.option('--unique', '-u', 'unique', help='Returns only unique models, disregarding the fact'
                                               'that there may be more than one entry for each model. '
                                               'This happens when a model is trained used more than one'
                                               'scoring function', is_flag=True)
def ls(name, version, m_type, active, model_id, unique):
    """
    Running::

        $ racket ls -a  # returns the active model's metadata

    Will return::

          model_id  model_name                 major    minor    patch    version_dir  active    created_at                  model_type    scoring_fn      score
        ----------  -----------------------  -------  -------  -------  -------------  --------  --------------------------  ------------  ------------  -------
                 4  keras-simple-regression        1        2        1              3  True      2018-11-16 19:16:48.437517  regression    loss          106.519

    """
    result = list_models(name, version, m_type, active, model_id, unique)
    dict_tabulate(result)
