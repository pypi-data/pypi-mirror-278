The `elliptic` package implements elliptic curves over various fields.

## Introduction

An elliptic curve is defined by an equation over a field. For a point on the curve, that means the values of its coordinates are elements of the field. Elliptic curves can support a group structure: their points can be added and substracted together, like numbers.

The `elliptic.curves` module implements elliptic curves. An interface for fields is specified in the `elliptic.abc` module. This package provides several field implementations:
- `elliptic.mod`: modular fields
- `elliptic.fin`: Galois fields
- `elliptic.inf`: infinite fields

The implementation is not concerned with cryptographic safety. It cares for results being correct, but not secure.

## Algebra

A field is a set whose elements behave like natural numbers: they can be added, substracted, multiplied and divided. The most commonly known are the field of rational numbers, the field of real numbers and the field of complex numbers.

### Groups

A binary operation `+` forms a group over a set *G* when:
- it is a closure of *G*  
  if *x* and *y* are in *G* then so is *x* + *y*
- it has a neutral element 0  
  *x* = *x* + *y* if and only if *y* = 0
- it is associative  
  *x* + (*y* + *z*) = (*x* + *y*) + *z*
- it is commutative  
  *x* + *y* = *y* + *x*
- it is invertible  
  for any *x* there is *y* such that *x* + *y* = 0

The simplest group has a single element 0. The most commonly known is the group of integers. Groups can be used to define more elaborate structures.

Group implementations should provide an operator with a return type of `typing.Self`. Python operators can be overloaded by special methods such as `__add__()` to allow for infix notation. Conventionally, such methods should accept an operand of type `typing.Any` and return `NotImplemented` as appropriate.

### Fields

Two binary operations `+` and `*` form a field over a set *F* when:
- `+` forms a group over *F* with a neutral element 0
- `*` forms a group over *F* (except 0) with a neutral element 1
- `*` is distributive over operation `+`  
  *x* * (*y* + *z*) = *x* * *y* + *x* * *z*

Fields need not be infinite. Modular integers are an example: for any prime number *p*, the integers from 0 to *p*-1 trivially form a field.
Every element has a unique multiplicative inverse, which can be computed using Fermat's little theorem.

When a field is finite, its order is the number of the elements it contains. Modular integers represent fields whose order is a prime number.

### Spaces

A scalar is an element of a field *F*. A vector over *F* is a series of scalar coefficients. The length of the series, which may be infinite, is called the dimension of the vector.

Vectors of a specific dimension form a vector space. They can be added and substracted as elements of a group. They can also be multiplied by a scalar using the @ operation.

Three binary operations `+`, `*` and `@` form a vector space *K* over a set *F* when:
- `+` and `*` form a field over *F*
- `+` forms a group over *K*
- `@` is a closure of *K*  
  if *f* is in F and *x* is in *K* then (*f* @ *x*) is in *K*
- `@` is linear  
  *f* @ (*x* + *y*) = (*f* @ *x*) + (*f* @ *y*)  
  if *f* @ *x* = *f* @ *y* then either *f* = 0 or *x* = *y*
- `@` is compatible with `*`  
  (*f* * *g*) @ *x* = *f* @ (*g* @ *x*)

This is a minimal definition and some vector spaces support much more elaborate structures. Metric spaces have a unary norm operator, which returns the scalar magnitude of a vector, defining the notion of distance. Hilbert spaces have a binary operator called the scalar product, which defines the notion of angle.

### Polynomials

The univariate polynomials over a field *F* form an infinite-dimensional vector space. The vector coefficients are represented by a polynomial expression of a single variable.

The product of two vectors can be defined using their polynomial representation. Polynomials can be uniquely decomposed into a product of irreducible factors, akin to the prime factors composing an integer. Similarly, polynomials support an equivalent of Euclidian division and concepts such as divisibility.

The dimension of the polynomial space is infinite even if the field *F* is finite, because the degree of polynomials is unbounded. It is always trivial to construct a polynomial of any arbitrary degree.

However, for a given integer *n*, the polynomials whose degree is lower than *n* form a finite-dimensional vector space. If the underlying field is finite, then such a bounded polynomial space contains a finite number of vectors.

The infinite-dimensional space of univariate polynomials over modular integers is implemented in the `elliptic.poly` module.

### Galois extension

For a prime number *p*, the modular integers from 0 to *p*-1 are a representation of the finite field of order *p*. For a positive integer *d*, that field can be extended as a *d*-dimensional vector space and provided with a multiplicative operation, through a process called Galois extension.

The univariate polynomials with modular integer coefficients between 0 and *p*-1 whose degree is lower than *d* form a vector space *G* with *p*<sup>*d*</sup> elements.

The regular multiplication of polynomials is not a closure of *G*. However, by choosing an irreducible polynomial of degree *d*, the product can become a closure, using the remainder of the Euclidian division by that polynomial.

The space *G* now supports regular vector addition and the herebefore defined multiplication. Together they form a field of order *p*<sup>*d*</sup> called a Galois field.

## Geometry

An elliptic curve is an algebraic, non-singular, smooth, cubic curve in the projective plane of a field. Projective curves exist as a two-dimensional object in a three-dimensional space. They contain points at infinity, at which parallel lines intersect.

