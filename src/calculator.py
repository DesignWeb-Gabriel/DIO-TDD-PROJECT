"""Módulo calculator com operações básicas."""


class Calculator:
    """Classe para operações matemáticas básicas."""

    def add(self, a: float, b: float) -> float:
        """Soma dois números.

        Args:
            a: Primeiro número
            b: Segundo número

        Returns:
            A soma de a e b
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtrai dois números.

        Args:
            a: Primeiro número
            b: Segundo número

        Returns:
            A subtração de b de a
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiplica dois números.

        Args:
            a: Primeiro número
            b: Segundo número

        Returns:
            O produto de a e b
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide dois números.

        Args:
            a: Dividendo
            b: Divisor

        Returns:
            O resultado da divisão de a por b

        Raises:
            ValueError: Se b for zero
        """
        if b == 0:
            raise ValueError("Divisão por zero não é permitida")
        return a / b
