![tucan](https://images.unsplash.com/photo-1611788542170-38cf842212f4?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

TUCAN (Tool to Unformat, Clean, and Analyse) is a code parser for scientific codebases. Its target languages are:

- Very old FORTRAN
- Recent FORTRAN
- Python (Under development)
- C/C++ (Early development)

## Installation

You can instal it from [PyPI](https://pypi.org/project/tucan/) with:

```bash
pip install tucan
```

You can also install from the sources from one of our [gitlab mirrors](https://codehub.hlrs.de/coes/excellerat-p2/uc-2/tucan).


## What is does?


### Remove coding archaisms

First it is a code cleaner. For example, this loop in `tranfit.f', a piece of [CHEMKIN](https://en.wikipedia.org/wiki/CHEMKIN) II package  in good'old FORTRAN77. (Do not worry, recent Chemkin is not written that way, probably)  :

```fortran
(547)      DO 2000 K = 1, KK-1
(548)         DO 2000 J = K+1, KK
(549)            DO 2000 N = 1, NO
(550)               COFD(N,J,K) = COFD(N,K,J)
(551) 2000 CONTINUE
```

Is translated  with the command `tucan clean tranfit.f` as : 
```fortran
(547-547)        do 2000 k  =  1,kk-1
(548-548)           do 2000 j  =  k+1,kk
(549-549)              do 2000 n  =  1,no
(550-550)                 cofd(n,j,k)  =  cofd(n,k,j)
(551-551)              end do ! 2000
(551-551)           end do ! 2000
(551-551)        end do ! 2000
```


The cleaned version is a simpler code for further analysis passes, like computing cyclomatic complexity, extracting structures, etc...


### Extracting code structure


Here we start from a file of [neko](https://github.com/ExtremeFLOW/neko/blob/develop/src/adt/htable.f90), an HPC code in recent Fortran, finalist for the Gordon Bell Prize in 2023.

`tucan struct htable.f90` provides a nested dictionary of the code structure. Here is a part of the output:

```yaml
(...)
type htable.h_tuple_t :
    At path ['htable', 'h_tuple_t'], name h_tuple_t, lines 47 -> 52
    6 statements over 6 lines
    Complexity 1
    Refers to 1 callables:
       - class
    Contains no inner structures
    Contains no annotations

type_public_abstract htable.htable_t :
    At path ['htable', 'htable_t'], name htable_t, lines 55 -> 64
    10 statements over 10 lines
    Complexity 1
    Refers to 2 callables:
       - pass
       - t
    Contains no inner structures
    Contains no annotations

function_pure htable.interface_abstract66.htable_hash :
    At path ['htable', 'interface_abstract66', 'htable_hash'], name htable_hash, lines 67 -> 72
    6 statements over 6 lines
    Complexity 1
    Refers to 2 callables:
       - class
       - htable_hash
    Contains no inner structures
    Contains no annotations

interface_abstract htable.interface_abstract66 :
    At path ['htable', 'interface_abstract66'], name interface_abstract66, lines 66 -> 73
    8 statements over 8 lines
    Complexity 1
    Contains no callables
    Contains 1 elements:
    - htable.interface_abstract66.htable_hash
    Contains no annotations
(...)
```

*(This output will change as we update and improve tucan in the next versions!)*

This information allows the creation and manipulation of graphs to extract the structure of the code


### Interpreting Conditional Inclusions "IF DEFS". 

An other example of tucan is the analysis of [ifdefs](https://en.cppreference.com/w/c/preprocessor/conditional) in C or FORTRAN:

```
#ifdef FRONT
        WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        SUBROUTINE dummy_front(a,b,c)
        WRITE(*,*) " FRONT 1"     ! partial front subroutine
#else                
        SUBROUTINE dummy_front(a,d,e)
        WRITE(*,*) " FRONT 2"       ! partial front subroutine
#endif
        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)
#ifdef BACK
        WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        WRITE(*,*) " BACK 1"    ! partial back subroutine
        END SUBROUTINE  
#else
        WRITE(*,*) " BACK 2"    ! partial back subroutine
        END SUBROUTINE  
#endif
```

Depending on the pre-definition of variables FRONT and BACK, this code snippet can be read in four ways possible.
Here are usages:

`tucan ifdef-clean templates_ifdef.f` yields:

```fortran
        SUBROUTINE dummy_front(a,d,e)
        WRITE(*,*) " FRONT 2"       ! partial front subroutine
        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)


        WRITE(*,*) " BACK 2"    ! partial back subroutine
        END SUBROUTINE
```


`tucan ifdef-clean templates_ifdef.f -v FRONT` yields:

```fortran
        WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        SUBROUTINE dummy_front(a,b,c)
        WRITE(*,*) " FRONT 1"     ! partial front subroutine


        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)


        WRITE(*,*) " BACK 2"    ! partial back subroutine
        END SUBROUTINE
```

`tucan ifdef-clean templates_ifdef.f -v FRONT,BACK` yields:

```fortran
         WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        SUBROUTINE dummy_front(a,b,c)
        WRITE(*,*) " FRONT 1"     ! partial front subroutine


        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)
        WRITE(*,*) " BACK is enabled " ! partial front subroutine
        WRITE(*,*) " BACK 1"    ! partial back subroutine
        END SUBROUTINE
```

#### scanning ifdef variables

A simpler usage of tucan : scan the current ifdefs variables. Still on [neko](https://github.com/ExtremeFLOW/neko) in the `/src` folder (an old version though) : 

```bash
/neko/src >tucan ifdef-scan-pkge .
 - Recursive path gathering ...
 - Cleaning the paths ...
 - Analysis completed.
 - Global ifdef variables : HAVE_PARMETIS, __APPLE__
 - Local to device/opencl/check.c : CL_ERR_STR(err)
 - Local to math/bcknd/device/opencl/opr_opgrad.c : CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/opr_dudxyz.c : CASE(LX), STR(X)
 - Local to common/sighdl.c : SIGHDL_ALRM, SIGHDL_USR1, SIGHDL_USR2, SIGHDL_XCPU
 - Local to math/bcknd/device/opencl/opr_conv1.c : CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/opr_cfl.c : CASE(LX), STR(X)
 - Local to krylov/bcknd/device/opencl/pc_jacobi.c : CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/ax_helm.c : CASE(LX), STR(X)
 - Local to bc/bcknd/device/opencl/symmetry.c : MAX(a,
 - Local to gs/bcknd/device/opencl/gs.c : GS_OP_ADD, GS_OP_MAX, GS_OP_MIN, GS_OP_MUL
 - Local to sem/bcknd/device/opencl/coef.c : DXYZDRST_CASE(LX), GEO_CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/opr_cdtp.c : CASE(LX), STR(X)
```
This feature is useful to see all potential variables that surcharge your codebase via conditional inclusions.

## More about tucan

`Tucan` is used by  `anubis`, our open-source  tool to explore the git repository of a code, and `marauder's map`  our open-source tool to show codes structures by in-depth vizualisation of callgraphs and code circular-packing .

