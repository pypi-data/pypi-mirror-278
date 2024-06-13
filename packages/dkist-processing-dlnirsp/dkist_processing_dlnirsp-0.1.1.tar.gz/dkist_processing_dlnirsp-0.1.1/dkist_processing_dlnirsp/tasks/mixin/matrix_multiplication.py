"""Mixin for doing matrix multiplication on high-dimensional arrays."""
# TODO: Once `*-math` is updated, get rid of this.
import numpy as np


class MatrixMultiplicationMixin:
    """
    Helpers for doing complicated matrix multiplication.

    Doesn't follow naming conventions because eventually these functions will be imported from `dkist-procesing-math`.
    """

    @staticmethod
    def nd_left_matrix_multiply(
        *, vector_stack: np.ndarray, matrix_stack: np.ndarray
    ) -> np.ndarray:
        """
        Left-multiply an arbitrarily dimensioned stack of vectors by a similarly dimensioned stack of matrices.

        In math:

            result = M @ v

        where M is a matrix with dimensions ([n1, ...nn], D1, D2)
        and v is a vector with dimensions ([n1, ...nn], D2).

        The higher-order dimensions (n1, ...nn) can be anything (or nothing), but they must be the same for M and v.

        Parameters
        ----------
        vector_stack : np.ndarray
            ([n1, ...nn], D2) ND stack of vectors with length D2

        matrix_stack : np.ndarray
            ([n1, ...nn], D1, D2) ND stack of matrices with shape (D1, D2)


        Returns
        -------
        np.ndarray
            ([n1, ...nn], D1) ND stack of vectors with length D1
        """
        return np.sum(matrix_stack * vector_stack[:, :, None, :], axis=3)
