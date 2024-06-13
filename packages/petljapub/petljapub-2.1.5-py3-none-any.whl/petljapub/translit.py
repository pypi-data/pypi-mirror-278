import sys, re, yaml

def translit(obj, translit_str_fun):
    if isinstance(obj, str):
        return translit_str_fun(obj)
    if isinstance(obj, dict):
        result = dict()
        for key, value in obj.items():
            result[translit(key, translit_str_fun)] = translit(value, translit_str_fun)
        return result
    if isinstance(obj, list):
        return map(lambda x: translit(x, translit_str_fun), obj)
    return obj

def translit_str(str, translit_letter_fun):
    return "".join(map(translit_letter_fun, str))

def cyr_to_lat(obj):
    def cyr_to_lat_letter(letter):
        f = {"а":"a", "б":"b",  "в":"v", "г":"g",  "д":"d",
             "ђ":"đ", "е":"e",  "ж":"ž", "з":"z",  "и":"i",
             "ј":"j", "к":"k",  "л":"l", "љ":"lj", "м":"m",
             "н":"n", "њ":"nj", "о":"o", "п":"p",  "р":"r",
             "с":"s", "т":"t",  "ћ":"ć", "у":"u",  "ф":"f",
             "х":"h", "ц":"c",  "ч":"č", "џ":"dž", "ш":"š",
             "А":"A", "Б":"B",  "В":"V", "Г":"G",  "Д":"D",
             "Ђ":"Đ", "Е":"E",  "Ж":"Ž", "З":"Z",  "И":"I",
             "Ј":"J", "К":"K",  "Л":"L", "Љ":"Lj", "М":"M",
             "Н":"N", "Њ":"Nj", "О":"O", "П":"P",  "Р":"R",
             "С":"S", "Т":"T",  "Ћ":"Ć", "У":"U",  "Ф":"F",
             "Х":"H", "Ц":"C",  "Ч":"Č", "Џ":"Dž", "Ш":"Š"}
        return f[letter] if letter in f else letter
    cyr_to_lat_str = lambda str: translit_str(str, cyr_to_lat_letter)
    return translit(obj, cyr_to_lat_str)

def lat_to_cyr(obj):
    f = {"a":"а", "b":"б",  "v":"в", "g":"г",  "d":"д",
         "đ":"ђ", "e":"е",  "ž":"ж", "z":"з",  "i":"и",
         "j":"ј", "k":"к",  "l":"л", "lj":"љ", "m":"м",
         "n":"н", "nj":"њ", "o":"о", "p":"п",  "r":"р",
         "s":"с", "t":"т",  "ć":"ћ", "u":"у",  "f":"ф",
         "h":"х", "c":"ц",  "č":"ч", "dž":"џ", "š":"ш",
         "A":"А", "B":"Б",  "V":"В", "G":"Г",  "D":"Д",
         "Đ":"Ђ", "E":"Е",  "Ž":"Ж", "Z":"З",  "I":"И",
         "J":"Ј", "K":"К",  "L":"Л", "Lj":"Љ", "M":"М",
         "N":"Н", "Nj":"Њ", "O":"О", "P":"П",  "R":"Р",
         "S":"С", "T":"Т",  "Ć":"Ћ", "U":"У",  "F":"Ф",
         "H":"Х", "C":"Ц",  "Č":"Ч", "Dž":"Џ", "Š":"Ш"}

    def lat_to_cyr_letter(letter):
        return f[letter] if letter in f else letter

    def lat_to_cyr_str(str):
        letters = []
        i = 0
        while i < len(str):
            letter = str[i]
            i += 1
            if i < len(str) and (letter + str[i]) in f:
                letter += str[i]
                i += 1
            letters.append(letter)
        return "".join(map(lat_to_cyr_letter, letters))

    return translit(obj, lat_to_cyr_str)


# split initial Metadata in Yaml format 
def parse_front_matter(text):
    # Taken from Jekyll
    # https://github.com/jekyll/jekyll/blob/3.5-stable/lib/jekyll/document.rb#L13
    YAML_FRONT_MATTER_REGEXP = r"\A---\s*\n(.*?)\n?^((---|\.\.\.)\s*$\n?)"

    match = re.search(YAML_FRONT_MATTER_REGEXP, text, re.DOTALL|re.MULTILINE)
    if not match:
        return text, {}
    
    try:
        header = yaml.safe_load(match.group(1))
        content = match.string[match.end():]
        return content, header
    except:
        return text, {}

def lat_to_cyr_in_brackets(text):
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, text)
    if match:
        return text.replace(match.group(1), lat_to_cyr_md(match.group(1)))
    else:
        return text

def lat_to_cyr_in_table(text):
    pattern = r'Table:([^\n]+)({[^}]+})?'
    match = re.search(pattern, text)
    if match:
        return text.replace(match.group(1), lat_to_cyr_md(match.group(1)))
    else:
        return text
    
