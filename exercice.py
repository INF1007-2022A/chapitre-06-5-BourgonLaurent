#!/usr/bin/env python


from typing import Sequence


def check_brackets(text: str, brackets: Sequence[str]):
    opening_brackets = brackets[0::2]
    closing_brackets = brackets[1::2]
    get_close_from_open = dict(zip(opening_brackets, closing_brackets))

    stack = []
    for char in text:
        if char in opening_brackets:
            stack.append(get_close_from_open[char])
        elif char in closing_brackets:
            if not stack or char != stack.pop():
                return False

    return not stack


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


def get_tag_prefix(
    text: str,
    opening_tags: Sequence[str],
    closing_tags: Sequence[str],
) -> tuple[str | None, str | None]:
    for matching_tags in zip(opening_tags, closing_tags):
        if text.startswith(m := matching_tags[0]):
            return (m, None)
        elif text.startswith(m := matching_tags[1]):
            return (None, m)

    return (None, None)


def check_tags(
    full_text: str,
    tag_names: Sequence[str],
    comment_tags: Sequence[str],
) -> bool:
    text = remove_comments(full_text, *comment_tags)
    if not text:
        return False

    close_to_open_tags = {f"</{t}>": f"<{t}>" for t in tag_names}

    stack = []
    while text:
        tag = get_tag_prefix(text, close_to_open_tags.values(), close_to_open_tags)  # type: ignore
        if t := tag[0]:
            stack.append(t)
            text = text[len(t) :]
        elif t := tag[1]:
            if not stack or stack.pop() != close_to_open_tags[t]:
                return False

            text = text[len(t) :]
        else:
            text = text[1:]

    return not stack


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
