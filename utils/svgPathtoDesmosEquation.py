class coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class cubic_bezier:
    def __init__(self, initial_point: coordinates, first_control_point: coordinates, second_control_point: coordinates, final_point: coordinates):
        self.initial_point = initial_point
        self.first_control_point = first_control_point
        self.second_control_point = second_control_point
        self.final_point = final_point
    
    # {color: "#000000", domain: { min: '0', max: '1' }, id: String(i+1), type: "expression", points: false, lines: true, dragMode: "NONE", latex: svgPaths[i], parametricDomain: { min: '0', max: '1' }}
    # f"\\left(\\left(1-t\\right)^{{3}}c_{{1}}+3t\\left(1-t\\right)^{{2}}c_{{2}}+3t^{{2}}\\left(1-t\\right)c_{{3}}+t^{{3}}c_{{4}}\\ ,\\ \\left(1-t\\right)^{{3}}v_{{1}}+3t\\left(1-t\\right)^{{2}}v_{{2}}+3t^{{2}}\\left(1-t\\right)v_{{3}}+t^{{3}}v_{{4}}\\right)\\ \\left\\{{0\\le t\\le1\\right\\}}" 
    def create_desmos_equation_string(self) -> str:
        return f"\\left(\\left(1-t\\right)^{{3}}({self.initial_point.x})+3t\\left(1-t\\right)^{{2}}({self.first_control_point.x})+3t^{{2}}\\left(1-t\\right)({self.second_control_point.x})+t^{{3}}({self.final_point.x})\\ ,\\ \\left(1-t\\right)^{{3}}({self.initial_point.y})+3t\\left(1-t\\right)^{{2}}({self.first_control_point.y})+3t^{{2}}\\left(1-t\\right)({self.second_control_point.y})+t^{{3}}({self.final_point.y})\\right)\\ \\left\\{{0\\le t\\le1\\right\\}}" 

class line:
    def __init__(self, initial_point: coordinates, final_point: coordinates):
        self.initial_point = initial_point
        self.final_point = final_point

    # {color: "#000000", id: String(i+1), type: "expression", points: false, lines: true, dragMode: "NONE", latex: svgPaths[i]}
    # f"\\left(1,0\\right),\\left(2,4\\right)" 
    def create_desmos_equation_string(self) -> str:
        return f"\\left({self.initial_point.x},{self.initial_point.y}\\right),\\left({self.final_point.x},{self.final_point.y}\\right)" 
    

