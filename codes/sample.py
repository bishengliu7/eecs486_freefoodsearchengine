import random
import sys

def sample(filename, num, outfile):
  f = open(outfile, 'wb')

  for i in random.sample(list(open(filename)), num):
    f.write(i)



if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("python sample.py csv_filename sample_size, output_csv_filename")
    sys.exit()
  csvfile = sys.argv[1]
  size = int(sys.argv[2])
  output = sys.argv[3]
  sample(csvfile, size, output)
