#
# Readme.txt for pythononwheels, the The small, quick and easy to use rapid web appliction generator framework, based on python
# by khz, Aug, 2011
#

Announcement:
---------------------------------------------
I'm very happy to announce the  first public release of pyhton on wheels, or short: pow. A plain and easy to use web generator framework for python.

You might say: "oh, no! What the world needs is more lawyers and another web app framework for python!", 
but let me quickly explain why I think there is room for python on wheels.


The pow principle:
---------------------------------------------
  Python on wheels is the plain, simple, quick and easy to use web generator framework. 
  If you want start to develop your application instead of spending weeks to learn the framework, 
  you are in the right place. PoW feels right if you do not reconize that you use it.


Main value and design goals for pow:
---------------------------------------------
  * Plain. 
  * Easy to use. 
  * Simple to understand. 
  * Generative. 
  * Based on proven python standards, tools and frameworks. (thank you very much for the tremendous work.)
	** wsgi
	** sqlAlchemy
	** Mako Templates 
	** Beaker Sessions
	** jQuery
  * Keep the developer focus on the web app, not on the framework 
  * Shall offer the rails way to python users but beeing even a little more focused on simplicity. 
  

Main features:
---------------------------------------------
  * Model, View, Controller Pattern
  * web app batteries included:
	** Session support
	** basic authentication
  * apache mod_wsgi ready 
  * includes a ready to run simple_server
  * no installation needed, just unpack the archive and you are ready to run
  * views are fully css controllable
  * jQuery support included
  * includes scaffolding.
  * includes migrations
  * automatically create and remove realtions (has_many, belongs_to, has_many_and_belongs_to)
  * includes migration jobs to backup or restore tables or do any other db related task.
  

Why Pyhton On Wheels was brought to life:
---------------------------------------------
  I read about ruby on rails some years ago (man, time goes by..) and was really impressed by the ideas and principles 
  behind it. I tried it myself and was even more impressed how easy and fluent the feeling was while using it. 
  It also was the first framework or toolset (or however you want to call it ) that really brought all the ideas of design patterns 
  into a standardized practical usage.
  But I have to admit that I am not the ruby guy and so I looked for something similar for python. 
  I found some frameworks which you all might know but I wasn't really happy with them. This was basically for two reasons,
  they were either too low level (ontop of wsgi for instance) or too big, high level and sophisticated (and also mostly not 
  based on standards, then). 

  I would have tended to use one of the bigger frameworks but really quickly got into the situation where I, again, had to 
  learn a Framework instead of developing my small web app.
  This was the time where I thought there should be a solution 'in the middle' which keeps small things small but let's you develop 
  a small web app in almost no time. (the famous weblog in 8 Minutes - and just because I type slowely ;)


Have a look and give it a try:
---------------------------------------------
  * get an impression: a-weblog-in-8-minutes-with-pow
  * homepage: www.pythononwheels.org

  Although it is an early release, it is fully usable. For example the www.pythononwheels.org page is hosted on pow.
  we really appreciate all of your feedback on pow. 


Thanks:
---------------------------------------------
  * to rails which started it all off, 
    we are 'only' on 'wheels but it feels like having wings ;) 
    Just try it yourself.

  * to all developers of the tools and frameworks pow is based on. Really amazing work.

  * To the snake ;)

  * To My family who let me work on it (from 23:00 to 01:00 - so I call pow internally 1121)
  
  * To Beckzman no team can be just one man ;)
