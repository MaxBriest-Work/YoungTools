from typing import Iterator

# from sage.calculus.var import var
from sage.combinat.integer_lists.invlex import IntegerListsLex
from sage.functions.other import floor

# from sage.matrix.constructor import matrix
# from sage.misc.table import table
# from sage.modules.free_module_element import vector
# from sage.rings.abc import SymbolicRing
from sage.rings.integer_ring import ZZ

# from homogeneous import *
from young.diagram import YoungDiagram

# from sage.rings.rational_field import QQ
# from sage.structure.element import Expression


class YoungDiagrams(object):

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if self.__repr__() == other.__repr__():
                return True
            else:
                return False
        else:
            return False

    def __init__(self, height: int, width: int) -> None:
        # Height
        assert height in ZZ, "The input for `height` needs to be an integer."
        assert 0 <= height, "The height needs to be non-negative."
        self._height = height
        # Width
        assert width in ZZ, "The input for `width` needs to be an integer."
        assert 0 <= width, "The width needs to be non-negative."
        self._width = width
        # n (half perimeter)
        self._n = self._height + self._width

    def __repr__(self) -> tuple:
        """
        Returns a developer-friendly description of `self`.
        """
        return self._height, self._width

    def __str__(self) -> str:
        """
        Returns a user-friendly description of `self`.
        """
        return "Young diagrams of height {h}, width {w}.".format(
            h=self._height, w=self._width
        )

    def get_minimal_upper_triangulars(self) -> Iterator[YoungDiagram]:
        cyclic_orbits = []
        for YD in self.get_upper_triangulars():
            YD_did_already_appear = False
            for cyclic_orbit in cyclic_orbits:
                if YD in cyclic_orbit:
                    YD_did_already_appear = True
                    break
            if not YD_did_already_appear:
                minimal_object = YD
                cyclic_orbit = []
                for fellow in YD.cyclic_orbit():
                    if fellow.is_upper_triangular():
                        cyclic_orbit += [fellow]
                        if fellow < minimal_object:
                            minimal_object = fellow
                cyclic_orbits += [cyclic_orbit]
                yield minimal_object

    def get_upper_triangulars(self) -> Iterator[YoungDiagram]:
        if 0 < self._height:
            ceiling = [
                floor(self._width * (self._height - row_counter - 1) / self._height)
                for row_counter in range(self._height)
            ]
            usual_descriptions = [
                tuple(usual_description)
                for usual_description in IntegerListsLex(
                    max_part=self._width,
                    length=self._height,
                    ceiling=ceiling,
                    max_slope=0,
                )
            ]
            usual_descriptions.reverse()
            return (
                YoungDiagram(self._width, self._height, usual_description)
                for usual_description in usual_descriptions
            )
        else:
            raise NotImplementedError()

    def slope(self) -> "Rational":
        if 0 < self._width:
            return self._height / self._width
        else:
            raise NotImplementedError()
