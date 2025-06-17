const app = {
    mode: 'view',
    unhideButton: null,
    current: {
        marker: null,
        building: null
    },

    map: {
        markers: null,
        buildings: null,
        faculties: null,
        drawnItems: null,
        instance: null,
        
        init: function() {
            this.instance = L.map('map').setView([10.642529, -61.400225], 13);
            this.drawnItems = new L.FeatureGroup();
            this.instance.addLayer(this.drawnItems);
            M.toast({html: 'Tip: You can double click buildings!'})
            L.control.locate({
                position: 'bottomright',
                strings: {
                    title: "Pan to current location"
                },
                keepCurrentZoomLevel: true
            }).addTo(this.instance);
    
            this.instance.doubleClickZoom.disable();
            this.instance.zoomControl.setPosition('bottomright'); // Move zoom controls under the layer control toggle, with some CSS styling done in <style>
            document.body.style.overflow = 'hidden';

            this.instance.on("zoomend", () => {
                let show = this.instance.getZoom() >= 19;
                document.querySelectorAll('.transparent-tooltip-building, .transparent-tooltip').forEach(el => {
                  el.style.opacity = show ? '1' : '0';
                  el.style.visibility = show ? 'visible' : 'hidden';
                });
            })

            //Clean basemap no building names
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
                minZoom: 16,
                maxZoom: 50,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
                subdomains: 'abcd'
            }).addTo(this.instance);
        
            //Original basemap with building names
            /*L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                minZoom: 16,
                maxZoom: 50,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(map);*/
            // Prevent scrolling
        }
    },

    layers: {
        layerControl: null,
        drawingLayer: null,
        markerLayer: null,
        facultyKeys: [
            "ENG", "FST", "FHE", "FOL", "FFA", "FSS", "FMS", "FSP", "Admin/Guild", "Other"
        ],
        floorKeys: [
            "Floor 0", "Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6"
        ],
        faculties: {},
        floors: {},
        facultyLayersTree: {},
        floorLayersTree: {},

        filterSelectedFaculties: null,
        filterSelectedFloors: null,
        init: function() {
            this.filterSelectedFaculties = new Set(app.layers.facultyKeys);
            this.filterSelectedFloors = new Set(app.layers.floorKeys)

            this.facultyKeys.forEach(faculty => {
              this.faculties[faculty] = L.layerGroup().addTo(app.map.instance);
            });
            this.floorKeys.forEach(floor => {
              this.floors[floor] = L.layerGroup().addTo(app.map.instance);
            })

            this.facultyLayersTree = {
                label: "Faculties",
                selectAllCheckbox: true,
                collapsed: true,
                children: this.facultyKeys.map(faculty => ({
                  label: faculty,
                  layer: this.faculties[faculty]
                }))
            };
        
            this.floorLayersTree = {
                label: "Floors",
                selectAllCheckbox: true,
                collapsed: true,
                children: this.floorKeys.map(floor => ({
                  label: floor,
                  layer: this.floors[floor]
                }))
            };
        
            this.layerControl = L.control.layers.tree(null, [this.facultyLayersTree, this.floorLayersTree], {
              position: 'bottomright',
              collapsed: true
            }).addTo(app.map.instance)

            //By default the filter button opens and closes when you hover in/out of the button. It's super annoying, so we just disabled it completely
            //by basically killing the event when it triggers.
            let control = document.querySelector('.leaflet-control-layers');
            ['mouseover', 'mouseenter', 'mouseout', 'mouseleave'].forEach(eventName => {
                control.addEventListener(eventName, function (e) {
                  e.stopImmediatePropagation();
                }, true);
            });
            
        }
    },

    init: function() {
        app.map.init()
        app.layers.init()
    }
}

export default app