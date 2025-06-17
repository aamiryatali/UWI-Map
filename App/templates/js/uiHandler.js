import app from './app.js'

const uiHandler = {
    closeContainer: function(oldLat=null, oldLng=null) {
        let pane = document.querySelector('#pane');
        pane.innerHTML = '';
        pane.style.left = '-300px';
        if(app.current.marker){ //Disables dragging on the current marker if it was enabled before.
            if(app.current.marker.dragging){
                app.current.marker.dragging.disable();
            }
            if(oldLat != null && oldLng != null){
                app.current.marker.setLatLng([oldLat, oldLng]);
            }
        }
        if(app.current.building){
            drawnItems.removeLayer(app.current.building);
        }
        app.mode = 'view'
    },

    removeUnhideButton: function() {
        app.unhideButton.style.left = '-300px'
    },

    initMaterialBox: function() {
        // Initialize Materialboxed for the image
        let elems = document.querySelectorAll('.materialboxed');
        let instances = M.Materialbox.init(elems, {
            onCloseEnd: function() {
                let pane = document.querySelector('#pane');
                if (pane) {
                    pane.style.overflow = 'auto';
                }
            }
        });
    },

    hideInformation: function() {
        let pane = document.querySelector('#pane');
        if (pane) {
            pane.style.left = '-300px';
            app.unhideButton.style.left = '10px'; // Show the unhide button
        }
    },

    // Function to unhide the information panel
    unhideInformation: function() {
        let pane = document.querySelector('#pane');
        if (pane) {
            pane.style.left = '10px';
            app.unhideButton.style.left = '-300px'; // Hide the unhide button
        }
    },

    // Function to remove the unhide button
    removeUnhideButton: function () {
        app.unhideButton.style.left = '-300px'; // Hide the unhide button
    },

    showLoader: function() {
        document.getElementById('loading-bar').style.display = 'block';
    },

    hideLoader: function() {
        document.getElementById('loading-bar').style.display = 'none';
    },

    init: function() {
        // Add swipe functionality for the pane
        app.unhideButton = document.createElement('button');  // Add the unhide button to the document body
        app.unhideButton.innerHTML = 'Unhide Information';
        app.unhideButton.className = 'waves-effect waves-light green btn';
        app.unhideButton.style.position = 'fixed';
        app.unhideButton.style.bottom = '10px';
        app.unhideButton.style.left = '-300px'; // Initially hidden
        app.unhideButton.style.zIndex = '1500';
        app.unhideButton.onclick = this.unhideInformation;
        document.body.appendChild(app.unhideButton)

        let touchStartX, touchEndX;
        let pane = document.querySelector('#pane')
        pane.addEventListener('touchstart', e => {
            // Restrict swipe to ribbon or text, ignore buttons, input fields, materialboxed elements, and their overlays
            if (e.target.tagName === 'BUTTON' || 
                e.target.tagName === 'INPUT' || 
                e.target.tagName === 'TEXTAREA' || 
                e.target.tagName === 'SELECT' || 
                e.target.closest('.materialboxed') || 
                e.target.closest('.materialbox-overlay')) {
                return;
            }
            touchStartX = e.targetTouches[0].clientX;
        });
    
        pane.addEventListener('touchmove', e => {
            if (touchStartX !== undefined) {
                touchEndX = e.targetTouches[0].clientX;
            }
        });
    
        pane.addEventListener('touchend', () => {
            if (touchStartX !== undefined && touchStartX - touchEndX > 45) { // Swipe left to close
                this.closeContainer();
            }
            touchStartX = undefined; // Reset touchStartX
        });

        this.showLoader()
    }
}

export default uiHandler