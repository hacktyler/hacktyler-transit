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
        _.each(data, function(stop, index) {
            $("#stops ul").append(STOP_LIST_ITEM_TEMPLATE(stop));
        });
        
        $('#stops .stop').click(function() {
            window.location.hash = "stop/" + $(this).attr("id");
        });
    }

    function showHome() {
        $(".page").hide()
        $("#home").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showFavorites() {
        var favorites = getFavorites();

        var i = 1;

        $("#favorites .stop").remove();

        _.each(favorites, function(favorite) {
            var stop = _.detect(TRANSIT_STOPS, function(stop) {
                return stop["slug"] == favorite;
            });

            $("#favorites ul").append(STOP_LIST_ITEM_TEMPLATE(stop));

            if (i % 2 == 0) {
                $("#favorites #" + stop["slug"]).addClass("even");
            }

            i += 1;
        });


        $('#favorites .stop').click(function() {
            window.location.hash = "stop/" + $(this).attr("id");
        });

        $(".page").hide()
        $("#favorites").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showLines() { 
        $(".page").hide()
        $("#lines").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showStops(line_slug) {
        var i = 1;

        $("#stops .stop").removeClass("even").hide();

        // Show stops for the selected line
        _.each(TRANSIT_STOPS, function(stop) {
            if (stop["line-slug"] == line_slug) {
                $("#stops #" + stop["slug"]).show();

                if (i % 2 == 0) {
                    $("#stops #" + stop["slug"]).addClass("even");
                }

                i += 1;
            }
        });

        $(".page").hide()
        $("#stops").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function viewStop(stop) {
        if (stop === null) {
            throw("No stop provided!");
        }

        var weekday_schedule = _.map(stop["weekday_schedule"], function(time) {
            ampm = time.substr(time.length - 2, 2);
            no_ampm = time.substr(0, time.length - 3);
            parts = no_ampm.split(":");
            hours = parseInt(parts[0]);
            minutes = parseInt(parts[1]);

            if (ampm == "PM" && hours != "12") {
                hours += 12;
            }

            d = new Date(); 
            d.setHours(hours);
            d.setMinutes(minutes);
            d.setSeconds(0);
            d.setMilliseconds(0);

            return d;
        });

        var now = new Date();

        var next_departure = _.detect(weekday_schedule, function(time) {
            return time > now;
        });

        if (_.isUndefined(next_departure) || next_departure === null) {
            stop["next_departure"] = null;
            stop["next_departure_in"] = null;
        } else {
            stop["next_departure"] = stop["weekday_schedule"][weekday_schedule.indexOf(next_departure)]

            var delta = next_departure.getTime() - now.getTime();
            stop["next_departure_in"] = Math.floor((delta / 1000) / 60);
        }

        stop["is_favorite"] = isFavorite(stop["slug"]);

        $(".page").hide()
        $("#detail .contents").html(STOP_DETAIL_TEMPLATE(stop));

        $('#detail .favorite').click(function() {
            if (isFavorite(stop["slug"]) === true) {
                removeStopFromFavorites(stop["slug"]);
                $(this).text("Add to favorites");
            } else {
                addStopToFavorites(stop["slug"]);
                $(this).text("Remove from favorites");
            }
        });

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

    function getFavorites() {
        favs = store.get("favorite_stops");

        if (_.isUndefined(favs)) {
            favs = new Array();
        }

        return favs;
    }

    function isFavorite(slug) {
        return (_.indexOf(getFavorites(), slug) > -1);
    }

    function setFavorites(favs) {
        store.set("favorite_stops", favs);
    }

    function addStopToFavorites(slug) {
        favs = getFavorites();
        favs.push(slug);
        setFavorites(favs);
    }

    function removeStopFromFavorites(slug) {
        favs = getFavorites();
        setFavorites(_.without(favs, slug));
    }

    window.StopController = Backbone.Controller.extend({
        routes: {
            "": "home",
            "favorites": "favorites",
            "find": "lines",
            "line/:line": "line",
            "stop/:stop": "stop",
        },

        home: function() {
            showHome();
        },

        favorites: function() {
            showFavorites();
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

    $("#find-a-stop").click(function() {
        window.location.hash = "find";
    });
    
    $("#view-favorites").click(function() {
        window.location.hash = "favorites";
    });

    $('#lines .line').click(function() {
        window.location.hash = "line/" + $(this).attr("id");
    });

    $(".close").click(function() {
        history.back(); 
    });

    addStops(TRANSIT_STOPS);
    Backbone.history.start();
});

