"""Module for the normal TextView class for Table."""

from typing import Any


class TextField:
  """Class to represent text field in python"""
  
  def __init__(self, name: str, value_type: Any):
    """Method to initialize the text field with name and value type.
      
    Args:
      name: str: Name of the text field
      value_type: str: Type of the value in the text field

    Raises:
      ValueError: If the value type is invalid
    """

    self.name = name
    self.value_type = value_type
    self.rows: list[str, bool, float, int, None] = []
    self.index = 0

  def get_type(self) -> Any:
    """Method to get the type of the text field"""
    return self.value_type

  def add_row(self, value: Any):
    """Method to add row to the text field"""
    self.rows.append(self.value_type(value))

  def __len__(self) -> int:
    """Method to get the length of the text field"""
    return len(self.rows)

  def __getitem__(self, index: int) -> list[str, bool, float, int, None]:
    """Method to get the value of the text field at the given index"""
    if index >= len(self.rows):
      raise IndexError("Index out of range")
    return self.rows[index]

  def __setitem__(self, index: int, value: Any):
    """Method to set the value of the text field at the given index"""
    if index >= len(self.rows):
      raise IndexError("Index out of range") 
    self.rows[index] = self.value_type(value)

  def append(self, value: Any):
    """Method to append value to the text field"""
    if not isinstance(value, self.value_type):
      raise ValueError(f"Invalid value type: {type(value)}")
    self.rows.append(self.value_type(value))

  def __iter__(self):
    """Method to iterate over the text field"""
    self.index = 0
    return self

  def __next__(self) -> Any:
    """Method to get the next value of the text field"""
    if self.index >= len(self.rows):
      self.index = 0
      raise StopIteration
    self.index += 1
    return self.rows[self.index - 1]

  def __str__(self):
    return f"<input type='text' value='{self.name}'>"
