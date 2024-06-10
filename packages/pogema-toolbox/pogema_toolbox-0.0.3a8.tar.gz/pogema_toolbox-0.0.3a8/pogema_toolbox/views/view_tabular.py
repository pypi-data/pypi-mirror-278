from numpy import random
from tabulate import tabulate

from pogema_toolbox.registry import ToolboxRegistry
from pogema_toolbox.views.view_utils import View, eval_logs_to_pandas, drop_na
from typing import Literal


class TabularView(View):
    print_results: bool = False
    type: Literal['tabular'] = 'tabular'
    table_format: str = 'psql'
    show_std: bool = True
    skip_zero_std: bool = True


def preprocess_table(eval_configs, view):
    df = eval_logs_to_pandas(eval_configs)

    drop_na(df)

    # Ensure eval_configs[0]['metrics'] and view.drop_keys are lists or convert them
    metrics_keys = [key for key in eval_configs[0].get('metrics', []) if key in df.columns]
    drop_keys = list(view.drop_keys) if hasattr(view, 'drop_keys') else []
    group_by = [col for col in df.columns if col not in metrics_keys + drop_keys]

    # Define aggregation operations
    agg_ops = {key: ['mean', 'std'] for key in metrics_keys} if view.show_std else {key: 'mean' for key in metrics_keys}

    # Perform aggregation
    df_agg = df.groupby(by=group_by, as_index=False).agg(agg_ops).round(view.round_digits)

    if view.show_std:
        df_agg.columns = ['_'.join(col).rstrip('_') for col in df_agg.columns]

        for key in metrics_keys:
            mean_col = f"{key}_mean"
            std_col = f"{key}_std"
            valid_std = (df_agg[std_col].notna()) & ((df_agg[std_col] != 0) | view.skip_zero_std)

            # Create a combined mean and std string for valid std values
            combined_str = df_agg[mean_col].astype(str) + " ± " + df_agg[std_col].astype(str)
            df_agg[key] = df_agg[mean_col].astype(str)  # Initialize the key column with mean values as strings

            # Update the key column with combined_str where valid_std is True
            df_agg.loc[valid_std, key] = combined_str

            # Drop the now redundant mean and std columns
            df_agg.drop(columns=[mean_col, std_col], inplace=True)

    # Drop specified keys, handle sorting, and renaming if required
    df_agg.drop(columns=drop_keys, errors='ignore', inplace=True)
    if hasattr(view, 'sort_by') and view.sort_by:
        df_agg.sort_values(by=view.sort_by, inplace=True)
    if hasattr(view, 'rename_fields') and view.rename_fields:
        df_agg.rename(columns=view.rename_fields, inplace=True)

    return df_agg


def process_table_view(results, view: TabularView):
    df = preprocess_table(results, view)

    table = tabulate(df, headers='keys', tablefmt=view.table_format)
    if view.print_results:
        ToolboxRegistry.info('\n' + table)


def generate_mock_data(num_results=25, ):
    results = []
    for i in range(num_results):
        result = {
            "metrics": {
                "avg_throughput": random.uniform(0.01, 0.25),  # Random float between 0.01 and 0.25
                "avg_num_agents_in_obs": random.uniform(1.4, 1.7),  # Random float between 1.4 and 1.7
                "runtime": random.uniform(29, 55)  # Random float between 29 and 55
            },
            "env_grid_search": {
                "map_name": f"mazes-seed-{i}-10x10",
                "num_agents": random.randint(10, 16),
                "seed": random.randint(0, 3)  # Random int between 0 and 1
            },
            "algorithm": "MATS-LP"
        }
        results.append(result)
    return results


def main():
    results = generate_mock_data()
    process_table_view(results, TabularView(round_digits=2, print_results=True, drop_keys=['seed', 'map_name']))
    process_table_view(results, TabularView(round_digits=2, print_results=True, drop_keys=[]))


if __name__ == '__main__':
    main()
