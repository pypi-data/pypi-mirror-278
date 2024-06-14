import sys
import kute.routines._diffusion_coefficient as diffusion_coefficient
import kute.routines._electric_conductivity as electric_conductivity
import kute.routines._viscosity as viscosity

routines = {
    "diffusion_coefficient": diffusion_coefficient,
    "electric_conductivity": electric_conductivity,
    "viscosity": viscosity
}
def main():
    STRING_AVAILABLE = f"Available routines: {list(routines.keys())}"
    if len(sys.argv) == 1:
        print(STRING_AVAILABLE)
        return
    if sys.argv[1] in routines:
        sys.argv[0] = "kute " + sys.argv[1]
        name = sys.argv.pop(1)
        routines[name].main()
    else:
        print(STRING_AVAILABLE)
        sys.exit(1)
        
if __name__ == "__main__":
    main()