def svg_path_to_desmos_equation(svg_path: str) -> list:
    # list of strings of multiple desmos equations which represent the path
    svg_path_desmos_equations_array = list()
    
    # from potrace formatting
    if svg_path[0] != 'M':
        print("Error: SVG format not supported (M)")
        return []
    
    # sets cursor to (0, 0)
    cursor = coordinates(0, 0)
    initial_cursor = coordinates(0, 0)
    
    # splits svg_path into individual numbers
    path_elements = svg_path.split()
    path_elements_length = len(path_elements) 
    
    # list of individual path classes in the overall svg path, splits polybeziers into cubic ones, polylines into lines
    svg_curves = list()
    
    
    #==================================PARSING=====================================
    
    # parses svg, places everything into classes
    i = 0
    while i < path_elements_length:
        # temporary list to store strings representing an overall curve
        path_curve_elements = list()
        path_curve_elements.append(path_elements[i])
        i += 1
        
        
        #---------- READING SEGMENTS ----------
        
        # goes until or l/c/m____
        while i < path_elements_length and (not path_elements[i][0].isalpha()):
            path_curve_elements.append(path_elements[i])
            i += 1
            
        #---------- PARSING ----------
            
        #print(path_curve_elements)
            
        # if M
        if path_curve_elements[0][0] == 'M':
            # sets cursor (absolute)
            cursor.x = int(path_curve_elements[0][1:])
            cursor.y = int(path_curve_elements[1])
            # because of the way the thing formats the uhh svg i can do this to get the initial thing of the path
            initial_cursor.x = cursor.x
            initial_cursor.y = cursor.y
        
        # if m
        elif path_curve_elements[0][0] == 'm':
            # sets cursor (relative)
            cursor.x += int(path_curve_elements[0][1:])
            cursor.y += int(path_curve_elements[1])
            # because of the way the thing formats the uhh svg i can do this to get the initial thing of the path
            initial_cursor.x = cursor.x
            initial_cursor.y = cursor.y
        
        # if c
        elif path_curve_elements[0][0] == 'c':
            # cut off initial 'c'
            path_curve_elements[0] = path_curve_elements[0][1:]
            
            # check if in pairs of 3
            if len(path_curve_elements) % 6 != 0:
                print("Improperly formatted SVG")
                return []       
            
            # create cubic bezier curve classes and append to svg_curves
            path_curve_elements_length = len(path_curve_elements)
            
            for j in range(path_curve_elements_length // 6):
                # flag for ending with z
                z_flag = False
                
                # check if final element is __z
                if path_curve_elements[j * 6 + 5][-1] == 'z':
                    # removes z
                    path_curve_elements[j * 6 + 5] = path_curve_elements[j * 6 + 5][:-1]
                    # sets z flag
                    z_flag = True
                
                # create bezier curve class
                new_cubic_bezier_curve = cubic_bezier(
                    initial_point = coordinates(cursor.x, cursor.y),
                    first_control_point = coordinates(cursor.x + int(path_curve_elements[j * 6]), cursor.y + int(path_curve_elements[j * 6 + 1])),
                    second_control_point = coordinates(cursor.x + int(path_curve_elements[j * 6 + 2]), cursor.y + int(path_curve_elements[j * 6 + 3])),
                    final_point = coordinates(cursor.x + int(path_curve_elements[j * 6 + 4]), cursor.y + int(path_curve_elements[j * 6 + 5]))
                )
                # append to list of curve classes
                svg_curves.append(new_cubic_bezier_curve)
                # sets cursor to final point
                cursor = coordinates(new_cubic_bezier_curve.final_point.x, new_cubic_bezier_curve.final_point.y)
                
                if z_flag:
                    # if ending with z, create a line class
                    new_z_line = line(
                        initial_point = coordinates(cursor.x, cursor.y),
                        final_point = coordinates(initial_cursor.x, initial_cursor.y)
                    )
                    # append to list of curve classes
                    svg_curves.append(new_z_line)
                    # sets cursor to initial point
                    cursor = coordinates(new_z_line.final_point.x, new_z_line.final_point.y)
                

        # if l
        elif path_curve_elements[0][0] == 'l':
            # cut off initial 'l'
            path_curve_elements[0] = path_curve_elements[0][1:]
            
            # check if in pairs of 2
            if len(path_curve_elements) % 2 != 0:
                print("Improperly formatted SVG")
                return []       
            
            path_curve_elements_length = len(path_curve_elements)
            
            for j in range(path_curve_elements_length // 2):
                # flag for ending with z
                z_flag = False
                
                # check if final element is __z
                if path_curve_elements[j * 2 + 1][-1] == 'z':
                    # removes z
                    path_curve_elements[j * 2 + 1] = path_curve_elements[j * 2 + 1][:-1]
                    # sets z flag
                    z_flag = True

                # create line class
                new_line = line(
                    initial_point = coordinates(cursor.x, cursor.y),
                    final_point = coordinates(cursor.x + int(path_curve_elements[j * 2]), cursor.y + int(path_curve_elements[j * 2 + 1]))
                )
                # append to list of curve classes
                svg_curves.append(new_line)
                # sets cursor to final point
                cursor = coordinates(new_line.final_point.x, new_line.final_point.y)
                
                if z_flag:
                    # if ending with z, create a line class
                    new_z_line = line(
                        initial_point = coordinates(cursor.x, cursor.y),
                        final_point = coordinates(initial_cursor.x, initial_cursor.y)
                    )
                    # append to list of curve classes
                    svg_curves.append(new_z_line)
                    # sets cursor to final point
                    cursor = coordinates(new_z_line.final_point.x, new_z_line.final_point.y)
          
        # if neither
        else:
            print("Error, path element not known")
            return [] 


    #===================================CONVERSION====================================
        
    # Converts all classes to strings and adds them to desmos equation array

    for curve_class in svg_curves:
        if type(curve_class) is line or type(curve_class) is cubic_bezier:
            svg_path_desmos_equations_array.append(curve_class.create_desmos_equation_string())
        else:
            print("Class error")
            return []
        
    return svg_path_desmos_equations_array

#def svgPathtoDesmosEquation(svgPath: str) -> list:
#    svgArray = svgPath.split()
#    svgArrayLength = len(svgArray)
#    done = False
#    cur = { 'x':0, 'y':0 }
#    svgArrayLocation = 0
#    equationsPlusZ = []
#    initialPoint = { 'x':0, 'y':0 }
#    
#    while not done:
#        
#        z = False
#        equation = ''
#        
#        if svgArrayLocation >= svgArrayLength:
#            done = True
#            if cur != initialPoint:
#                equationFinal = f"\\left({cur['x']},\\ {cur['y']}\\right), \\left({initialPoint['x']},\\ {initialPoint['y']}\\right)"
#                cur = initialPoint
#                equationsPlusZ.append(equationFinal)
#        
#        elif str(svgArray[svgArrayLocation]).startswith('M'):
#            svgArray[svgArrayLocation] = svgArray[svgArrayLocation][1:]; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            cur['x'] = initialPoint['x'] = int(svgArray[svgArrayLocation])
#            svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            cur['y'] = initialPoint['y'] = int(svgArray[svgArrayLocation])
#            try:
#                svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            except:
#                done = True
#        
#        elif str(svgArray[svgArrayLocation]).startswith('m'):
#            svgArray[svgArrayLocation] = svgArray[svgArrayLocation][1:]; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            cur['x'] += int(svgArray[svgArrayLocation])
#            svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            cur['y'] += int(svgArray[svgArrayLocation])
#            try:
#                svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            except:
#                done = True
#        
#        elif str(svgArray[svgArrayLocation]).startswith('l'):
#            equation += f"\\left({cur['x']},\\ {cur['y']}\\right)"
#            curXorY = 'x'
#            svgArray[svgArrayLocation] = svgArray[svgArrayLocation][1:]; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation]); n = int(svgArray[svgArrayLocation])
#            cur[curXorY] += n
#            equation += f" ,\\left({cur[curXorY]},\\ "
#            curXorY = 'y'
#            svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            while svgArray[svgArrayLocation][0].isdigit() or svgArray[svgArrayLocation][0] == '-':
#                n = int(svgArray[svgArrayLocation])
#                if curXorY == 'x':
#                    cur[curXorY] += n
#                    equation += f" ,\\left({cur[curXorY]},\\ "
#                    curXorY = 'y'
#                elif curXorY == 'y':
#                    cur[curXorY] += n
#                    equation += f"{cur[curXorY]}\\right)"
#                    curXorY = 'x'
#                else:
#                    print("BRUH")
#                    raise
#                try:
#                    svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#                except:
#                    break
#
#        elif str(svgArray[svgArrayLocation]).startswith('c'):
#            svgArray[svgArrayLocation] = svgArray[svgArrayLocation][1:]; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            while svgArray[svgArrayLocation][0].isdigit() or svgArray[svgArrayLocation][0] == '-':
#                x = { '0': cur['x'] } # curve 1, curve 2, end 3
#                y = { '0': cur['y'] } # curve 1, curve 2, end 3
#                for i in range(3):
#                    cur['x'] += int(svgArray[svgArrayLocation])
#                    x.update({ str(i+1): cur['x'] })
#                    svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#                    cur['y'] += int(svgArray[svgArrayLocation])
#                    y.update({ str(i+1): cur['y'] })
#                    try:
#                        svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#                    except:
#                        break
#                #tempEquation = f"\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){x['0']}+t{x['1']}\\right)+t\\left(\\left(1-t\\right){x['1']}+t{x['2']}\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){x['1']}+t{x['2']}\\right)+t\\left(\\left(1-t\\right){x['2']}+t{x['3']}\\right)\\right),\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){y['0']}+t{y['1']}\\right)+t\\left(\\left(1-t\\right){y['1']}+t{y['2']}\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){y['1']}+t{y['2']}\\right)+t\\left(\\left(1-t\\right){y['2']}+t{y['3']}\\right)\\right)\\right)"
#                tempEquation = f"\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){x['0']}+t\\left({x['1']}\\right)\\right)+t\\left(\\left(1-t\\right){x['1']}+t\\left({x['2']}\\right)\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){x['1']}+t\\left({x['2']}\\right)\\right)+t\\left(\\left(1-t\\right){x['2']}+t\\left({x['3']}\\right)\\right)\\right),\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){y['0']}+t\\left({y['1']}\\right)\\right)+t\\left(\\left(1-t\\right){y['1']}+t\\left({y['2']}\\right)\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){y['1']}+t\\left({y['2']}\\right)\\right)+t\\left(\\left(1-t\\right){y['2']}+t\\left({y['3']}\\right)\\right)\\right)\\right)"
#                equationsPlusZ.append(tempEquation)
#                if svgArrayLocation >= svgArrayLength:
#                    break
#
## c dx1 dy1, dx2 dy2, dx dy (from cur to dx, dy)
#
##"\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)x_{0}+tx_{1}\\right)+t\\left(\\left(1-t\\right)x_{1}+tx_{2}\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)x_{1}+tx_{2}\\right)+t\\left(\\left(1-t\\right)x_{2}+tx_{3}\\right)\\right),\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)y_{0}+ty_{1}\\right)+t\\left(\\left(1-t\\right)y_{1}+ty_{2}\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)y_{1}+ty_{2}\\right)+t\\left(\\left(1-t\\right)y_{2}+ty_{3}\\right)\\right)\\right)"
#
#        elif str(svgArray[svgArrayLocation]).startswith('C'):
#            svgArray[svgArrayLocation] = svgArray[svgArrayLocation][1:]; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#            while svgArray[svgArrayLocation][0].isdigit() or svgArray[svgArrayLocation][0] == '-':
#                x = { '0': cur['x'] } # curve 1, curve 2, end 3
#                y = { '0': cur['y'] } # curve 1, curve 2, end 3
#                for i in range(3):
#                    x.update({ str(i+1): int(svgArray[svgArrayLocation]) })
#                    svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#                    y.update({ str(i+1): int(svgArray[svgArrayLocation]) })
#                    try:
#                        svgArrayLocation += 1; svgArray[svgArrayLocation], z = checkZ(svgArray[svgArrayLocation])
#                    except:
#                        break
#                tempEquation = f"\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){x['0']}+t\\left({x['1']}\\right)\\right)+t\\left(\\left(1-t\\right){x['1']}+t\\left({x['2']}\\right)\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){x['1']}+t\\left({x['2']}\\right)\\right)+t\\left(\\left(1-t\\right){x['2']}+t\\left({x['3']}\\right)\\right)\\right),\\left(1-t\\right)\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){y['0']}+t\\left({y['1']}\\right)\\right)+t\\left(\\left(1-t\\right){y['1']}+t\\left({y['2']}\\right)\\right)\\right)+t\\left(\\left(1-t\\right)\\left(\\left(1-t\\right){y['1']}+t\\left({y['2']}\\right)\\right)+t\\left(\\left(1-t\\right){y['2']}+t\\left({y['3']}\\right)\\right)\\right)\\right)"
#                equationsPlusZ.append(tempEquation)
#                if svgArrayLocation >= svgArrayLength:
#                    break
#        
#        if z:
#            equationZ = f"\\left({cur['x']},\\ {cur['y']}\\right), \\left({initialPoint['x']},\\ {initialPoint['y']}\\right)"
#            cur = initialPoint
#            equationsPlusZ.append(equationZ)
#        
#        if equation != '':
#            equationsPlusZ.append(equation)
#    
#    #print('\n'.join(equationsPlusZ))
#    print(equationsPlusZ)
#    return equationsPlusZ

if __name__ == '__main__':
    print(svg_path_to_desmos_equation(input("Enter Path: ")))
    
# l-6 -23 1691 0 1691 0 0 3600 0 3600 -6400 0 -6400 0 0 -3600z