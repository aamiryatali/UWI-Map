import app from './app.js'

const queryFunctions = {
    //Custom filter function as the default does not do what we need.
    filterMarkers: function(filterName, mode) {
        app.layers.markerLayer.eachLayer(function(layer){ //For each marker
            if(mode == "add"){ 
                if(filterName.length === 3 || filterName === "Admin/Guild" || filterName === 'Other'){ //If mode == "add", add the faculty to the selectedFaculties list if it is a faculty
                    app.layers.filterSelectedFaculties.add(filterName);
                } else if (filterName.includes("Floor")){ //Likewise for floors
                    app.layers.filterSelectedFloors.add(filterName);
                }
            } else if(mode == "remove"){ //Remove it from the list is mode = "remove"
                if(filterName.length === 3 || filterName === "Admin/Guild" || filterName === 'Other'){
                    app.layers.filterSelectedFaculties.delete(filterName);
                } else if (filterName.includes("Floor")){
                    app.layers.filterSelectedFloors.delete(filterName);
                }
            }
            //If both the marker's current faculty and floor are present in the lists, then add it to the map, as it satisfies the filter conditions
            if(app.layers.filterSelectedFaculties.has(layer.data.facultyAbbr) && app.layers.filterSelectedFloors.has("Floor " + layer.data.floor)){
                if(!app.instance.hasLayer(layer)){
                    app.instance.addLayer(layer)
                }
            } else if(app.instance.hasLayer(layer)){ //Otherwise remove it from the map if it was there already
                app.instance.removeLayer(layer)
            }
        });

        //These grab the 2 'select all' checkboxes for Floors and Faculties
        let floorHeader = getHeaderCheckboxByLabel("Floors");
        let facultiesHeader = getHeaderCheckboxByLabel("Faculties");
        if(app.layers.filterSelectedFaculties.size < 10){ //If every faculty is not currently ticked, untick the select all box
            facultiesHeader.checked = false;
        } else {
            facultiesHeader.checked = true; //Otherwise tick it
        }

        if(app.layers.filterSelectedFloors.size < 7){ //Likewise for floors
            floorHeader.checked = false;
        } else {
            floorHeader.checked = true;
        }
    },

    //This function just grabs the select all DOM elements which are used in the filter function.
    getHeaderCheckboxByLabel: function(labelText) {
        let headers = document.querySelectorAll('.leaflet-layerstree-header');
        for (let header of headers) {
          let labelSpan = header.querySelector('.leaflet-layerstree-header-name');
          if (labelSpan && labelSpan.textContent.trim() === labelText) {
            return header.querySelector('input[type="checkbox"]');
          }
        }
        return null;
    },

    //Prepare and sort marker names
    markerNames: {},
    namesArray: [],
    searchFunctionality: function(){
        app.layers.markerLayer.eachLayer(function(layer) {
            namesArray.push(layer.data.name);
        });
        //Sort alphabetically
        namesArray.sort((a, b) => a.localeCompare(b));
        //Build autocomplete data object
        namesArray.forEach(function(name) {
            markerNames[name] = null;
        });
    },

    //Filtering logic (shared between input and selection)
    filterMarkersByName: function(query) {
        if (!query) {
            //If input is empty, show all markers
            /*markerLayer.eachLayer(function(layer) {
                if (!map.hasLayer(layer)) map.addLayer(layer);
            });*/
            this.filterMarkers("none", "all");
            return;
        }

        app.layers.markerLayer.eachLayer(function(layer) {
            let markerName = layer.data.name.toLowerCase();
            if (markerName.includes(query)) {
                if (!app.instance.hasLayer(layer)) app.instance.addLayer(layer);
                //If exact match, center and zoom
                if (markerName === query) {
                    app.instance.setView(layer.getLatLng(), 19);
                    foundMatch = true;
                }
            } else {
                if (app.instance.hasLayer(layer)) app.instance.removeLayer(layer);
            }
        });
    },

    init: function() {
        //By default the plugin for the filters does not actually do what is needed. It doesn't stack filters ontop of each other
        //Eg. I can't filter for floor 2 in FST, only by FST or only by Floor 2. This bit of code prevents the default behavior for the filters'
        //labels, and replaces them with custom behavior to implement the needed kind of filter.
        setTimeout(() => {
            let labels = document.querySelectorAll('.leaflet-layerstree-header-name'); //Grab all the labels
        
            labels.forEach(labelSpan => {
              labelSpan.addEventListener('click', function (e) { //For each label in the filters menu, stop the default behavior onClick;
                e.preventDefault();
                e.stopPropagation();
            
                    //These few lines just grab the name of the label by drilling down from the parent
                    let parentLabel = this.closest('.leaflet-layerstree-header-label'); //Grab the parent container
                    let checkbox = parentLabel?.querySelector('input[type="checkbox"]'); //Grab the checkbox
                    let layerName = this.textContent.trim(); //Grab the name
            
                    if(layerName == "Floors"){ //If the label clicked on wazs one of the 'select all' labels:
                        let floorGroup = parentLabel.closest('.leaflet-layerstree-node'); 
                        let floorCheckboxes = floorGroup.querySelectorAll('input[type="checkbox"]');
                        let toggleToChecked = !checkbox.checked;  // If the select all button for Floors was checked, uncheck it and vice versa.
                        floorCheckboxes.forEach(floorCheckbox => {
                            floorCheckbox.checked = toggleToChecked; //Also toggle all the children checkboxes
                        });
                    
                        this.filterSelectedFloors.clear() //Now clear the current list of filters applied
                        let floors = app.layers.floorLayersTree.children //The names of all the floor labels are in this structure
                        if(checkbox.checked == true){ //If the state of the select all checkbox was toggle from unchecked to checked:
                            for(let floor of floors){
                                this.filterSelectedFloors.add(floor['label']); //Add every floor to the current list of filtered floors.
                            }
                        }
                        filterMarkers(layerName, "all"); //Then call the custom filter function
                    
                    } else if (layerName == "Faculties"){ //Do the same for the Faculties select all button
                        let facultiesGroup = parentLabel.closest('.leaflet-layerstree-node');
                        let facultiesCheckboxes = facultiesGroup.querySelectorAll('input[type="checkbox"]');
                        let toggleToChecked = !checkbox.checked;
                        facultiesCheckboxes.forEach(facultiesCheckbox => {
                            facultiesCheckbox.checked = toggleToChecked;
                        });

                        this.filterSelectedFaculties.clear()
                        let filterFaculties = app.layers.facultyLayersTree.children
                        if(checkbox.checked == true){
                            for(let faculty of filterFaculties){
                                this.filterSelectedFaculties.add(faculty['label']);
                            }
                        }
                        filterMarkers(layerName, "all");
                    
                    } else { //If none of the 2 above were true, then an individual checkbox was clicked, so just toggle that one.
                        if (checkbox.checked) {
                            filterMarkers(layerName, "remove"); //If it was checked before, uncheck it and remove it from the list of current filters
                            checkbox.checked = !checkbox.checked;
                        } else {
                            filterMarkers(layerName, "add"); //Otherwise check it and add it
                            checkbox.checked = !checkbox.checked;
                        }
                    }
                });
            });
        }, 300)

        //Initialize Autocomplete with both input and onAutocomplete handlers
        let searchInput = document.getElementById('marker-search');
        let autocompleteInstance = M.Autocomplete.init(searchInput, {
            data: markerNames,
            minLength: 0,
            limit:3,
            onAutocomplete: function(selectedName) {
                this.filterMarkersByName(selectedName.toLowerCase()); // Ensure this handles selection
            }
        });
    
        //Live filtering on input
        searchInput.addEventListener('input', function () {
            let query = this.value.trim().toLowerCase();
            this.filterMarkersByName(query);
        })

         //Clears search input
        let clearBtn = document.getElementById('clear-search')
        clearBtn.addEventListener('click', function () {
            searchInput.value = '';
            this.filterMarkers("none", "all"); //Reshow all markers
            //recenterMap();
        });
    }
}

export default queryFunctions
    