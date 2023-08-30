import re, sys

args = sys.argv
filename = args[1]

with open(filename, 'r') as fin:
  firstpass=[]
  for l in fin.readlines():
    # Remove anything after a comment
    try:
      l = l[:l.index("//")]
    except ValueError:
      pass
    # Remove newlines
    l = re.sub("\n","",l)
    # Skip empty lines
    if l == "":
      continue
    firstpass.append(l)
  with open('.'.join(filename.split('.')[:-1] + ['asm']), 'w') as fout:
    for l in firstpass:
      fout.write("// " + l + "\n")
      if re.match("push constant \d+", l):
        m = re.match("push constant (\d+)", l)
        i = m.groups()[0]
        fout.write("""@%s
D=A
@SP
A=M
M=D
@SP
M=M+1
""" % i)
      elif re.match("pop local \d+", l):
        m = re.match("pop local (\d+)", l)
        i = m.groups()[0]
        fout.write("""@LCL
D=M
@%s
D=D+A
@SP
M=M-1
A=M
M=D
""" % i)

# addr=LCL+ i, SP--, *addr=*SP

# @LCL
# D=M
# @i
# D=D+A
# @R13
# M=D

# @SP
# M=M-1

# @SP
# A=M
# D=M
# @R13
# A=M
# M=D