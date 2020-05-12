import subprocess
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


start = date(year=2019,month=1,day=13)
end = date(year=2019,month=2,day=28)

for current in daterange(start, end):
    #print(current)
    filename = '%s%s%s%s%s%s.grid' % \
         (
            str(current.year).zfill(4), str(current.month).zfill(2), str(current.day).zfill(2), 
            str(current.year).zfill(4), str(current.month).zfill(2), str(current.day).zfill(2)
         )
    f = open(filename, "r")

    ncols = int(f.readline().split()[1])
    nrows = int(f.readline().split()[1])
    xllcenter = float(f.readline().split()[1])
    yllcenter = float(f.readline().split()[1])
    cellsize = float(f.readline().split()[1])
    nodata_value = float(f.readline().split()[1])

    # St Lucia
    target_x = 153.0065457
    target_y = -27.5020447
    # THe Gap
    #target_x = 152.9444
    #target_y = -27.44639

    tl_x = xllcenter
    tl_y = yllcenter

    nx = int((target_x - tl_x) / cellsize)
    ny = nrows - int((target_y - tl_y) / cellsize)

    z = 0
    for i in range(nrows):
        t = 0
        z += 1
        for j in f.readline().split():
            t += 1
            if t == nx and z == ny:
                print(filename, j)

