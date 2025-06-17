import app from './app.js'

const htmlBuilder = {
    buildingInfo: function(building) {
        //currentBuilding = e.target.feature.properties; // Ensure currentBuilding is set correctly
        //let pane = document.querySelector('#pane');
        //let building = currentBuilding; // Use currentBuilding for consistency
        let html = `
    <div class="row" style="overflow-x: hidden;" id='editBuildingForm' name='editBuildingForm'>
        <div class="col s12">
            <div class="col s12" style="background-color: #a5d6a7">
                <p style="font-family: 'Pridi', cursive">Building Information</p>
                <button class="btn-floating btn-small transparent" style="position: absolute; top: 10px; right: 10px; z-index: 1500;" onclick="closeContainer()">
                    <i class="material-icons">exit_to_app</i>
                </button>
            </div>
            <div>`;
        if (building.image != '') {
            html += `
            <div class="card-image crop-box">
                <img class="materialboxed full-img" src="${building.image}" height="200" style="border-radius: 0; object-fit:cover; object-position: 20% 10%;">
            </div>`;
        } else {
            html += `<div style="margin-top: 2.5em;"></div>`;
        }
        html += `
                <div name="buildingInfoForm" id="buildingInfoForm" class="card-content">
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Name</strong></h6>
                    <p style="font-family: 'Pridi', cursive">${building.name}</p>
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Faculty</strong></h6>
                    <p style="font-family: 'Pridi', cursive">${building.facultylong}</p>
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Description</strong></h6>
                    <p style="font-family: 'Pridi', cursive">${building.description}</p>
                </div>
            </div>
            </form>
        </div>
    </div>`;
        return html
        //pane.innerHTML = html;
        //pane.style.left = '10px';
    
        // Initialize Materialboxed for the image
        //var elems = document.querySelectorAll('.materialboxed');
        //var instances = M.Materialbox.init(elems);
        //removeUnhideButton(); // Remove unhide button
    },

    markerInfo: function(marker) {
        let html = `
    <div class="row" id='markerInfo' name='markerInfo'>
        <div class="col s12">
        <div class ="col s12" style="background-color: #a5d6a7">
            <p style="font-family: 'Pridi', cursive">Marker Information</p>
        </div>
            <div>`
        //Only add the image if one exists for the current marker
        if(marker.data.image != ''){
            html += `
            <div class="card-image">
                <button class="btn-floating btn-small transparent" style="position: absolute; top: 10px; right: 10px; z-index: 1500;" onclick="closeContainer()">
                    <i class="material-icons">exit_to_app</i>
                </button>
                <div class="crop-box">
                    <img class="materialboxed full-img" src=${marker.data.image}>
                </div>
            </div>
            `
        } else {
            html += `<button class="btn-floating btn-small transparent" style="position: absolute; top: 10px; right: 10px; z-index: 1500;" onclick="closeContainer()">
                        <i class="material-icons">exit_to_app</i>
                     </button>
                     <div style="margin-top: 2.5em;"></div>`
        }
        html += `
                <div name="markerInfoForm" id="markerInfoForm" class="card-content">
                    <span class="card-title"></span>
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Name</strong></h6>
                    <p style="font-family: 'Pridi', cursive">${marker.data.name}</p>
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Building</strong></h6>
                    <p style="font-family: 'Pridi', cursive">${marker.data.buildingName}</p>
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Floor Number</strong></h6>
                    <p style="font-family: 'Pridi', cursive">${marker.data.floor}</p>
                    <h6 style="font-family: 'Pridi', cursive; color: #4caf50"><strong>Description</strong></h6>`
                    if(marker.data.description != ''){
                        html += `<p style="font-family: 'Pridi', cursive">${marker.data.description}</p>`
                    } else {
                        html += `<p style="font-family: 'Pridi', cursive">No description provided</p>`
                    }
                html += `</div>
            </div>
            </form>
        </div>
    </div>
            `;
        return html;
    }
}

export default htmlBuilder