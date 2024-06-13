import sys, re
from .messages import msg

# max width (number of charaters) of an example (input or output)
def max_width(buffer):
    if re.search(r"verbatim", buffer[2]):
        return max(max(len(line) for line in buffer[3:-1]), 5)
    else:
        return max(max(len(line) for line in buffer[2:]), 5)

# total width of an example if its items (input and output) are placed
# horizontally, next to each other
# only first two itmes (input and output) are analyzed
def example_width_horizontal(example):
    no = 0
    width = 0
    for item in example:
        if isinstance(item, list):
            width += max_width(item) + 2
            no += 1
            if no == 2:
                break
    return width

# total width of an example if its items (input and output) are placed
# vertically, one below the other.
# only first two itmes (input and  ouptut) are analyzed
def example_width_vertical(example):
    rbr = 0
    max_w = 0
    for item in example:
        if isinstance(item, list):
            max_w = max(max_w, max_width(item))
            rbr += 1
            if rbr == 2:
                break
    return max_w

def print_example(example):
    global result, current_width, minipages

    MAX_WIDTH = 70

    # are items placed horizontally or vertically
    horizontally = True
    example_width = example_width_horizontal(example)
    if example_width > MAX_WIDTH:
        horizontally = False
        example_width = example_width_vertical(example)

    if current_width + example_width >= MAX_WIDTH:
        result += "\n\n"
        current_width = 0

    current_width += example_width

    if minipages and horizontally:
        result += "\\begin{minipage}[t]{%dpt}" % (5 * example_width + 30) + "\n"
    num = 0
    for item in example:
        if isinstance(item, list):
            width = max_width(item)
            if num < 2 and horizontally:
                result += "\\begin{minipage}[t]{%dpt}" % (5 * width + 20) + "\n"
            for line in item:
                result += line + "\n"
            if num < 2 and horizontally:
                result += "\\end{minipage}" + "\n"
            num += 1
            if num == 2:
                result += "\n\n"
        else:
            result += item + "\n"
    if minipages and horizontally:
        result += "\\end{minipage}" + "\n"

    
def fix_examples(tex):
    global result, current_width, minipages

    result = ""

    STATE_INITIAL = 0
    STATE_INPUT = 1
    STATE_OUTPUT = 2
    STATE_EXPLANATION = 3
    STATE_EXAMPLE = 4

    state = STATE_INITIAL

    line_no = 0
    while line_no < len(tex):
        line = tex[line_no].rstrip()
        line_no += 1
        if state == STATE_INITIAL:
            if re.match(r"\\textbf{" + msg("EXAMPLE") + r"(\s\d+)?}", line):
                state = STATE_EXAMPLE
                current_width = 0
                example = [line, "\n"]
                minipages = True
            else:
                result += line + "\n"
        elif state == STATE_EXAMPLE:
            if re.match(r"\\textbf{" + msg("EXAMPLE"), line):
                print_example(example)
                example = [line, "\n"]
            elif line == "\\emph{" + msg("INPUT") + "}":
                state = STATE_INPUT
                buffer = [line]
            elif line == "\\emph{" + msg("OUTPUT") + "}":
                state = STATE_OUTPUT
                buffer = [line]
            elif re.match(r"\\emph{" + msg("EXPLANATION") + r"}", line):
                minipages = False
                state = STATE_EXPLANATION
                buffer = [line]
            elif re.match(r"\\textbf{" + msg("SOLUTION") + r"}|\\hypertarget", line):
                print_example(example)
                state = STATE_INITIAL
                result += "\n"
                result += line + "\n"
        elif state == STATE_INPUT or state == STATE_OUTPUT:
            buffer.append(line)
            if line == "\\end{verbatim}":
                example.append(buffer)
                state = STATE_EXAMPLE
        elif state == STATE_EXPLANATION:
            if re.match(r"\\textbf{" + msg("SOLUTION") + r"}|\\hypertarget", line):
                example.append(buffer)
                print_example(example)
                state = STATE_INITIAL
                result += "\n"
                result += line + "\n"
            else:
                buffer.append(line)

def fix_latex(tex):
    global result
    fix_examples(tex)
    result = re.sub(r"\\addcontentsline", r"\\phantomsection\\addcontentsline", result)
    # avoid empty lines at the beginning and end of environments
    result = re.sub(r"\\begin{([^}]+)}\n+", r"\\begin{\1}\n", result)
    result = re.sub(r"\n+\\end",r"\n\\end", result)
    return result
                
if __name__ == "__main__":
    tex = sys.stdin.readlines()
    tex = fix_latex(tex)
    print(tex)
