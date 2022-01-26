import argparse
import math
import uuid
from pathlib import Path


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


def main():
    parser = argparse.ArgumentParser(description='Create notebook')
    parser.add_argument('--num_cells', type=int, default=25)
    parser.add_argument('--chars_per_cell', type=int, default=500)
    parser.add_argument('--nb_path', help="target notebook", default="")
    parser.add_argument('--replace_all',
                        help="All notebooks will be replaced in the current directory",
                        action='store_true', default=False)
    args = parser.parse_args()
    if args.nb_path:
        generate_notebook(args.nb_path, args.num_cells, args.chars_per_cell)
    elif args.replace_all:
        replace_all_notebooks(args.num_cells, args.chars_per_cell)
    else:
        parser.print_help()
        parser.exit(message="Either nb_path should be set or replace_all should be true\n")


if __name__ == '__main__':
    main()
