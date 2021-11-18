from nltk.text import ConcordanceLine, ConcordanceIndex

bcols = {
    'HEADER' : '\033[95m',
    'OKBLUE' : '\033[94m',
    'OKCYAN' : '\033[96m',
    'OKGREEN' : '\033[92m' ,
    'WARNING' : '\033[93m' ,
    'FAIL' : '\033[91m',
    'ENDC' : '\033[0m',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m'
}


class UdapiConcordanceIndex(ConcordanceIndex):
    def __init__(self, nodes, mark='1', color=None, width=80):
        tokens = [(n.form, 'yes' if
                    n.misc['Mark'] == mark else 'no') for n in nodes]
        self.width = width
        self.color = bcols.get(color.upper(), None) if color else None
        super().__init__(tokens, key=lambda x: x[1])
        self._tokens = [t[0] for t in tokens]

    def offsets(self, word):
        return self._offsets[word]

    def find_concordance(self, word, width=80):
        # if isinstance(word, list):
        #     phrase = word
        # else:
        #     phrase = [word]
        #
        # half_width = (self.width - len(" ".join(phrase)) - 2) // 2
        context = self.width // 4  # approx number of words of context

        # Find the instances of the word to create the ConcordanceLine
        concordance_list = []

        offsets = self.offsets('yes')
        if offsets:
            for i in offsets:
                query_word = self._tokens[i]
                # Find the context of query word.
                left_context = self._tokens[max(0, i - context): i]
                right_context = self._tokens[i + 1: i + context]
                # Create the pretty lines with the query_word in the middle.
                half_width = (self.width - len(query_word) - 2) // 2
                left_print = " ".join(left_context)[-half_width:]
                if len(left_print) < half_width:
                    left_print = left_print.rjust(half_width, ' ')
                right_print = " ".join(right_context)[:half_width]
                # The WYSIWYG line of the concordance.
                if self.color:
                    colored_word = f'{self.color}{query_word}{bcols["ENDC"]}'
                else:
                    colored_word = query_word
                line_print = "\t".join([left_print, colored_word, right_print])
                # Create the ConcordanceLine
                concordance_line = ConcordanceLine(
                    left_context,
                    query_word,
                    right_context,
                    i,
                    left_print,
                    right_print,
                    line_print,
                )
                concordance_list.append(concordance_line)
        return concordance_list
