[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

# computor_v1
Computor v1 is a simple secondary degree equation solver.
It takes as argument a string representing an equation of degree n.
The program then reduces the equation so that it is of the form:
 
![equation](http://latex.codecogs.com/gif.latex?$\sum_{i=0}^n$&space;a_ix^{^{i}}&space;=&space;0)

It then solves the equation if the last non-null degree is lower or equal to two.


## Input

The input is a string representing a mathematical equation.
Examples of valid inputs :

X + 2 = 3  
2 * (X + 2) = -3  
(X + 2) * 2 = -5 -4*X  
-X - 2 * X^0 = -3  
-X - 2 * X^0 = -3 - 4*X  
-X - 2 * X^0 -(-3 - 4*X) = 0  
-X - 2 * X^0 *(-3 - 4*X) = 0  
-X - 2 * X^0 * (+3 - 4*X) = 0  
-X - 2 * X^0 - (-3 * 4*X) = 0  
X - 4 + 2*X + 30 = -4*X  
3 * X^0 + 2 * X^1 * (2 + 3 * X^1 - 2 * X) = -(32 + 2*X - X^2)  
X^4 - 9.7 * X^3 + 3 + 4 + X^0 = - 3 * X^1 * X^3  
12 + 2*X * 5*X + 5*X^1 = -2  
12 + 2*X * (5*X + 5*X^1) = -2  
(-3 + X - X^2)*(2 - 3*X) = 0  
X^2 + 3 - (2*X^2 + X) = -3*X^0  
(-1 -X)^2 = 0  
(-1 + X)^2 = X^2  
(3*X + 9) + (1 - X + 3*X^2)^3 = -X -X^3  
(3*X + 9) + (- X + 3*X^2)^3 = -X -X^3  
(3*X + 9) * (- X + 3*X^2)^3 = (-2*X^2 + 5)^4  
(3.7*X + 9) / (- X + 3*X^2)^3 = 1 / (-X -X^3)  

