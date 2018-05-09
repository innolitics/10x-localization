# Estimating Fiducial Localization Error Using Simulations

Audience:

- Potential team members (want to give developers a feeling for what it is like working with us)
- Potential customers at larger companies (a CTO or high-level engineer who is searching for a team that is familiar with registration)
- Potential customers at a startup
- Google (want to have keywords that are related to medical imaging)

## Image Registration

Image registration is the process of transforming two or more images into the same coordinate system.

For example, we may want to register:

- a high-resolution CT of a patient, used to plan radiation therapy
- a low-resolution cone-beam CT of the immobilized patient, taken from within the [linac](https://en.wikipedia.org/wiki/Linear_particle_accelerator)

Registering these images will ensure that the patient's position within the planning CT coordinate system is known and can be adjusted.  Registration errors will result in misalignments going uncorrected, and less effective radiation therapy because healthy tissue will be irradiated instead of the tumor.

There are many types of registration problems, for example:

- registering a series of CTs taken of the same patient at different points in time
- registering a set of images from different patients
- registering an MRI with a CT
- registering a 2D x-ray projection with a 3D CT.

There are also types of registrations one can apply to these problems, for example:

- rigid (i.e., translation and rotation)
- affine (i.e., translation, rotation, reflections, and scaling)
- constrained non-rigid.

See references [1] and [2] for more general categorizations of registration problems.

## Types of Registration Algorithms

Overview of types of registration algorithms.

The most common approaches to 

## Fiducial-Based Registration Algorithms

## Fiducial Localization Error (FLE) and Registration Error

## Factors that Affect FLE

## Using a Simulator to Estimate FLE

## Reece Results

## Dillon Results

## Zach Results

## Willy Results

## References

- Medical Imaging Registration article that we read in our 10x discussion
- The newer registration article
- The fiducial localization article for particle tracking
