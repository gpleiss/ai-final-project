from nltk.corpus import movie_reviews
import string

preamble = """
<h1>Find the sentence in the movie review that best summarizes the review.</h1>
<ul>
    <li>Read the entire movie review below.</li>
    <li>After you have finished reading the review, choose which sentence you believe best summarizes the review.</li>
    <li>Below the review text, click the radio box next to the sentence you believe best summarizes the review.</li>
</ul>
<br>
<br>


"""

fileid = movie_reviews.fileids(categories="neg")[0]
turk_entry_filename = "entry-%s" % fileid.replace("/", "-")

with open(turk_entry_filename, "wb") as f:
    f.write(preamble)
    f.write("\n\n\n<h1>Review</h1>\n\n<p>")
    f.write(movie_reviews.raw(fileid).replace("\n", "<br/>\n"))
    f.write("</p>\n")

    f.write("\n\n\n<h1>Select Summary Sentence</h1>\n\n<p>")
    for i, sent in enumerate(movie_reviews.sents(fileid)):
        opentag = '<input type="radio" name="%s" value="sent%i">' % (fileid, i)
        taginner = string.join(sent, " ")
        closetag = "</input><br/>\n"
        f.write(opentag + taginner + closetag)
    f.write("</p>\n")

