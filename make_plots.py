import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os

def load_data(filename):
    data = pd.read_csv(filename)
    data['Volume'] = data['Weight'] * data['Reps']
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    return data

def make_plot_dir(plot_dir):
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

def get_top_exercises(data, n=20):
    exercise_counts = data['Exercise Name'].value_counts()
    if len(exercise_counts) < n:
        n = len(exercise_counts)
    top_ex = exercise_counts[:n]
    print(f"Your top {n} exercises are:")
    for i in range(n):
        num_sets = top_ex[i]
        name = top_ex.index[i]
        print(f"{i + 1}. {name} ({num_sets})")
    return list(top_ex.index)

def plot_exercises(data, names, plot_dir):
    for name in names:
        plot_exercise(data, name, plot_dir)

def plot_exercise(data, name, plot_dir):
    fig, axes = plt.subplots(2, 1, figsize=(6, 6))
    grouped = data[data['Exercise Name'] == name].groupby('Date')
    volumes = grouped['Volume'].sum()
    axes[0].scatter(pd.to_datetime(volumes.index), volumes)
    axes[0].set_ylabel('Volume per session / kg')

    max_weights = grouped['Weight'].max()
    axes[1].scatter(pd.to_datetime(max_weights.index), max_weights)
    axes[1].set_ylabel('Max weight per session / kg')
    axes[1].set_xlabel('Date')

    fig.suptitle(name)

    for ax in axes:
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()
    name_formatted = name.replace(' ', '_').replace(')', '').replace('(', '')
    plt.savefig(f'{plot_dir}/{name_formatted}.png', dpi=150)
    plt.close()

def reps_hist(data, plot_dir, use_log=False):
    fig, ax = plt.subplots(figsize=[4, 3])
    min_x, max_x = 5, 16
    ax.hist(data['Reps'], bins=np.arange(min_x - 0.5, max_x + 0.5));
    plt.xticks(np.arange(min_x, max_x));
    plt.xlabel('Reps')
    ylabel = 'log(Sets)' if use_log else 'Sets'
    plt.ylabel(ylabel)
    if use_log:
        plt.yscale('log')
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/num_reps{"_log" if use_log else ""}.png', dpi=150)
    plt.close()

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <filename>")
        exit(-1)

    data = load_data(sys.argv[1])

    plot_dir = "plots/"
    make_plot_dir(plot_dir)

    top_ex = get_top_exercises(data)
    plot_exercises(data, top_ex, plot_dir)

    reps_hist(data, plot_dir)
    reps_hist(data, plot_dir, True)

    print(f"Saved plots to {plot_dir}")

if __name__ == "__main__":
    main()

