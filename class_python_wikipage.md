Inside the directory `python/`, accessible from the root directory of CLASS, lives a Python wrapper written in Cython. This page details how to install and use it. It also contains instructions on how to use the testing suite that makes use of the wrapper, which might help you debugging a modification of CLASS.

If you intend to use CLASS as it is through the parameter extraction codes **Cobaya** or **Monte Python**,
you do not need to understand how the wrapper works. However, if you have modified CLASS and want to expose new derived parameters, or new functionality, to the sampling frameworks, you need to make some additions to the Cython code. You can find an example of this below. 


### Installation of the wrapper

First, you must do a step more than for running CLASS traditionally. If you simply did

~~~ code
class]$ make class
~~~

when compiling, you did not create the library (`libclass.a` file). You should do rather a

~~~ code
class]$ make
~~~

Now, go to the `python` subfolder, and run the installation script:

~~~ code
class]$ cd python/
python]$ python setup.py install --user
~~~

You might get some warnings about error messages, which are harmless. As long as you do not get any errors here, you are good to proceed. To check that the installation truly succeeded, simply run:

~~~ code
python]$ python -c 'from classy import Class'
~~~

If it succeeds (and does not return any error), the Python wrapper is installed.


### Basic Usage

As a first note on the names, writing a wrapper for a code called `CLASS` in an object-oriented framework required some thought. `CLASS` in all-caps designate the code in C, `class` is the standard keyword for classes in Python, and `Class` is the Python `class` that wraps `CLASS`. There you go.

The wrapper is designed to follow as closely as possible the behaviour of the underlying code. The main differences are the following:

* there is no file `something.ini` to read from, instead, you will use a Python dictionary.
* the `main` routine of CLASS is actually separated into two methods of the class `Class`: `compute` and `struct_cleanup`. The former doing all the `structure_init()` calls, and the latter all the `structure_free()` calls.

The basic flow to call CLASS through this interface, in a python script is the following

1. import the module
2. Create an instance of `Class`
3. Define a dict holding the parameters you want to test
4. Set the parameters to the `Class` instance
5. Initialise the structures with the `compute` method
6. Do stuff with what is inside (access the C_l, the power spectrum, thermodynamics quantities, what have you)
7. Free the structures with the `struct_cleanup` method
8. Delete the parameters inside the instance, with the `empty` method.
9. Restart from step 3) with another set of parameters.

Here follows an example of such a python script. Create a file `temp.py`, and copy paste the following lines:

~~~ python
from classy import Class

# Define your cosmology (what is not specified will be set to CLASS default parameters)
params = {
    'output': 'tCl lCl',
    'l_max_scalars': 2000,
    'lensing': 'yes',
    'A_s': 2.3e-9,
    'n_s': 0.9624, 
    'h': 0.6711,
    'omega_b': 0.022068,
    'omega_cdm': 0.12029}

# Create an instance of the CLASS wrapper
cosmo = Class()

# Set the parameters to the cosmological code
cosmo.set(params)

# Run the whole code. Depending on your output, it will call the
# CLASS modules more or less fast. For instance, without any
# output asked, CLASS will only compute background quantities,
# thus running almost instantaneously.
# This is equivalent to the beginning of the `main` routine of CLASS,
# with all the struct_init() methods called.
cosmo.compute()

# Access the lensed cl until l=2000
cls = cosmo.lensed_cl(2000)

# Print on screen to see the output
print cls
# It is a dictionnary that contains the fields: tt, te, ee, bb, pp, tp

# plot something with matplotlib...

# Clean CLASS (the equivalent of the struct_free() in the `main`
# of CLASS. This step is primordial when running in a loop over different
# cosmologies, as you will saturate your memory very fast if you ommit
# it.
cosmo.struct_cleanup()

# If you want to change completely the cosmology, you should also
# clean the arguments, otherwise, if you are simply running on a loop
# of different values for the same parameters, this step is not needed
cosmo.empty()
~~~

### Automated testing

