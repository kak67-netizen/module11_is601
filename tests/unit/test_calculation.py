
import pytest
from pydantic import ValidationError

from app.calculation_factory import CalculationFactory
from app.schemas.calculation import CalculationCreate


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("Add", 10, 5, 15),
        ("Sub", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
    ],
)
def test_calculation_operations(operation, a, b, expected):
    calculation = CalculationCreate(
        a=a,
        b=b,
        type=operation,
    )

    result = CalculationFactory.calculate(calculation)

    assert result == expected


def test_invalid_operation():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Invalid")


def test_division_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="Divide")


def test_missing_operand():
    with pytest.raises(ValidationError):
        CalculationCreate.model_validate(
            {"a": 10, "type": "Add"}
        )


def test_invalid_operand():
    with pytest.raises(ValidationError):
        CalculationCreate(a="hello", b=5, type="Add")
