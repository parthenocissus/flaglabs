$(document).ready(function () {

    let flagGenAPI = "_generate",
        saveAPI = "_save",
        urlGen = $SCRIPT_ROOT + flagGenAPI,
        urlSave = $SCRIPT_ROOT + saveAPI,
        svgCount = 0;

    let setSvgEvents = () => {
        for (let i = 0; i < svgCount; i++) {
            d3.select("#flag" + i).on("click", () => {
                let saveParams = {vector: i};
                $.getJSON(urlSave, saveParams).done(() => {
                    console.log("flag saved.");
                });
            });
        }
    };

    $("#go").click(() => {

        let flags = $("#flags");
        flags.empty();

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

        console.log(data);

        let params = {vector: JSON.stringify(data)};
        $.getJSON(urlGen, params, (result) => {
            flags.empty();
            result.forEach((i) => {
                flags.append(i);
            });
            svgCount = result.length;
        }).done(() => {
            setSvgEvents();
            console.log("flags received from backend, baby");
        });

    });

});