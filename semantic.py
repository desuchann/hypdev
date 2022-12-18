import spacy

def findSimilarity(itr, model='en_core_web_md'):
    nlp = spacy.load(model)
    tokens = nlp(itr)

    for token1 in tokens:
        for token2 in tokens:
            print(token1.text.ljust(8), token2.text.ljust(8), token1.similarity(token2))
    print('\n')

tokens = findSimilarity('cat apple monkey banana ')

# cat and monkey are both animals so the high-ish score makes sense
# banana and apple have a similar score as they're both fruits
# monkey and banana have a somewhat high score presumably because monkeys are known to eat bananas
# the others have quite a low similarity

tokens = findSimilarity('car wheel vehicle circle')

# I chose the words im a similar way and got mostly the expected result:
# car and vehicle are extremely related, closely followed by car and wheel and vehicle and wheel
# wheel and circle got a much lower score than expected, perhaps because it's not a relation ship that's often verbalised
# the others had a very low score

# ==== Running example.py ====
# On trying to run example.py with the sm model, I got a warning saying it's less accurate because
# it doesn't have word vectors and depends on other attributes to calculate similarity
# I can indeed see that the scores cover a wider range, with some being as low as 0.1 for the sm model
# whereas the score is consistently high for the md model