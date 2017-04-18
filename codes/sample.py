import random
import sys

def sample(filename, num, outfile):
  #random choose some files to generate a sample with specific size
  f = open(outfile, 'wb')
  file  = list(open(filename))
  f.write(file[0])
  file.pop(0)

  for i in random.sample(file, num):
    f.write(i)



if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("python sample.py csv_filename sample_size, output_csv_filename")
    sys.exit()
  csvfile = sys.argv[1]
  size = int(sys.argv[2])
  output = sys.argv[3]
  sample(csvfile, size, output)
