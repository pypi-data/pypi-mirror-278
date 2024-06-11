
# Standardize Phones

## Overview
Standardizes phone to E164 standard.

## Installing and Supported Versions
Standardize Phones available on PyPI:

`$ python -m pip install padroniza-telefone`

**Officially supports Python 3.8+.**

## Cloning the repository

`$ git clone https://github.com/tatianno/padroniza-telefone.git`

## Example
```
from padroniza_telefone import Telefone

telefone = Telefone(numero='12344123', codigo_area='11', codigo_pais='55')
print(telefone.numero)
```