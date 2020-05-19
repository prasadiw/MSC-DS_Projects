# RedditSubRedditRecommender
A recommender application to provide Reddit users links to discussion threads similar to the current discussion thread.

==============================

This project includes a installer with automatic setup but I have not shared that in this repository.
This repo only has source files and if you like to use installer just send me an email.

Below is the description of each main program of this application.

# Main Programs

**Indexer**

An inverted index is used to build the logic to scoring and recommending sub reddits. Whoosh, psaw and pushshift.io have been used to build up the logic.

Whoosh is a pure Python search engine library which contains more sophisticated helper functions for a ranking system. It defaults to Okapi BM 25. It supports gradual, continual, updates, etc. Furthermore, it allows to store things with the inverted index as well as index multiple “fields” of a document.

Using psaw and pushshift.io created another benefit or option. Rather than starting with nothing and building the inverted index as new comments roll on in, psaw.pushshift.io created the option to specify a start time in the recent past. The indexer will then start pulling in all the comments from that moment in time.

**Watcher**

The main process of Watcher is eatch/track mentions in realtime. Basically, we used reddit inbox as the storage for recommondation requests and we query the user mentions received to the inbox.is reading the user mentions of the reddit box.

**Responder**

Responder processes the request and responds with the proper sub reddit recommendation. It first use the inverted index and okapai BM25 to score the document and and then select the top 10% of the ranked subreddits. The ranking logic is applied to this selected set of subreddits. Main steps of Responder logic:

	*Use the inverted index and Okapi BM25 to score the documents

	*Select the top 10%

	*Group by submission

	*Take the harmonic mean within each submission

	*Multiply by the log of the count of matched documents per submission
	
	
# Assumptions
	*Current version of recommender request does not work when the request is made by the same person who created the post.
	*The Bot will not work if the post has been deleted/archived concurrently right after you entered the request.
	

