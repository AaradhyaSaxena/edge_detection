# edge_detection

Implementation of the paper "Detecting Faint Curved Edges in Noisy Images".
Authors : Sharon Alpert, Meirav Galun, Boaz Nadler, Ronen Basri

Abstract. A fundamental question for edge detection is how faint an
edge can be and still be detected. In this paper we offer a formalism
to study this question and subsequently introduce a hierarchical edge
detection algorithm designed to detect faint curved edges in noisy im-
ages. In our formalism we view edge detection as a search in a space
of feasible curves, and derive expressions to characterize the behavior of
the optimal detection threshold as a function of curve length and the
combinatorics of the search space. We then present an algorithm that
efficiently searches for edges through a very large set of curves by hi-
erarchically constructing difference filters that match the curves traced
by the sought edges. We demonstrate the utility of our algorithm in
simulations and in applications to challenging real images.

Steps:
1. Create tiles of size 5x5 in the image (either resize/crop the image to ensure it is multiple of 5x5, or pad)

2. For each tile of 5x5, for each pixel pair (p1, p2) on the boundaries of the 5x5 tile (I have written for loops i=0 to 4 and j-0 to 4, which is wrong because that will also include pixels inside), compute response(p1, p2) as follows.

    - Compute L(p1, p2) - L is infinity norm, i.e. max of absolutes of the elements of the vector. 
    In this case, p1 and p2 are 2-dimensional vectors, so it means max(abs(p1.x - p2.x), abs(p1.y - p2.y)). 
    Note that we have to incorporate 'trapezoidal rule' here - for now please 
    add a comment to the code saying this has to be done, will be done later.

    - Compute F(p1, p2) - integration of intensities of pixels from p1 to p2 divided by L(P1, p2). 
    Please add comment to the code that this is to be computed using Bicubic interpolation, trapezoidal rule later. 
    For now I will write an approx integration function and send.

   - quadrilateralResp and parallelogramResp functions I think are fine, use them as they are

   - onOppositeSide function to be written as discussed

   - tileResponse function is fine I think

   - computeTileResp - for loops to be changed to take into account only the pixels on borders of the 5x5 tile 
   and not middle ones
