import os
import random
import subprocess
import time

max_authors = 1

comment_string = {'py': '#', 'sh': "#",  'cpp': '//'}


def get_authors(file_contents, ptype):
    Authors = []
    for line in file_contents.lower().splitlines():
        if line.startswith(comment_string[ptype]) and "copyright" in line:
            try:
                _, email = line.rsplit(" ", 1)
                if email.endswith('@bu.edu'):
                    Authors.append(email)
            except:
                pass
    return Authors


def progtype(program):
    try:
        _, program_type = program.split('.')
    except:
        return 'sh'
    return program_type

testwords = ['apple', 'orange', 'kiwi', 'banana',
             'strawberry', 'pineapple', 'rasberry']


def test_fourargspy(actualname):
    s = ""
    for n in [0, 3, 4, 5, 7]:
        words = random.sample(testwords, n)
        try:
            T = subprocess.run(['python', actualname, *words],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,timeout=2)
        except:
            s +="your script timed out."
            return s

        if T.stdout.decode() != ''.join([a+'\n' for a in words[:4]]):
            s += f"Your stdout is not correct for {n} arguments.\n"
        if T.stderr.decode() != ''.join([a+'\n' for a in words[4:]]):
            s += f"Your stderr is not correct for {n} arguments.\n"
    return s


def test_fourargscpp(actualname):
    s = ""
    compiledprogram = actualname[:-4]
    C = subprocess.run(['g++', actualname, '-o', compiledprogram],
                       stderr=subprocess.PIPE)
    if C.returncode:
        s = 'g++ found problems, as follows:\n'
        s += C.stderr.decode()
        return s
    for n in [0, 3, 4, 5, 7]:
        words = random.sample(testwords, n)
        try:
            T = subprocess.run([compiledprogram, *words], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,timeout=1)
        except:
            s +="your script timed out."
            return s
        if T.stdout.decode() != ''.join([a+'\n' for a in words[:4]]):
            s += f"Your stdout is not correct for {n} arguments.\n"
        if T.stderr.decode() != ''.join([a+'\n' for a in words[4:]]):
            s += f"Your stderr is not correct for {n} arguments.\n"
    return s


def test_fourargssh(actualname):
    s = ""
    try:
        T = subprocess.run([actualname], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=5)
    except TimeoutError:
        s +="your script timed out.\n"
        return s
    except Exception as e:
        s += str(e)
        return s


    if len(T.stdout.decode().strip().split('\n')) != 14:
        s += 'your shell script is not correct (stdout problem)\n'
        s += 'You printed out:'+T.stdout.decode()
    if len(T.stderr.decode().strip().split('\n')) != 4:
        s += 'your shell script is not correct (stderr problem)\n'
    return s



DIR='files_for_args_checker'
def make_files():
    this_dir = os.getcwd()
    if DIR not in os.listdir():
        os.mkdir(DIR)
        os.system('wget -N curl.bu.edu/static/content/ec602_fal18/test_files.zip')
        os.system('unzip test_files.zip')

    testfiles = ['one','two.txt','three.py','four.cpp','five.md','six.exe','seven.java']
    
    return testfiles


def test_recent(actualname):
    orderedfiles = make_files()

    this_dir = os.getcwd()
    os.chdir(DIR)
    
    s = ""
    for n in [1,3,6]:
        try:
            T = subprocess.run(['../'+actualname,str(n)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True,timeout=5)
        except TimeoutError:
            s +="your script timed out.\n"
            continue
        except Exception as e:
            s += f"exception: {e}\n"
            continue


        output = T.stdout.strip().split('\n')
        if output != orderedfiles[:n]:
            s += f"your script failed on the case {actualname} {n}\n"
            s += f"your output: {output}\n"
            s += f"correct output: {orderedfiles[:n]}\n"
        
    
    os.chdir(this_dir)

    return s

def test_oldest(actualname):
    orderedfiles = make_files()
    orderedfiles.reverse()

    this_dir = os.getcwd()
    os.chdir(DIR)
    
    s = ""
    for n in [1,3,6]:
        try:
            T = subprocess.run(['../'+actualname,str(n)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True,timeout=5)
        except TimeoutError:
            s +="your script timed out.\n"
            continue
        except Exception as e:
            s += f"exception: {e}\n"
            continue

        output = T.stdout.strip().split('\n')
        if output != orderedfiles[:n]:
            s += f"your script failed on the case {actualname} {n}\n"
            s += f"your output: {output}\n"
            s += f"correct output: {orderedfiles[:n]}\n"
        
    
    os.chdir(this_dir)

    return s


programs = {'fourargs.py': test_fourargspy,
            'fourargs.cpp': test_fourargscpp,
            'fourargs.sh': test_fourargssh,
            'recent':test_recent,
            'oldest':test_oldest}


def analyse(program,actualprogramname=None):
    
    actualprogramname = actualprogramname or program

    s = f'Checking {program} for EC602 submission.\n'
    ptype = progtype(program)
    try:
        f = open(actualprogramname)
        contents = f.read()
        f.close()
    except:
        s += f'The program {actualprogramname} does not exist here.\n'
        return 'No file', s

    authors = get_authors(contents, ptype)
    s += 'authors       : {}\n'.format(" ".join(authors))

    if ptype=='sh' and 'sudo' in contents:
        s += "Please do not use sudo in your program."
        return False, s
    
    if len(authors) > max_authors:
        s += "You have exceeded the maximum number of authors.\n"
        return 'Too many authors', s

    res = programs[program](actualprogramname)
    s += 'program check :'
    if res:
        s += " failed.\n"
        s += res
        return False, s
    else:
        s += " passed.\n"
        return "Pass", s

if __name__ == '__main__':
    for program in programs:
        summary, results = analyse(program)
        print(results)
