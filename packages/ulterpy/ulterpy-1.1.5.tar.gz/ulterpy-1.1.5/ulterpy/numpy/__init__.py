from numpy import *

def split_sequence(sequence, steps):
  x, y = list(), list()
  for i in range(len(sequence)):
    end = i + steps
    if end > len(sequence) - 1:
      break
    seq_x, seq_y = sequence[i:end], sequence[end]
    x.append(seq_x)
    y.append(seq_y)
  return array(x), array(y)
