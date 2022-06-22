Language translator implemenntation 

-- issues with power

--known issues: 
1) 
var = 2^2^3
var2 = 2^(2^3)
both should be 256

2) nested curly braces issue
deadline: 21-22 06

wed 22 June 2022  ^^ fixed bugs


--- HOW TO RUN: 
--Precoditions: should be run with python3
1. current working directory should be set to: compiler_c2
2. `> python main.py`
3. Example of output:
```
Код програми у постфіксній формі (ПОЛІЗ): 
[('varpow1', 'ident'), ('2', 'int'), ('2', 'int'), ('3', 'int'), ('^', 'mult_op'), ('^', 'mult_op'), ('=', 'assign_op'), ('varpow2', 'ident'), ('2', 'int'), ('2', 'int'), ('3', 'int'), ('^', 'mult_op'), ('^', 'mult_op'), ('=', 'assign_op'), ('counter', 'ident'), ('0', 'int'), ('=', 'assign_op'), ('counter', 'ident'), ('counter', 'ident'), ('1', 'int'), ('+', 'add_op'), ('=', 'assign_op'), ('counter2', 'ident'), ('0', 'int'), ('=', 'assign_op'), ('counter2', 'ident'), ('counter2', 'ident'), ('1', 'int'), ('+', 'add_op'), ('=', 'assign_op'), ('counter2', 'ident'), ('3', 'int'), ('<', 'rel_op'), ('m2', 'label'), ('JT', 'jt'), ('m2', 'label'), (':', 'colon'), ('counter', 'ident'), ('5', 'int'), ('<', 'rel_op'), ('m1', 'label'), ('JT', 'jt'), ('m1', 'label'), (':', 'colon'), ('a', 'ident'), ('2', 'int'), ('2', 'int'), ('+', 'add_op'), ('=', 'assign_op'), ('c', 'ident'), ('3', 'int'), ('3', 'int'), ('*', 'mult_op'), ('=', 'assign_op'), ('z', 'ident'), ('a', 'ident'), ('1', 'int'), ('+', 'add_op'), ('a', 'ident'), ('1', 'int'), ('-', 'add_op'), ('*', 'mult_op'), ('=', 'assign_op'), ('var', 'ident'), ('2', 'int'), ('2', 'int'), ('2', 'int'), ('*', 'mult_op'), ('+', 'add_op'), ('=', 'assign_op'), ('var2', 'ident'), ('2', 'int'), ('2', 'int'), ('+', 'add_op'), ('2', 'int'), ('*', 'mult_op'), ('=', 'assign_op'), ('d', 'ident'), ('z', 'ident'), ('a', 'ident'), ('^', 'mult_op'), ('=', 'assign_op'), ('b', 'ident'), ('a', 'ident'), ('z', 'ident'), ('>', 'rel_op'), ('=', 'assign_op'), ('b', 'ident'), ('3.4', 'float'), ('3.2', 'float'), ('/', 'mult_op'), ('=', 'assign_op'), ('a', 'ident'), ('c', 'ident'), ('<', 'rel_op'), ('m3', 'label'), ('JF', 'jf'), ('foo', 'ident'), ('a', 'ident'), ('1', 'int'), ('+', 'add_op'), ('=', 'assign_op'), ('m4', 'label'), ('JMP', 'jump'), ('m3', 'label'), (':', 'colon'), ('foo', 'ident'), ('c', 'ident'), ('1', 'int'), ('+', 'add_op'), ('=', 'assign_op'), ('m4', 'label'), (':', 'colon')]
\Код програми: 
varpow1 = 2^2^3
varpow2 = 2^(2^3)

counter = 0
do {
  counter = counter + 1
    counter2 = 0
  do {
    counter2 = counter2 + 1
  } while (counter2 < 3)
  
} while (counter < 5)

a= 2 + 2
c = 3 * 3
z = (a + 1 ) * (a - 1)

var = 2 + 2 * 2
var2 = (2 + 2) * 2

d = z^a
b = a > z
b =  3.4 / 3.2


if (a < c) {
  foo = a + 1
} else {
  foo = c + 1
}


Таблиця змінних:
 {'varpow1': (1, 'int', 256.0), 'varpow2': (2, 'int', 256.0), 'counter': (3, 'int', 5), 'counter2': (4, 'int', 3), 'a': (5, 'int', 4), 'c': (6, 'int', 9), 'z': (7, 'int', 15), 'var': (8, 'int', 6), 'var2': (9, 'int', 8), 'd': (10, 'int', 50625.0), 'b': (11, 'float', 1.0625), 'foo': (12, 'int', 5)}
```

