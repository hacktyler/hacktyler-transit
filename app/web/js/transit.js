$(function() {
    /* PLATFORM DETECTION */
    window.using_phonegap = (!_.isUndefined(window.device));
    var uagent = navigator.userAgent.toLowerCase();
    window.platform = null;
    
    if (uagent.search('android') > -1) {
        platform = 'android';
    } else if (uagent.search('ipad') > -1) {
        platform = 'ipad';
    } else if (uagent.search('ipod') > -1 || uagent.search('iphone') > -1) {
        platform = 'iphone';
    } else if (uagent.search('blackberry') > -1) {
        platform = 'blackberry';
    }

    /* RENDER DYNAMIC CONTENT? */
    window.RENDER_DYNAMIC = false;

    // Render extras when using Phonegap and a strong connection is available
    if (window.using_phonegap) {
        if (_.indexOf([Connection.ETHERNET, Connection.WIFI, Connection.CELL_4G], navigator.network.connection.type) > 0) {
            if (network.isReachable(reachableHostname, reachableCallback, [reachableOptions])) {
                window.RENDER_DYNAMIC = true;
            }
        }
    // Also render extras if not on a mobile device (ipad is assumed to be an exception
    } else {
        if (_.indexOf(['android', 'ios', 'blackberry'], platform) == -1)
        {
            window.RENDER_DYNAMIC = true;
        }
    }

    /* GLOBALS */
    window.BUS_LINES = {
        "red-line-north": "Red Line North",
        "red-line-south": "Red Line South",
        "blue-line-northwest":" Blue Line Northwest",
        "blue-line-southwest": "Blue Line Southwest",
        "green-line-northeast": "Green Line Northeast",
        "green-line-southeast": "Green Line Southeast",
        "yellow-line-southwest": "Yellow Line Southwest",
        "yellow-line-southeast": "Yellow Line Southeast"
    };

    window.STOP_LIST_ITEM_TEMPLATE = _.template($('#stop-list-item-template').html());
    window.FAVORITE_LIST_TEMPLATE = _.template($('#favorite-list-template').html());
    window.STOP_DETAIL_TEMPLATE = _.template($('#stop-detail-template').html());

    window.currentStop = null;

    /* PAGES */
    function showHome() {
        $(".page").hide()
        $("#home").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showFavorites() {
        var favorites = getFavorites();

        var stops = new Array();

        _.each(favorites, function(favorite) {
            var stop = _.detect(TRANSIT_STOPS, function(stop) {
                return stop["order"] == favorite;
            });

            stops.push(stop);
        });

        console.log(stops);

        $("#favorites .contents").html(FAVORITE_LIST_TEMPLATE({ "stops": stops }));

        $('#favorites .stop').click(function() {
            window.location.hash = "stop/" + $(this).attr("id").substr("favorite-".length, 3);
        });

        $(".page").hide()
        $("#favorites").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showMap() { 
        // Create map on demand
        if ($("#transit-map .canvas").is(":empty")) {
            // TODO
        }

        $(".page").hide();
        $("#transit-map").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    function showAbout() { 
        $(".page").hide()
        $("#about").show();

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
                $("#stops #stop-" + stop["order"]).show();

                if (i % 2 == 0) {
                    $("#stops #stop-" + stop["order"]).addClass("even");
                }

                i += 1;
            }
        });

        $("#stops .line-name").text(BUS_LINES[line_slug]);

        $(".page").hide()
        $("#stops").show();

        $(window).scrollTop(0)
        currentStop = null;
    }

    /* UTILS */
    function addStops(data) {
        _.each(data, function(stop, index) {
            $("#stops ul").append(STOP_LIST_ITEM_TEMPLATE(stop));
        });
        
        $('#stops .stop').click(function() {
            window.location.hash = "stop/" + $(this).attr("id").substr("stop-".length, 3);
        });
    }

    function timesFromSchedule(entries) {
       return _.map(entries, function(time) {
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
    }

    function viewStop(stop) {
        if (stop === null) {
            throw("No stop provided!");
        }

        var today = new Date();
        var day = today.getDay();

        // Sunday
        if (day == 0) {
            stop["schedule"] = null;
            stop["schedule_message"] = "Tyler Transit buses do not run on Sunday.";
        // Saturday
        } else if (day == 6) {
            // TODO
            stop["schedule"] = null;
            stop["schedule_message"] = "The Saturday bus schedule is not yet available.";
        // Weekday
        } else {
            stop["schedule"] = stop["weekday_schedule"];
            stop["schedule_message"] = null;
        }


        // If there is a schedule, highlight next stop
        if (!_.isNull(stop["schedule"])) {
            times = timesFromSchedule(stop["schedule"]);

            var now = new Date();

            var next_departure = _.detect(times, function(time) {
                return time > now;
            });

            if (_.isUndefined(next_departure) || next_departure === null) {
                stop["next_departure"] = null;
                stop["next_departure_in"] = null;
            } else {
                stop["next_departure"] = stop["schedule"][times.indexOf(next_departure)]

                var delta = next_departure.getTime() - now.getTime();
                stop["next_departure_in"] = Math.floor((delta / 1000) / 60);
            }
        }

        stop["is_favorite"] = isFavorite(stop["order"]);

        $(".page").hide()
        $("#detail .contents").html(STOP_DETAIL_TEMPLATE(stop));

        $('#detail .favorite').click(function() {
            if (isFavorite(stop["order"]) === true) {
                removeStopFromFavorites(stop["order"]);
                $(this).text("Add to favorites");
            } else {
                addStopToFavorites(stop["order"]);
                $(this).text("Remove from favorites");
            }
        });

        $("#detail").show();

        $(window).scrollTop(0);
        currentStop = stop;
    }
    
    function viewStopById(order) {
        var stop = _.detect(TRANSIT_STOPS, function(stop) {
                return stop["order"] == order;
            });

        if (stop != null) {
            viewStop(stop);
        }
    }

    /* FAVORITES */
    function getFavorites() {
        favs = store.get("favorite_stops");

        if (_.isUndefined(favs)) {
            favs = new Array();
        }

        return favs;
    }

    function isFavorite(order) {
        return (_.indexOf(getFavorites(), order) > -1);
    }

    function setFavorites(favs) {
        store.set("favorite_stops", favs);
    }

    function addStopToFavorites(order) {
        favs = getFavorites();
        favs.push(order);
        setFavorites(favs);
    }

    function removeStopFromFavorites(order) {
        favs = getFavorites();
        setFavorites(_.without(favs, order));
    }

    /* URL ROUTING */
    window.StopController = Backbone.Controller.extend({
        routes: {
            "": "home",
            "favorites": "favorites",
            "map": "map",
            "about": "about",
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

        map: function() {
            showMap();
        },

        about: function() {
            showAbout();
        },

        lines: function() {
            showLines();
        },

        line: function(line) {
            showStops(line);
        },

        stop: function(stop) {
            viewStopById(stop);
        },
    });

    window.Controller = new StopController();

    /* EVENT HANDLERS */
    $('header h1').click(function() {
        window.location.hash = "";
    });

    $("#find-a-stop").click(function() {
        window.location.hash = "find";
    });
    
    $("#view-favorites").click(function() {
        window.location.hash = "favorites";
    });
        
    $("#view-map").click(function() {
        window.location.hash = "map";
    });

    $("#view-about").click(function() {
        window.location.hash = "about";
    });

    $('#lines .line').click(function() {
        window.location.hash = "line/" + $(this).attr("id");
    });

    $(".close").click(function() {
        history.back(); 
    });

    /* SETUP */
    if (window.RENDER_DYNAMIC) {
        $("#view-map").show();
    }

    addStops(TRANSIT_STOPS);
    Backbone.history.start();
});

