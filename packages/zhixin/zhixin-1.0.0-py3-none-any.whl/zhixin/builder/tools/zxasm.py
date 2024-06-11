import SCons.Tool.asm  # pylint: disable=import-error

#
# Avoid forcing .S to bare assembly on Windows OS
#

if ".S" in SCons.Tool.asm.ASSuffixes:
    SCons.Tool.asm.ASSuffixes.remove(".S")
if ".S" not in SCons.Tool.asm.ASPPSuffixes:
    SCons.Tool.asm.ASPPSuffixes.append(".S")


generate = SCons.Tool.asm.generate
exists = SCons.Tool.asm.exists
