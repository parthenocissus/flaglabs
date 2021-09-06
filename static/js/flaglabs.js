$(document).ready(function () {

    let flagGenAPI = "_generate";
    let url = $SCRIPT_ROOT + flagGenAPI;

    $("#go").click(() => {

        let flags = $("#flags");
        flags.empty();

        let data = [];
        $("input").each(function(){
            let input = $(this);
            let d = {
                "value": +input.val(),
                "key": input.attr("name"),
                "type": input.attr("data-input-type")
            };
            data.push(d);
        });

        let dataOut = { vector: JSON.stringify(data) };
        $.getJSON(url, dataOut, (result) => {
            flags.empty();
            result.forEach((i) => {
                flags.append(i);
            });
        }).done(() => {
            console.log("flags received from backend, baby");
        });

    });

});