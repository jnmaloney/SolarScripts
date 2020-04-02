
data_list = []

def add_data_to_state(pc, name, state, c0, c1):
    data_list.append([pc, name, state, c0, c1])

# def dms_to_dec(dms):
#     if len(dms) < 3: return -9999.99
#     tokens = dms.split(":")
#     degrees = int(tokens[0])
#     minutes = int(tokens[1])
#     seconds = int(tokens[2])
#     return degrees + (1./60.) * minutes + (1./3600.) * seconds

# Open and store postcode data
# f = open('radioactive.txt', 'r')
# for line in f.readlines():
#     tokens = line.split(',')
#     pc = int(tokens[0])
#     name = tokens[1]
#     state = tokens[2]
#     c0 = dms_to_dec(tokens[3])
#     c1 = dms_to_dec(tokens[4])
#
#     #print(name)
#     add_data_to_state(pc, name, state, c0, c1)
f = open('postcode_envelopes_join.txt', 'r')
for line in f.readlines():
    tokens = line.split(';')
    pc = tokens[0]
    name = ''
    state = tokens[1]
    pos_tokens = tokens[2].split(',')
    c0 = 0.5 * (float(pos_tokens[0]) + float(pos_tokens[1]))
    c1 = 0.5 * (float(pos_tokens[2]) + float(pos_tokens[3]))

    #print(name)
    add_data_to_state(pc, name, state, c0, c1)

# ------------------
import irradiance_module
import capacity_module
import output_module

irradiance_module.load_daily_irradiance()
capacity_module.load_capacity()

#print(irradiance_module.get_daily_irradiance(152.9444, -27.44639))
#print(irradiance_module.get_daily_irradiance(138.6025, -34.94306))

postcodes_not_found = 0
no_data_irradiance = 0

def add_solar_capacity(record):
    postcode = record[0]
    capacity = capacity_module.get_capacity(postcode)
    if capacity == -1:
        capacity = 0
        global postcodes_not_found
        postcodes_not_found += 1
    record.append(capacity)

def add_daily_irradiance(record):
    # reorder coordinate
    c0 = record[3]
    c1 = record[4]
    irradiance = irradiance_module.get_daily_irradiance(c0, c1)
    if irradiance > 99999:
        global no_data_irradiance
        no_data_irradiance += 1
    record.append(irradiance)

def calculate_daily_output(record):
    a = record[5]
    b = record[6]
    c = output_module.get_output(a, b)
    record.append(c)

state_totals = {
'0': 0,
'1': 0, # NSW
'2': 0, # Vic
'3': 0, # Qld
'4': 0, # SA
'5': 0, # WA
'6': 0, # Tas
'7': 0, # NT
'8': 0, # ACT
'9': 0, # Other Territories
'ACT':0,
'NSW':0,
'QLD':0,
'NT':0,
'SA':0,
'TAS':0,
'VIC':0,
'WA':0,
}
national_total = 0
def collate(record):
    global national_total
    state = record[2]
    est = record[7]
    state_totals[state] += est
    national_total += est

for item in data_list:
    #   Add solar capacity
    add_solar_capacity(item)

    #   Add daily irradiance
    add_daily_irradiance(item)

    #   Calculate daily output
    calculate_daily_output(item)

    collate(item)

#   Sum output into state and national areas

print("Total: ", '{:,} kWh'.format(int(national_total)))
for i, j in state_totals.items():
    print(i, '{:,} kWh'.format(int(j)))

# Count errors:
# Postcode not located
print("Postcodes missing: %i" % postcodes_not_found)
# No data for irradiance
print("No data irradiance: %i" % no_data_irradiance)

n = len(capacity_module.pc_data)
m = n - postcodes_not_found - no_data_irradiance
print("%i / %i (%.1f%%) postcodes calculated" % (m, n, 100.0 * m / n))
