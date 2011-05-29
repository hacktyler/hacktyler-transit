$(function() {
    // PLATFORM DETECTION
    window.using_phonegap = (typeof(Media) != 'undefined');
    var uagent = navigator.userAgent.toLowerCase();
    window.platform = null;
    
    if (uagent.search('android') > -1) {
        platform = 'android';
    } else if (uagent.search('ipad') > -1 || uagent.search('ipod') > -1 || uagent.search('iphone') > -1) {
        platform = 'ios';
    } else if (uagent.search('blackberry') > -1) {
        platform = 'blackberry';
    }

    window.STOP_LIST_ITEM_TEMPLATE = _.template($('#stop-list-item-template').html());
    window.STOP_DETAIL_TEMPLATE = _.template($('#stop-detail-template').html());

    window.currentStop = null;

    function addStops(data) {
        _.each(data, function(stop) {
            $("#stops ul").prepend(STOP_LIST_ITEM_TEMPLATE(stop));
        });
        
        $('#stops .stop').click(function() {
            window.location.hash = "stop/" + $(this).attr("id");
        });
    }

    function showLines() { 
        $("#detail").hide();
        $("#stops").hide();
        $("#lines").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showStops(line_slug) {
        // Show stops for the selected line
        _.each(TRANSIT_STOPS, function(stop) {
            if (stop["line-slug"] == line_slug) {
                $("#" + stop["slug"]).show();
            } else {
                $("#" + stop["slug"]).hide();
            }
        });

        $("#lines").hide();
        $("#detail").hide();
        $("#stops").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function viewStop(stop) {
        if (stop === null) {
            throw("No stop provided!");
        }

        $("#lines").hide();
        $("#stops").hide();
        $("#detail .contents").html(STOP_DETAIL_TEMPLATE(stop));
        $("#detail").show();

        $(window).scrollTop(0);
        currentStop = stop;
    }
    
    function viewStopBySlug(slug) {
        var stop = _.detect(TRANSIT_STOPS, function(stop) {
                return stop["slug"] == slug;
            });

        if (stop != null) {
            viewStop(stop);
        }
    }

    window.StopController = Backbone.Controller.extend({
        routes: {
            "": "lines",
            "line/:line": "line",
            "stop/:stop": "stop",
        },

        lines: function() {
            showLines();
        },

        line: function(line) {
            showStops(line);
        },

        stop: function(stop) {
            viewStopBySlug(stop);
        },
    });

    window.Controller = new StopController();


    $('header h1').click(function() {
        window.location.hash = "";
    });

    $('#lines .line').click(function() {
        window.location.hash = "line/" + $(this).attr("id");
    });

    $('#stops .close').click(function() {
        window.location.hash = "";
    });

    $('#detail .close').click(function() {
        window.location.hash = "line/" + currentStop["line-slug"];
    });

    addStops(TRANSIT_STOPS);
    Backbone.history.start();
});

