#!/usr/bin/env python
"""
A simple script to aid appending locations to existing TAP
it updates the site.txt file and move the cubes to the right location
"""

import os
import AddViewer


def main(RootDir, AppendNo, StartSites,  TAPViewerPath, CubesPath, Seasons, CubeRootName, BuildMudFlatCubes):
    print "\n---Updating Site.txt---"

    with open(os.path.join(RootDir, "site.txt"), 'r') as file:
        data = file.readlines()

    # Find the line where number of cubes is given and add one
    for i, line in enumerate(data):
        if 'CUBES' in line:
            change = i
            text = data[i][:]
            No = text.partition(' ')
            NewNo = int(No[0]) + 1
    data[change] = "%i CUBES\n" % NewNo

    # Add new cube location to the file:
    print "Adding the start site"
    data.append(StartSites + "\n")

    # and write everything back
    with open(os.path.join(RootDir, "site.txt"), 'w') as file:
        file.writelines(data)

    with open(os.path.join(RootDir, "BinLocs_"+ AppendNo +".txt"), 'w') as file:
        file.write("%i %s\n" % (NewNo, StartSites))

    print "\n---Adding Viewer---"
    AddViewer.main(RootDir, TAPViewerPath, CubesPath, Seasons, CubeRootName, NewNo)

    if BuildMudFlatCubes:
        print "\n---Adding MudFlat Viewer---"
        tapviewerpath_mf = TAPViewerPath + '_mf'
        cubespath_mf = CubesPath + '_mf'
        AddViewer.main(RootDir, tapviewerpath_mf, cubespath_mf, Seasons, CubeRootName, NewNo)


if __name__ == '__main__':
    import Setup_TAP as tap

    main(tap.RootDir, tap.StartSites, tap.TAPViewerPath, tap.CubesPath,
         tap.Seasons, tap.CubesRootNames, tap.BuildMudFlatCubes)
