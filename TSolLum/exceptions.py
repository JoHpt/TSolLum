class TSolLumError(Exception):
    """Custom exception class for errors related to TransmittanceSpectrum calculations.

    Attributes
    ----------
        message (str): A descriptive error message.
    """
    def __init__(self, message: str) -> None:
        """Initialize the TSolLumError instance with a custom error message.

        Parameters
        ----------
            message (str): A descriptive error message explaining the cause
            of the exception.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Returns a string representation of the exception.

        Returns
        -------
            str: A string containing the custom error message.
        """
        return f"{self.message}"
    
class SpectrumError(Exception):
    
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Returns a string representation of the exception.

        Returns
        -------
            str: A string containing the custom error message.
        """
        return f"{self.message}"

