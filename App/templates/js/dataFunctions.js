import app from './app.js'

const dataFunctions = {
    addObjects: function(){
        markers = app.map.markers;
        buildings = app.map.buildings;
        faculties = app.map.faculties;
        for(marker of markers){
            let newMarker = L.marker([marker['x'], marker['y']], {title: marker['name']}).addTo(app.map.instance); // Adds each marker to the map

            newMarker.on('click', onMarkerClick);
            newMarker.data = marker //The marker object attributes from the backend is basically just recreated here.
            newMarker.bindTooltip(marker['name'], {permanent: true, offset: [-15, 40], direction: "center", className: 'transparent-tooltip'});
            app.layers.markerLayer.addLayer(newMarker).addTo(app.instance.map); // Add each marker to the layerGroup

            const facultyIconUrls = {
                "FST": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png",
                "FHE": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
                "ENG": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png",
                "FOL": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png",
                "FFA": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
                "FSS": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
                "Admin/Guild": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png",
                "Other": "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png"
            };
            
            //Dynamically change the color of the marker icon depending on the faculty.
            const facultyLayer = app.layers.faculties[marker['facultyAbbr']] || app.layers.faculties["Other"];
            const markerColorIcon = facultyIconUrls[marker['facultyAbbr']] || facultyIconUrls["Other"]

            facultyLayer.addLayer(newMarker).addTo(app.map.instance);

            /*switch(marker['facultyAbbr']) {
                case "FST":
                    fst.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png"
                    break;
                case "FHE":
                    fhe.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png"
                    break;
                case "ENG":
                    eng.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png"
                    break;
                case "FOL":
                    fol.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png"
                    break;
                case "FFA":
                    ffa.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png"
                    break;
                case "FSS":
                    fss.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png"
                    break;
                case "Admin/Guild":
                    admin.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png"
                    break;
                default:
                    other.addLayer(newMarker).addTo(map);
                    markerColorIcon = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png"
                    break;
            }*/
            let newIcon = L.icon({
                iconUrl: markerColorIcon,
                iconSize: [25, 41], 
                iconAnchor: [12, 41],  
                popupAnchor: [1, -34],
                tooltipAnchor: [16, -28]
              });
            newMarker.setIcon(newIcon);
        }
        
        //Recreating pseudo-building objects from the backend.
        for(building of buildings){
            let name = building['name'];
            let newDrawingCoords = JSON.parse(building['drawingCoords'])
            
            newDrawingCoords.properties["id"] = building['id']
            newDrawingCoords.properties["name"] = name;
            newDrawingCoords.properties["faculty"] = building['facultyAbbr']
            newDrawingCoords.properties["facultylong"] = building['facultyName']
            newDrawingCoords.properties["image"] = building['image']
            newDrawingCoords.properties["description"] = building['description']
            app.layers.drawingLayer.addData(newDrawingCoords)
        }
        
        const facultyColors = {
            "FST": "gold",
            "FHE": "royalblue",
            "ENG": "slategrey",
            "FOL": "black",
            "FFA": "green",
            "FSS": "red",
            "Admin/Guild": "purple",
            "Other": "grey"
        };

        //Dynamically color each building depending on the faculty
        app.layers.drawingLayer.eachLayer(function(layer){
            layer.bindTooltip(layer.feature.properties.name, {permanent: true, offset: [0, 0], direction: "center", className: 'transparent-tooltip-building'});
            var facultyColor;
            var fillFacultyColor;
            switch(layer.feature.properties.faculty) {
                case "FST":
                    facultyColor='gold'
                    fillfacultyColor='yellow'
                    break;
                case "FHE":
                    facultyColor='royalblue'
                    fillfacultyColor='royalblue'
                    break;
                case "ENG":
                    facultyColor='slategrey'
                    fillfacultyColor='slategrey'
                    break;
                case "FOL":
                    facultyColor='black'
                    fillfacultyColor='black'
                    break;
                case "FFA":
                    facultyColor='green'
                    fillfacultyColor='green'
                    break;
                case "FSS":
                    facultyColor='red'
                    fillfacultyColor='red'
                    break;
                case "Admin/Guild":
                    facultyColor='purple'
                    fillfacultyColor='purple'
                    break;
                default:
                    facultyColor='grey'
                    fillfacultyColor='grey'
                    break;
            }
            layer.setStyle({
                color: facultyColor,
                fillColor: fillFacultyColor,
                weight: 1,
                fillOpacity: 0.2
              });
            layer.on('dblclick', onBuildingClick); //Double clicking a building will bring up the info pane for it.
        });
    }
}

export default dataFunctions