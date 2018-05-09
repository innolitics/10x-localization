# Estimating Fiducial Localization Error Using Simulations

Audience:

- Potential team members (want to give developers a feeling for what it is like working with us)
- Potential customers at larger companies (a CTO or high-level engineer who is searching for a team that is familiar with registration)
- Potential customers at a startup
- Google (want to have keywords that are related to medical imaging)

## Image Registration

Image registration is the process of transforming two or more images into the same coordinate system.

For example, we may want to register:

- a high-resolution CT of a patient, used to planning radiation therapy or an image-guided surgery
- a low-resolution cone-beam CT of the immobilized patient, taken in the radiation therapy device or on the surgery table.

Registering these images will ensure that the patient's position within the planning CT coordinate system is known.  Registration errors will result in misalignment of the patient, and ultimately may mean that healthy tissue is irradiated instead of the tumor, or that the surgery is ineffective.

Many medical imaging applications require registration is a frequently encountered building block of more complex image processing algorithms.

## Types of Registration Algorithms

## Quick Overview of Fiducial-Based Registration Algorithms

## Relationship Between FLE and Registration Error

## Factors that can Affect FLE

## Using a Simulator to Estimate FLE

## Reece Results

## Dillon Results

## Zach Results

## Willy Results

## References

- Medical Imaging Registration article that we read in our 10x discussion
- The newer registration article
- The fiducial localization article for particle tracking
