import spacy
nlp = spacy.load('en_core_web_md')


def findSimilarity(desc):
    ''' Provided a movie desc, find the most similar in the list provided. '''

    # set up
    with open('movies.txt', 'r') as f:
        movies = []
        for line in f:
            # planning on returning movie letter only, and exclude it from the nlp
            line = line.split(':')
            movies += [(line[0], line[1])]

    desc_token = nlp(desc)
    movie_tokens = [(movie[0], nlp(movie[1])) for movie in movies]
    sim_scores = []
    # create a list of movie letter + similarity score tuples
    for movie_token in movie_tokens:
        sim_scores.append(
            (movie_token[0], desc_token.similarity(movie_token[1])))
    # find the highest similarity score
    high_score = max(v for _, v in sim_scores)
    # extract the movie matching that score
    best_match = [score[0].strip()
                  for score in sim_scores if high_score in score][0]
    print('You should watch %s!' % best_match)


# run it
desc = '''Will he save
their world or destroy it? When the Hulk becomes too dangerous for the
Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a
planet where the Hulk can live in peace. Unfortunately, Hulk land on the
planet Sakaar where he is sold into slavery and trained as a gladiator.'''

findSimilarity(desc)
