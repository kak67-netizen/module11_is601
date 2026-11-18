
from app.operations import add, subtract, multiply, divide
from app.schemas.calculation import CalculationCreate, CalculationType


class CalculationFactory:

    @staticmethod
    def calculate(calculation: CalculationCreate) -> float:
        operations = {
            CalculationType.Add: add,
            CalculationType.Sub: subtract,
            CalculationType.Multiply: multiply,
            CalculationType.Divide: divide,
        }

        operation = operations[calculation.type]

        return operation(calculation.a, calculation.b)
