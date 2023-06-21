GROSS_INCOME = 78624
STD_DEDUCTION = 13850

taxable_income = GROSS_INCOME - STD_DEDUCTION

income_tax = 0
income_tax += 11000 * .1 if taxable_income > 11000 else taxable_income * .1
income_tax += (44725-11000) * .12 if taxable_income > 44725 else (taxable_income-11000) * .12
income_tax += (95375-44725) * .22 if taxable_income > 95375 else (taxable_income-44725) * .22

self_employment_tax = (GROSS_INCOME) * .153/2
print((income_tax+self_employment_tax)/4)

print(100*3893.129*4/78624)