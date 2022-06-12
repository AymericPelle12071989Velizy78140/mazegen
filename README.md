# Mazegen

## Dependencies

```bash
pip install openpyxl
pip install wand
tkinter
```

## Use

Use `-D` to display generated image file(s).

### Generate a maze image from an input file

```bash
python mazegen.py    maze_drawer.json maze.xlsx .
python mazegen.py -D maze_drawer.json maze.xlsx output_dir
```

### Generate maze images from an input directory

All `input_dir/*.xlsx` files are treated.

```bash
python mazegen.py    maze_drawer.json input_dir output_dir
python mazegen.py -D maze_drawer.json input_dir output_dir
```

## License

[MIT License](https://github.com/arapelle/mazegen/blob/master/LICENSE.md) © mazegen
