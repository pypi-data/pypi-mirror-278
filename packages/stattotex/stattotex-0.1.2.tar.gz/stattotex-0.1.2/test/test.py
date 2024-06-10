# Import module from "stattotex/stattotex.py"
# Add to path
import sys
sys.path.append('stattotex')
from stattotex import stattotex

# Formatted number to save
number = 2532.01
# Format
f_number = '{:,.2f}'.format(number)
stattotex("FormatTest", f_number, "test/testVars.tex", clear_file=True)

# String with a percent sign
pct_string = "0.3%"
stattotex("PctTest", pct_string, "test/testVars.tex")

# Let's try saving another number with the same name to see if it overrides but does not overwrite
pct = 100.3
pct_string = str(pct) + "%"
stattotex("PctTest", pct_string, "test/testVars.tex")

# Try saving a word
if pct > 0.0:
    word = "increased"
elif pct == 0.0:
    word = "stayed the same"
else:
    word = "decreased"
stattotex("WordTest", word, "test/testVars.tex")

# Try saving a number with an underscore in number name
number = 1000
try:
    stattotex("Num_Test", number, "test/testVars.tex")
except ValueError as e:
    err = e
# Throw an error if the try didn't throw a ValueError
if err is None:
    raise "Failed to throw ValueError for variable name with underscore."
