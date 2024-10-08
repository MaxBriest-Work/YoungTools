from typing import Iterator

from sage.misc.table import table
from sage.rings.integer_ring import ZZ


class YoungDiagram(object):

    def __mul__(self, other: "YoungDiagram") -> "YoungDiagram":
        assert isinstance(
            other, YoungDiagram
        ), "The input for `other` needs to be a Young diagram."
        return YoungDiagram.Construct_From_Binary_Description(
            self._binary_description + other._binary_description
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if self.__repr__() == other.__repr__():
                return True
            else:
                return False
        else:
            return False

    def __ge__(self, other: "Bundle") -> bool:
        """
        Test if a first Young diagram `self` is greater than or equal to an-
        other Young diagram `other`.

        ALGORITHM:

        We test if either `self` is equal to `other` or `other` is smaller than
        `self`. Hence, we need implementations for both methods `__eq__` and
        `__lt__`.
        """
        return (self == other) or (self > other)

    def __gt__(self, other: "Bundle") -> bool:
        """
        Test if a first Young diagram `self` is greater than another Young dia-
        gram `other`.

        ALGORITHM:

        We test if `other` is smaller than `self`. Hence, we need implementa-
        tions for the method `__lt__`.
        """
        assert isinstance(
            other, YoungDiagram
        ), "The input for `other` needs to be an object of the class `YoungDiagram`."
        return other < self

    def __init__(self, height: int, width: int, usual_description: tuple[int]) -> None:
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
        # Usual description
        assert isinstance(
            usual_description, tuple
        ), "The input for `usual_description` needs to be a tuple."
        assert (
            len(usual_description) <= self._height
        ), "The length of `usual_description` (number of rows) needs to be less than or equal to the height {h}.".format(
            h=self._height
        )
        stock = []
        previous_row_length = self._width
        for row_counter, row_length in enumerate(usual_description):
            assert (
                row_length in ZZ
            ), "The {i}-th entry in `usual_description` needs to be an integer.".format(
                i=row_counter
            )
            assert (
                0 <= row_length
            ), "The {i}-th entry in `usual_description` needs to be non-negative.".format(
                i=row_counter
            )
            assert (
                row_length <= previous_row_length
            ), "The {i}-th row length needs less than or equal to the previous one.".format(
                i=row_counter
            )
            stock += [row_length]
            previous_row_length = row_length
        self._usual_description = tuple(stock + (self._height - len(stock)) * [0])
        # Binary description
        x, y = (
            0,
            self._height,
        )
        self._binary_description = ""
        for step in range(self._n):
            if y == 0:
                self._binary_description += "R"
            else:
                if x < self._usual_description[y - 1]:
                    self._binary_description += "R"
                    x += 1
                else:
                    self._binary_description += "U"
                    y += -1

    def __le__(self, other: "Bundle") -> bool:
        """
        Test if a first Young diagram `self` is less than or equal to another
        bundle `other`.

        ALGORITHM:

        We test if either `self` is equal to `other` or `self` is smaller than
        `other`. Hence, we need implementations for both methods `__eq__` and
        `__lt__`.
        """
        return (self == other) or (self < other)

    def __len__(self) -> int:
        """
        Returns the length of `self`.
        """
        return self._n

    def __lt__(self, other: "Bundle") -> bool:
        """
        Test if a first Young diagram `self` is less than another Young diagram
        `other` with respect to the lexicographical order.
        """
        assert isinstance(
            other, YoungDiagram
        ), "The input for `other` needs to be a Young diagram."
        assert (
            self._height == other._height
        ), "The two Young diagrams have different height."
        assert (
            self._width == other._width
        ), "The two Young diagrams have different width."
        for row_counter in range(self._height):
            e1 = self._usual_description[row_counter]
            e2 = other._usual_description[row_counter]
            if e1 < e2:
                return True
            elif e1 == e2:
                pass
            else:
                return False
        return False

    def __repr__(self) -> tuple:
        """
        Returns a developer-friendly description of `self`.
        """
        return self._height, self._width, self._usual_description

    def __rshift__(self, step: int = 1) -> "YoungDiagram":
        return self.cyclic_action(step)

    def __str__(self) -> str:
        """
        Returns a user-friendly description of `self`.
        """
        return "Young diagram of height {h}, width {w}, and with partition {p}.".format(
            h=self._height, w=self._width, p=self._usual_description
        )

    def column_lengths(self) -> tuple[int]:
        return tuple(
            [
                sum(
                    [
                        1
                        for row_length in self.row_lengths()
                        if column_counter <= row_length - 1
                    ]
                )
                for column_counter in range(self._width)
            ]
        )

    def complement(self) -> "YoungDiagram":
        old = self._binary_description
        new = old[::-1]
        return YoungDiagram.Construct_From_Binary_Description(new)

    @staticmethod
    def Construct_From_Binary_Description(string: str) -> "YoungDiagram":
        n = len(string)
        height = string.count("U")
        width = string.count("R")
        assert (
            n == height + width
        ), "The binary description contains a symbol different from `U` or `R`."
        column_heights = []
        column_height = height
        for value in string:
            if value == "U":
                column_height += -1
            elif value == "R":
                column_heights += [column_height]
        row_widths = [
            sum(
                [
                    1
                    for column_height in column_heights
                    if row_counter <= column_height - 1
                ]
            )
            for row_counter in range(height)
        ]
        usual_description = tuple(row_widths)
        return YoungDiagram(
            height=height, width=width, usual_description=usual_description
        )

    @staticmethod
    def Construct_From_Usual_Description(*mu: tuple[int]) -> "YoungDiagram":
        height = len(mu)
        for counter, entry in enumerate(mu):
            assert entry in ZZ, "The {i}-th entry needs to be an integer.".format(
                i=counter
            )
        width = max(mu)
        usual_description = tuple(mu)
        return YoungDiagram(
            height=height, width=width, usual_description=usual_description
        )

    def cyclic_action(self, steps: int = 1) -> "YoungDiagram":
        if 0 < self._n:
            assert steps in ZZ, "The input for `steps` needs to be an integer."
            steps = steps % self._n
            old = self._binary_description
            new = old[self._n - steps :] + old[:-steps]
            return YoungDiagram.Construct_From_Binary_Description(new)
        else:
            raise NotImplementedError()

    def cyclic_orbit(self) -> Iterator["YoungDiagram"]:
        """
        Runs through the cyclic orbit of `self`.
        """
        first_object = self
        current_object = first_object
        while True:
            yield current_object
            current_object = current_object >> 1
            if current_object == first_object:
                break

    def is_lower_triangular(self) -> bool:
        return self.complement().is_upper_triangular()

    def is_upper_triangular(self) -> bool:
        if 0 < self._height:
            stock = [
                row_length <= self._width * (self._height - row_counter) / self._height
                for row_counter, row_length in enumerate(self._usual_description)
            ]
            return not False in stock
        else:
            raise NotImplementedError()

    def orbit_length(self) -> int:
        """
        The numerical characteristic o(lambda).
        """
        initial_string = self._binary_description
        previous_string = initial_string
        counter = 0
        while True:
            counter += 1
            next_string = previous_string[self._n - 1 :] + previous_string[:-1]
            if next_string == initial_string:
                return counter
            else:
                previous_string = next_string

    def row_lengths(self) -> tuple[int]:
        return self._usual_description

    def show(self) -> "Table":
        if 0 < self._height and 0 < self._width:
            return table(
                rows=[
                    row_length * ["x"] + (self._width - row_length) * [" "]
                    for row_length in self._usual_description
                ],
                frame=True,
            )
        else:
            return None

    def slope(self) -> "Rational":
        """
        The numerical characteristic s(lambda).
        """
        if 0 < self._width:
            return self._height / self._width
        else:
            raise NotImplementedError()

    def steps_to_next_lower_triangular(self):
        """
        The numerical characteristic d(lambda).
        """
        steps = 0
        current = self
        while steps < self._n:
            if current.is_lower_triangular():
                return steps
            else:
                current = current >> 1
                steps += 1

    def transpose(self) -> "YoungDiagram":
        return YoungDiagram(
            height=self._width,
            width=self._height,
            usual_description=self.column_lengths(),
        )

    def volume(self) -> int:
        return sum(self._usual_description)