def next_token(text):
    regexes = [("SPACES", re.compile(r"^\s+")),
               ("DISPLAY_MATH", re.compile(r"^\$\$[^\$]+\$\$")),
               ("INLINE_MATH", re.compile(r"^\$[^\$`~]+\$")),
               ("BEGIN_EQNARRAYSTAR", re.compile(r"^\\begin{eqnarray\*}")),
               ("END_EQNARRAYSTAR", re.compile(r"^\\end{eqnarray\*}")),
               ("BEGIN_ALIGNSTAR", re.compile(r"^\\begin{align\*}")),
               ("END_ALIGNSTAR", re.compile(r"^\\end{align\*}")),
               ("LAT", re.compile(r"\\latin{[^\n]*}")),
               ("NEWCOMMAND", re.compile(r"^\\(re)?newcommand[^\n]+")),
               ("PROVIDECOMMAND", re.compile(r"^\\providecommand[^\n]+")),
               ("LABEL", re.compile(r"^\\label{[^}]+}")),
               ("REF", re.compile(r"^\\ref{[^}]+}")),
               ("LATEX_COMMAND", re.compile(r"^\\\w+({([^\\{]|\\{)*})*")),
               ("VERB_LATEX", re.compile(r"^```{=latex}[^`]+```")),
               ("VERB_TILDE", re.compile(r"^~~~")),
               ("VERB_BACKTICKS", re.compile(r"^```")),
               ("INLINE_DOUBLE_VERB", re.compile(r"^``[^`]+``")),
               ("INLINE_VERB", re.compile(r"^`[^`]+`")),
               ("MAGIC_COMMENT", re.compile(r"^<!---\s*({})\s*:\s*({})([^\n]*)--->")),
               ("START_COMMENT", re.compile(r"^<!---")),
               ("END_COMMENT", re.compile(r"^--->")),
               ("URL", re.compile(r"^<[^>\n]+>")),
               ("REFERENCE", re.compile(r"^@[a-z]+:\S+")),
               ("ANCHOR", re.compile(r"^{(#[a-z]+:\S+)|([.]unnumbered)}")),
               ("LANG", re.compile("^\((eng|engl|hol|fr|it|nem|gr|češ)[.][^)]+\)")),
               ("IMAGE", re.compile(r"^!\[([^]\n]*)\]\(([-a-zA-Z_0-9./]*)\)({[^}]+})?")),
               ("TABLE", re.compile(r"^Table:[^\n]+({[^}]+})?")),
               ("WORD", re.compile(r"^(\w|[-+#])+")),
               ("OTHER", re.compile(r"^\S"))]
    for (token, regex) in regexes:
       match = regex.match(text)
       if match:
          return (token, match.group(), text[match.end():])      

LAT = set(["DISPLAY_MATH", "INLINE_MATH", "NEWCOMMAND", "PROVIDECOMMAND", "LABEL", "REF", "LATEX_COMMAND", "INLINE_VERB", "INLINE_DOUBLE_VERB", "LANG", "REFERENCE", "ANCHOR", "IMAGE", "TABLE", "MAGIC_COMMENT", "VERB_LATEX", "URL", "LAT"])
BRACKETS = {"VERB_TILDE": "VERB_TILDE",
            "VERB_BACKTICKS": "VERB_BACKTICKS",
            "START_COMMENT": "END_COMMENT",
            "BEGIN_EQNARRAYSTAR": "END_EQNARRAYSTAR",
            "BEGIN_ALIGNSTAR": "END_ALIGNSTAR"}
LAT_LEXEMES = set(["C++", "JAVA", "Java", "Python", "C#", "XOR", "point", "range", "update", "query", "reTRIEval", "encryption", "decryption", "BIT", "DFS", "BFS", "vertex", "edge", "MCST", "RSA", "FFT", "NTT", "ISBN", "IBAN", "CAS", "TLS", "PDF", "KMP", "DSU", "QuickSort", "MergeSort"])

def lat_to_cyr_md(text):
    result = []
    
    text, meta = parse_front_matter(text)
    if meta:
        result.append("---\n")
        for key, value in meta.items():
            result.extend([key, ": ", lat_to_cyr(value) if key == "title" else str(value), "\n"])
        result.append("---\n\n")

    open_bracket = ""
    while text:
        (token, lexeme, text) = next_token(text)
#        print(token, lexeme)
        if open_bracket:
            result.append(lexeme)
            if token == BRACKETS[open_bracket]:
                open_bracket = ""
        else:
            if token in LAT:
                if token == "LAT":
                    match = re.search(r"\\latin{(.*)}", lexeme)
                    result.append(match.group(1))
                elif token == "LANG":
                    match = re.search(r'\((\w+)\.', lexeme)
                    lang = match.group(1)
                    result.append(lexeme.replace(lang, lat_to_cyr(lang)))
                elif token == "IMAGE":
                    result.append(lat_to_cyr_in_brackets(lexeme))
                elif token == "TABLE":
                    result.append(lat_to_cyr_in_table(lexeme))
                elif token == "MAGIC_COMMENT" or token == "VERB_LATEX":
                    result.append(lat_to_cyr_in_brackets(lexeme))
                else:
                    result.append(lexeme)
            elif token in BRACKETS:
                result.append(lexeme)
                open_bracket = token
            else:
                if lexeme in LAT_LEXEMES:
                    result.append(lexeme)
                else:
                    result.append(lat_to_cyr(lexeme))

    return "".join(result)
