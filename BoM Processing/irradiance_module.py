
data_rows = []
data_meta = {}

# Return irradiance from lat-lon pair
def get_daily_irradiance(x, y):
    tl_x = data_meta["xllcenter"]
    tl_y = data_meta["yllcenter"]
    cellsize = data_meta["cellsize"]
    nrows = data_meta["nrows"]

    nx = int((x - tl_x) / cellsize)
    ny = nrows - int((y - tl_y) / cellsize)
    try:
        return data_rows[ny][nx]
    except:
        return data_meta["nodata_value"] 

# Read grid file and save values
def load_daily_irradiance():

    filename = 'latest.grid'
    #filename = 'data/2020010120200101.grid'
    f = open(filename, "r")

    data_meta["ncols"] = int(f.readline().split()[1])
    data_meta["nrows"] = int(f.readline().split()[1])
    data_meta["xllcenter"] = float(f.readline().split()[1])
    data_meta["yllcenter"] = float(f.readline().split()[1])
    data_meta["cellsize"] = float(f.readline().split()[1])
    data_meta["nodata_value"] = float(f.readline().split()[1])

    for i in range(data_meta["nrows"]):
        row = [float(j) for j in f.readline().split()]
        data_rows.append(row)
