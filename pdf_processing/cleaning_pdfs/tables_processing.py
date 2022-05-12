from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io

# Read the only the page n°6 of the file
food_calories = read_pdf('etude cas_témois_beszilpdf-6.pdf', pages = 1,
                         multiple_tables = False, stream = False)

# Transform the result into a string table format
table = tabulate(food_calories)

# Transform the table into dataframe
df = pd.read_fwf(io.StringIO(table))

# Save the final result as excel file
zdzf.to_excel("./data/food_calories.xlsx")