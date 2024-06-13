# Chroma Console

Chroma console is a python package for adding color and style to terminal text output using ANSI escape codes.

* if ***requests*** is installed this package updates automaticaly
* some terminals still don't support *ANSI escape*

<br>

## Installation

```shell
pip install chromaconsole
```

<br>

### How styling works
This package works using ***[ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)***

<br>

## Functions
<details>
<summary>Click here to see all functions</summary>

```python
#styling
Styling.disable()
Styling.enable()
Style.reset()
Style.bold()
Style.faint()
Style.italic()
Style.underlined()
Style.slow_blink()
Style.rapid_blink()
Style.reverse()
Style.hidden()
Style.strikethrough()
Style.doubly_underlined()
Style.normal_intensity()
Style.not_italic()
Style.not_underlined()
Style.not_blinking()
Style.proportional_spacing()
Style.not_reversed()
Style.reveal()
Style.not_strikethrough()
Style.not_proportional_spacing()
Style.overlined()
Style.not_overlined()
Style.minecraft(*args)

#coloring
Color.text(*args)
Color.text_gradient("text", color, color)
Color.default_text()
Color.background(*args)
Color.background_gradient("text", color, color)
Color.default_background()
Color.Text.black()
Color.Text.red()
Color.Text.green()
Color.Text.yellow()
Color.Text.blue()
Color.Text.magenta()
Color.Text.cyan()
Color.Text.white()
Color.Text.br_black()
Color.Text.br_red()
Color.Text.br_green()
Color.Text.br_yellow()
Color.Text.br_blue()
Color.Text.br_magenta()
Color.Text.br_cyan()
Color.Text.br_white()
Color.Background.black()
Color.Background.red()
Color.Background.green()
Color.Background.yellow()
Color.Background.blue()
Color.Background.magenta()
Color.Background.cyan()
Color.Background.white()
Color.Background.br_black()
Color.Background.br_red()
Color.Background.br_green()
Color.Background.br_yellow()
Color.Background.br_blue()
Color.Background.br_magenta()
Color.Background.br_cyan()
Color.Background.br_white()

#some other things (not finished)
Console.clr_scr_to_end()
Console.clr_scr_to_begin()
Console.clr_entire_scr()
Console.clr_line_to_end()
Console.clr_line_to_begin()
Console.clr_entire_line()
Console.scroll_up(int)
Console.scroll_down(int)
Console.bell()
Console.save_cursor()
Console.restore_cursor()
Console.switch_alt_scr()
Console.switch_orig_scr()
Console.show_cursor()
Console.hide_cursor()
```
</details>

<br>

## Example usage

```python
from chromaconsole import *

print(f"{Color.Text.red()}here is red colored text{Style.reset()}")
print(f"{Color.text(r, g, b)}here is RGB colored text{Style.reset()}")
print(f"{Color.background(r, g, b)}here is RGB colored background{Style.reset()}")

print(f"{Color.text('#rrggbb')}here is HEX colored text{Style.reset()}")
print(f"{Color.background('#rrggbb')}here is HEX colored background{Style.reset()}")

print(f"{Style.bold()}Bold {Style.reset()}")
print(f"{Style.italic()}Italic {Style.reset()}")
print(f"{Style.underlined()}Underlined {Style.reset()}")
print(f"{Style.strikethrough()}Strikethrough {Style.reset()}")

print(f"{Style.bold()}{Style.italic()}bold+italic {Style.reset()}")
print(f"{Style.minecraft('§','§ahello §4world§r')}")
```

<br>

## .enable() and .disable():

After executing the `Styling.disable()` command, the system will no longer apply coloring and styling to the content. To re-enable these features, simply use the `Styling.enable()` command.

```python
from chromaconsole import Styling
#disable the coloring and styling
Styling.disable()
print(f"{Color.text(r, g, b)}text without color and style{Style.reset()}")
Styling.enable()
print(f"{Color.text(r, g, b)}text with color and style{Style.reset()}")
```