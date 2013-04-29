Rachel and Geoff's AI project, spring 2013.

Given a movie review, finds the sentence which best summmarizes the review. Based on research by Zhuang et al., available [here](http://research.microsoft.com/en-us/um/people/leizhang/Paper/cikm06_movie.pdf).

Requires Stanford Parser, written in Java. We've got the python wrapper included, but you need

Setup
======
* ``git clone git@github.com:gpleiss/ai-final-project.git``
* Download the Java code from [MIT](http://projects.csail.mit.edu/spatial/Stanford_Parser), and copy the 3rdParty directory to this project. (We added it to the .gitignore, because it was huge)
* You'll need to install JPype for python. We found [these instructions](http://blog.y3xz.com/blog/2011/04/29/installing-jpype-on-mac-os-x/) helpful for installing JPype on our Macs
* There's a chance you'll have more debugging to do. It took us about 4 hours to get the Stanford Parser working.
* To see whether things are set up properly:

    >>> from stanford_parser import parser as sp
    >>> parser = sp.Parser()
        Loading parser from serialized file 3rdParty/stanford-parser/stanford-parser-2010-08-20/../englishPCFG.July-2010.ser ... done [0.9 sec].
    >>> print parser.parseToStanfordDependencies("this movie was utterly fantastic")
    sentence='this movie was utterly fantastic'
    det(movie, this)
    nsubj(fantastic, movie)
    cop(fantastic, was)
    advmod(fantastic, utterly)
* If the above code works, you're good to go

To Use
======
To summarize each review included in the NLTK movie_reviews corpus:
    python summarizer.py

To summarize a movie review not included in the NLTK:
    python summarizer.py filename.txt
(We include 2 NYTimes movie reviews, review_oblivion.txt and review_painandgain.txt)
