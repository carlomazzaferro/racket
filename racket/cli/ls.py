import click

from racket.operations.schema import active_model_, model_filterer_, query_all_, query_by_id_
from racket.operations.utils import merge_and_unfold, unfold
from racket.utils import dict_tabulate


@click.command()
@click.option('--name', '-n', help='List available models with a specific name', default=None)
@click.option('--version', '-v', help='Retrieve modles of only a specific version, e.g. '
                                      'M1, m2, or p1 (M: Major, m: minor, p: patch', default=None)
@click.option('--type', '-t', 'm_type', help='Filter on model type', is_flag=False)
@click.option('--active', '-a', help='Returns currently active model', is_flag=True)
@click.option('--id', 'model_id', help='Filters on model id', default=None)
def ls(name, version, m_type, active, model_id):
    """List available models, filtering and sorting as desired

    Examples
    --------

    Running::

        $ racket ls -a  # returns the active model's metadata

    Will return::

          model_id  model_name      major    minor    patch    version_dir  active    created_at                  model_type    scoring_fn            score
        ----------  ------------  -------  -------  -------  -------------  --------  --------------------------  ------------  ------------------  -------
                 1  base                0        1        0              1  True      2018-11-14 22:53:52.455635  regression    loss                9378.25
                 1  base                0        1        0              1  True      2018-11-14 22:53:52.455635  regression    mean_squared_error  9378.25


    """
    if active:
        dict_tabulate(merge_and_unfold(active_model_(scores=True), filter_keys=['id']))
        return

    if model_id:
        dict_tabulate(merge_and_unfold(query_by_id_(model_id, scores=True), filter_keys=['id']))
        return

    if any([name, m_type, version]):
        result_set = model_filterer_(name, version, m_type)
        dict_tabulate(merge_and_unfold(result_set, filter_keys=['id']))
        return

    return dict_tabulate(merge_and_unfold(query_all_()))
