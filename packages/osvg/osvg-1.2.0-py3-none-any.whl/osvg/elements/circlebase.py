"""
Module to define class for SVG ellipse elements.
"""

import osvg.elements.elementbase


class CircleBase(osvg.elements.elementbase.SVGElement):
    """
    Meta class for circle like elements.
    """

    def create_default_connectors(self) -> None:
        """
        Create Positions as connectors and add them.
        """
        self.add_connector_at_angle(angle=225, name="top-left", respect_rotation=True)
        self.add_connector_at_angle(angle=270, name="top-center", respect_rotation=True)
        self.add_connector_at_angle(angle=315, name="top-right", respect_rotation=True)
        self.add_connector_at_angle(
            angle=180, name="center-left", respect_rotation=True
        )
        self.add_connector(self.position, "center")
        self.add_connector_at_angle(angle=0, name="center-right", respect_rotation=True)
        self.add_connector_at_angle(
            angle=135, name="bottom-left", respect_rotation=True
        )
        self.add_connector_at_angle(
            angle=90, name="bottom-center", respect_rotation=True
        )
        self.add_connector_at_angle(
            angle=45, name="bottom-right", respect_rotation=True
        )

    def add_connector_at_angle(
        self,
        angle: float | int | osvg.float.Float,
        name: str,
        respect_rotation: bool = False,
    ):
        """
        Add a connector at element's border at the angle
        in relation to the center.
        """
        if not issubclass(type(angle), osvg.float.Float):
            angle = osvg.float.Const(angle)
        if respect_rotation:
            calc_angle = angle
        else:
            calc_angle = osvg.float_math.Sum(
                angle, osvg.float_math.InvertedSign(self.rotation)
            )
        relative_shifted_position = self.angled_position(angle=calc_angle)
        if not respect_rotation:
            relative_shifted_position = osvg.positions.RotatedPosition(
                origin=relative_shifted_position,
                center=osvg.positions.Position(),
                angle=self.rotation,
            )

        calculated_position = osvg.positions.ShiftedPosition(
            origin=self.position,
            x_shift=relative_shifted_position.x,
            y_shift=relative_shifted_position.y,
        )
        return self.add_connector(
            position=calculated_position,
            name=name,
            respect_rotation=respect_rotation,
        )

    def angled_position(self, angle: osvg.float.Float) -> osvg.positions.Position:
        """
        Return position on border at given angle
        """
        raise NotImplementedError
