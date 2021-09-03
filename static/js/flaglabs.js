$(document).ready(function () {

    let flagGenAPI = "_generate";
    let url = $SCRIPT_ROOT + flagGenAPI;

    let data1;
    // let ruleKeys = ["layout", "colors", "symbols"];
    let dataDefault = {
        "layout": [],
        "colors": [],
        "symbols": []
    };

    let factors = {

        "warm": {
            "colors": [
                {"factor": 100, "name": "red"},
                {"factor": 100, "name": "orange"},
                {"factor": 100, "name": "yellow"},
                {"factor": 50, "name": "white"},
                {"factor": 50, "name": "pink"},
                {"factor": 20, "name": "brown"}
            ]
        },

        "anarchist": {
            "layout": [
                {"factor": 100, "name": "bicolor_diagonal_left"},
                {"factor": 100, "name": "bicolor_diagonal_right"},
                {"factor": 20, "name": "bend_left"},
                {"factor": 20, "name": "bend_right"},
            ],
            "colors": [
                {"factor": 5, "name": "red"},
                {"factor": 100, "name": "black"}
            ],
            "symbols": [
                {"factor": 100, "name": "anarchism"},
                {"factor": 100, "name": "anarchism_rough"},
                {"factor": 10, "name": "pentagram"}
            ]
        },

        "african": {
            "colors": [
                {"factor": 100, "name": "red"},
                {"factor": 100, "name": "black"},
                {"factor": 100, "name": "green"},
                {"factor": 100, "name": "yellow"}
            ]
            // "colors": [
            //     {"factor": 60, "name": "red"},
            //     {"factor": 100, "name": "pink"},
            //     {"factor": 100, "name": "purple"},
            //     {"factor": 50, "name": "blue"},
            //     {"factor": 50, "name": "yellow"},
            //     {"factor": 50, "name": "green"},
            //     {"factor": 50, "name": "brown"},
            //     {"factor": 50, "name": "orange"}
            // ],
            // "layout": [
            //     {"factor": 10, "name": "stripes_horizontal"},
            //     {"factor": 5, "name": "stripes_vertical"}
            // ]
        },

        "slavic": {
            "layout": [
                {"factor": 20, "name": "tricolor_vertical" },
                {"factor": 100, "name": "tricolor_horizontal"},
                {"factor": 10, "name": "bicolor_vertical" },
                {"factor": 10, "name": "bicolor_horizontal"},
                {"factor": 10, "name": "chevron"}
            ],
            "colors": [
                {"factor": 100, "name": "red"},
                {"factor": 100, "name": "blue"},
                {"factor": 100, "name": "white"}
            ],
            "symbols": [
                {"factor": 3, "name": "pentagram"},
                {"factor": 20, "name": "orthodox_cross"},
                {"factor": 20, "name": "russian_cross"}
            ]
        },

        "corporate": {
            "symbols": [
                {"factor": 100, "name": "dollar"},
                {"factor": 100, "name": "apple_logo"},
                {"factor": 100, "name": "nike"},
                {"factor": 100, "name": "mcdonalds"}
            ]
        }
    };

    let dummyData = {
        "layout": [{"name": "unicolor", "factor": 100}],
        "colors": [{"name": "red", "factor": 100}],
        "symbols": [{"name": "anarchism", "factor": 100}]
    };

    let fineTune = function (input, qoef, key, name="name") {
        if (input.hasOwnProperty(key)) {
            input[key].forEach((inItem) => {
                let result = data[key].filter(dItem => {
                    return dItem[name] === inItem[name];
                });
                let dataPoint = result[0];
                inItem.factor *= qoef;
                if (!dataPoint) {
                    data[key].push(inItem);
                } else if (inItem.factor > dataPoint.factor) {
                    dataPoint.factor = inItem.factor;
                }
            });
        }
    };

    let adjustFactors = function (input, qoef) {
        Object.keys(dataDefault).forEach((key) => {
            fineTune(input, qoef, key);
        });
    };

    $("#go").click(() => {

        let flags = $("#flags");
        flags.empty();

        // let duplicateFactors = JSON.parse(JSON.stringify(factors));
        // data = JSON.parse(JSON.stringify(dataDefault));
        // Object.keys(duplicateFactors).forEach((key) => {
        //     let qoef = $('#' + key).val() / 100;
        //     adjustFactors(duplicateFactors[key], qoef);
        // });
        // console.log(data);

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

        // Object.keys(duplicateFactors).forEach((key) => {
        //     let qoef = $('#' + key).val() / 100;
        //     adjustFactors(duplicateFactors[key], qoef);
        // });
        //
        // let dataOut = { vector: JSON.stringify(dummyData) };

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