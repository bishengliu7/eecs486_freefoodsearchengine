import random

def sample(filename, num, outfile):
  f = open(outfile, 'wb')

  for i in random.sample(list(open(filename)), num):
    f.write(i)

if __name__ == "__main__":
  sample('events.csv', 100, 'trainevets.csv')