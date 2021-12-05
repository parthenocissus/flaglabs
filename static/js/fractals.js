$(document).ready(function () {

    let base = 2;
    let size = {w: 150 * base, h: 100 * base};

    let flagSelectAPI = "_get_random",
        flagSelectDatabaseAPI = "_get_from_database",
        saveSvgAPI = "_save_svg_string";

    let urlSelectGenerate = $SCRIPT_ROOT + flagSelectAPI,
        urlSelectFromDatabase = $SCRIPT_ROOT + flagSelectDatabaseAPI,
        urlSaveSvg = $SCRIPT_ROOT + saveSvgAPI;

    // let urlSelect = urlSelectGenerate;
    let urlSelect = urlSelectFromDatabase;

    let svg = d3.select("svg")
        .attr("viewBox", "0 0 " + size.w + " " + size.h)
        .attr("preserveAspectRatio", "xMidYMid meet");

    let createGs = (start, metaLvl, dim = {x: 2, y: 2}) => {
        let scaleFactor = Math.pow(1 / dim.x, metaLvl);
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

    let getSliderData = () => {
        let data = [];
        $("input[type=range]").each(function () {
            let input = $(this);
            let d = {
                "value": +input.val(),
                "key": input.attr("name"),
                "type": input.attr("data-input-type")
            };
            data.push(d);
        });
        return data;
    };

    let getNewFlags = (start, metaLvl, number = base * base) => {

        let rawInput = JSON.stringify(getSliderData());

        $.getJSON(urlSelect, {n: number, raw: rawInput}, (results) => {

            let singleDim = Math.sqrt(number);
            let dim = {x: singleDim, y: singleDim};
            let gs = createGs(start, metaLvl, dim);

            results.forEach((svg, index) => {
                let parser = new DOMParser();
                let doc = parser.parseFromString(svg, "image/svg+xml");
                const rootElement = doc.documentElement;
                gs[index].g.node().append(rootElement);
                let rootFlag = d3.select(rootElement);

                // const powerBase = (base === 2) ? 0.5 : 0.33;
                const factor = Math.pow(1 / base, metaLvl);
                let w = 150 * factor,
                    h = 100 * factor;

                let noGhosts = () => {
                    // comment for ghost patters:
                    gs[index].g.remove();
                }

                rootFlag.attr("width", w)
                    .attr("height", h)
                    .attr("viewBox", "0 0 150 100")
                    .attr("preserveAspectRatio", "xMidYMid meet")
                    .on("click", () => {
                        // gs[index].g.remove();
                        noGhosts();
                        let newStart = {x: gs[index].x, y: gs[index].y};
                        let nextMetaLvl = metaLvl + 1;
                        getNewFlags(newStart, nextMetaLvl);
                    })
                    .on("contextmenu", function (d, i) {
                        d3.event.preventDefault();
                        noGhosts();
                        // gs[index].g.remove();
                        let newStart = {x: gs[index].x, y: gs[index].y};
                        getNewFlags(newStart, metaLvl, 1);
                    });
            });

        }).done(() => {
            console.log("flags received from backend, baby");
        });

    };

    let startAgain = () => {
        $("#total-flag").empty();
        let start = {x: 0, y: 0};
        let metaLvl = 0;
        getNewFlags(start, metaLvl);
    };

    $("#generate").click(() => {
        startAgain();
    });

    $("#save").click(() => {
        let compositeFlagSvg = document.getElementById('total-flag');
        let svgText = JSON.stringify(compositeFlagSvg.outerHTML);
        $.getJSON(urlSaveSvg, {svg: svgText}, (result) => {
            console.log("composite fractal flag saved on backend.");
        });
    });

    $('input[type=radio]').click(function () {
        urlSelect = (this.id === "radio-generate") ? urlSelectGenerate : urlSelectFromDatabase;
    });

    startAgain();

});