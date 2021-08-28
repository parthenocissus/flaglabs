$(document).ready(function () {

    let flagGenAPI = "_generate";
    let url = $SCRIPT_ROOT + flagGenAPI;

    let data;
    let dataDefault = {
        "layout": [],
        "colors": [],
        "special_rules": [],
        "symbols": []
    };

    let factors = {

        "warm": {
            "colors": [
                {"factor": 100, "primary": "red"},
                {"factor": 100, "primary": "orange"},
                {"factor": 100, "primary": "yellow"},
                {"factor": 50, "primary": "white"},
                {"factor": 50, "primary": "pink"},
                {"factor": 20, "primary": "brown"}
            ]
        },

        "anarchist": {
            "layout": [
                {"factor": 100, "fn": "bicolor_diagonal_left"},
                {"factor": 100, "fn": "bicolor_diagonal_right"},
                {"factor": 20, "fn": "bend_left"},
                {"factor": 20, "fn": "bend_right"},
            ],
            "colors": [
                {"factor": 5, "primary": "red"},
                {"factor": 100, "primary": "black"}
            ],
            "symbols": [
                {"factor": 100, "name": "anarchism"},
                {"factor": 100, "name": "anarchism_rough"},
                {"factor": 10, "name": "pentagram"}
            ]
        },

        "african": {
            "colors": [
                {"factor": 100, "primary": "red"},
                {"factor": 100, "primary": "black"},
                {"factor": 100, "primary": "green"},
                {"factor": 100, "primary": "yellow"}
            ]
        },

        "slavic": {
            "layout": [
                {factor: 20, "fn": "tricolor_vertical" },
                {factor: 100, "fn": "tricolor_horizontal"},
                {factor: 10, "fn": "bicolor_vertical" },
                {factor: 10, "fn": "bicolor_horizontal"},
                {factor: 10, "fn": "chevron"}
            ],
            "colors": [
                {"factor": 100, "primary": "red"},
                {"factor": 100, "primary": "blue"},
                {"factor": 100, "primary": "white"}
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
        "layout": [{"fn": "unicolor", "factor": 100}],
        "colors": [{"primary": "red", "factor": 100}],
        "symbols": [{"name": "anarchism", "factor": 100}]
    };

    let fineTune = function (input, qoef, key, name) {
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
        [
            {key: "layout", name: "fn"},
            {key: "special_rules", name: "name"},
            {key: "colors", name: "primary"},
            {key: "symbols", name: "name"}
        ].forEach((i) => {
            fineTune(input, qoef, i.key, i.name);
        });

    };

    $("#go").click(() => {

        let flags = $("#flags");
        flags.empty();

        let duplicateFactors = JSON.parse(JSON.stringify(factors));
        data = JSON.parse(JSON.stringify(dataDefault));
        Object.keys(duplicateFactors).forEach((key) => {
            let qoef = $('#' + key).val() / 100;
            console.log(key + " " + qoef);
            adjustFactors(duplicateFactors[key], qoef);
        });
        console.log(data);

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