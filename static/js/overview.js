// event listener on delete buttons
const buttons = document.querySelectorAll('button[name="delete"]');

buttons.forEach(btn => {
    btn.addEventListener("click", function(event) {
        let npcID = btn.value;

        deleteClicked(npcID)
    })
});

// delete function
async function deleteClicked(npcID) {

    const alertPlaceholder = document.getElementById('deleteAlertPlaceholder');

    try {
        const response = await fetch("/api/delete_npc", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: npcID })
        });
        const result = await response.json()
        if (!response.ok) {
            console.error("Server error:", result);
            alert("Error: " + result.error);
            return;
        }
        window.location.href = "/overview?deletion=success";    
        }
        
    catch (err) {
        alertPlaceholder.innerHTML = 
            `<div class="alert alert-danger alert-dismissible" role="alert">
            <div>Error catch: ${err}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`
            return
}}

// off canvas requests - AI help
let offcanvas_btn = document.querySelectorAll('button[data-bs-target="#offcanvasInfo"]');
const missingSpecies = ["goliath", "aasimar"];

offcanvas_btn.forEach(btn => {
    btn.addEventListener('click', function(event){
        
        console.log("btn: ", btn)
        offcanvasInfo(btn);
    })
});

async function offcanvasInfo(btn) {
    const dataType = btn.dataset.type;
    const race = btn.dataset.race;
    const alignment = btn.dataset.alignment.replace(" ", "-").toLowerCase();
    console.log('species: ', race.toLowerCase());

    headline = document.getElementById('offcanvasLabel');
    body = document.getElementById('offcanvasBody');

    // handle species missing in API
    if(missingSpecies.includes(race.toLowerCase())) {
        // fallbackdaten
        headline.innerHTML = dataType;
        body.innerHTML = "Coming soon..";
        return;
    }

    if(dataType === "age") {
        const response = await fetch(`https://www.dnd5eapi.co/api/2014/races/${race.toLowerCase()}`);
        const result = await response.json();
        headline.innerHTML = "Age";
        body.innerHTML = `<p>${result.age}</p>`
    } else if(dataType === "alignment") {
        const response = await fetch(`https://www.dnd5eapi.co/api/2014/alignments/${alignment.toLowerCase()}`);
        const result = await response.json();
        headline.innerHTML = "Alignment";
        body.innerHTML = `<p>${result.desc}</p>`
    } else {
        body.innerHTML = "Something went wrong."
    }
}
// alignment_offcanvas.addEventListener('show.bs.offcanvas', async function(event) {
//     let id = document.querySelector('button[data-bs-target="#offcanvasAlignment"]').value;
//     let alignment_offcanvas_content = document.getElementById('alignment-details' + id);

//     alignment_offcanvas_content.innerHTML = "Loading...";
//     console.log("alignment_offcanvas: ", alignment_offcanvas);
//     // console.log("missingspecies: ", missingSpecies);
//     console.log("species + id: ", 'species' + id)
//     species = document.getElementById('species' + id).innerHTML.toLowerCase();
//     // console.log('species: ', species);
     
//     // handle species missing in API
//     if(missingSpecies.includes(species)) {
//         // fallbackdaten
//         species_offcanvas_content.innerHTML = "Coming soon..";
//         return;
//     }

//     // api request
//     const response = await fetch(`https://www.dnd5eapi.co/api/2014/races/${species}`);
//     const result = await response.json();

//     // fill offcanvas
//     alignment_offcanvas_content.innerHTML = `<p>${result.alignment}</p>`
// })

// let age_offcanvas = document.querySelectorAll('offcanvasAge');
// let age_offcanvas_content = document.getElementById('age-details');

// age_offcanvas.addEventListener('show.bs.offcanvas', async function(event) {
//     age_offcanvas_content.innerHTML = "Loading...";
//     id = document.querySelector('button[data-bs-target="#offcanvasAge"]').value;
    
//     species = document.getElementById('species' + id).innerHTML.toLowerCase();

//     if(missingSpecies.includes(species)) {
//         // fallbackdaten
//         species_offcanvas_content.innerHTML = "Coming soon..";
//         return;
//     }

//     // api request
//     const response = await fetch(`https://www.dnd5eapi.co/api/2014/races/${species}`);
//     const result = await response.json();

//     // fill offcanvas
//     age_offcanvas_content.innerHTML = `<p>${result.age}</p>`


// })