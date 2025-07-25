"""Testes para o módulo calculator."""

import pytest
from src.calculator import Calculator


class TestCalculator:
    """Testes para a classe Calculator."""

    def test_add_two_numbers(self):
        """Teste para adição de dois números."""
        calc = Calculator()
        result = calc.add(2, 3)
        assert result == 5

    def test_subtract_two_numbers(self):
        """Teste para subtração de dois números."""
        calc = Calculator()
        result = calc.subtract(5, 3)
        assert result == 2

    def test_multiply_two_numbers(self):
        """Teste para multiplicação de dois números."""
        calc = Calculator()
        result = calc.multiply(4, 3)
        assert result == 12

    def test_divide_two_numbers(self):
        """Teste para divisão de dois números."""
        calc = Calculator()
        result = calc.divide(10, 2)
        assert result == 5.0

    def test_divide_by_zero_raises_error(self):
        """Teste para verificar se divisão por zero levanta exceção."""
        calc = Calculator()
        with pytest.raises(ValueError, match="Divisão por zero não é permitida"):
            calc.divide(10, 0)
