"""Class to represnt UI materials for the table view in Python."""

from typing import *

from .text_field import TextField


class Table:
  """Class to represent HTML table like view in python"""

  def __init__(self, column_order: list[str]):
    """Method to initialize the table with name.
      
    Args:
      column_order: list[str]: List of column names
    """
    self.column_order = column_order
    self.columns: list[TextField] = []
    self.columns_dict: dict[str, TextField] = {}

  def add_column(self, name: str, value_type: Any):
    """Method to add column to the table"""
    text_field = TextField(name, value_type)
    self.columns.append(text_field)
    self.columns_dict[name] = text_field

#  def add_row(self, name: str, value: str | bool | float | int | None):
#    """Method to add row to the table"""
#    if name not in self.columns_dict:
#      raise ValueError(f"Invalid column name: {name}")
#    self.columns_dict[name].append(value)

  def add_rows(self, values: list[Any]):
    """Method to add row to the table"""
    if len(values) != len(self.columns):
      raise ValueError("Number of values should be equal to number of columns")
    for index, column in enumerate(self.columns):
      if not isinstance(values[index], column.get_type()):
        raise ValueError(f"Invalid value type: {type(values[index])}")
      column.append(values[index])

  def __len__(self) -> int:
    """Method to get the length of the table"""
    return len(self.columns_dict)

  def __contains__(self, value: str) -> bool:
    """Method to check if the column is in the table"""
    return value in self.columns_dict

  def __getitem__(self, name: str) -> list[Any]:
    """Method to get the row of the table at the given index"""
    if name not in self.columns_dict:
      raise IndexError("Column not in table")
    return self.columns_dict[name].rows

  def to_html(self) -> str:
    """Method to get the HTML representation of the table"""
    no_of_rows = len(self.columns[0]) if self.columns else 0
    html = """<style>
        table {
            border: 2px solid black;
            width: 100%;
            border-collapse: collapse;
        }

        th,
        td {
            border: 2px solid #7a3f3f;
            padding: 20px;
            text-align: center;
        }

    </style>\n"""
    table = f"{html}\n<table>\n"
    table += "<thead>\n"
    table += "<tr>\n"
    for column_name in self.column_order:
      table += f"<th>{column_name}</th>\n"
    table += "</tr>\n"
    table += "</thead>\n"
    table += "<tbody>\n"
    for index in range(len(self.columns[0])):
      table += "<tr>\n"
      for column_name in self.column_order:
        table += f"<td>{self.columns_dict[column_name][index]}</td>\n"
      table += "</tr>\n"
    table += "</tbody>\n"
    table += "</table>\n"
    return table
    
