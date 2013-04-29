"""
    Creates html for a mechanical turk entry for a movie review.
    Entry asks reader to read every sentence of a review, and then choose
    (via radio-button form) the most summarizing sentence of the review
"""


from nltk.corpus import movie_reviews
import string, sys


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

# Create the html for the mechanical turk entry
def make_mech_turk_entry():
    fileid = movie_reviews.fileids(categories=category)[fileid_num]
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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python make_mech_turk_entry.py <category> <fileid_num>"
    else:
        category = sys.argv[1]
        fileid_num = int(sys.argv[2])