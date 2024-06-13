from enchant.tokenize import Filter

class ProperNounsFilter(Filter):
    """If a word looks like a proper nouns (first letter is a capital letter),
    ignore it.
    """
    def _skip(self, word):

        return (word[0].isupper() # first letter caps
                 and
                 not word[1:].isupper()
                 )
