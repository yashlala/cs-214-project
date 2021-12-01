#!/usr/bin/python
import os
import argparse
from argparse import RawTextHelpFormatter

# Bubble sorting algorithm
def sort_bubble(numbers):
  for sorted in reversed(range(len(numbers))):
      for index in range(len(numbers[:sorted])):
          if numbers[index] > numbers[index + 1]:
            numbers[index], numbers[index + 1] = numbers[index + 1], numbers[index]
  return numbers

# Insertion sorting algorithm
def sort_insertion(numbers):
  for index in range(1, len(numbers)):
    for i in reversed(range(index)):
      if numbers[index] < numbers[i]:
        numbers[index], numbers[i] = numbers[i], numbers[index]
      else: break
  return numbers

# Selection sorting algorithm
def sort_selection(numbers):
  for index in range(len(numbers)):
        index_min = index + numbers[index:].index(min(numbers[index:]))
        numbers[index], numbers[index_min] = numbers[index_min], numbers[index]
  return numbers

# Argument parser
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Sort a file containing numbers', formatter_class=RawTextHelpFormatter)
parser.add_argument('file_in',  
                    type=str,
                    nargs='?',
                    default='unsorted.txt',
                    help='file containing unsorted numbers')
parser.add_argument('file_out', 
                    type=str,
                    nargs='?',
                    help='file to write sorted number to \n(Default: input file)')
parser.add_argument('-d','--delimiter',
                    type=str,
                    default=',', 
                    help='specify what delimiter to use \n(Default: \"\\n\")')
parser.add_argument('-o','--order',
                    choices=['ascending','descending'],
                    default='ascending',
                    help='specify how numbers should be ordered \n(Default: ascending)')
parser.add_argument('-s','--sorting-algorithm',
                    choices=['bubble','insertion','selection'],
                    default='selection',
                    help='specify what sorting algorithm to use \n(Default: selection)')
args = parser.parse_args()

# Write to input file if no output file is defined
if not args.file_out : args.file_out = args.file_in


def main():
  # Read file
  
  numbers = list(map(int, open(args.file_in,'r').read().split(args.delimiter)))

  # Sort numbers
  {
      'bubble' : sort_bubble(numbers),
      'insertion' : sort_insertion(numbers),
      'selection' : sort_selection(numbers)
  }[str(args.sorting_algorithm)]

  # Order ascending or descending
  if str(args.order) == 'descending' : numbers = reversed(numbers) 

  # Write file
  open(args.file_out, 'w').write(args.delimiter.join(map(str, numbers)))

if __name__ == '__main__':
    main()