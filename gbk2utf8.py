#! /usr/bin/python3




import sys



def main():
  line_nr = 0
  with open(sys.argv[1], encoding="gbk") as orig, open("_out_" + sys.argv[1], "w", encoding="utf-8") as trans:
      while True:
        data = orig.readline()
        if not data:
            break
        line_nr += 1
        trans.write(data)
  print(f"一共{line_nr}行")




main()