Finally, a file `test_class.py` is present in this `python/` subfolder. It makes use of Python techniques to automatize tests. It loops over many different cosmological scenarios, combining them with different output, with or without non-linearities, in synchronous or newtonian gauge. More will be added over-time, but already the execution is fairly long (roughly 100 tests cases as this current version).

To run it, you need to install the Python module `nose`, which provides the command `nosetests`, and `nose-parameterized` to loop over the different scenarios, as explained below. You would then simply call

~~~ code
python]$ nosetests test_class.py
~~~

and go grab yourself a coffee. 

The key part of the code are the following lines (which might be expanded with more cases now, but the principle is the same).

~~~ python

    @parameterized.expand(
        itertools.product(
            ('LCDM',
             'Mnu',
             'Positive_Omega_k',
             'Negative_Omega_k'),
            ({}, {'output': 'mPk'}, {'output': 'tCl'},
             {'output': 'tCl lCl'}, {'output': 'mPk tCl lCl'},
             {'output': 'nCl sCl'}, {'output': 'mPk nCl sCl'}),
            ({'gauge': 'newtonian'}, {'gauge': 'sync'}),
            ({}, {'non linear': 'halofit'})))
    def test_parameters(self, name, scenario, gauge, nonlinear):
        ....
~~~

The decorator `@parameterized.expand` takes what comes after, the `itertools.product` and will create as many methods as needed, which will be fed the proper arguments. There are four arguments of the method, hence there are four tuples that are multiplied together by the `itertools.product`. Think of it as a Cartesian product. For instance, the first set of arguments, fed to the first function, will be:

~~~ python
    name=`LCDM`, scenario={}, gauge='newtonian', nonlinear={}
~~~

the `name` keyword defines what the cosmological parameters will be. The keyword `scenario` manages the different possible outputs, then `gauge` and `nonlinear` are pretty self-explanatory.

*Note that this test suite tests both the underlying code* **and** *the wrapper. An error during the run is not necessarily a fault in CLASS.*

When the code fails, it will output to a `stdout` the parameters which were used to provoke the error. Simply try them out in CLASS to identify if your modification broke something inside CLASS, or inside the wrapper.

### Exposing a new parameter

Suppose you have modified CLASS to take into account a new dark energy model based on some modification of gravity. 
You may have added a new fundamental input parameter `mymodel_input_par`
that specifies the model on the background level, and you have done this by adding it to the background structure defined in `include/background.h` and using the macro 
~~~ C
class_read_double("mymodel_input_par", pba->mymodel_input_par)
~~~ 
This will automatically work for both, reading from `.ini` files and exposing the parameter to Cobaya or MontePython, 
which set up virtual `.ini` files. 

Suppose now that you also have an output parameter, for example the fraction of dark energy in your model today, `Omega0_de`, which you have declared in the background structure in `include/background.h` as well. In our example, this number may be computed from a closure condition for the flat universe when CLASS is starting up, given LCDM matter and radiation densities and `mymodel_input_par`. It would be nice to add this quantity as a derived parameter to the sampling framework. 

To do so, we repeat the declaration of the parameter from the background structure in the header file `python/cclassy.pxd`,

~~~ python
cdef extern from "class.h":
    """ 
        ...
    """

    cdef struct background:
        """ 
            ...
        """
        double Omega0_de
~~~

and add two lines to the source file `python/classy.pyx`, in the definition of the class `Class`,

~~~ python
def get_current_derived_parameters(self, names):
    """ 
        ...
    """
    for name in names: 
        """ 
            ...
        """
        elif name == 'Omega_de' or name == 'Omega0_de':
            value = self.ba.Omega0_de
            
        """ 
            ...
        """


~~~

This exposes the parameter `Omega0_de` from the background structure to the sampling framework, where it is now known as a derived parameter under the names `Omega_de` and `Omega0_de`.

Of course, new functionality, if required in a Python notebook or your own likelihood, can be added to the class `Class`, as well, e.g. 

~~~ python
    def Omega_nlde(self):
        return self.ba.Omega0_de 
~~~




