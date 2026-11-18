
import pytest
from pydantic import ValidationError

from app.database import SessionLocal
from app.models.calculation import Calculation
from app.calculation_factory import CalculationFactory
from app.schemas.calculation import CalculationCreate, CalculationRead


def test_create_calculation():
    data = CalculationCreate(a=10, b=5, type="Add")
    result = CalculationFactory.calculate(data)

    with SessionLocal() as db:
        calculation = Calculation(
            a=data.a,
            b=data.b,
            type=data.type.value,
            result=result,
        )

        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        assert calculation.id is not None
        assert calculation.a == 10
        assert calculation.b == 5
        assert calculation.type == "Add"
        assert calculation.result == 15

        saved = db.get(Calculation, calculation.id)

        assert saved is not None
        assert saved.result == 15

        response = CalculationRead.model_validate(saved)
        assert response.result == 15

        db.delete(calculation)
        db.commit()


def test_invalid_calculation_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Invalid")


def test_division_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="Divide")
