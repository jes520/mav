# .. -*- coding: utf-8 -*-
#
# ****************************************************
# Python_tutorial.py - A brief introduction to Python.
# ****************************************************
"""
# Running Python
# ==============
# The guaranteed way to make a Python script run: ``python script_name.py``. For
# example, on Windows, ``Python_tutorial.py 1 2`` produces
# ``['C:\\Users\\bjones\\Documents\\mav\\tutorial\\Python_tutorial.py']``.
# In other words, Windows throws the command-line arguments away. To be safe,
# use ``python Python_tutorial.py 1 2`` instead.
from sys import argv
print(argv)
#
# Variables and arithmetic
# ========================
# This program is used to compute compund interest over a given period.
#
# Note that this variable begins as an integer. However, its type dynamicaly
# changes to a float.
principal = 2000
# The amount of money after interest increases the value of the principal.
net_gain = principal
rate = 0.05
numyears = 5
year = 1
while year <= numyears:
    # Before, we used ``principle = principle*(1 + rate)``. Using the ``*=``\
    # operator `DRYs <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_
    # the code. Note that the expression to the right of the ``*=`` operator is
    # implicitly encolosed in parentheses.
    net_gain *= 1 + rate
    # Use the `format <https://docs.python.org/2/library/stdtypes.html#str.format>`_
    # method to nicely format a string.
    print('In year {}, the total value is {}, with an increase of {} from the original investment.\n'.format(year, net_gain, net_gain - principal)),
    # Note that this block isn't placed in a for loop, so we need to manually
    # incrememnt the counter. **So....** we should rewrite this as a for loop.
    #
    # This add 1 to year. **This is bad comment** -- it's doesn't explain why,
    # and it repeats what's already stated in the code.
    year += 1
#
# Conditionals
# ============
a = 5
b = 7
if (a < b and
 number_of_chipmunks < (number_of_squirrels + number_of_rabbits) ):
    pass
elif a > b:
    print('elif')
else:
    print("more")

# Note that ``true`` is the WRONG spelling. Use ``True``.
if true:
    print("True")
else:
    print("False")


if '':
    print("True")
else:
    print("False")
    


# Conversions
# ===========
a = 5
print('The value of a is ' + str(a))
b = '4'
print(a + int(b))


# Strings
# =======
# ...and indexing...
a = 'hello'
print(a[1:2])

print(a[1:5])
print(a[1:])
print(a[-4:])
print("hello "
      "world.")
"""

# Lists
# =====
l = ['1', 2, 3.5, True]
print(l)

