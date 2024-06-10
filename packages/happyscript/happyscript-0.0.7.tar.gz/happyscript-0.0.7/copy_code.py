
# import python_minify

import shutil
import os
import python_minifier
import io, tokenize


PYPI_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","happyscript")

def delete_old_code():
    ''' Delete all the code in the pypi\happyscript directory.
    '''
    
    assert os.path.isdir(PYPI_DIR), f"Strange... {PYPI_DIR} should be a directory."
    
    folder = os.path.join(PYPI_DIR, "happyscript")
    
    print(f"Deleting all files in {folder}")
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
            
def list_all_source_files():
    ''' Return a list with all directories and with all source files (as a tuple dirs,files).
    '''
    dir_list = []                                               # lists for storing files and dirs found
    file_list = []
        
    for root, dirs, files in os.walk(SOURCE_DIR, topdown=False):    # traverse entire directory

        rel_path = os.path.relpath(root, start=SOURCE_DIR)      # calculate relative path 
        
        for name in files:
            _, ext = os.path.splitext(name)                     # get file extension
            if ext in (".fbp", ):                               # skip specific extensions
                continue

            # print("FILE", os.path.join(rel_path, name) )
            file_list.append( os.path.join(rel_path, name)  )   # remember file using relative path
            
        for name in dirs:
            # print("DIR", os.path.join(rel_path, name) )        
            dir_list.append( os.path.join(rel_path, name)  )    # remember dir using relative path
            
    return dir_list, file_list

def copy_full(src,dst):
    ''' Complete copy of the files, without obfuscation.
    '''
    # shutil.copyfile(src,dst)
    
    with open(src, 'r') as rf:
        old_code = rf.read()
        
        with open(dst, 'w') as wf:
            wf.write(old_code) 

            
def copy_minified(src,dst):
    ''' Copy file, with some obfuscation of the code.
    '''
    with open(src, 'r') as rf:
        old_code = rf.read()
        
        new_code = python_minifier.minify(old_code,
            remove_annotations = True, # If type annotations should be removed where possible
            remove_pass = True,  # If Pass statements should be removed where possible
            remove_literal_statements = True,  # If statements consisting of a single literal should be removed, including docstrings
            combine_imports = True,  #Combine adjacent import statements where possible
            hoist_literals = False,  # If str and byte literals may be hoisted to the module level where possible.
            rename_locals = False,  # If local names may be shortened
            preserve_locals = None,  # Locals names to leave unchanged when rename_locals is True (list of strings)
            rename_globals = False,  # If global names may be shortened
            preserve_globals = None,  #Global names to leave unchanged when rename_globals is True (list of strings)
            remove_object_base = False,  #If object as a base class may be removed
            convert_posargs_to_args = False,  #If positional-only arguments will be converted to normal arguments
            preserve_shebang = False,  #Keep any shebang interpreter directive from the source in the minified output
            remove_asserts = True,  # If assert statements should be removed
            remove_debug = True,  # If conditional statements that test '__debug__ is True' should be removed
            remove_explicit_return_none = True, # If explicit return None statements should be replaced with a bare return

            )
        
        with open(dst, 'w') as wf:
            wf.write(new_code) 
            

def remove_comments_and_docstrings(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            if token_string.startswith("#stop-amalgamation"):
                break
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out


def copy_without_comments(src,dst):
    """ Copy with comments and empty lines removed
    """
    
    inFile = open(src)
    theCode = inFile.read()
    theCode = theCode.replace("\t", "    ")
    
    theCode = remove_comments_and_docstrings(theCode)
    
    with open(dst, 'w') as wf:
        for line in theCode.splitlines():
            if not line.strip():
                continue
            if line.startswith("#stop-amalgamation"):
                break
            if line.strip().startswith('#'):
                continue
              
            wf.write(line.rstrip())
            wf.write('\n')
            
def copy_all_code():
    ''' Copy all sources to the pypi folder.
        Code wordt van commentaar gestript met een 'minifier' :
            https://dflook.github.io/python-minifier/installation.html 
            
    '''
    assert os.path.isdir(PYPI_DIR), f"Strange... {PYPI_DIR} should be a directory."
    assert os.path.isdir(SOURCE_DIR), f"Strange... {SOURCE_DIR} should be a directory."

    print(f"Copying source files from {SOURCE_DIR} to {PYPI_DIR}")
    
    dir_list, file_list = list_all_source_files()
    
    for name in dir_list:
        if "__pycache__" in name:
            continue
        new_dir = os.path.join(PYPI_DIR,"happyscript",name)
        print(f"Creating dir {new_dir}")
        os.makedirs( new_dir, exist_ok=True )
            
    for name in file_list:
        if "__pycache__" in name:
            continue
        new_file = os.path.join(PYPI_DIR,"happyscript",name)
        old_file = os.path.join(SOURCE_DIR,name)
        
        assert os.path.isfile(old_file), f"Strange... {old_file} should exist"
        assert not os.path.isfile(new_file), f"Strange... {new_file} should not exist"
        
        print(f"Copying file {name}")
        
        # copy_full(old_file,new_file)
        # copy_minified(old_file,new_file)
        copy_without_comments(old_file,new_file)
            
            
if __name__=="__main__":
    delete_old_code()
    copy_all_code()
    print("Done")
    