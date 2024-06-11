import pytest
from pyplate.pyplate import Substance, Container, Plate, Recipe


def test_eugene_simple_plate():
    print()
    solvent_THF = Substance.liquid("THF", mol_weight=72.11, density=0.8876)
    product_AB = Substance.solid("AB", mol_weight=550.0)

    stock_AB = Container.create_solution(product_AB, solvent_THF, concentration='0.100 M', total_quantity='10.0 mL')  # M, mL
    stock_THF = Container('THF', initial_contents=((solvent_THF, '1 L'),))
    plate = Plate("test plate", max_volume_per_well='500.0 uL')  # in uL

    recipe = Recipe()
    recipe.uses(plate, stock_AB, stock_THF)

    recipe.transfer(source=stock_AB, destination=plate["A:1"], quantity="100 uL")
    recipe.transfer(source=stock_THF, destination=plate["A:1"], quantity="100 uL")
    recipe = recipe.bake()

    plate = recipe['test plate']

    print(plate.get_volume('uL'))
    print(plate.get_volumes())
    print(plate.get_moles(product_AB, 'umol'))
