$(document).ready(function () {

    let flagGenAPI = "_generate";
    let url = $SCRIPT_ROOT + flagGenAPI;

    let jsonTest = {
        "name": "test", "value": 0.7
    };
    let dummyData = {
        "layout": [
            {"fn": "unicolor", "factor": 100}
        ],
        "colors": [
            {"primary": "red", "factor": 100}
        ],
        "symbols": [
            {"name": "anarchism", "factor": 100}
        ]
    }

    let dataIn;

    $("#go").click(() => {

        let val = $('#anarchist').val();
        console.log(val);

        let dataOut = {
            vector: JSON.stringify(dummyData)
        };

        let flags = $("#flags");
        $.getJSON(url, dataOut, (result) => {

            flags.empty();
            result.forEach((i) => {
                // console.log(i);
                flags.append(i);
            });

        }).done(() => {
            // console.log("done")
        });

    });

});