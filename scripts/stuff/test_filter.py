#
# test the pre_/post_filter functionality
#


import AppController
import ApplicationController

if __name__ == "__main__":
    app = AppController.AppController()
    app.pre_filter("authenticate","only", ["thanks"])
    app.pre_filter("authenticate","any")
    app.thanks()
    
    