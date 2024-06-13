import re
import sys
import os, glob, shutil
import tempfile
import time
import statistics
import yaml
import json

from enum import Enum

from .md_util import parse_front_matter
from . import md_util
from .messages import msg
from .util import read_file, write_to_file, dump_file
from .compilation import compile_c, compile_cpp, compile_cs, run_py, run_exe
from .default_checker import compare_files
from petljapub.serialization import ZipWriter

from . import logger

base_dir = os.path.dirname(os.path.abspath(__file__))

# Parse the problem statement and extract it's important parts
#   - problem description
#   - input format description
#   - output format description
#   - examples (example input, example output, example description)

class StParser:
    class State(Enum):
        STATEMENT = 1
        INPUT = 2
        OUTPUT = 3
        EXAMPLE = 4
        EXAMPLE_INPUT = 5
        EXAMPLE_OUTPUT = 6
        EXAMPLE_EXPLANATION = 7
    
    def __init__(self, st):
        self._st = st
        self._state = StParser.State.STATEMENT
        self._statement = ""
        self._input_description = ""
        self._output_description = ""
        self._examples = []
        self.parse()

    def new_example(self):
        self._examples.append({"input": "", "output": "", "explanation": ""})

    def parse(self):
        text = {StParser.State.INPUT: md_util.heading(msg("INPUT"), 2),
                StParser.State.OUTPUT: md_util.heading(msg("OUTPUT"), 2),
                StParser.State.EXAMPLE: md_util.heading(msg("EXAMPLE"), 2),
                StParser.State.EXAMPLE_INPUT: md_util.heading(msg("INPUT"), 3),
                StParser.State.EXAMPLE_OUTPUT: md_util.heading(msg("OUTPUT"), 3),
                StParser.State.EXAMPLE_EXPLANATION: md_util.heading(msg("EXPLANATION"), 3)
        }

        self._state = StParser.State.STATEMENT
        
        for line in self._st.split("\n"):
            if self._state == StParser.State.STATEMENT:
                if line.startswith(text[StParser.State.INPUT]):
                    self._state = StParser.State.INPUT
                else:
                    self._statement += line + "\n"
            elif self._state == StParser.State.INPUT:
                if line.startswith(text[StParser.State.OUTPUT]):
                    self._state = StParser.State.OUTPUT
                else:
                    self._input_description += line + "\n"
            elif self._state == StParser.State.OUTPUT:
                if line.startswith(text[StParser.State.EXAMPLE]):
                    self._state = StParser.State.EXAMPLE
                    self.new_example()
                else:
                    self._output_description += line + "\n"
            elif self._state == StParser.State.EXAMPLE:
                if line.startswith(text[StParser.State.EXAMPLE_INPUT]):
                    self._state = StParser.State.EXAMPLE_INPUT
            elif self._state == StParser.State.EXAMPLE_INPUT:
                if line.startswith(text[StParser.State.EXAMPLE_OUTPUT]):
                    self._state = StParser.State.EXAMPLE_OUTPUT
                else:
                    self._examples[-1]["input"] += line + "\n"
            elif self._state == StParser.State.EXAMPLE_OUTPUT:
                if line.startswith(text[StParser.State.EXAMPLE_EXPLANATION]):
                    self._state = StParser.State.EXAMPLE_EXPLANATION
                elif line.startswith(text[StParser.State.EXAMPLE]):
                    self._state = StParser.State.EXAMPLE
                    self.new_example()
                else:
                    self._examples[-1]["output"] += line + "\n"
            elif self._state == StParser.State.EXAMPLE_EXPLANATION:
                if line.startswith(text[StParser.State.EXAMPLE]):
                    self._state = StParser.State.EXAMPLE
                    self.new_example()
                else:
                    self._examples[-1]["explanation"] += line + "\n"
                

    def statement(self):
        return self._statement.strip()

    def input_description(self):
        return self._input_description.strip()

    def output_description(self):
        return self._output_description.strip()

    def examples(self, strip_md_verbatim):
        verb_str = "~~~"

        def strip_newline(str):
            str = re.sub(r"^[ \t]*\n", "", str, count=1)
            str = re.sub(r"\n[ \t]*$", "", str, count=1)
            return str
        
        def split_output_and_explanation(output):
            (_, output, explanation) = output.split(verb_str, 2)
            output = verb_str + output + verb_str
            explanation = explanation.strip()
            return (output, explanation)

        for i in range(len(self._examples)):
            self._examples[i]["input"] = self._examples[i]["input"].strip()
            (output, explanation) = split_output_and_explanation(self._examples[i]["output"])
            self._examples[i]["output"] = output
            if explanation != "":
                self._examples[i]["explanation"] = explanation + "\n" + self._examples[i]["explanation"]

            if strip_md_verbatim:
                self._examples[i]["input"] = strip_newline(self._examples[i]["input"].strip(verb_str))
                self._examples[i]["output"] = strip_newline(self._examples[i]["output"].strip(verb_str))

        return self._examples
    
