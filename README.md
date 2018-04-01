# 10x Localization Project

This repository contains code developed as one of [Innolitic's](http://innolitics.com) [10x mini-projects](http://innolitics.com/10x/discussions/).

## Introduction

- problem has shown up on multiple client projects
- sensors; integration vs sampling
- background
- noise
- relative size of the object

Problem: find the location of the object (usually a fiducial used for image registration) as accurately as possible.

## Formalized 1D Problem

We mode the underlying object that we are imaging as a continuous, 1D function over the domain [0, 100].

This function has the form:

```
I(x) = rect((x - c)/w) + b(x)
```

Where

- `c` = "Center of the object"
- `w` = "Width of the object
- `b(x)` = "Background function".

For now, we assume that the background function is linear, that is:

```
I(x) = A*rect((x - c)/w) + b0 + x*b1
```

Now that we have modeled the underlying object, we need to model the processing of converting this object into a image.

Assume an image of this object is formed using an imager with 100 sensor elements.  For now we assume that each sensor element acts as a perfect integrator.  I.e.,

```
I_integrated[k] = \int_k^{k+1} I(x) dx
```

for `k` = 0 to 99.

In the other extreme, each sensor element acts as a perfect sampler.  I.e.,

```
I_sampled[k] = I(k + 0.5) * alpha
```

where alpha is an arbitrary constant.

In practice, one would expect image sensors to be a combination.  If `s` is a number between 0 and 1, representing how full the image sensor is:

```
I_b[k] = \int_{k + s/2}^{k + 1 - s/2} I(x) dx
```

The bit-depth of the Analog to Digital converter also plays a roll in image formation.

Finally, we expect a certain amount of noise to be introduced by the sensor, readout machinery, etc.  For now, we assume that all of the noise is zero-mean Gaussian noise (this is certainly not the case).

For now, we model these effects using:

- `N` = "number of bits available in A to D"
- `A_max` = "maximum measurable value"
- `A_min` = "minimum measurable value"
- `s` = "relative size of the sensor elements, [0, 1]"
- `sigma` = "standard deviation of the gaussian noise".

## Problem

We are interested in developing an algorithm that can determine object's center, `c`, as accurately as possible given an `I[k]`.

We know `N`, `A_min`, `A_max`, and `s` before hand, since they are attributes of the imaging system.  We may also know the approximate ranges that the image `w`, `b0`, `b1`, and `sigma` will take.

We can also assume that `c` is in the middle of the image, i.e., `c \in [25, 75]`.

If our algorithm guesses `c_expected`, then we define the localization error to be:

```
E = |c - c_expected|
```

## Questions to investigate

- What algorithm have the lowest mean localization error?
- For a given algorithm, what is the relationship between mean localization error an `X`?  (where `X` is a paramater of our model, such as `w`, `N`, `b0`, `b1`, `s`, or `sigma`).
- Generalize to 2D
- Investigate the effect of different types of background functions

## References

- [Wikipedia article about super-resolution imaging](https://en.wikipedia.org/wiki/Super-resolution_imaging)
