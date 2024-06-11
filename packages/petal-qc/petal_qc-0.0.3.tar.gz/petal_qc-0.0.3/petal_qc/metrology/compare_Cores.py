#!/usr/bin/env python3
"""Compare quantities."""

import sys
import argparse
import glob
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def get_value(data, value_path):
    """Get the value."""
    a = data
    for k in value_path.split('/'):
        a = a[k]

    return a


def main(options):
    labels = []
    front = {}
    back = {}
    
    for fnam in options.files:
        ifile = Path(fnam).expanduser().resolve()
        print(ifile.name)
        if not ifile.exists():
            print("File does not exist: ", fnam)
            continue

        data = None
        with open(ifile, 'r', encoding="UTF-8") as fp:
            data = json.load(fp)

        if data is None:
            print("Problems reading ", fnam)
            continue

        tmp = ifile.name.split('-')
        label = tmp[0]
        if not label in labels:
            labels.append(label)
            
        is_front = False
        if "front" in tmp[1].lower():
            is_front = True
            
        val = get_value(data, options.value)
        if is_front:
            front[label] = val
        else:
            back[label] = val

    labels.sort()
    X = np.arange(0, len(labels))
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    fig.suptitle(options.value)
    ax.set_xticks(range(len(labels)), labels=labels)
    ax.grid()
    
    vfront = [front[x] for x in labels]
    vback = [back[x] for x in labels]
    ax.plot(X, vfront, '*', label="Front")
    ax.plot(X, vback, 'o', label="Back")
    ax.legend()
    
    if options.out:
        fig.savefig(options.out, dpi=300)
    
    plt.show()
    

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help="Input files")
    parser.add_argument("--value", default=None, help="Value to plot")
    parser.add_argument("--out", default=None, help="File to store the figure.")

    options = parser.parse_args()
    if len(options.files) == 0:
        print("I need at least one input file")
        sys.exit()

    if len(options.files) == 1:
        xxx = any(elem in options.files[0] for elem in r"*?")
        if xxx:
            options.files = glob.glob(options.files[0])

    if options.value[0] == '/':
        options.value = options.value[1:]
    options.value = "results/METROLOGY/" + options.value
    main(options)
