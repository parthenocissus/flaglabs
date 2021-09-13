$(document).ready(function () {

    let size = {w: 600, h: 400};

    // let rect = svg.append("rect")
    //     .attr("width", size.w)
    //     .attr("height", size.h)
    //     .attr("stroke", "none")
    //     .attr("fill", "blue");

    let flagSelectAPI = "_get_random",
        urlSelect = $SCRIPT_ROOT + flagSelectAPI;

    // let flags = $("#flags");

    $.getJSON(urlSelect, {vector: 0}, (result) => {

        let svg = d3.select("svg")
            .attr("viewBox", "0 0 " + size.w + " " + size.h)
            .attr("preserveAspectRatio", "xMidYMid meet");

        let g1 = svg.append("g");
        let g2 = svg.append("g")
            .attr("transform", "translate(300, 0)");
        let g3 = svg.append("g")
            .attr("transform", "translate(0, 200)");
        let g4 = svg.append("g")
            .attr("transform", "translate(300, 200)");
        let gs = [g1, g2, g3, g4];

        result.forEach((svg, index) => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(svg, "image/svg+xml");

            const rootElement = doc.documentElement;
            const firstTier = rootElement.childNodes;

            // for (const child in firstTier) {
            //     let svgItem = firstTier[child];
                // if (svgItem instanceof SVGElement) {
                //     svg.node().append(svgItem);
                // }
            // }
            // g1.node().append(rootElement);

            gs[index].node().append(rootElement);

            // d3.select("#flag31")
            d3.select(rootElement)
                .attr("width", 300)
                .attr("height", 200)
                .attr("viewBox", "0 0 150 100")
                .attr("preserveAspectRatio", "xMidYMid meet");

        });

    }).done(() => {
        console.log("flags received from backend, baby");
    });

    // d3.xml(fn)
    // .then(data => {
    //     svg.node().append(data.documentElement);
    // });

});