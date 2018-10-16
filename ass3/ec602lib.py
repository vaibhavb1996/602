"""tools for analyzing and checking C++ and Py programs"""
import subprocess
import difflib
import unittest
import re
import tokenize
import dis
import io
import cpplint
import sys
import pycodestyle

VERSION = (2, 3)

STDLINT = ['-readability/alt_tokens',"+build/include_alpha"]

ignore_lint = [x[1:] for x in STDLINT if x.startswith('-')]

ASTYLE_OPTIONS = [
    '--style=google', '--indent=spaces=2', '--formatted', '--dry-run'
]

COMMENT_STRING = {'py': '#', 'sh': "#", 'cpp': '//'}

#CPP_CODE_ONLY = [
#    'g++', '-std=c++14', '-P', '-x', 'c++', '-dD', '-E', '-fpreprocessed'
#]


def read_file(filename):
    "read the contents of filename into string"
    filehand = open(filename)
    contents = filehand.read()
    filehand.close()
    return contents

def read_file_for_cpplint(filename):
    "read the contents of filename into list of strings"
    filehand = open(filename)
    contents = filehand.read()
    filehand.close()
    lines = contents.splitlines()
    if contents.endswith('\n'):
        lines.append('')
    return lines


def code_analysis_cpp(program_filename):
    Errors = {}
    def error_fcn(filename,line_number,lint_type,level,message):
        category,subcategory = lint_type.split('/')
        if category not in Errors:
            Errors[category]=[]
        Errors[category].append( (line_number,lint_type,message) )

    lines = read_file_for_cpplint(program_filename)
    cpplint.RemoveMultiLineComments(program_filename,lines,error_fcn)

    clean_lines = cpplint.CleansedLines(lines)

    cpplint.ProcessFileData(program_filename,'cpp',lines,error_fcn)


    num_lines = sum(bool(x.strip()) for x in clean_lines.lines)
    num_words = sum(len(x.split()) for x in clean_lines.lines)
    

    original = read_file(program_filename)
    proc_astyle = subprocess.run(
        ['astyle', *ASTYLE_OPTIONS],
        input=original.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    if proc_astyle.returncode:
        unchanged='error'
    else:
        original = original.splitlines()
        newprog = proc_astyle.stdout.decode().splitlines()
        matcher = difflib.SequenceMatcher()
        matcher.set_seqs(original, newprog)
        unchanged = matcher.ratio()

    RealErrors={}

    for e in Errors:
        for x in Errors[e][:3]:
            if [True for s in ignore_lint if x[1] not in s]:
                RealErrors[e]=Errors[e]

    return {'lines': num_lines, 'words': num_words, 'errors':RealErrors,'astyle':unchanged}


def code_analysis_py(program_contents):
        "count lines and words in python"
        f = io.BytesIO(program_contents.encode())
        g = tokenize.tokenize(f.readline)
        processed_tokens = []
        for tok in g:
            t_type = tok[0]
            if t_type not in [tokenize.COMMENT]:
                processed_tokens.append(tok)

        # remove the docstring
        i = 0
        while processed_tokens[i][0] == tokenize.NL:
            i = i + 1
        if processed_tokens[i][0] == tokenize.STRING:
            processed_tokens = processed_tokens[i + 1:]
        # remove strings

        newtok=[]
        i = 0
        while (i < len(processed_tokens)-2):
            if processed_tokens[i][0]==tokenize.INDENT:
                pass
                #print('a',processed_tokens[i],processed_tokens[i+1],processed_tokens[i+2])
                #print('b',tokenize.INDENT,tokenize.STRING,tokenize.NEWLINE)
            if processed_tokens[i][0] == tokenize.INDENT \
                    and processed_tokens[i+1][0] == tokenize.STRING \
                    and processed_tokens[i+2][0] == tokenize.NEWLINE:
               i += 3
            newtok.append(processed_tokens[i])
            i += 1

        newtok= newtok + processed_tokens[i:i+2]
        #for t in newtok:
        #    print(t)
        src = "\n".join(
            x for x in tokenize.untokenize(newtok).decode().splitlines()
            if x.strip() and x != "\\")


        return {'lines': len(src.splitlines()), 'words': len(src.split())}

pylint_options=["--enable=all","--reports=yes","--persistent=no",
"--msg-template='{category:10s}:{line:3d},{column:2d}: {msg} ({symbol})'"]

def pylint_check(program_name):
    process = subprocess.run(['pylint',program_name,*pylint_options],
        stdout=subprocess.PIPE,universal_newlines=True)
    
    out_str = process.stdout
    for scoreline in out_str.splitlines()[-4:]:
        try:
            score = float(re.search('Your code has been rated at ([\d|\.]*)/10',scoreline).groups()[0])
            return score, out_str
        except:
            pass
    raise ValueError('could not get your pylint score')


def pycodestylpe_check(filename):
    "run pycodestyle, return #errors and error string"

    pycodestyle_res = io.StringIO()

    sys.stdout = pycodestyle_res
    pycodestyle_errors = pycodestyle.Checker(filename).check_all()
    sys.stdout = sys.__stdout__

    res = pycodestyle_res.getvalue()


    return pycodestyle_errors,res


def progtype(program):
    "which type, cpp or py"
    _, program_type = program.split('.')
    return program_type


def get_includes(file_contents):
    "get included libraries in C/C++"
    includes = set()
    for line in file_contents.lower().splitlines():
        text = line.strip()
        search_str = r"#include\s*<(.*)>"
        matches = re.match(search_str, text)
        if matches:
            includes.add(matches.group(1))
        matches = re.match("#include \"(.*)\"", text)
        if matches:
            includes.add(matches.group(1))
    return includes


def get_python_imports(file_contents):
    "get the imports of file_contents as a set"
    try:
        instructions = dis.get_instructions(file_contents)
        imports = [__ for __ in instructions if 'IMPORT' in __.opname]
    except:
        return {'ERROR PROCESSING PYTHON SCRIPT'}

    grouped = set()
    for instr in imports:
        if instr.opname == "IMPORT_NAME":
            grouped.add(instr.argval)

    return grouped


AUTHWARN = "WARNING, NO VALID AUTHOR LINES FOUND"


def get_authors(file_contents, ptype):
    """get the authors in file_contents"""
    authors = []
    if ptype == 'json':
        A = json.loads(file_contents)
        return A.get('authors',[])

    for line in file_contents.lower().splitlines():
        if line.startswith(COMMENT_STRING[ptype]) and "copyright" in line:
            try:
                _, email = line.strip().rsplit(" ", 1)
                if email.endswith('@bu.edu'):
                    authors.append(email)
            except:
                pass
    return authors


def check_program(testclass):
    """return any errors as a list of strings"""
    errors = []
    passed = []
    gradesummary = {'pass': [], 'fail': []}

    if hasattr(testclass, "setUpClass"):
        testclass.setUpClass()

    loader = unittest.loader.TestLoader()
    tests = loader.loadTestsFromTestCase(testclass)
    for test in sorted(tests, key=lambda x: x.shortDescription()):
        run = test.run()
        if run.wasSuccessful():
            passed.append('Passed: {}\n'.format(test.shortDescription()))
            gradesummary['pass'].append(test.shortDescription()[0])
        else:
            err = 'Failed: {}\n'.format(test.shortDescription())
            for testmsg, res in run.failures + run.errors:
                casetext = re.search(".*CASE='(.*)'", str(testmsg))
                if casetext:
                    err += "CASE: {}\n".format(casetext.group(1))
                if 'AssertionError:' in res:
                    _, msg = res.split('AssertionError: ')
                else:
                    msg = res
                err += msg
            errors.append(err)
            gradesummary['fail'].append(test.shortDescription()[0])

    if hasattr(testclass, "tearDownClass"):
        testclass.tearDownClass()

    return errors, passed, gradesummary


EMPTYGRADE = {'pass': [], 'fail': []}


def errors_msg(errors):
    "format error message"
    msg = '-----------------errors found--------------\n'
    for testmsg in errors:
        msg += testmsg + "\n-------\n"
    return msg


SIZE_REPORT_TEMPLATE = """lines of code    : {}, {:4.0%} of reference
tokens in code   : {}, {:4.0%} of reference
"""


def code_size_report(submitted_code, reference_code):
    "generate message about code size"
    return SIZE_REPORT_TEMPLATE.format(
        submitted_code['lines'],
        submitted_code['lines'] / reference_code['lines'],
        submitted_code['words'],
        submitted_code['words'] / reference_code['words'])


def overallcpp(program_name,
               testclass,
               refcode,
               program=None,
               orig_program=None,
               lintoptions=None,
               docompile=True):
    "evaluate c++ program in file program_name"

    if not lintoptions:
        lintoptions = STDLINT
    if not orig_program:
        orig_program = program_name
    retstr = 'Checking {} for EC602 submission.\n'.format(orig_program)
    if not program:
        program = program_name[:-4]

    try:
        the_program = read_file(program_name)
    except:
        retstr += 'The program {} does not exist here.\n'.format(orig_program)
        return 'No file', retstr, EMPTYGRADE

    authors = get_authors(the_program, progtype(program_name))

    includes = get_includes(the_program)
    retstr += '\n---- analysis of your code structure ----\n\n'

    retstr += 'authors       : {}\n'.format(" ".join(authors)
                                            if authors else AUTHWARN)

    retstr += 'included libs : {}\n'.format(" ".join(includes))

    if docompile:
        proc_comp = subprocess.run(
            ['g++', '-std=c++14', program_name, '-o', program],
            stderr=subprocess.PIPE)
        retstr += 'compile       : {}\n'.format("error" if proc_comp.returncode
                                                else "ok")

    comments = 0
    for line in the_program.splitlines():
        if '//' in line:
            comments += 1


 
    code_metrics = code_analysis_cpp(program_name)


    if code_metrics['errors']:
        retstr += "\ncpplint       : {} problems\n".format(len(code_metrics['errors']))
        cpplint_call_list = [
            'cpplint', '--filter=' + ','.join(lintoptions), orig_program
        ]

        retstr += '  [using {}]\n\n'.format(' '.join(cpplint_call_list))

        for e in code_metrics['errors']:
            print(e,len(code_metrics['errors'][e]))
            for x in code_metrics['errors'][e][:3]:
                    retstr += '  line {} ({}): {}\n'.format(*x)
    else:
        retstr += "\ncpplint       : ok\n"


    
    retstr += "\nastyle        : {:.1%} code unchanged.\n".format(code_metrics['astyle'])

    retstr += code_size_report(code_metrics, refcode)

    retstr += "comments      : {}\n".format(comments)

    retstr += '\n---- check of requirements ----\n'
    try:
        errors, passed, gradesummary = check_program(testclass)
    except unittest.SkipTest as exc:
        retstr += str(exc)
        return "Errors", retstr, EMPTYGRADE

    for testmsg in passed:
        retstr += testmsg

    if errors:
        retstr += errors_msg(errors)
        return 'Errors', retstr, gradesummary

    return 'Pass', retstr, gradesummary


def overallpy(program_name, testclass, refcode, orig_program=None):
    "evaluate python script in file program_name"
    if not orig_program:
        orig_program = program_name
    retstr = 'Checking {} for EC602 submission.\n'.format(orig_program)

    try:
        the_program = read_file(program_name)

    except:
        retstr += 'The program {} does not exist here.\n'.format(orig_program)
        return 'No file', retstr, EMPTYGRADE

    authors = get_authors(the_program, progtype(program_name))

    imported = get_python_imports(the_program)
    retstr += '\n---- analysis of your code structure ----\n\n'

    retstr += 'authors          : {}\n'.format(" ".join(authors)
                                               if authors else AUTHWARN)

    retstr += 'imported modules : {}\n'.format(" ".join(imported))

    comments = 0
    for line in the_program.splitlines():
        if '#' in line:
            comments += 1

    proc_pycodestyle = subprocess.run(['pycodestyle', program_name], stdout=subprocess.PIPE)

    prob = False
    if proc_pycodestyle.returncode:
        prob = proc_pycodestyle.stdout.decode().rsplit(" ", 1)[-1].strip()

    retstr += "pycodestyle check       : {}\n".format("{} problems".format(
        len(proc_pycodestyle.stdout.decode().splitlines())) if prob else "ok")

    proc_pylint = subprocess.run(
        ['pylint', program_name], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    # (pylint_stdout, pylint_stderr) =     lint.py_run(program_name +
    #      " --enable=all --reports=yes --persistent=no --msg-template='{category:10s}:{line:3d},{column:2d}: {msg} ({symbol})'",return_std=True)
    # print('py stdout')
    # print(pylint_stdout.readlines())
    # print('py stderr')
    # print(pylint_stderr.readlines())
    # quit()
    pylint_report = proc_pylint.stdout.decode().splitlines()
    if "previous" in pylint_report[-2]:
        pylint_score=pylint_report[-2].split()[6]
    else:
        pylint_score = pylint_report[-2].split()[-1]
        
    retstr += "pylint score     : {}\n".format(pylint_score)
 
    code_metrics = code_analysis_py(the_program)
    retstr += code_size_report(code_metrics, refcode)

    retstr += "comments         : {}\n".format(comments)

    retstr += '\n---- check of requirements ----\n'
    errors, passed, gradesummary = check_program(testclass)
    for testmsg in passed:
        retstr += testmsg

    if errors:
        retstr += errors_msg(errors)
        return 'Errors', retstr, gradesummary

    return 'Pass', retstr, gradesummary

def pyshell(Parms,q):
      summary, results, gradesummary = overallpy(**Parms)    
      q.put([summary,results,gradesummary])
