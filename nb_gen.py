import argparse
import math
import uuid
from pathlib import Path
import random


def create_cell(num_chars):
    line_length = 74  # uuid1-uuid2\n
    num_lines = math.ceil(num_chars / line_length)
    ret = []
    for i in range(num_lines):
        ret.append(f'{uuid.uuid1()} {uuid.uuid1()}')
    return '\n'.join(ret) + '\n'


def generate_notebook(outpath, num_cells, chars_per_cell):
    ret = [create_cell(chars_per_cell) for _ in range(num_cells)]
    cell_sep = '\n# COMMAND ----------\n'
    nb_header = '# Databricks notebook source\n'
    nb_content = nb_header + cell_sep.join(ret)
    Path(outpath).expanduser().write_text(nb_content)


def replace_all_notebooks(num_cells, chars_per_cell):
    for nb in Path(".").glob("**/notebook*.py"):
        print(f"Generating {nb}")
        generate_notebook(nb, num_cells, chars_per_cell)

def randomly_update_notebooks(update_chance, replace_chance):
    for nb in Path(".").glob("**/notebook*.py"):
        choice = random.random()
        if choice < update_chance:
            print(f"Updating {nb}")
            with nb.open("a") as f:
                f.write(f'{uuid.uuid1()} {uuid.uuid1()}')
        elif update_chance <= choice and choice < update_chance + replace_chance:
            new_nb = nb.with_stem(nb.stem + "_mod")
            print(f"Replacing {nb} with {new_nb}")
            nb.rename(new_nb)
        else:
            print(f"Skipping {nb}")

def randomly_update_files(update_chance, replace_chance):
    for file in Path(".").glob("**/file*.txt"):
        choice = random.random()
        if choice < update_chance:
            print(f"Updating {file}")
            with file.open("a") as f:
                f.write("added content")
        elif update_chance <= choice and choice < update_chance + replace_chance:
            new_file = file.with_stem(file.stem + "_mod")
            print(f"Replacing {file} with {new_file}")
            file.rename(new_file)
        else:
            print(f"Skipping {file}")

def randomly_update_notebooks_and_files(update_chance, replace_chance):
    randomly_update_notebooks(update_chance, replace_chance)
    randomly_update_files(update_chance, replace_chance)


def main():
    parser = argparse.ArgumentParser(description='Create notebook')
    parser.add_argument('--num_cells', type=int, default=25)
    parser.add_argument('--chars_per_cell', type=int, default=500)
    parser.add_argument('--nb_path', help="target notebook", default="")
    parser.add_argument('--replace_all',
                        help="All notebooks will be replaced in the current directory",
                        action='store_true', default=False)
    parser.add_argument('--randomly_update',
                        help="Randomly updates all notebooks and files under the current directory",
                        action='store_true', default=False)
    parser.add_argument('--update_chance',
                        help="Chance of modifying each notebook or file",
                        type=float,
                        default=0.025)
    parser.add_argument('--replace_chance',
                        help="Chance of replacing each notebook or file",
                        type=float,
                        default=0.025)
    args = parser.parse_args()
    if args.nb_path:
        generate_notebook(args.nb_path, args.num_cells, args.chars_per_cell)
    elif args.replace_all:
        replace_all_notebooks(args.num_cells, args.chars_per_cell)
    elif args.randomly_update:
        randomly_update_notebooks_and_files(args.update_chance, args.replace_chance)
    else:
        parser.print_help()
        parser.exit(message="Either nb_path should be set or replace_all should be true or randomly_update should be true\n")


if __name__ == '__main__':
    main()
