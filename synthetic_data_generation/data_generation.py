import argparse
import json
import numpy as np
import pandas as pd

def generate_variable_data(name, var_type, n, seed):
    np.random.seed(seed)
    if var_type == 'continuous':
        return np.random.normal(loc=0, scale=1, size=n)
    elif var_type == 'discrete':
        return np.random.choice([0, 1], size=n)
    else:
        raise ValueError(f"Unsupported type for variable {name}: {var_type}")

def apply_dependency(inputs, dep_type, noise_std=0.1):
    data = np.zeros_like(inputs[0])

    if dep_type == 'linear':
        for i, inp in enumerate(inputs):
            data += (i + 1) * inp
    elif dep_type == 'nonlinear':
        for inp in inputs:
            data += np.sin(inp) + np.log(np.abs(inp) + 1)
    elif dep_type == 'multiplicative':
        data = np.ones_like(inputs[0])
        for inp in inputs:
            data *= inp
    elif dep_type == 'conditional':
        cond = inputs[0]
        base = inputs[1]
        data = np.where(cond > 0, base + np.random.normal(0, noise_std, len(cond)),
                        np.random.normal(0, 1, len(cond)))
    else:
        raise ValueError(f"Unsupported dependency type: {dep_type}")

    return data + np.random.normal(0, noise_std, len(data))

def build_synthetic_data(var: dict, dependencies: dict, n_samples=1_000_000, seed=42):
    np.random.seed(seed)
    df = pd.DataFrame()

    for var_name in var:
        if var_name not in dependencies:
            df[var_name] = generate_variable_data(var_name, var[var_name], n_samples, seed + hash(var_name) % 1000)

    for var_name in dependencies:
        inputs = [df[input_var] for input_var in dependencies[var_name]['depends_on']]
        dep_type = dependencies[var_name]['type']
        raw_output = apply_dependency(inputs, dep_type)

        if var[var_name] == 'discrete':
            df[var_name] = (raw_output > np.median(raw_output)).astype(int)
        else:
            df[var_name] = raw_output

    return df

def main():
    parser = argparse.ArgumentParser(description="Synthetic Data Generator")
    parser.add_argument('--config', required=True, help='Path to JSON config file with variable definitions and dependencies')
    parser.add_argument('--n_samples', type=int, default=1_000_000, help='Number of samples to generate')
    parser.add_argument('--out_path', required=True, help='Path to save output Parquet file')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')

    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = json.load(f)

    var = config['variables']
    dependencies = config['dependencies']

    df = build_synthetic_data(var, dependencies, n_samples=args.n_samples, seed=args.seed)
    df.to_parquet(args.out_path, index=False)
    print(f"✅ Done. Output shape: {df.shape}. File saved at: {args.out_path}")

if __name__ == "__main__":
    main()