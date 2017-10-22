import pudb
import sys
import os
import glob
import Cython
from distutils.core import setup
from distutils.extension import Extension

MAINDIR = 'placer'
# Use latest clang
os.environ['CC'] = '/usr/local/opt/llvm/bin/clang'

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except:
    print("You don't seem to have Cython installed. Please get a")
    print("copy from www.cython.org and install it")
    sys.exit(1)

try:
    from Cython.Compiler.Options import get_directive_defaults
    directive_defaults = get_directive_defaults()
except ImportError:
    # for Cython < 0.25
    from Cython.Compiler.Options import directive_defaults

if "--debug" in sys.argv:
    debug_mode = True
    compiler_directives = {'linetrace': True, 'annotate': True}
    macros = [('CYTHON_TRACE', '1')]
    extra_link_args = ['-g', '-fopenmp']
    Cython.Compiler.Options.annotate = True

    sys.argv.remove("--debug")
else:
    debug_mode = False
    compiler_directives = {}
    macros = []
    extra_link_args = ['-fopenmp']
print('Using debug mode: {}'.format(debug_mode))

directive_defaults['language_level'] = 3
if debug_mode:
    directive_defaults['linetrace'] = True
    directive_defaults['binding'] = True


# scan the 'dvedit' directory for extension files, converting
# them to extension names in dotted notation
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


# generate an Extension object from its dotted name
def makeExtension(extpath):
    dirpath = os.path.dirname(extpath.replace(".", os.path.sep))
    dirpath = os.path.dirname(extpath.replace(".", os.path.sep))
    extname = extpath.split('.')[-1]
    pyxfile = extname + '.pyx'
    pyxpath = os.path.join(dirpath, pyxfile)
    extensioncpp = extname + '.cpp'
    extensioncppppath = os.path.join(dirpath, extensioncpp)
    cpppaths = glob.glob(os.path.join(dirpath, '*.cpp'))
    if extensioncppppath in cpppaths:
        cpppaths.remove(
            extensioncppppath)    # Dont need to compile it in again.
    allsources = [pyxpath] + cpppaths

    e = Extension(
        extpath,
        allsources,
        include_dirs=[".", '/opt/X11/include'
                      ],    # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args=[
            "-O3", "-Wall", "-std=c++14", "-ffast-math", "-march=native",
            "-fopenmp"
        ],
        extra_link_args=extra_link_args,
        define_macros=macros,
        library_dirs=['/usr/local/opt/llvm/lib', '/opt/X11/lib'],
        libraries=['X11'],
        language="c++", )
    e.compiler_directives = compiler_directives
    return e


extNames = scandir(MAINDIR)

# and build up the set of Extension objects
extensions = [makeExtension(name) for name in extNames]

# finally, we can pass all this to distutils
setup(
    name=MAINDIR,
    packages=[MAINDIR],
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext}, )
