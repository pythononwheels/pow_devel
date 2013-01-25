#
# project_name = python on wheels
# author = khz
# author_email = khz@pythononwheels.org
# short_description = python rapid web app generator framework
# homepage_base_url = http://www.pythononwheels.org
#
# New style main config file for PythonOnWheels.
# Uses python data structures (dict, list etc) instead of ini-style
# way better handling ;)
# Date: July 2012
# 

global_conf = { 
    "ENV"               :   "development",
    "DEFAULT_TEMPLATE"  :   "hero.tmpl",
    "DEFAULT_ENCODING"  :   "utf-8",
    "PORT"              :   "8080",
    "MAX_FILE_UPLOAD"   :   "100000",
    "STD_BINARY_PATH"   :   "/static/img/",
    "DEFAULT_IMAGE_NAME":   "image",
    "DEFAULT_VIDEO_NAME":   "video",
    "DEFAULT_AUDIO_NAME":   "audio",
    "DEFAULT_TEXT_NAME" :   "text"
}

routes = {
     "default"  :   "/app/welcome" 
}

logging = {
      "LOGFILE"                 :   "log.txt",
      "LOGFILE_MODE"            :   "w",
      # log_level = DEBUG or INFO
      "LOG_LEVEL"               :   "DEBUG",
      # see: http://docs.python.org/howto/logging.html#logging-basic-tutorial
      "FORMAT"                  :   "%(asctime)s %(message)s",
      "SQLALCHEMY_LOGGING"      :   "True"
}