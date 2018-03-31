# 10x Localization Project

This repository contains code developed as one of [Innolitic's](http://innolitics.com) [10x mini-projects](http://innolitics.com/10x/discussions/).

## Introduction

- problem has shown up on multiple client projects
- sensors; integration vs sampling
- background
- noise
- relative size of the object

## Formalized 1D Problem

We mode the underlying object that we are imaging as a continuous, 1D function over the domain [0, 100].

This function has the form:

I(x) = A*rect((x - c)/w) + b(x)

Where

A = "Amplitude of the object"
c = "Center of the object"
w = "Width of the object
b(x) = "Background function".

We form an image of this object using an imaging sensor with 100 elements.  The sensor elements don't fill their enire range, but they integrate where they do.

## Ideas

- Investigate thresholded center of mass vs un-thresholded center of mass
- Generalize to 2D
- Determine how the noise distribution affects the problem
- Investigate different types of background functions

## References

- [Wikipedia article about super-resolution imaging](https://en.wikipedia.org/wiki/Super-resolution_imaging)
