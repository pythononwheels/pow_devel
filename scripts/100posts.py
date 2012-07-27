# -*- coding: utf-8 -*-
#
# create 100 Post entries
#

import sys, string

sys.path.append("../models/")

import Post

if __name__=="__main__":
    p = Post.Post()
    for elem in range(1,10):
        p.title = u"This is new post number %s" % (str(elem))
        p.content = u"""
        Das Blog [blɔg] (auch: der Blog) oder auch Web-Log [ˈwɛb.lɔg], engl. [ˈwɛblɒg], 
        Wortkreuzung aus engl. World Wide Web und Log für Logbuch, ist ein auf einer Website 
        geführtes und damit – meist öffentlich – einsehbares Tagebuch oder Journal, in 
        dem mindestens eine Person, der Web-Logger, kurz Blogger, Aufzeichnungen führt, 
        Sachverhalte protokolliert oder Gedanken niederschreibt.

        Häufig ist ein Blog „endlos“, d. h. eine lange, abwärts chronologisch sortierte 
        Liste von Einträgen, die in bestimmten Abständen umbrochen wird. 
        Der Herausgeber oder Blogger steht, anders als etwa bei Netzzeitungen, als 
        wesentlicher Autor über dem Inhalt, und häufig sind die Beiträge aus der 
        Ich-Perspektive geschrieben. Das Blog bildet ein für Autor und Leser einfach 
        zu handhabendes Medium zur Darstellung von Aspekten des eigenen Lebens und von 
        Meinungen zu spezifischen Themen. Meist sind aber auch 
        Kommentare oder Diskussionen der Leser über einen Artikel zulässig
        """
        p.content = p.content.replace("\n","<br>")
        p.create()
        print " -- created post number: ", str(elem)