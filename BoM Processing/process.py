import subprocess

for fff in range(1, 20+1):
    filename = 'data/202001%s202001%s.grid' % (str(fff).zfill(2), str(fff).zfill(2))
    #filename = 'data/2020010120200101.grid'
    filenamez = filename + '.Z'
    #subprocess.run(["gzip", "-d", filenamez])

    f = open(filename, "r")

    ncols = int(f.readline().split()[1])
    nrows = int(f.readline().split()[1])
    xllcenter = float(f.readline().split()[1])
    yllcenter = float(f.readline().split()[1])
    cellsize = float(f.readline().split()[1])
    nodata_value = float(f.readline().split()[1])

    #target_x = 138.6025
    #target_y = -34.94306
    # target_x = 153.021072
    # target_y = -27.470125
    # THe Gap
    target_x = 152.9444
    target_y = -27.44639

    #tl_x = xllcenter - 0.5 * ncols * cellsize
    #tl_y = yllcenter - 0.5 * nrows * cellsize
    tl_x = xllcenter
    tl_y = yllcenter

    nx = int((target_x - tl_x) / cellsize)
    ny = nrows - int((target_y - tl_y) / cellsize)
    #print(nx, ny)

    ## Print Map ##
    # z = 0
    # for i in range(nrows):
    #     t = 0
    #     z += 1
    #     line = ''
    #     for j in f.readline().split():
    #         t += 1
    #         if t % 10 == 0 and z % 10 == 0:
    #             #if t == 530 and z == 500:
    #             if t == 820 and z == 350:
    #                 line += 'X'
    #             elif float(j) == nodata_value:
    #                 line += ' '
    #             else:
    #                 line += '.'
    #
    #     if len(line): print(line)

    z = 0
    for i in range(nrows):
        t = 0
        z += 1
        for j in f.readline().split():
            t += 1
            if t == nx and z == ny:
                print(filename, j)

# For each file

# Open file

# Unzip

# Read data
