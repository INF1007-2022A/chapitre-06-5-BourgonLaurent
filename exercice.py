#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Sequence


def check_brackets(text: str, brackets: Sequence[str]):
    opening_brackets = brackets[0::2]
    closing_brackets = brackets[1::2]
    get_close_from_open = dict(zip(opening_brackets, closing_brackets))

    queue = []
    for char in text:
        if char in opening_brackets:
            queue.append(get_close_from_open[char])
        elif char in closing_brackets:
            if not queue or char != queue.pop():
                return False

    return not queue


def remove_comments(full_text: str, comment_start: str, comment_end: str):
    end_comm_len = len(comment_end)
    while True:
        start_pos = full_text.find(comment_start)
        end_pos = full_text.find(comment_end)

        ## Check failures
        #
        #    If both failed: removed all comments
        if start_pos == -1 and end_pos == -1:
            return full_text
        #    One of them failed: incomplete comments
        # OR
        #    Wrong type of matching comments
        elif start_pos == -1 or end_pos == -1 or start_pos > end_pos:
            return None

        full_text = full_text[:start_pos] + full_text[end_pos + end_comm_len :]


def get_tag_prefix(text, opening_tags, closing_tags):
    return (None, None)


def check_tags(full_text, tag_names, comment_tags):
    return False


if __name__ == "__main__":
    brackets = ("(", ")", "{", "}")
    yeet = "(yeet){yeet}"
    yeeet = "({yeet})"
    yeeeet = "({yeet)}"
    yeeeeet = "(yeet"
    print(check_brackets(yeet, brackets))
    print(check_brackets(yeeet, brackets))
    print(check_brackets(yeeeet, brackets))
    print(check_brackets(yeeeeet, brackets))
    print()

    spam = "Hello, /* OOGAH BOOGAH */world!"
    eggs = "Hello, /* OOGAH BOOGAH world!"
    parrot = "Hello, OOGAH BOOGAH*/ world!"
    print(remove_comments(spam, "/*", "*/"))
    print(remove_comments(eggs, "/*", "*/"))
    print(remove_comments(parrot, "/*", "*/"))
    print()

    otags = ("<head>", "<body>", "<h1>")
    ctags = ("</head>", "</body>", "</h1>")
    print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("</h1></body>", otags, ctags))
    print(get_tag_prefix("</body>", otags, ctags))
    print()

    spam = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    </title>"
        "  </head>"
        "  <body>"
        "    <h1>Hello, world</h1>"
        "    <!-- Les tags vides sont ignorés -->"
        "    <br>"
        "    <h1/>"
        "  </body>"
        "</html>"
    )
    eggs = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    <!-- Il manque un end tag"
        "    </title>-->"
        "  </head>"
        "</html>"
    )
    parrot = (
        "<html>"
        "  <head>"
        "    <title>"
        "      Commentaire mal formé -->"
        "      Example"
        "    </title>"
        "  </head>"
        "</html>"
    )
    tags = ("html", "head", "title", "body", "h1")
    comment_tags = ("<!--", "-->")
    print(check_tags(spam, tags, comment_tags))
    print(check_tags(eggs, tags, comment_tags))
    print(check_tags(parrot, tags, comment_tags))
    print()
