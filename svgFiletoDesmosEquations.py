from utils import svgPathtoDesmosEquation as PtoDEq
from utils import cannyEdgeDetection
import fileinput
import sys

def convert_SVG_path(svg_string: str) -> list:
    #if svgString.find('path') >= 0:
    #    start = svgString.find('<path d=\"') + 9
    #    svgString = svgString[start:]
    #    end = svgString.find('\"')
    #    svgMiniString = svgString[:end]
    #    svgString = svgString[end:]
    #    print(svgMiniString)
    #    print(svgString)
    #    equationArray = convertSVGPath(svgString)
    #    return [*PtoDEq.svgPathtoDesmosEquation(svgMiniString), *equationArray]
    #
    #else:
    #    return []
    if (path_begin_index := svg_string.find('<path d=\"')) < 0:
        return []
    else:
        svg_string = svg_string[path_begin_index + 9: -3]
        #print(svg_string)
        return PtoDEq.svg_path_to_desmos_equation(svg_string)
        

if __name__ == '__main__':
    if sys.argv[1] == "cannyEdge":
        cannyEdgeDetection.image_to_canny_edge_bmp(sys.argv[2])
    
    elif sys.argv[1] == "toDesmos":
        svg_file_path = sys.argv[2]
        with open(svg_file_path, 'r') as svg_file:
            svg_string = svg_file.read()
            #svg_lines = svg_file.read().splitlines()
            d = ">"
            for line in svg_string:
                svg_lines =  [e+d for e in svg_string.split(d) if e]
            #for line in svgFile:
            #    line = line.rstrip()
            #    line += ' '
            #    svgString += line
            equation_array = []
            for line in svg_lines:
                equation_array += convert_SVG_path(line.strip())
            with open("./output/desmos_equation_array.txt", 'w') as output_desmos_file:
                output_desmos_file.write(str(equation_array))
            with open("./output/updateDesmos.js", "w") as output_js_file:
                with open("./utils/updateDesmosTemplate.js") as template_js_file:
                    for i, line in enumerate(template_js_file):
                        if i == 1:
                            line = line[:-4]
                            line += str(equation_array)
                            line += ';\n'
                                    
                        output_js_file.write(line)
                    
    
    else:
        print("Invalid argument provided")