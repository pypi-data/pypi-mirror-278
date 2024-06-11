from langchain_core.tools import tool
import numpy as np

class StatisticalTools:
    
    @tool("calculate_mean")
    def calculate_mean(values: list):
        """Calculate the mean of a list of numbers.

        Args:
            values (list): A list of numbers.
                Example: [1, 2, 3, 4, 5]

        Returns:
            float: The mean of the list of numbers.
        """
        return sum(values) / len(values)

    @tool("calculate_median")
    def calculate_median(numbers: list) -> float:
        """
        Calculate the median of a list of numbers.

        Args:
            numbers (list): The list of numbers to calculate the median of. Should be passed as a key in a dictionary.

        Returns:
            float: The median of the numbers.
        """
        return float(np.median(numbers))

    @tool("calculate_std")
    def calculate_std(numbers: list) -> float:
        """
        Calculate the standard deviation of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the standard deviation of. Should be passed as a key in a dictionary.
        
        Returns:
            float: The standard deviation of the numbers.
        """
        return np.std(numbers)

    @tool("calculate_variance")
    def calculate_variance(numbers: list) -> float:
        """
        Calculate the variance of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the variance of. Should be passed as a key in a dictionary.
        
        Returns:
            float: The variance of the numbers.
        """
        return np.var(numbers)

    @tool("calculate_min")
    def calculate_min(numbers: list) -> float:
        """
        Calculate the minimum value of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the minimum value of. Should be passed as a key in a dictionary.
        
        Returns:
            float: The minimum value of the numbers.
        """
        return np.min(numbers)

    @tool("calculate_max")
    def calculate_max(numbers: list) -> float:
        """
        Calculate the maximum value of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the maximum value of. Should be passed as a key in a dictionary.
        
        Returns:
            float: The maximum value of the numbers.
        """
        return np.max(numbers)

    @tool("calculate_sum")
    def calculate_sum(numbers: list) -> float:
        """
        Calculate the sum of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the sum of. Should be passed as a key in a dictionary.
        
        Returns:
            float: The sum of the numbers.
        """
        return np.sum(numbers)

    @tool("calculate_percentile")
    def calculate_percentile(numbers: list, percentile: float) -> float:
        """
        Calculate the given percentile of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the percentile of. Should be passed as a key in a dictionary.
            percentile (float): The percentile to calculate (0-100).
        
        Returns:
            float: The calculated percentile of the numbers.
        """
        return np.percentile(numbers, percentile)

    @tool("calculate_mode")
    def calculate_mode(numbers: list) -> float:
        """
        Calculate the mode of a list of numbers.
        
        Args:
            numbers (list): The list of numbers to calculate the mode of. Should be passed as a key in a dictionary.
        
        Returns:
            float: The mode of the numbers.
        """
        return float(max(set(numbers), key=numbers.count))
    
    @tool("Calculator")
    def calculate(operation):
        """Useful to perform any mathematical calculations, 
        like sum, minus, multiplication, division, etc.
        The input to this tool should be a mathematical 
        expression, a couple examples are `200*7` or `5000/2*10`
        """
        return eval(operation)