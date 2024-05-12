function svgPathtoDesmos(){
    svgPaths = [];
    state = Calc.getState();
    state.expressions.list = [];
    for (let i = 0; i < svgPaths.length; i++){
        if (svgPaths[i].includes("t")){
            expression = {color: "#000000", id: String(i+1), type: "expression", points: false, lines: true, dragMode: "NONE", latex: svgPaths[i], parametricDomain: { min: '0', max: '1' }};
        }
        else{
            expression = {color: "#000000", id: String(i+1), type: "expression", points: false, lines: true, dragMode: "NONE", latex: svgPaths[i]};
        }
        state.expressions.list.push(expression);
    }
    Calc.setState(state);
}