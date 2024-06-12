from .interface import Interface
from .operators import sqrt, cos, sin, tan
from .utils import anyToMetal, anyToCtypes, anyToNumpy

import platform
assert platform.system() == "Darwin", "[MetalGPU] MetalGPU is only supported on macOS"
