$(document).ready(function () {

    let mappingsAPI = "_get_mappings",
        flagSelectAPI = "_get_random",
        flagSelectDatabaseAPI = "_get_from_database",
        saveSvgAPI = "_save_svg_string"

    let urlMappings = $SCRIPT_ROOT + mappingsAPI,
        urlSelectGenerate = $SCRIPT_ROOT + flagSelectAPI,
        urlSelectFromDatabase = $SCRIPT_ROOT + flagSelectDatabaseAPI,
        urlSaveSvg = $SCRIPT_ROOT + saveSvgAPI;

    // let urlSelect = urlSelectGenerate;
    let urlSelect = urlSelectFromDatabase;

    /* Interface Interactivity */

    let sliderHtml = (key, label, type, data) => {
        return `<div id="slider-group"><div class="slider-div"><input type="range" ` +
            `id="${key}" name="${key}" min="${data.min}" max="${data.max}" ` +
            `value="${data.value}" step="${data.step}" data-input-type="${type}">` +
            `<label for="warm">${label}</label></div></div>`;
    };

    let selectHtml = (key, label) => {
        return `<option value="${key}">${label}</option>`;
    };

    let chosen = $(".chosen");
    let sliderGroup = $('#slider-group');
    let sliderHeader = $('#slider-header');

    $.getJSON(urlMappings, {vector: 0}, (mapping) => {

        for (let key in mapping) {
            $("#choose-params").append(selectHtml(key, mapping[key]["label"]));
        }

        chosen.chosen({max_selected_options: 5})
            .change(function () {
                sliderGroup.empty();
                let keys = $(this).val();
                let visible = (keys.length > 0) ? "visible" : "hidden";
                sliderHeader.css("visibility", visible);
                keys.forEach(key => {
                    let type = mapping[key]["type"];
                    let label = mapping[key]["label"];
                    let data = mapping[key]["data"];
                    sliderGroup.append(sliderHtml(key, label, type, data));
                });
            });

        chosen.bind("chosen:maxselected", () => {
            alert("Max parameters limit reached.");
        });
    });

    /* Radio Buttons */

    $('input[type=radio]').click(function () {
        urlSelect = (this.id === "radio-generate") ? urlSelectGenerate : urlSelectFromDatabase;
    });

    /* Drawing */

    let size = {w: 300, h: 200};

    let svg = d3.select("svg")
        .attr("viewBox", "0 0 " + size.w + " " + size.h)
        .attr("preserveAspectRatio", "xMidYMid meet");

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

    let getNewFlags = (start, metaLvl, number = 4) => {

        let rawInput = JSON.stringify(getSliderData());

        $.getJSON(urlSelect, {n: number, raw: rawInput}, (results) => {

            let gs = createGs(start, metaLvl);

            results.forEach((svg, index) => {
                let parser = new DOMParser();
                let doc = parser.parseFromString(svg, "image/svg+xml");
                const rootElement = doc.documentElement;
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
                        let newStart = {x: gs[index].x, y: gs[index].y};
                        let nextMetaLvl = metaLvl + 1;
                        getNewFlags(newStart, nextMetaLvl);
                    })
                    .on("contextmenu", function (d, i) {
                        d3.event.preventDefault();
                        rootFlag.remove();
                        let newStart = {x: gs[index].x, y: gs[index].y};
                        getNewFlags(newStart, metaLvl, 1);
                        console.log("right click!");
                        // react on right-clicking
                    });
            });

        }).done(() => {
            console.log("flags received from backend, baby");
        });

    };

    let startAgain = () => {
        let start = {x: 0, y: 0};
        let metaLvl = 0;
        getNewFlags(start, metaLvl);
    };

    $("#generate").click(() => {
        startAgain();
    });

    $("#save").click(() => {
        let compositeFlagSvg = document.getElementById( 'total-flag' );
        let svgText = JSON.stringify(compositeFlagSvg.outerHTML);
        $.getJSON(urlSaveSvg, {svg: svgText}, (result) => {
            console.log("composite fractal flag saved on backend.");
        });
    });

    startAgain();

});