Elliptic curves have a group structure, so their points can be added together. An elliptic curve contains a single point at infinity, which is the neutral element of the group.

### Projective planes

A projective plane is constructed in a three-dimensional vector space. Formally, the projective plane is the quotient of the space by the equivalence class of the proportionality relation.

Two vectors *v* and *w* are equivalent when there is a non-zero scalar *s* such that *v* = *s* @ *w*. Their equivalence class represents a point of the projective plane.

In order to fix the points at infinity, the plane must be oriented in space. By convention, the normal plane of the applicate axis is chosen. The points at infinity are the classes of vectors (*X*, *Y*, *Z*) such that *Z* = 0.

With the plane conceptually fixed, homogeneous coordinates *x* = *X*/*Z* and *y* = *Y*/*Z* can be defined. Except for the points at infinity, the projective plane is then equivalent to the plane at *Z* = 1.

The projective plane thereby constructed comes with a couple of neat properties:
- There is exactly one line between two points
- There is exactly one point between two lines

The points at infinity are not conceptually anywhere on the plane. They form a line at the edge of the plane, infinitely far and ever unreachable. Like the horizon: where parallel lines intersect.

### Elliptic curves

An elliptic curve depends on two scalar coefficients *a* and *b*. It is defined by a cubic equation in Weierstrass form, for the homogeneous coordinates *x* and *y* of a projective point:

> *x*<sup>3</sup> + *a* * *x* + *b* = *y*<sup>2</sup>

The curve must be non-singular, so its coefficients *a* and *b* must not verify:

> 4 * *a*<sup>3</sup> + 27 * *b*<sup>2</sup> = 0

As cubic, non-singular curves on a projective plane, elliptic curves verify Bézout's theorem. If a line has at least two intersection points with such a curve, then it has exactly three. Intersection is meant with multiplicity, so tangent points count twice.

In the projective plane, the curve is symmetric by reflection around the abscissa axis. It becomes asymptotically vertical at larger abscissa up to infinity. Its intersection with the line at infinity is a single point *o*.

The equation in Weierstrass form contains only even-degree terms of *y*, showing the reflectional symmetry of the curve. The point *o* is the class of vector (0, 1, 0) as shown by the equation in full form:

> *X*<sup>3</sup> + *a* * *X* * *Z*<sup>2</sup> + *b* * *Z*<sup>3</sup> = *Y*<sup>2</sup> * *Z*

### Group structure

Now the sum *p* + *q* of two points *p* and *q* can be defined. The line joining *p* and *q* intersects with the curve at a third point *p* @ *q*. However, that operation is not associative: *p* @ (*q* @ *r*) may not always equal (*p* @ *q*) @ *r*.

Instead, consider the line joining the points *o* and *p* @ *q*:

> *p* + *q* = *o* @ (*p* @ *q*)

Operation + forms a group over the points of the curve. Its neutral element is the point *o*.

It is now possible to multiply points by an integer. Multiplication is defined recursively by adding a point to itself, taking successive tangents on the curve to find the next point.

If the curve is defined over a finite field, then it has a finite number of points. As a finite group element, a curve point *p* has an order: the lowest nonzero integer *n* such that:

> *n* * *p* = *o*

A point that cycles through all other points when summed with itself before adding up to infinity is called a generator. The order of the curve is the order of its generators: it is the number of points on the curve.

## Algorithmics

The additive operation on elliptic curve points is implemented geometrically. As preliminary definitions:

> -(*x*, *y*) = (*x*, -*y*)

> -*o* = *o*

The sum of two points can then be computed. If they are opposites of one another, then the sum is the point at infinity. If any of the two points is at infinity, the result is the opposite of the the other. Otherwise, the slope of the line joining the points can be calculated; if the two points are equal, then the derivative of the curve is used to get the slope of the tangent line. Solving the curve equation using the slope gives the third intersection point, the opposite of which is the sum of the two points.

### Discrete logarithm

The complexity of adding two points together is linear. The product of a point by an integer *n* can be implemented using fast multiplication with O(log(*n*)) complexity, so it is also linear.

Given two points *p* and *n* * *p*, the problem of computing *n* is called the discrete logarithm. Its complexity is O(sqrt(*k*)) which is exponential respective to the order *k* of the curve. That makes it much more difficult than calculating *n* * *p* from *n* and *p*.

Finite curves implement Shanks' algorithm (known as "baby step giant step") in order to solve the discrete logarithm:

```python
>>> from elliptic.curves import P256
>>> prod = 123456 * P256.point         # Fast
>>> P256.curve.bsgs(P256.point, prod)  # Slow
123456
```

### Notes

Besides "baby step giant step", various algorithms are used throughout this package:
- Modular square root uses the Tonelli-Shanks algorithm
- Polynomial square-free factorization uses Yun's algorithm
- Polynomial distinct-degree factorization uses Gauss' algorithm
- Polynomial equal-degree factorization uses the Cantor–Zassenhaus algorithm
- Galois square root uses the Adleman-Manders-Miller algorithm

## License

The `elliptic` package is distributed under the terms of the [GNU General Public License v3.0+](https://www.gnu.org/licenses/).

The curve definitions are republished courtesy of the [National Institute of Standards and Technology](https://www.nist.gov).

***

Copyright © 2023-2024 Nicolas Canceill
