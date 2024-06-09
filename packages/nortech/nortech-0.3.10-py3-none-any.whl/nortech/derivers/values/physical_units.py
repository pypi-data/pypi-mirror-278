from pint import UnitRegistry

from nortech.derivers.values.physical_units_schema import (
    PhysicalQuantity,
    PhysicalUnit,
)

unit_registry = UnitRegistry()

temperature = PhysicalQuantity(
    name="Temperature",
    description="Temperature is a physical quantity that quantitatively expresses the attribute of hotness or coldness.",
    SIUnit=str(unit_registry.kelvin),
    SIUnitSymbol=f"{unit_registry.kelvin:~}",
)

kelvin = PhysicalUnit(
    name=str(unit_registry.kelvin),
    description="The Kelvin scale is an absolute scale, which is defined such that 0 K is absolute zero and a change of thermodynamic temperature T by 1 kelvin corresponds to a change of thermal energy kT by 1.380649x10-23 J.",
    symbol=f"{unit_registry.kelvin:~}",
    physicalQuantity=temperature,
)

celsius = PhysicalUnit(
    name=str(unit_registry.celsius),
    description="The Celsius scale is a temperature scale that is used in the United States and Canada. It is defined such that 0 °C is the freezing point of water and a change of temperature by 1 °C corresponds to a change of thermal energy of 1.15 J.",
    symbol=f"{unit_registry.celsius:~}",
    physicalQuantity=temperature,
)

fahrenheit = PhysicalUnit(
    name=str(unit_registry.fahrenheit),
    description="The Fahrenheit scale is a temperature scale that is used in the United States and Canada. It is defined such that 0 °F is the freezing point of water and a change of temperature by 1 °F corresponds to a change of thermal energy of 0.5555555555555556 J.",
    symbol=f"{unit_registry.fahrenheit:~}",
    physicalQuantity=temperature,
)

rotational_frequency = PhysicalQuantity(
    name="Rotational Frequency",
    description="Rotational frequency, also known as rotational speed or rate of rotation, is the frequency of rotation of an object around an axis.",
    SIUnit=str(unit_registry.rps),
    SIUnitSymbol=f"{unit_registry.rps:~}",
)

rpm = PhysicalUnit(
    name=str(unit_registry.rpm),
    description="Revolutions per minute (abbreviated rpm, RPM, rev/min, r/min, or r⋅min−1) is a unit of rotational speed (or rotational frequency) for rotating machines.",
    symbol=f"{unit_registry.rpm:~}",
    physicalQuantity=rotational_frequency,
)

pressure = PhysicalQuantity(
    name="Pressure",
    description="Pressure (symbol: p or P) is the force applied perpendicular to the surface of an object per unit area over which that force is distributed.",
    SIUnit=str(unit_registry.pascal),
    SIUnitSymbol=f"{unit_registry.pascal:~}",
)

pascal = PhysicalUnit(
    name=str(unit_registry.pascal),
    description="The pascal (symbol: Pa) is the unit of pressure in the International System of Units (SI).",
    symbol=f"{unit_registry.pascal:~}",
    physicalQuantity=pressure,
)

speed = PhysicalQuantity(
    name="Speed",
    description="In everyday use and in kinematics, the speed (commonly referred to as v) of an object is the magnitude of the change of its position over time or the magnitude of the change of its position per unit of time; it is thus a scalar quantity.",
    SIUnit=str(unit_registry("m/s").units),
    SIUnitSymbol=f"{unit_registry('m/s').units:~}",
)

knots = PhysicalUnit(
    name=str(unit_registry.knot),
    description="The knot (/nɒt/) is a unit of speed equal to one nautical mile per hour, exactly 1.852 km/h (approximately 1.151 mph or 0.514 m/s).",
    symbol=f"{unit_registry.knot:~}",
    physicalQuantity=speed,
)

percentage = PhysicalQuantity(
    name="Percentage",
    description="A percentage is a number or ratio expressed as a fraction of 100.",
    SIUnit=str(unit_registry.percent),
    SIUnitSymbol=f"{unit_registry.percent:~}",
)

percent = PhysicalUnit(
    name=str(unit_registry.percent),
    description="The percent symbol (%) is used to express a ratio or proportion as a fraction of 100.",
    symbol=f"{unit_registry.percent:~}",
    physicalQuantity=percentage,
)

angle = PhysicalQuantity(
    name="Angle",
    description="An angle is the figure formed by two rays, called the sides of the angle, sharing a common endpoint, called the vertex of the angle.",
    SIUnit=str(unit_registry.radian),
    SIUnitSymbol=f"{unit_registry.radian:~}",
)

degree = PhysicalUnit(
    name=str(unit_registry.degree),
    description="A degree (°) is a measurement of plane angle, representing 1/360 of a full rotation.",
    symbol=f"{unit_registry.degree:~}",
    physicalQuantity=angle,
)

radian = PhysicalUnit(
    name=str(unit_registry.radian),
    description="A radian is the SI unit of angular measure, used in many areas of mathematics. The length of an arc of a unit circle is numerically equal to the measurement in radians of the angle that it subtends.",
    symbol=f"{unit_registry.radian:~}",
    physicalQuantity=angle,
)
