#!/usr/bin/env python

"""
A simple script that copies all the cubes and everything into the right places
This has not been well set up to work universally. It's only been tested on one setup
"""
import os, shutil


def main(RootDir, TAPViewerPath, CubesPath, Seasons, CubeRootName, NewNo):
    TAPViewerDir = os.path.join(RootDir, TAPViewerPath)
    TAPDATADir = os.path.join(TAPViewerDir, "TAPDATA")

    # copy the site.txt file
    shutil.copy(os.path.join(RootDir, "site.txt"), TAPDATADir)

    FullCubesPath = os.path.join(RootDir, CubesPath)

    for (season, junk) in Seasons:
        SeasonPath = os.path.join(TAPDATADir, season)
        if not os.path.isdir(SeasonPath):
            print "Creating:", SeasonPath
            os.mkdir(SeasonPath)
        SeasonCubesPath = os.path.join(FullCubesPath, season)
        print SeasonPath, SeasonCubesPath

        for name in os.listdir(SeasonCubesPath):
            print "Moving:", name
            d = 'pos_%03i' % NewNo
            Newname = "%s%s%s" % (CubeRootName, d[4:7].zfill(4), ".bin")
            os.rename(os.path.join(SeasonCubesPath, name),
                      os.path.join(SeasonPath, Newname))


if __name__ == '__main__':
    import Setup_TAP as tap

    main(tap.RootDir, tap.TAPViewerPath, tap.CubesPath, tap.Seasons, tap.CubesRootNames)
