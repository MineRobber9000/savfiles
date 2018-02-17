SAVFiles v0.0.1
===============

How to use it::

    import sav
    savfile = sav.SAVFile() # creates basic MBC1 .sav file
    print savfile[0][0]==0xFF # True (all bytes in MBC1 default to 255)
    savfile[0][0]=0x12
    print savfile[0][0]==0xFF # False (now that the byte's been set it's no longer 255)
    savfile.output("testing.sav") # output save to file
    # In another session...
    import sav
    savfile = sav.SAVFile("testing.sav")
    print savfile[0][0]==0x12 # True (file loaded)
    savfile.load("another_save.sav")
    print savfile[0][0]==0x12 # most likely will be False (new save loaded)
