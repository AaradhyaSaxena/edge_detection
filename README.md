# edge_detection

Implementation of the paper "Detecting Faint Curved Edges in Noisy Images".
Authors : Sharon Alpert, Meirav Galun, Boaz Nadler, Ronen Basri

Abstract. A fundamental question for edge detection is how faint an
edge can be and still be detected. In this paper we offer a formalism
to study this question and subsequently introduce a hierarchical edge
detection algorithm designed to detect faint curved edges in noisy images. 
In our formalism we view edge detection as a search in a space
of feasible curves, and derive expressions to characterize the behavior of
the optimal detection threshold as a function of curve length and the
combinatorics of the search space. We then present an algorithm that
efficiently searches for edges through a very large set of curves by 
hierarchically constructing difference filters that match the curves traced
by the sought edges. We demonstrate the utility of our algorithm in
simulations and in applications to challenging real images.
