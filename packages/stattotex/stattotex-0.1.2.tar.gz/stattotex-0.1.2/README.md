# stattotex-python

A simple function for automatically updating LaTeX documents with numbers or strings from Python. No more manually copying your calculations over every time your code is re-run!

Inspired by the Stata package [isapollnik/stattotex](https://github.com/isapollnik/stattotex).

## Installation

`pip install stattotex`

## Usage

For examples, see the "demo.py" and "Demo Report.tex" and the overall [demo](https://github.com/ijyliu/stattotex-python/tree/main/demo) folder. A summary is below:

In Python, import the function with

`from stattotex.stattotex import stattotex`

and use it with

`stattotex(variable_name, variable_value, filename, clear_file)`

where `variable_name` is a name you want to assign to the variable in LaTeX (note that you may not include underscores), `variable_value` is a number or string, `filename` is a file path string to save the variable to, and `clear_file` is an optional True/False flag to delete a pre-existing file.

Then, in your LaTex document, put

`\input{<your filename>}`

in the preamble and add your variable with

`\<your variable_name>`

You may find it helpful to insert `\space` afterwards (`\<your variable_name> \space`) to correct the spacing.
