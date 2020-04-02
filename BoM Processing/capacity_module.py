
pc_data = {}

def get_capacity(postcode):
    if postcode not in pc_data: return -1
    record = pc_data[postcode]
    return record[0]

def load_capacity():
    filename = 'postcodes_1618.csv'
    f = open(filename, "r")
    # headers
    f.readline()
    # postcodes
    for line in f.readlines():
        tokens = line.split(',')
        if len(tokens[0].strip('"')) == 0: continue
        if len(tokens[4].strip('"')) == 0: continue
        postcode = tokens[0].strip('"')
        capacity = float(tokens[4].strip('"'))
        #potkw = int(tokens[11])

        pc_data[postcode] = [capacity]
