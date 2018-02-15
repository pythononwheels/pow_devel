#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest
import os
import shutil
import {{appname}}.config as cfg

# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform


if __name__ == "__main__":
    migs_before=os.listdir(os.path.join("..", "migrations/versions"))
    # save the old sqlite db 
    dbname=cfg.database["sql"]["dbname"]
    backup_path=os.path.join("..", "pow_test_sqlitdb.bak")
    backed_up_sqlite=False
    try:
        shutil.copy(dbname, backup_path)
        backed_up_sqlite=True
    except:
        print(" no sqlite.db so far")
        
    print(55*"-")
    print(" running pow Tests on: " + sys.platform)
    print(" ... ")
    if sys.platform.startswith("darwin"):
        # osx
        ret = pytest.main(["-k-notonosx", "--junitxml=result.xml", "pow_tests.py"])
    else:
        ret = pytest.main(["--junitxml=result.xml", "pow_tests.py"])
    
    print(" Failures: " +str(ret))
    print(55*"-")
    print("cleaning up:")
    print("  .. removing migrations")
    migs_after=os.listdir(os.path.join("..", "migrations/versions"))
    del_migs=list(set(migs_after) - set(migs_before))
    #print("    .. Migs before: {}".format(str(migs_before)))
    #print("    .. Migs after: {}".format(str(migs_after)))
    print("    .. Migrationss to delete: {}".format(str(del_migs)))

    for elem in del_migs:
        os.remove(os.path.join("../migrations/versions", elem))
        print("      .. deleted: {}".format(elem))
    #
    # removing the test DB
    #
    os.remove(dbname)
    if backed_up_sqlite:
        print("  .. I save your sqlite DB to: {}".format(backup_path))
        print("    .. restoring it now ..... back to: {}".format(dbname))
        shutil.copy(backup_path, dbname)
    else:
        print("  .. You did not have a sqlite DB so nothing to restore")
    print("  .. finally removing the Test model...")
    os.remove(os.path.join("../models/sql/", "pow_test_model.py"))
    print("done.")
    print(55*"-")
    print("  You can use: junit2html result.xml result.html to generate a html test report.")
    print(55*"-")
