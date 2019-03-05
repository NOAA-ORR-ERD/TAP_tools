#!/usr/bin/env python

"""
A simple script that copies all the cubes and everything into the right places

This has not been well set up to work universally. It's only been tested on one setup

"""
import os, shutil


def main(RootDir, TAPViewerPath, TAPViewerSource, StartTimeFiles, MapFileName, CubesPath, Seasons, Data_Dir):
    TAPViewerDir = os.path.join(RootDir, TAPViewerPath)

    # Check if TAP Viewer Dir exists:
    if not os.path.isdir(TAPViewerDir):
        print "making new TAP Viewer Directory"
        os.mkdir(TAPViewerDir)

    # Check for TAPDATA
    TAPDATADir = os.path.join(TAPViewerDir, "TAPDATA")
    if not os.path.isdir(TAPDATADir):
        print "Making TAPDATA Directory"
        os.mkdir(TAPDATADir)

    # copy the TAPCONFIG file
    shutil.copy(os.path.join(TAPViewerSource, "TAPCONFIG.txt"), TAPDATADir)

    # copy the TAP.exe file
    shutil.copy(os.path.join(TAPViewerSource, "TAP.exe"), TAPViewerDir)

    # copy the site.txt file
    shutil.copy(os.path.join(RootDir, "site.txt"), TAPDATADir)

    # copyt the map file
    shutil.copy(os.path.join(Data_Dir, MapFileName), TAPDATADir)

    # copy the start times file (not required, but it's good to have it there
    print StartTimeFiles
    for (filename, _) in StartTimeFiles:
        shutil.copy(filename, TAPDATADir)

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
            shutil.move(os.path.join(SeasonCubesPath, name),
                        os.path.join(SeasonPath, name))


if __name__ == '__main__':
    import Setup_TAP as tap

    maint(tap.RootDir, tap.TAPViewerPath, tap.TAPViewerSource, tap.StartTimeFiles, tap.MapFileName, tap.CubesPath,
          tap.Seasons, tap.Data_Dir)
