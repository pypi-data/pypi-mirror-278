from .interface import Interface
from .operators import sqrt, cos, sin, tan
from .utils import anyToMetal, anyToCtypes, anyToNumpy

import os
import subprocess

curr_path = os.path.dirname(__file__)

def build():
    cd_to_path = f"cd {curr_path}/lib"
    clone_git_repo = f"git clone https://github.com/Al0den/metalgpu"
    cd_to_c_code = f"cd metalgpu/metal-gpu-c"
    clone_metal_cpp = f"git clone https://github.com/bkaradzic/metal-cpp"
    cmake_cmd = f"cmake ."
    install = f"make install"
    copy_to_correct_path = f"cp ./libmetalgpucpp-arm.dylib ../.."
    remove_prev_folder = f"rm -rf metalgpu"
    remove_down_folder = f"rm -rf ../../metalgpu"
 
    final_command = f"{cd_to_path} && {remove_prev_folder} && {clone_git_repo} && {cd_to_c_code} && {clone_metal_cpp} && {cmake_cmd} && {install} && {copy_to_correct_path} && {remove_down_folder}"
    subprocess.run(final_command, shell=True)

import platform
assert platform.system() == "Darwin", "[MetalGPU] MetalGPU is only supported on macOS"

if __name__=="__main__":
    build()
else:
    assert os.path.isfile(curr_path + "/lib/libmetalgpucpp-arm.dylib"), "[MetalGPU] Error: libmetalgpucpp-arm.dylib not found. Please run 'python -m metalgpu' to build the library."
