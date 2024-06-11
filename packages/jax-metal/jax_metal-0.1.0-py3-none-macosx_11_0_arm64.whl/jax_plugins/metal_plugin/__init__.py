from pathlib import Path
import jax._src.xla_bridge as xb

def initialize():
  platform_lib_name = "pjrt_plugin_metal_14.dylib"
  path = Path(__file__).resolve().parent / platform_lib_name
  xb.register_plugin("METAL",
                     priority=500,
                     library_path=str(path),
                    )
  
def version():
  return '0.1.0'