class Task:
    def __init__(self, task_dir, normalize_md = lambda x: x, translit = lambda x: x):
        self._task_dir = task_dir
        self._task_id = Task.extract_id_from_dir(task_dir)
        self._normalize_md = normalize_md
        self._translit = translit

    # alias for task on petlja
    # takes the task id and removes everything that 
    # isn't a word character, a dash or an underscore 
    # and makes everything lowercase to comply with
    # the petlja problem alias format
    def task_alias(self):
        return re.sub(r"[^a-z0-9]", "", self.id()).lower()
    
    # competition directory of the task
    # returns parent directory name
    # or None if parent directory isn't
    # a legal petljapub dir name
    def competition_dir(self):
        comp_dir = os.path.dirname(self._task_dir)
        if not Task.is_task_dir(os.path.basename(comp_dir)):
            return None
        return comp_dir

    # full path of the directory of the task
    def dir(self):
        return self._task_dir

    # last modification of some source file of the task
    def modification_time(self):
        return max(os.path.getmtime(file) for file in glob.glob(os.path.join(self.dir(), '*')))

    # check if the given dir is a legal task dir name (it must start
    # with two digits, followed by a space, dash or an underscore)
    @staticmethod
    def is_task_dir(dir):
        return re.match(r"\d{2}[_ -].+", dir)
         
    # extract id of the task from its directory name (remove two leading digits)
    # e.g. 01 task_id -> task_id
    @staticmethod
    def extract_id_from_dir(dir):
        return re.sub(r'^\d{2}[a-z]?[ _-]', '', os.path.basename(dir)).rstrip(os.path.sep)

    # id of the task
    def id(self):
        return self._task_id
        
    # title of the task
    def title(self):
        title = self.metadatum('title')
        return title

    # status of the task
    def status(self):
        return self.metadatum('status')

    def is_complete(self):
        return self.status() == "KOMPLETAN"

    # timelimit (in seconds) set in the metadata
    def timelimit(self):
        return float(self.metadatum('timelimit'))

    # list of solutions (and their descriptions) of the task
    def solutions(self):
        sols = self.metadatum('solutions')
        if not sols:
            sols = []
        return sols

    # description for the given solution
    def solution(self, sol_name):
        for sol in self.solutions():
            if sol["name"] == sol_name:
                return sol
        return None

    # expected status for the given solution
    def expected_status(self, sol_name):
        solutions = self.solutions()
        for sol in solutions:
            if sol["name"] == sol_name:
                if "expected-status" in sol:
                    return sol["expected-status"]
                else:
                    return "OK"
        return "OK"

    # available languages
    def langs(self):
        solutions = self.solutions();
        result = set()
        for sol in solutions:
            for lang in sol["lang"]:
                result.add(lang)
        return list(result)
    
    # raw text of the statement of the task
    def st_content(self):
        # parse -st.md file
        st, metadata = parse_front_matter(self.st_path())
        # apply normalizations
        st = self._normalize_md(st)
        st = self._translit(st)
        return st

    # text of the task description (without input and output)
    def statement(self):
        parser = StParser(self.st_content())
        return parser.statement()

    # text of the input format description
    def input_description(self):
        parser = StParser(self.st_content())
        return parser.input_description()

    # text of the output format description
    def output_description(self):
        parser = StParser(self.st_content())
        return parser.output_description()

    # examples of input and output
    def examples(self, strip_md_verbatim=False):
        parser = StParser(self.st_content())
        return parser.examples(strip_md_verbatim)

    # complete IO specification (description + examples)
    def io(self):
        return self.io_description() + self.io_examples()
        
    # IO description
    def io_description(self):
        md = ""
        md += md_util.heading(msg("INPUT_DESC"), 2) + "\n\n" + self.input_description() + "\n\n"
        md += md_util.heading(msg("OUTPUT_DESC"), 2) + "\n\n" + self.output_description() + "\n\n"
        return md

    # IO examples
    def io_examples(self):
        md = ""
        examples = self.examples()
        for i, example in enumerate(examples):
            example_num = " " + str(i+1) if len(examples) > 1 else ""
            md += md_util.heading(msg("EXAMPLE"), 2) + example_num + "\n\n"
            md += md_util.heading(msg("INPUT"), 3) + "\n\n" + example["input"] + "\n\n"
            md += md_util.heading(msg("OUTPUT"), 3) + "\n\n" +example["output"] + "\n\n"
            if example["explanation"]:
                md += md_util.heading(msg("EXPLANATION"), 3) + "\n\n" + example["explanation"] + "\n\n"
        return md
    
    # raw content of the solution descriptions of the task
    def sol_content(self):
        # parse sol-md file
        sol, metadata = parse_front_matter(self.sol_path())

        # warn if raw links are present
        m = re.search(r'(?<![!])\[[^]()]+\]\([^)]+\)', sol, re.MULTILINE)
        if m:
            logger.error("raw link", m.group(0).replace("\n", " "), "in", self.id())
        
        # apply normalizations
        sol = self._normalize_md(sol)
        sol = self._translit(sol)
        return sol

    # raw source code for the given solution ("ex0", "ex1", ...)  in
    # the given language ("cs", "cpp", "py", ...) 
    def src_code(self, sol_id, lang):
        src_file = self.src_file_path(sol_id, lang)
        code = read_file(src_file)
        if code is None:
            logger.error("Error reading code", src_file)
            return None
        # convert tabs to spaces
        code = code.replace('\t', ' '*8)
        return code.rstrip()

    # the list all generated testcases paths
    def generated_testcases(self):
        testcases = os.path.join(self.generated_testcases_dir() , "*.in")
        return sorted(glob.glob(testcases))

    # return the number of generated testcases
    def number_of_generated_testcases(self):
        return len(self.generated_testcases())

    # the list all example testcases paths
    def example_testcases(self):
        testcases = os.path.join(self.example_testcases_dir() , "*.in")
        return sorted(glob.glob(testcases))
    
    # return the number of example testcases
    def number_of_example_testcases(self):
        return len(self.example_testcases())

    # the list all crafted testcases paths
    def crafted_testcases(self):
        testcases = os.path.join(self.crafted_testcases_dir() , "*.in")
        return sorted(glob.glob(testcases))
    
    # return the number of crafted testcases
    def number_of_crafted_testcases(self):
        return len(self.crafted_testcases())

    # the list of all testcase paths
    def all_testcases(self):
        return self.example_testcases() + self.generated_testcases() + self.crafted_testcases()
    

    # generate yaml description of testcases
    def scoring_yaml(self, subtask=False):
        ex = self.number_of_example_testcases()
        gen = self.number_of_generated_testcases()
        cft = self.number_of_crafted_testcases()

        if not subtask:
            scores = []
            for i in range(1, ex + 1):
                scores.append({'name': i, 'score': 0})
            for i in range(ex + 1, ex + gen + cft + 1):
                scores.append({'name': i, 'score': 1})
            
            data = {'type': 'testcase',
                    'score_total': gen + cft,
                    'score_overrides': scores,
                    'public': list(range(1, ex+1))}
        else:
            groups = []
            for i in range(1, ex + 1):
                groups.append({'id': i, 'score': 0, 'testcases': [i]})
            groups.append({'id': ex + 1, 'score': gen + cft, 'testcases': list(range(ex+1, ex+gen+cft+1))})
            data = {'type': 'subtask',
                    'score_total': gen + cft,
                    'groups': groups,
                    'public': list(range(1, ex+1))}

        # ensure that the build dir exists
        build_dir = self.build_dir()
        if not os.path.isdir(build_dir):
            try:
                os.makedirs(build_dir)
            except:
                logger.error("Could not create build directory", build_dir)
            
        file = os.path.join(build_dir, "scoring.yaml")
        
        write_to_file(file,
                      yaml.dump(data, sort_keys = False, default_flow_style=None))
        logger.info(file, "successfully generated")
    
    # check if there is a custom checker for the task
    def has_checker(self):
        return os.path.isfile(self.checker_src_path())
    
    # full metadata
    def metadata(self):
        # read the metadata from the -st.md file
        stmd_file = self.st_path()
        text, metadata = parse_front_matter(stmd_file)
        return metadata

    # a single entry from the metadata
    def metadatum(self, key):
        # read all metadata
        metadata = self.metadata()
        # get the entry for the specified key
        if key in metadata:
            data = metadata[key]
            data  = self._translit(data)
            return data
        return None


    ####################################################################
    # Paths and file names
    
    # full path of the -st.md file
    def st_path(self):
        return os.path.join(self.dir(), self.id() + "-st.md")
        
    # full path of the -sol.md file
    def sol_path(self):
        return os.path.join(self.dir(), self.id() + "-sol.md")

    # name of the source file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def src_file_name(self, sol_id, lang):
        suffix = "" if sol_id == "ex0" else "-" + sol_id
        return self.id() + suffix + "." + lang
    
    # full path of the source file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def src_file_path(self, sol_id, lang):
        return os.path.join(self.dir(), self.src_file_name(sol_id, lang))

    # name of the build directory
    @staticmethod
    def build_dir_name():
        return "_build"

    # full path of the build directory (where exe and testcases are stored)
    def build_dir(self):
        return os.path.join(self.dir(), Task.build_dir_name())
    
    def clear_build_dir(self):
        if os.path.isdir(self.build_dir()):
            try:
                shutil.rmtree(self.build_dir_name())
            except:
                logger.error("Error removing directory", Task.build_dir_name())

    # name of the executable file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def exe_file_name(self, sol, lang):
        lang_ = "-" + lang if lang != "cpp" else ""
        sol_name = "-" + sol if sol != "ex0" else ""
        if lang == "py":
            return self.id() + sol_name + ".py"
        return self.id() + sol_name + lang_ + ".exe"
    
    # full path of the executable file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def exe_file_path(self, sol, lang):
        return os.path.join(self.build_dir(), self.exe_file_name(sol, lang))

    # name of the test generator source file
    def tgen_src_file_name(self):
        return self.id() + "-tgen.cpp"

    # name of the test generator executable file (in the build directory)
    def tgen_exe_file_name(self):
        return self.id() + "-tgen.exe"

    # full path for the test generator source file
    def tgen_src_path(self):
        return os.path.join(self.dir(), self.tgen_src_file_name())

    # full path for the test generator exe file (in the build directory)
    def tgen_exe_path(self):
        return os.path.join(self.build_dir(), self.tgen_exe_file_name())

    # directories where testcases are stored
    @staticmethod
    def testcases_dir_name():
        return "testcases"

    @staticmethod
    def generated_testcases_dir_name():
        return os.path.join(Task.testcases_dir_name(), "generated")

    @staticmethod
    def example_testcases_dir_name():
        return os.path.join(Task.testcases_dir_name(), "example")

    @staticmethod
    def crafted_testcases_dir_name():
        return os.path.join(Task.testcases_dir_name(), "crafted")

    # full path of the root directory where all testcases are stored
    def testcases_dir(self):
        return os.path.join(self.build_dir(), Task.testcases_dir_name())
    
    def zipped_testcases_dir(self):
        return os.path.join(self.build_dir(), "testcases.zip")
    
    # full path of the directory where generated testcases are stored
    def generated_testcases_dir(self):
        return os.path.join(self.build_dir(), Task.generated_testcases_dir_name())

    # full path of the directory where example testcases are stored
    def example_testcases_dir(self):
        return os.path.join(self.build_dir(), Task.example_testcases_dir_name())

    # full path of the directory where crafted testcases are stored
    def crafted_testcases_dir(self):
        return os.path.join(self.build_dir(), Task.crafted_testcases_dir_name())
    
    # full path of a generated testcase with a given number
    def generated_testcase_path(self, i):
        in_file = self.id() + "_" + str(i).zfill(2) + ".in"
        return os.path.join(self.generated_testcases_dir(), in_file)

    # full path of an example testcase with a given number
    def example_testcase_path(self, i):
        in_file = self.id() + "_" + str(i).zfill(2) + ".in"
        return os.path.join(self.example_testcases_dir(), in_file)

    # full path of a crafted testcase with a given number
    def crafted_testcase_path(self, i):
        in_file = self.id() + "_" + str(i).zfill(2) + ".in"
        return os.path.join(self.crafted_testcases_dir(), in_file)

    # full path of a testcase (first param is "example", "crafted", or "generated")
    def testcase_path(self, testcase_type, testcase_no):
        if testcase_type[0].lower()  == "e":
            return self.example_testcase_path(testcase_no)
        if testcase_type[0].lower() == "c":
            return self.crafted_testcase_path(testcase_no)
        if testcase_type[0].lower() == "g":
            return self.generated_testcase_path(testcase_no)
        return ""

    # testing output dir
    def test_output_dir(self):
        return os.path.join(self.build_dir(), "output")

    # output dir for example testcases
    def example_test_output_dir(self):
        return os.path.join(self.test_output_dir(), "example")

    # output dir for generated testcases
    def generated_test_output_dir(self):
        return os.path.join(self.test_output_dir(), "generated")

    # output dir for crafted testcases
    def crafted_test_output_dir(self):
        return os.path.join(self.test_output_dir(), "crafted")
    
    # name of the source file with the custom checker
    def checker_src_file_name(self):
        return self.id() + "-check.cpp"

    # name of the executable file of the custom checker
    def checker_exe_file_name(self):
        return self.id() + "-check.exe"
    
    # full path of the source file with the custom checker
    def checker_src_path(self):
        return os.path.join(self.dir(), self.checker_src_file_name())

    # full path of the executable file of the custom checker
    def checker_exe_path(self):
        return os.path.join(self.build_dir(), self.checker_exe_file_name())

    # default checker exe file path
    def default_checker_exe_path(self):
        return os.path.join(base_dir, "DefaultChecker.exe")
    

    ####################################################################
    # Compiling and running

    # compile source code for the given solution ("ex0", "ex1", ...)
    # in the given language ("cs", "cpp", "py", ...) 
    def compile(self, sol, lang, force = True):
        if lang == "py":
            return True
        
        # full paths of the source and resulting exe file
        src_file = self.src_file_path(sol, lang)
        exe_file = self.exe_file_path(sol, lang)

        # report error if source file does not exist
        if not os.path.isfile(src_file):
            logger.error("input file", src_file, "does not exist")
            return False
        
        # ensure that the build dir exists
        build_dir = self.build_dir()
        if not os.path.isdir(build_dir):
            try:
                os.makedirs(build_dir)
            except:
                logger.error("Could not create build directory", build_dir)
                return
                
        # if exe file exists and compilation is not forced, we are done
        if os.path.isfile(exe_file) and not force:
            return True

        logger.info("Compiling:", os.path.basename(src_file))
        
        # call the compiler for the given programming language
        if lang == "cpp":
            if not compile_cpp(src_file, exe_file):
                return False
        elif lang == "cs":
            if not compile_cs(src_file, exe_file):
                return False
        elif lang == "c":
            if not compile_c(src_file, exe_file):
                return False
        else:
            logger.error("compilation not supported for language", lang)
            return False
        return True

    def clear_testcases(self):
        dir = os.path.abspath(self.testcases_dir())
        try:
            if os.path.isdir(dir):
                shutil.rmtree(dir)
        except:
            logger.warn("Could not remove testcases directory", dir)
    
    # extract testcases from examples on the problem statement
    def extract_example_testcases(self):
        logger.info("Extracting testcases from given examples:", self.id())
        # ensure that the directory for storing test cases exists
        examples_dir = self.example_testcases_dir()
        if not os.path.isdir(examples_dir):
            try:
                os.makedirs(examples_dir)
            except:
                logger.error("Could not create example testcases directory", examples_dir)
        # process all examples given in the problem statement
        examples = self.examples(strip_md_verbatim=True)
        for i, example in enumerate(examples):
            try:
                logger.info("Extracting example testcase", i)
                # extract input file
                input = self.example_testcase_path(i+1)
                write_to_file(input, example["input"])
                output = input[:-2]+"out"
                write_to_file(output, example["output"])
            except:
                logger.error("Error extracting example testcase", i)
        n = self.number_of_example_testcases()
        logger.info("Extracted {} example{}".format(n, "" if n == 1 else "s"))
                
    
    # generate testcases for the task with the given ID
    def generate_testcases(self):
        logger.info("Generating tests:", self.id())
        
        # compile the test generator
        tgen_src = self.tgen_src_path()
        tgen_exe = self.tgen_exe_path()

        if not os.path.exists(tgen_src):
            logger.warn(tgen_src + " does not exist - generating testcases skipped")
            return

        with open(tgen_src) as tgen:
            content = tgen.read()
            if re.search(r"void gen_test\([^)]*\)\s*{\s*}", content):
                logger.warn(tgen_src + " - gen_test function is empty - generating testcases skipped")
                return
            
        if not compile_cpp(tgen_src, tgen_exe):
            logger.error("compiling test generator failed")
            return False

        # compile the main solution used to generate outputs
        if not self.compile("ex0", "cpp", force=True):
            logger.error("compiling main solution failed")
            return False

        # ensure that the directory for storing generated test cases exists
        generated_dir = self.generated_testcases_dir()
        if os.path.isdir(generated_dir):
            try:
                shutil.rmtree(generated_dir)
            except:
                logger.error("Could not remove ", generated_dir)
                
        try:
            os.makedirs(generated_dir)
        except:
            logger.error("Could not create generated test cases directory", generated_dir)
            return
        # run the test generator
        logger.info("Generating test inputs - running test generator:", os.path.relpath(tgen_exe, self.dir()))
        exe_file = os.path.abspath(tgen_exe)
        args = [self.id(), Task.generated_testcases_dir_name()]
        if logger.verbosity() > 3:
            args.append("True")
        status, p = run_exe(exe_file, args=args, cwd=self.build_dir())
        if status == "RTE":
            logger.error("RTE while generating testcases")
            return False

        exe_file = self.exe_file_path("ex0", "cpp")
        logger.info("Generating test outputs - running default cpp solution:", os.path.relpath(exe_file, self.dir()))
        for testcase_num, input in enumerate(self.generated_testcases()):
            try:
                in_file = open(input)
                output = input[:-2] + "out"
                out_file = open(output, "w")
                logger.info("generating", os.path.relpath(output, self.dir()), "using", os.path.relpath(exe_file, self.dir()), verbosity=4)
                status, p = run_exe(exe_file, in_file=in_file, out_file=out_file)
            except:
                    logger.error("error generating output", output)

        logger.info("Generated", self.number_of_generated_testcases(), "testcases")
        return True

    
    # copy crafted testcases to testcases dir and generate expected output using default cpp solution, when
    # the default output files are not provided
    def prepare_crafted_testcases(self, crafted_dir):
        logger.info("Preparing crafted tests:", self.id())

        # check if valid directory is supplied
        if not os.path.isdir(crafted_dir):
            logger.error(crafted_dir, "is not a valid directory")
        
        # compile the main solution used to generate outputs
        if not self.compile("ex0", "cpp", force=False):
            logger.error("compiling main solution failed")
            return False
        
        # ensure that the target directory for storing crafted test cases exists
        target_dir = self.crafted_testcases_dir()
        if not os.path.isdir(target_dir):
            try:
                os.makedirs(target_dir)
            except:
                logger.error("Could not create crafted testcases directory", target_dir)

        # process every testcase found in the supplied crafted_dir
        i = 0
        for input in glob.glob(os.path.join(self.dir(), crafted_dir, "*.in")):
            i += 1
            logger.info("copying", input, verbosity=4)
            target_input = self.crafted_testcase_path(i)
            target_output = self.crafted_testcase_path(i)[:-2] + "out"
            
            try:
                shutil.copy(input, target_input)
            except:
                logger.error("error copying", input)
                continue

            # copy output file if it exists in the crafted_dir
            output = input[:-2] + "out"
            if os.path.isfile(output):
                logger.info("copying", output, verbosity=4)
                try:
                    shutil.copy(output, target_output)
                except:
                    logger.error("error copying", output)
                    continue
            else:
            # generate output file
                exe_file = self.exe_file_path("ex0", "cpp")
                logger.info("generating", os.path.relpath(output, self.dir()), "using", os.path.relpath(exe_file, self.dir()), verbosity=4)
                try:
                    in_file = open(input)
                    out_file = open(target_output, "w")
                    status, p = run_exe(exe_file, in_file=in_file, out_file=out_file)
                except:
                    logger.error("error generating output", target_output)

    def tests_zip(self, crafted_dir=None):
        self.clear_build_dir()
        
        self.extract_example_testcases()
        self.generate_testcases()
        if crafted_dir:
            self.prepare_crafted_testcases(crafted_dir)
        
        zip_file = os.path.join(self.build_dir(), "testcases.zip")
        writer = ZipWriter(zip_file)
        writer.open()

        i = 1
        for testcase_in in (self.example_testcases() + self.crafted_testcases() + self.generated_testcases()):
            logger.info(testcase_in)
            writer.copy_file(testcase_in, "{:02d}.in".format(i))
            testcase_out = testcase_in[0:-2] + "out"
            logger.info(testcase_out)
            writer.copy_file(testcase_out, "{:02d}.out".format(i))
            i += 1
        writer.close()
        logger.info("Testcases stored in", zip_file)
                
    # compile custom checker
    def compile_checker(self, force=True):
        # check if the checker exists
        if not self.has_checker():
            logger.error("no custom checker for", self.id())
            return False
        src = self.checker_src_path()
        exe = self.checker_exe_path()
        # skip compilation if it is not forced and exe file already exists
        if not force and os.path.isfile(exe):
            return True
        logger.info("Compiling checker:", os.path.basename(src))
        # compile the checker
        if not compile_cpp(src, exe):
            logger.error("compiling checker")
            return False
        return True
    
    # run a given exe file on a given testcase with a given timeout (in second)
    # testcase can be either a full path or a generated test-case number 
    def run(self, sol, lang, testcase, timeout=1.0, output=None):
        if timeout != None and type(timeout) != "float":
            timeout = float(timeout)
        
        # open in_file
        if isinstance(testcase, int):
            testcase = self.generated_testcase_path(testcase)
        if not os.path.isfile(testcase):
            logger.error("Testcase", testcase, "does not exist")
            return "RTE"
        in_file = open(testcase)

        # open out_file
        if output == None:
            out_file = tempfile.TemporaryFile()
        elif output != "stdout":
            try:
                out_file = open(output, "w")
            except:
                logger.error("Output file", output, "could not be created")
                return "RTE"
        else:
            out_file = sys.stdout

        # compile if necessary
        if not self.compile(sol, lang, False):
            return "CE"

        # run exe or interpret python
        if lang == "py":
            status, p = run_py(self.src_file_path(sol, lang), in_file=in_file, out_file=out_file, timeout=timeout)
        else:
            exe_file = self.exe_file_path(sol, lang)
            status, p = run_exe(exe_file, in_file=in_file, out_file=out_file, timeout=timeout)

        # close files
        in_file.close()
        if output != "stdout":
            out_file.close()

        # return execution status
        return status


    # run a given exe file interactively (reading from stdin and writing to stdout)
    def run_interactive(self, sol, lang):
        if not self.compile(sol, lang, False):
            return "CE"

        if lang == "py":
            return run_py(self.src_file_path(sol, lang), sys.stdin, sys.stdout)
        else:
            exe_file = self.exe_file_path(sol, lang)
            status, p = run_exe(exe_file, in_file=sys.stdin, out_file=sys.stdout)
            return status

    # Testing correctness of solutions
    
    # check the correctness of a given solution on the given testcase
    def test_on_testcase(self, sol, lang, input, expected_output, timeout=None, save_output_dir=None):
        logger.info("testing testcase", os.path.basename(input), verbosity=4)
        # compares expected and obtained output using a custom checker
        # for a given task
        def custom_checker_compare(output, expected_output, input):
            exe_file = self.checker_exe_path()
            args = [output, expected_output, input]
            status, p = run_exe(exe_file, args=args, check=False)
            return status == "OK" and p.returncode == 0

        # compares expected and obtained output using the default checker
        def default_checker_compare(output, expected_output, input):
            # if a compiled default checker exists, it is used
            if os.path.exists(self.default_checker_exe_path()):
                exe_file = self.default_checker_exe_path()
                args = [expected_output, output, input]
                status, p = run_exe(exe_file, args=args, check=False)
                return status == "OK" and p.returncode == 0
            # otherwise the python implementation is used (default_checker)
            return compare_files(expected_output, output)

        # test_01.in -> 01
        num = input[-5:-3] if re.search(r"\d{2}[.]in$", input) else ""
        
        # _build/tmp01.out
        user_output = os.path.join(self.build_dir(),
                                   "tmp" + num + ".out")

        # run solution skipping check if execution was terminated
        # due to timeout
        start_time = time.time()
        if timeout == None:
            timeout = self.timelimit()
        status = self.run(sol, lang, input, timeout, user_output)
        ellapsed_time = time.time() - start_time
        

        # if program was executed successfully
        if status == "OK":
            # check correctness of the output
            if self.has_checker():
                OK = custom_checker_compare(user_output, expected_output, input)
            else:
                OK = default_checker_compare(user_output, expected_output, input)

            # report error
            if not OK:
                status = "WA"
                # log error details
                logger.warn("WA", os.path.basename(self.exe_file_path(sol, lang)), os.path.basename(input), verbosity=3)
                if logger.verbosity() >= 5:
                    logger.info("Program output:", user_output, verbosity=4)
                    dump_file(user_output)
                    logger.info("..............................", verbosity=4)
                    logger.info("Expected output:", expected_output, verbosity=4)
                    dump_file(expected_output)
                    logger.info("..............................", verbosity=4)


        # remove temporary file with the user output
        if os.path.isfile(user_output):
            if save_output_dir == None:
                try:
                    os.remove(user_output)
                except:
                    logger.warn("Could not remove user output file", user_output)
            else:
                save_output_path = os.path.join(save_output_dir, os.path.basename(expected_output))
                logger.info("Saving output", os.path.relpath(save_output_path, os.getcwd()))
                try:
                    os.makedirs(os.path.dirname(save_output_path), exist_ok=True)
                    shutil.copy(user_output, save_output_path)
                except:
                    logger.warn("Could not save output file", save_output_path)    

        return status, ellapsed_time

    # test correctness of a given solution on all generated testcases
    def test_on_generated_testcases(self, sol, lang, timeout=None, force_recompile=False, reporter=None, save_outputs=False):
        logger.info("Testing on generated testcases")
        # ensure that generated testcases exist
        if self.number_of_generated_testcases() == 0:
            self.generate_testcases()

        save_outputs_dir = self.generated_test_output_dir() if save_outputs else None
        return self.test_on_given_testcases(sol, lang, self.generated_testcases(), timeout=timeout, force_recompile=force_recompile, reporter=reporter, save_outputs_dir=save_outputs_dir)

    # test correctness of a given solution on all example testcases
    def test_on_example_testcases(self, sol, lang, force_recompile=False, reporter=None, save_outputs=False):
        logger.info("Testing on example testcases")
        # ensure that all example testcases are extracted
        if self.number_of_example_testcases() == 0:
            self.extract_example_testcases()
            
        save_outputs_dir = self.example_test_output_dir() if save_outputs else None
        return self.test_on_given_testcases(sol, lang, self.example_testcases(), force_recompile=force_recompile, reporter=reporter, warn_status=False, warn_not_OK=True, save_outputs_dir=save_outputs_dir)

    # test correctness of a given solution on all crafted testcases
    def test_on_crafted_testcases(self, sol, lang, timeout=None, force_recompile=False, reporter=None, save_outputs=False):
        if self.number_of_crafted_testcases() > 0:
            logger.info("Testing on crafted testcases")
            save_outputs_dir = self.crafted_test_output_dir() if save_outputs else None
            return self.test_on_given_testcases(sol, lang, self.crafted_testcases(), timeout=timeout, force_recompile=force_recompile, reporter=reporter, save_outputs_dir=save_outputs_dir)
        return None
    

    # check correctness of a given solution on all testcases (example and generated)
    def test_on_all_testcases(self, sol, lang, timeout=None, force_recompile=False, reporter=None, save_outputs=False):
        if not force_recompile and reporter and not reporter.should_test(sol, lang):
            return None
        
        # compile solution
        if not self.compile(sol, lang, force_recompile):
            logger.error("Compilation failed for", sol, lang)
            return None
        
        if not self.test_on_example_testcases(sol, lang, force_recompile=False, reporter=reporter, save_outputs=save_outputs):
            return False
        if not self.test_on_generated_testcases(sol, lang, timeout=timeout, force_recompile=False, reporter=reporter, save_outputs=save_outputs):
            return False
        if not self.test_on_crafted_testcases(sol, lang, timeout=timeout, force_recompile=False, reporter=reporter, save_outputs=save_outputs):
            return False
        return True
    
    # test correctness of a given solution on all testcases
    def test_on_given_testcases(self, sol, lang, testcases, timeout=None, force_recompile=False, reporter=None, warn_status=True, warn_not_OK=False, save_outputs_dir=None):
        if not force_recompile and reporter and not reporter.should_test(sol, lang):
            return None

        # compile solution
        if not self.compile(sol, lang, force_recompile):
            logger.error("Compilation failed for", sol, lang)
            return None

        # compile custom checker if it exists
        if self.has_checker():
            if not self.compile_checker(force_recompile):
                return None

        logger.info("Running:", self.exe_file_name(sol, lang))

        # count testcase statuses
        statuses = {"OK": 0, "WA": 0, "TLE": 0, "RTE": 0}

        # check every testcase
        max_time = 0
        for input in testcases:
            expected_output = input[:-2] + "out" # test_01.in -> test_01.out

            # run test and measure ellapsed time            
            result, ellapsed_time = self.test_on_testcase(sol, lang, input, expected_output, timeout, save_output_dir=save_outputs_dir)
            max_time = max(max_time, ellapsed_time)

            if reporter:
                reporter.report_testcase(sol, lang, os.path.basename(input), result, ellapsed_time)
            
            if result == "RTE":
                logger.warn(self.id(), sol, lang, "runtime error while executing program")
            
            statuses[result] += 1;
                
        logger.info(statuses)
        logger.info("Max time:", int(1000*max_time))

        if reporter:
            reporter.report_solution(sol, lang, statuses, max_time)

        if statuses["RTE"] > 0:
            status = "RTE"
        elif statuses["WA"] > 0:
            status = "WA"
        elif statuses["TLE"] > 0:
            status = "TLE"
        else:
            status = "OK"
        
        if warn_status and status != self.expected_status(sol):
            if status == "OK" and self.expected_status(sol) == "TLE":
                logger.warn(self.id(), sol, lang, "status " + status + " different than expected " + self.expected_status(sol))
            else:
                logger.error(self.id(), sol, lang, "status " + status + " different than expected " + self.expected_status(sol))

        if warn_not_OK and status != "OK":
            logger.error(self.id(), sol, lang, "status not OK")
            
        return statuses

    # test correctness of all existing solutions of a given task
    def test_all(self, langs=[], sols=None, timeout=None, force_recompile=False, reporter=None):
        # log what checker is going to be used
        if self.has_checker():
            logger.info("Running custom checker...", verbosity=4)
        else:
            logger.info("Running default checker...", verbosity=4)
            
        # find existing, listed solutions (by intersecting sols and self.solutions())
        if not sols:
            sols = self.solutions()
        else:
            sols = [sol for sol in self.solutions() if sol["name"] in sols]
            
        # process all existing, listed solutions
        for sol in sols:
            # in all existing and listed langugages
            for lang in sol["lang"]:
                if langs and not lang in langs: continue
                # run the check
                self.test_on_all_testcases(sol["name"], lang=lang, timeout=timeout, force_recompile=force_recompile, reporter=reporter)

        if reporter:
            reporter.end()
    

    # Run all tests and measure runtime

    # full path to time.json file for a task with the given task_id in a
    # given source repository
    def time_json_path(self):
        return os.path.join(self.build_dir(), "time.json")

    # run all tests (all solutions specified in -st.md on all testcases)
    # for the given tasks
    def measure_all_runtimes(self, params = None):
        # list of supported languages
        supported_langs = ["cpp", "cs"]
        
        # substitute mising params with default parameter values
        if params == None:
            params = dict()
     
        default_params = {
            "force_run": False, # run tests again even if there exists time.json
            "repeat": 3,        # numer of repetitions for better accuracy
            "timeout": 1        # timeout in second
        }
     
        params = {**default_params, **params}
     
        # if the timing file already exists and run is not force, just
        # return data read from the file
        time_json = self.time_json_path()
        if not (params["force_run"]) and os.path.isfile(time_json):
            logger.info("Results loaded from", time_json)
            return json.load(open(time_json, "r"))
     
        # otherwise run the tests
        logger.info(self.id(), "-", "running tests to measure time...")
        
        # generate testcases if they do not exist
        num_testcases = self.number_of_generated_testcases()
        logger.info("Found {} testcases".format(num_testcases))
        if num_testcases == 0:
            logger.info("Generating tests")
            self.generate_testcases()
     
        # run tests and store the results in a dictionary
        result = {}
        result["id"] = self.id()
        result["dir"] = self.dir()
        
        # dictionary for storing all times
        all_times = {}
        
        # process all solutions specified in -st.md
        for sol in self.solutions():
            logger.info(sol)
     
            # dictionary for storing times for a given solution
            sol_times = {}
            
            # process all programming languages for that solution
            for lang in sol["lang"]:
                # skip unsuported languages
                if not (lang in supported_langs):
                    continue
                
                # ensure that exe file exists (compilation is not forced)
                if not self.compile(sol["name"], lang, False):
                    logger.error("compilation failed", self.src_file_name(sol["name"], lang))
     
                # dictionary for storing times for a specific language
                lang_times = {}

                logger.info("Running on generated testcases")
                
                # iterate through all testcases
                for infilename in self.generated_testcases():
                    # for better accuracy the test is repeated several
                    # number of times, and median time is calculated
                    ellapsed_times = []
                    for i in range(params["repeat"]):
                        # extract test number (e.g., _build/test-data/testcase_01.in -> 01.in)
                        test_number = os.path.basename(infilename)[-5:]
                        
                        # run test and measure ellapsed time
                        start_time = time.time()
                        timeout = self.run(sol["name"], lang, infilename, params["timeout"]) == False
                        ellapsed_time = time.time() - start_time
                        ellapsed_times.append(ellapsed_time)
                        
     
                    # calculate median time
                    lang_times[test_number] = \
                         round(1000 * statistics.median(ellapsed_times))
                    # note if timeout
                    if timeout:
                        lang_times[test_number + "_TO"] = True
                sol_times[lang] = lang_times
            all_times[sol["name"]] = sol_times
        result["times"] = all_times
        
        # store results in the time.json file
        time_json_file = open(time_json, "w")
        print(json.dumps(result, indent=4), file=time_json_file)
        time_json_file.close()
        return result
            
    ####################################################################
    # Modifying task data
    
    # set timeout (given in miliseconds)
    def set_timeout(self, timeout):
        try:
            # TODO: remove sed dependency
            os.system("sed -i '3s/.*/timelimit: {} # u sekundama/' \"{}\"".format(timeout/1000,
                                                                                  self.st_path()))
        except:
            logger.error("sed is not supported")
    
