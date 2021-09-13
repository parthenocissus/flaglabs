$(document).ready(function () {

    let size = {w: 300, h: 200};

    let flagSelectAPI = "_get_random",
        urlSelect = $SCRIPT_ROOT + flagSelectAPI;

    let svg = d3.select("svg")
        .attr("viewBox", "0 0 " + size.w + " " + size.h)
        .attr("preserveAspectRatio", "xMidYMid meet");

    // let g1 = svg.append("g");
    // let g2 = svg.append("g")
    //     .attr("transform", "translate(150, 0)");
    // let g3 = svg.append("g")
    //     .attr("transform", "translate(0, 100)");
    // let g4 = svg.append("g")
    //     .attr("transform", "translate(150, 100)");
    // let gs = [g1, g2, g3, g4];

    let createGs = (start, metaLvl, dim = {x: 2, y: 2}) => {
        let scaleFactor = Math.pow(0.5, metaLvl);
        let coords = [];
        for (let i = 0; i < dim.x; i++) {
            for (let j = 0; j < dim.y; j++) {
                let p = {
                    x: start.x + i * 150 * scaleFactor,
                    y: start.y + j * 100 * scaleFactor
                };
                let g = svg.append("g")
                    .attr("transform", "translate(" + p.x + ", " + p.y + ")");
                p.g = g;
                coords.push(p);
            }
        }
        return coords;
    };

    let createGrs = (metaLvl = 0, count = 4) => {
        let scaleFactor = Math.pow(0.5, metaLvl);
        let gCoords = computeCoordinates(scaleFactor = scaleFactor);
        let gs = [];
        gCoords.forEach(p => {
            let g = svg.append("g")
                .attr("transform", "translate(" + p.x + ", " + p.y + ")");
            gs.push(g);
        });
        return gs;
    };

    let getNewFlags = (start, metaLvl, number = 4) => {

        $.getJSON(urlSelect, {vector: number}, (results) => {

            let gs = createGs(start, metaLvl);

            results.forEach((svg, index) => {
                let parser = new DOMParser();
                let doc = parser.parseFromString(svg, "image/svg+xml");
                const rootElement = doc.documentElement;
                // const firstTier = rootElement.childNodes;

                gs[index].g.node().append(rootElement);

                let rootFlag = d3.select(rootElement);

                const factor = Math.pow(0.5, metaLvl);
                let w = 150 * factor,
                    h = 100 * factor;

                rootFlag.attr("width", w)
                    .attr("height", h)
                    .attr("viewBox", "0 0 150 100")
                    .attr("preserveAspectRatio", "xMidYMid meet")
                    .on("click", () => {
                        rootFlag.remove();
                        let newStart = { x: gs[index].x, y: gs[index].y };
                        let nextMetaLvl = metaLvl + 1;
                        getNewFlags(newStart, nextMetaLvl);
                    })
                    .on("contextmenu", function (d, i) {
                        d3.event.preventDefault();
                        console.log("right click!");
                       // react on right-clicking
                    });
            });

        }).done(() => {
            console.log("flags received from backend, baby");
        });

    };

    let start = { x: 0, y: 0 };
    let metaLvl = 0;
    getNewFlags(start, metaLvl);

});