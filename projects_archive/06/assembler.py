import re, sys

dests = {None:"000", "M":"001", "D":"010", "MD":"011", "A":"100", "AM":"101", "AD":"110", "AMD":"111"}
comps = {"0":"0101010", "1":"0111111", "-1":"0111010", "D":"0001100", "A":"0110000", "!D":"0001101",
        "!A":"0110001", "-D":"0001111", "-A":"0110011", "D+1":"0011111", "A+1":"0110111",
        "D-1":"0001110", "A-1":"0110010", "D+A":"0000010", "D-A":"0010011", "A-D":"0000111",
        "D&A":"0000000", "D|A":"0010101",
        "M":"1110000", "!M":"1110001", "-M":"1110011", "M+1":"1110111", "M-1":"1110010",
        "D+M":"1000010", "D-M":"1010011", "M-D":"1000111", "D&M":"1000000", "D|M":"1010101"}
jumps = {None:"000", "JGT":"001", "JEQ":"010", "JGE":"011", "JlT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}
symbols={"R0":0, "R1":1, "R2":2, "R3":3, "R4":4, "R5":5, "R6":6, "R7":7, "R8":8, "R9":9, "R10":10,
         "R11":11, "R12":12, "R13":13, "R14":14, "R15":15, "SCREEN":16384, "KBD":24576, "SP":0,
         "LCL":1, "ARG":2, "THIS":3, "THAT":4}

args = sys.argv
filename = args[1]

with open(filename, 'r') as fin:
  firstpass=[]
  used = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,16384,24576]
  i = 0
  for l in fin.readlines():
    # Remove anything after a comment
    try:
        l = l[:l.index("//")]
    except ValueError:
      pass
    # Remove whitespace
    l = "".join(l.split())
    # Skip empty lines
    if l == "":
      continue
    # try
    try:
      label = re.compile("\(([^()]*)\)").match(l).groups()[0]
      symbols[label] = i
      continue
    except AttributeError:
      firstpass.append(l)
      i += 1
    if l[0] == "@":
      try:
        num = int(l[1:])
        used.append(num)
      except ValueError:
        pass
  with open('.'.join(filename.split('.')[:-1] + ['hack']), 'w') as fout:
    for l in firstpass:
      # A-Instruction
      if l[0] == "@":
        # Check if its a number
        try:
          num = int(l[1:])
        # Try and resolve it as a symbol, or create a new symbol starting with the lowest free register
        except:
          if l[1:] not in symbols:
            found = False
            for q in range(24575):
              if q not in used:
                found = True
                break
            if found:
              symbols[l[1:]] = q
              used.append(q)
            else:
              print("Out of memory!")
          num = symbols[l[1:]]
        out = "0" + format(num, '015b') + "\n"
      # C-Instruction
      else:
        p=re.compile("(?:([^=]+)=)?([^=;]+)(?:;([^;]+))?")
        m=p.match(l)
        dest, comp, jump = m.groups()
        out = "111" + comps[comp] + dests[dest] + jumps[jump] + "\n"
      fout.write(out)