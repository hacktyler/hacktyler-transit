/*-----------------------------------
  Colors
------------------------------------- */
@greenery: #9FC069;
@redline: #ffd4c6;
@grey: #666;

/*-----------------------------------
  Fonts
------------------------------------- */
@sans: "DejaVu Sans Condensed";
@sansitalic: "DejaVu Sans Condensed Italic";
@sansbold: "DejaVu Sans Bold";

Map {
  background-color: #fff;
  }

#bus-stops {
  [line='Red'] {
    marker-fill: red;
  }
  [line='Blue'] {
    marker-fill: blue;
  }
  [line='Green'] {
    marker-fill: green;
  }
  [line='Yellow'] {
    marker-fill: yellow;
  }
  [order='100'],
  [order='200'],
  [order='300'],
  [order='400'],
  [order='500'],
  [order='600'],
  [order='700'],
  [order='800'],{
    marker-fill: purple;
  }
  [order='END'] {
    marker-opacity: 0.0;
  }
  marker-line-color: black;
  marker-allow-overlap: true;
}

#bus-routes {
  [line='RED'] {
    line-color: red;
    marker-fill: red;
    marker-line-color: red;
  }
  [line='BLUE'] {
    line-color: blue;
    marker-fill: blue;
    marker-line-color: blue;
  }
  [line='GREEN'] {
    line-color: green;
    marker-fill: green;
    marker-line-color: green;
  }
  [line='YELLOW'] {
    line-color: yellow;
    marker-fill: yellow;
    marker-line-color: yellow;
  }
  line-width: 2.0;
}

#water {
  line-color: @water;
  line-opacity: .15;
  line-width: 1;
}

#tyler {
  line-width: 2.0;
  line-color: #000;
}

#road-labels {
  text-name:"''";
  text-face-name: @sansbold;
  text-fill: @grey;
  text-placement: line;
  text-avoid-edges: true;
  text-size: 9;
  text-halo-radius: 1;
  [zoom>14] { text-name: "[name]"; }
  [highway='motorway'],
  [highway='primary'],
  [highway='secondary'] {
    [zoom >= 14] { text-name: "[name]"; }
  }
}

#roads-underlay {
  line-color: #cacaca;
  [zoom>9] { line-width: 0.2; }
  [zoom>12] { line-width: 0.5; }
}

#roads[highway='trunk'],
#roads[highway='trunk_link'],
#roads[highway='construction'],
#roads[highway='service'],
#roads[highway='unclassified'],
#roads[highway='residential'] {
  [zoom>15] { 
    line-width: 8; 
    line-color: white;
    line-join: round;
    line-cap: round;
  }
}
#roads-underlay[highway='trunk'],
#roads-underlay[highway='trunk_link'],
#roads-underlay[highway='construction'],
#roads-underlay[highway='service'],
#roads-underlay[highway='unclassified'],
#roads-underlay[highway='residential'] {
  [zoom>15] {
    line-join: round;
    line-cap: round;
    line-color: #cacaca;
    line-width: 10;
  }
}

#roads[highway='motorway'],
#roads[highway='motorway_link'],
#roads[highway='primary'],
#roads[highway='primary_link'],
#roads[highway='secondary'],
#roads[highway='secondary_link'],
#roads[highway='tertiary'],
#roads[highway='tertiary_link'] {
  line-color: white;
  line-width: 0.25;
  line-join: round;
  line-cap: round;
  [zoom >= 13] { line-width: 0.5; }
  [zoom >= 14] { line-width: 3; }
  [zoom >= 15] { line-width: 5; }
  [zoom >= 17] { line-width: 9; }
}

#roads-underlay[highway='motorway'],
#roads-underlay[highway='motorway_link'],
#roads-underlay[highway='primary'],
#roads-underlay[highway='primary_link'],
#roads-underlay[highway='secondary'],
#roads-underlay[highway='secondary_link'],
#roads-underlay[highway='tertiary'],
#roads-underlay[highway='tertiary_link'] {
  line-join: round;
  line-cap: round;
  line-color: #cacaca;
  line-width: 0.25;
  [zoom >= 13] { line-width: 1; }
  [zoom >= 14] { line-width: 4; }
  [zoom >= 15] { line-width: 7; }
  [zoom >= 17] { line-width: 11; }
}

#roads[highway='cycleway'],
#roads[highway='footway'] {
  line-color: @grey;
  line-opacity: .15;
  line-width: 1;
  line-dasharray: 2,2;
  }

#roads[highway='steps'] {
  line-color: @grey;
  line-opacity: 0.2;
  [zoom>17] { line-width: 20; line-dasharray: 2; }
  [zoom>18] { line-dasharray: 3; }
  [zoom>19] { line-dasharray: 4; }
  }

#parks {
  polygon-fill: @greenery;
  polygon-opacity: .1;
  line-color: @greenery;
  line-opacity: .25;
  line-width: .5;
  }

#buildings {
  building-fill: #f8f8f8;
  building-height: 3;
  }

#railroads {
  line-color: @redline;
  line-width: 0.6;
  [zoom>12] { line-width: 0.8; }
    [zoom >= 17] { line-width: 9; }
}
