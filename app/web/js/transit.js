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

    window.Stop = Backbone.Model.extend({});

    window.StopCollection = Backbone.Collection.extend({
        url: "/data/bus-stops.js",
        model: Stop,
    });

    window.Stops = new StopCollection(TRANSIT_STOPS);

    window.StopListItemView = Backbone.View.extend({
        tagName: "li",
        template: _.template($('#stop-list-item-template').html()),

        events: {
            "click": "view",
        },

        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('change', this.render);
        },

        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));

            return this;
        },

        view: function() {
            window.location.hash = "stop/" + this.model.get('slug');
        },

        hide: function () {
            $("#" + this.model.get('slug')).hide();
        },

        show: function() {
            $("#" + this.model.get('slug')).show();
        }
    });

    window.StopDetailView = Backbone.View.extend({
        tagName: "div",
        template: _.template($('#stop-detail-template').html()),

        events: {
            "click .close": "close"
        },

        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('change', this.render);
            this.model.view = this;
        },

        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },

        close: function() {
            window.location.hash = "line/" + this.model.get('line-slug');
        }
    });

    window.AppView = Backbone.View.extend({
        el: $("#content"),
        models: {},
        liviews: {},
        currentStopSlug: null,

        initialize: function() {
            _.bindAll(this, 'addStop', 'addStops', 'render');
            
            Stops.bind('add', this.addStop);
            Stops.bind('refresh', this.addStops);
            Stops.bind('all', this.render);
            Stops.fetch();
        },

        addStop: function(stop) {
            var view = new StopListItemView({ model: stop });
            this.models[stop.get('slug')] = stop;
            this.liviews[stop.get('slug')] = view;
            this.$("#stops").prepend(view.render().el);
        },

        addStops: function() {
            Stops.each(this.addStop);
        },

        showLines: function() { 
            this.$("#detail").hide();
            this.$("#stops").hide();
            this.$("#lines").show();

            $(window).scrollTop(0)
            this.currentStopSlug = null;
        },

        showStops: function(line) {
            Stops.each(function(stop, index, list) {
                if (stop.get('line-slug') == line) {
                    App.liviews[stop.get('slug')].show();
                    console.log("show");
                } else {
                    App.liviews[stop.get('slug')].hide();
                    console.log("hide");
                }
            });

            this.$("#lines").hide();
            this.$("#detail").hide();
            this.$("#stops").show();

            $(window).scrollTop(0)
            this.currentStopSlug = null;
        },

        viewStop: function(stop) {
            if (stop == null) {
                throw("No stop provided!");
            }

            var view = new StopDetailView({ model: stop });

            this.$("#lines").hide();
            this.$("#stops").hide();
            this.$("#detail").html(view.render().el).show();

            $(window).scrollTop(0);
            this.currentStopSlug = stop.get('slug');
        },
        
        viewStopBySlug: function(slug) {
            var stop = this.models[slug];
            if (stop != null) {
                this.viewStop(stop);
            }
        },
    });

    window.App = new AppView;

    window.StopController = Backbone.Controller.extend({
        routes: {
            "": "lines",
            "line/:line": "line",
            "stop/:stop": "stop",
        },

        lines: function() {
            App.showLines();
        },

        line: function(line) {
            App.showStops(line);
        },

        stop: function(stop) {
            App.viewStopBySlug(stop);
        },
    });

    window.Controller = new StopController();

    $('header h1').click(function() {
        window.location.hash = "";
    });

    $('#lines li').click(function() {
        window.location.hash = "line/" + $(this).attr("id");
    });

    window.App.addStops();
    Backbone.history.start();
});

