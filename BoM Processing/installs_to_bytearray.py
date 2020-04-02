import struct
import binascii

f = open("postcodes_1618.csv")
headings = f.readline()

g = open("postcode_installs.bin", "wb")

nlines = 0
for line in f.readlines():
  cells = line.split(",")
  postcode = cells[0].strip('"')
  if len(postcode) != 4: 
    postcode = "xxxx"
    print(line)
    continue
  try:
    installs = int(cells[1].strip('"'))
    dwellings = int(cells[2].strip('"'))
    cap_tot = float(cells[4].strip('"'))
    cap_under10 = float(cells[5].strip('"'))
    cap_10_100 = float(cells[6].strip('"'))
    cap_over100 = float(cells[7].strip('"'))  
  except:
    print(line)
    continue

  s = struct.Struct('4s ii ffff')
  values = (bytearray(postcode, 'utf-8'), installs, dwellings, cap_tot, cap_under10, cap_10_100, cap_over100)
  packed_data = s.pack(*values)

  #print('Original values:', values)
  #print('Format string  :', s.format)
  #print('Uses           :', s.size, 'bytes')
  #print('Packed Value   :', binascii.hexlify(packed_data))
  #g.write(binascii.hexlify(packed_data))
  g.write(packed_data)
  nlines += 1

print(nlines * 28)
