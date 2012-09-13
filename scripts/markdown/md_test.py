#
# what:     a short markdown to html test for PoW
# web:      www.pythononwheels.org
# email:    khz@pythononwheels.org
# who:      11to1.org sparetime development from 11pm to 1am ;)
#
#
import markdown

if __name__ == "__main__":
    infile = open("github.md", "r")
    text = infile.read()
    infile.close()
    html = markdown.markdown(text)
    of = open("github.html","w")
    of.write(html)
    of.close()
    