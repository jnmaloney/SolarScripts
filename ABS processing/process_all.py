# data
#mb_to_pc = {}
mb_to_name = {}
pc_to_mb = {}

mb_to_pc = {}
pc_to_names = {}

pc_to_state = {}

# Load data files
file = open("../POA_2016_AUST.csv", "r")
file.readline() # skip first line
for line in file.readlines():
    tokens = line.split(",")
    mb = tokens[0]
    pc = tokens[1]
    mb_to_pc[mb] = pc
    if pc not in pc_to_mb.keys():
        pc_to_mb[pc] = []
    pc_to_mb[pc].append(mb)

file = open("../SSC_2016_AUST.csv", "r")
file.readline() # skip first line
for line in file.readlines():
    tokens = line.split(",")
    mb = tokens[0]
    name = tokens[2]
    state = tokens[3]
    mb_to_name[mb] = name

    pc = mb_to_pc[mb]
    if pc not in pc_to_names.keys():
        pc_to_names[pc] = set()
    pc_to_names[pc].add(name)

    if pc in pc_to_state.keys() and pc_to_state[pc] != state: 
      print("%s was %s, changing to %s, %s" % (pc, pc_to_state[pc], state, tokens[4]))
    pc_to_state[pc] = state

# Geographic areas
import gdal
src_file = "../gpkg/ASGS 2016 Volume 3.gpkg"
source = gdal.OpenEx(src_file, 0)
layer = source.GetLayer(1)

# Add "area" to "postcode"
pc_envelopes = {}
pc_areas = {}
def addArea(pc, area):

    if area == None:
        print(pc) # Some postcodes have no area
        return

    if pc not in pc_envelopes.keys():
        #               ---long----  ----lat----
        pc_envelopes[pc] = [1000, -1000, 1000, -1000]

        pc_areas[pc] = 0

    env = area.GetEnvelope()
    if env[0] < pc_envelopes[pc][0]: pc_envelopes[pc][0] = env[0]
    if env[1] > pc_envelopes[pc][1]: pc_envelopes[pc][1] = env[1]
    if env[2] < pc_envelopes[pc][2]: pc_envelopes[pc][2] = env[2]
    if env[3] > pc_envelopes[pc][3]: pc_envelopes[pc][3] = env[3]

    pc_areas[pc] += area.Area()


feature = layer.GetNextFeature()

while feature != None:
    addArea(feature.GetField(1), feature.GetGeomFieldRef(0))
    feature = layer.GetNextFeature()

# Dump everything to a file
file = open("postcode_envelopes.txt", "w")
file_join = open("postcode_envelopes_join.txt", "w")
for pc, area in pc_areas.items():

    # Find a matching mb for this pc
    mb = pc_to_mb[pc][0]
    file_join.write( "%s;%s;%s;%s\n" % (pc, pc_to_state[pc], ','.join(map(str,pc_envelopes[pc])), area))

    names = pc_to_names[pc]
    for name in names:
        file.write( "%s;%s;%s;%s\n" % (pc, name, ','.join(map(str,pc_envelopes[pc])), area))
