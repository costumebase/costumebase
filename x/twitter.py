
Challenge #4 form "Exercises for Programmers: 57 Challenges"
# Book by Brian P. Hogan
how to Printing Quotes? here is python 
solution, you can print quote more straight forward way than this
but the goal of the book like you use little bit different way. 



def print_quote():
    quote = input('What is the quote? ')
    return quote


def print_author_name():
    author = input('Who said it? ')
    return author


def print_quotes(author_name, quote):
    """ Print quotes
    """
    print(f'{author_name} says, \"{quote}\"')


if __name__ == "__main__":
    quote = print_quote()
    author_name = print_author_name()
    print_quotes(author_name, quote)

    # output

What is the quote? Be in this world like a stranger or one who is passing trough.
Who said it? Prophet Muhammad(PBUH)
Prophet Muhammad(PBUH) says, "Be in this world like a stranger or one who is passing trough."
