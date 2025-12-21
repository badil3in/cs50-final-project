let attitude_locked = false;
let bodyshape_locked = false;
let environment_locked = false;
let look_locked = false;
let quirks_locked = false;
let region_locked = false;
let social_locked = false;
let style_locked = false;
let trait1_locked = false;
let trait2_locked = false;
let talents_locked = false;
let basics_generated = true;
let origin_generated = false;
let personality_generated = false;
let appearance_generated = false;

let attributes = {};

const iconLock = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-lock" viewBox="0 0 16 16">
<path fill-rule="evenodd" d="M8 0a4 4 0 0 1 4 4v2.05a2.5 2.5 0 0 1 2 2.45v5a2.5 2.5 0 0 1-2.5 2.5h-7A2.5 2.5 0 0 1 2 13.5v-5a2.5 2.5 0 0 1 2-2.45V4a4 4 0 0 1 4-4M4.5 7A1.5 1.5 0 0 0 3 8.5v5A1.5 1.5 0 0 0 4.5 15h7a1.5 1.5 0 0 0 1.5-1.5v-5A1.5 1.5 0 0 0 11.5 7zM8 1a3 3 0 0 0-3 3v2h6V4a3 3 0 0 0-3-3"/>
</svg>`

const iconUnlock = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-unlock" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M12 0a4 4 0 0 1 4 4v2.5h-1V4a3 3 0 1 0-6 0v2h.5A2.5 2.5 0 0 1 12 8.5v5A2.5 2.5 0 0 1 9.5 16h-7A2.5 2.5 0 0 1 0 13.5v-5A2.5 2.5 0 0 1 2.5 6H8V4a4 4 0 0 1 4-4M2.5 7A1.5 1.5 0 0 0 1 8.5v5A1.5 1.5 0 0 0 2.5 15h7a1.5 1.5 0 0 0 1.5-1.5v-5A1.5 1.5 0 0 0 9.5 7z"/>
</svg>`

// random integer function
function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// AI - get element ID in html of selected option = id in db
function getOptionIdByValue(selectedElement, value) {
    const option = Array.from(selectedElement)
                        .find(opt => opt.value === value);
    return option ? option.id : null;
}

// reusable lock-funcion - in progress
function btn_check(target_element, element_locked) {
    target_element.addEventListener('change', function(e){
        if (e.target.checked) {
            element_locked = true;
        } else {
            element_locked = false;
        }
    })
}

// output a random or the selected value in html
function randomizeOption(selected, options) {
    let output;
    if (selected == "Random") {
        // AI - exclude Random and None
        const exclude = ["Random", "None"];
        const validOptions = Array.from(options).filter(opt => !exclude.includes(opt.value)); // Ist der Wert nicht in der Ausschlussliste?
        // console.log("validOptions: ", validOptions);
        output = options[getRndInteger(0, validOptions.length - 1)].value;
    } else {
        output = selected;
    }
    return output;
}
function randomizeOption2(selectedID, options, nameKey, descKey) {
    let name;
    let description;
    console.log("options: ", options, "selectedID: ", selectedID);
    if (selectedID == "Random") {    
        // AI - exclude Random and None
        const exclude = ["Random", "None"];
        const validOptions = options.filter(opt => !exclude.includes(opt.value)); // Ist der Wert nicht in der Ausschlussliste?
        console.log("validOptions: ", validOptions);
        let index = getRndInteger(0, validOptions.length - 1);
        console.log("index: ", index);
        id = options[index].id;
        name = options[index][nameKey];
        description = options[index][descKey];
    } else {
        let selectedObject = options.filter(item => item.id === Number(selectedID));
        console.log("region else: ", selectedObject);
        id = options[0].id;
        name = selectedObject[0][nameKey];
        description = selectedObject[0][descKey];
    }
    return {id, name, description}
    // "<i>" + name + "</i>" + " - " + description;
}

// from a random or selected category randomly pick a specification  
function randomizeOptionFromCat(selected, cat_options, options, descKey) {
    // randomize category
    // selected = randomizeOption(selected, cat_options);
    // determine id of category
    // let id = selected.id;
    let optionsForID = Array.from(options);

    // filter options if category is selected
    if(selected != "Random") {
        let selectedID = getOptionIdByValue(cat_options, selected); 
        optionsForID = optionsForID.filter(item => item.category_id === Number(selectedID));
    }
    console.log("options for id talents: ", optionsForID);

    // random option
    let index = getRndInteger(0, optionsForID.length - 1);
    console.log("selected: ", selected, "index: ", index);
    // convert nodelist of options to array & filter entries by id 
    console.log("options for id: ", optionsForID);

    output = optionsForID[index][descKey];
    id = optionsForID[index].id;
    // randomize from filtered options
    
    return {output, id}
}

function randomizeMultipleOptions(selected, cat_options, options, nameKey, descKey) {
    // selected ermitteln - random oder gewählt
    // get ID from html-element of selected option = id in db
    // console.log("selectedID trait: ", selectedID, "selected: ", selected, "options: ", options);

    // add "0" (universal value) to digits
    const digits = [0]

    // involve alignment in case it is selected
    if (attributes.alignment) {
        // split alignment id in sigle digits
        let alignmentNumbers = attributes.alignment.toString().split('').map(Number);
        for (num of alignmentNumbers) {
            digits.push(num)
        }
    }

    // convert nodelist of options to array & filter entries by alignment_id array digits
    // item = current element in array
    let optionsForID = Array.from(options).filter(item => digits.includes(item.alignment_id));

    // let optionsForID = Array.from(options).filter(item => item.category_id === Number(selectedID));
    // console.log("selected", selected);
    // optionsForID = optionsForID.filter(item => Number(item.selectedAlignmentID) in digits);
    // console.log("optionForID 2. filter: ", optionsForID);

    // filter options if category is selected
    if(selected != "Random") {
        let selectedID = getOptionIdByValue(cat_options, selected); 
        optionsForID = optionsForID.filter(item => item.category_id === Number(selectedID));
    }
    console.log("trait options: ", options);
    console.log("optionsForID 3. filtered: ", optionsForID);

    // randomize 2 from filtered options
    
    let index1 = getRndInteger(0, optionsForID.length - 1);
    let index2;
    do {
    index2 = getRndInteger(0, optionsForID.length - 1);
    } while (index2 === index1);

    let output1 = "<i>" + optionsForID[index1][nameKey] + "</i>" + " - " + optionsForID[index1][descKey];
    let id1 = Array.from(options).filter(item => item[nameKey] === optionsForID[index1][nameKey])[0].id;
    let output2 = "<i>" + optionsForID[index2][nameKey] + "</i>" + " - " + optionsForID[index2][descKey];
    let id2 = Array.from(options).filter(item => item[nameKey] === optionsForID[index2][nameKey])[0].id;

    console.log("output: ", output1, id1, output2, id2);

    return {
        output1, id1,
        output2, id2
    } 
}

// generate basic attributes on button click
function basic_generator(event) {
    event.preventDefault();

    const data = new FormData(form_basics);

    let age = data.get('age');
    let alignment = data.get('alignment');
    let character_class = data.get('class');
    let gender = data.get('gender');
    let race = data.get('race');
    let selectedProf = data.get('profession');

    const age_options = document.querySelector('#age').options;
    const align_options = document.querySelector('#alignment').options;
    const gender_options = document.querySelector('#gender').options;
    const race_options = document.querySelector('#race').options;
    const profession_options = document.querySelector('#profession').options;

    let ageOutput = document.querySelector('#age_output');
    let alignOutput = document.querySelector('#alignment_output');
    let classOutput = document.querySelector('#class_output');
    let genderOutput = document.querySelector('#gender_output');
    let raceOutput = document.querySelector('#species_output');
    let profOutput = document.querySelector('#profession_output');

    let generatedAge = randomizeOption(age, age_options).toString().split('|', 2);
    ageOutput.innerHTML = generatedAge[1];
    attributes.age = Number(generatedAge[0]);
    
    let generatedAlign = randomizeOption(alignment, align_options).toString().split('|', 2);
    alignOutput.innerHTML = generatedAlign[1];
    attributes.alignment = Number(generatedAlign[0]);

    let generatedClass = character_class.toString().split('|', 2);
    classOutput.innerHTML = generatedClass[1];
    attributes.class = Number(generatedClass[0]);

    let generatedGender = randomizeOption(gender, gender_options).toString().split('|', 2);
    genderOutput.innerHTML =  generatedGender[1];
    attributes.gender = Number(generatedGender[0]);

    let generatedRace = randomizeOption(race, race_options).toString().split('|', 2);
    raceOutput.innerHTML = generatedRace[1];
    attributes.race = Number(generatedRace[0]);

    let generatedProf = randomizeOption(selectedProf, profession_options).toString().split('|', 2);
    profOutput.innerHTML = generatedProf[1];
    attributes.prof = Number(generatedProf[0]);

    // basics_generated = true;
    console.log("attributes: ", attributes); 
}

// generate appearance on button click
function appearance_generator(event) {
    event.preventDefault();

    const data = new FormData(form_appearance);

    let attitude = data.get('attitude');
    let bodyshape = data.get('bodyshape');
    let look = data.get('look');
    let style = data.get('style');
    
    const body_options = document.querySelector('#bodyshape').options;
    const look_options = document.querySelector('#look').options;
    const attitude_options = document.querySelector('#attitude').options;
    const style_options = document.querySelector('#style').options;

    console.log("body: ", body_options, "look: ", look_options, "attutide: ", attitude_options, "style: ", style_options);

    let bodyOutput = document.querySelector('#bodyshape_output');
    let lookOutput = document.querySelector('#look_output');
    let attitudeOutput = document.querySelector('#attitude_output');
    let styleOutput = document.querySelector('#style_output');

    if (!bodyshape_locked) {
        let generatedBodyshape = randomizeOption(bodyshape, body_options, bodyOutput).toString().split('|', 2);
        bodyOutput.innerHTML = generatedBodyshape[1];
        attributes.bodyshape = Number(generatedBodyshape[0]);
        console.log("attributes: ", attributes); 
    }
    if (!look_locked) {
        let generatedLook = randomizeOption(look, look_options, lookOutput).toString().split('|', 2);
        lookOutput.innerHTML = generatedLook[1];
        attributes.look = Number(generatedLook[0]);
    }
    if (!attitude_locked) {
        let generatedAttitude = randomizeOption(attitude, attitude_options, attitudeOutput).toString().split('|', 2);
        attitudeOutput.innerHTML = generatedAttitude[1];
        attributes.Attitude = Number(generatedAttitude[0]);
    }
    if (!style_locked) {
        let generatedStyle = randomizeOption(style, style_options, styleOutput).toString().split('|', 2);
        styleOutput.innerHTML = generatedStyle[1];
        attributes.Style = Number(generatedStyle[0]);
    }
    console.log("attributes: ", attributes); 
    appearance_generated = true;
}

// generate background attributes on button click
async function background_generator(event) {
    event.preventDefault();

    // api sinnvoll??
    async function loadRegions() {
        const response = await fetch("/api/regions");
        const data = await response.json();
        return data;
        };

    async function loadEnvironments() {
        const response = await fetch("/api/environments");
        const data = await response.json();
        return data;
        };

    async function loadSocials() {
        const response = await fetch("/api/socials");
        const data = await response.json();
        return data;
        };

    const data = new FormData(form_background);
    
    const regions = await loadRegions();
    const environments = await loadEnvironments();
    const socials = await loadSocials();

    // get selected id
    let selectedEnvironment = data.get('environments').toString().split('|', 1);
    let selectedRegion = data.get('regions').toString().split('|', 1);
    let selectedSocial = data.get('social_class').toString().split('|', 1);

    // const social_options = document.querySelector('#social_class').options;

    let environmentOutput = document.querySelector('#environment_output');
    let regionOutput = document.querySelector('#region_output');
    let socialOutput = document.querySelector('#social_output');

    console.log("regionsDesc: ", regions, ", ", regions);


    if (!social_locked) {
        let generatedSocial = randomizeOption2(selectedSocial, socials, "social", "social_desc");
        console.log("generatedSocial: ", generatedSocial);
        socialOutput.innerHTML = "<i>" + generatedSocial.name+ "</i>" + " - " + generatedSocial.description;
        attributes.social = generatedSocial.id;
    }

    if (!environment_locked) {
        let generatedEnvironment = randomizeOption2(selectedEnvironment, environments, "environment", "env_desc");
        environmentOutput.innerHTML = "<i>" + generatedEnvironment.name + "</i>" + " - " + generatedEnvironment.description;
        attributes.environment = generatedEnvironment.id;
    }

    if (!region_locked) {
        let generatedRegion = randomizeOption2(selectedRegion, regions, "region", "region_desc");
        regionOutput.innerHTML = "<i>"+ generatedRegion.name + "</i>" + " - " + generatedRegion.description;
        attributes.region = generatedRegion.id;
    }

    console.log("attributes: ", attributes); 
    origin_generated = true;

}

// generate personality attributes on button click
async function personality_generator(event) {
    event.preventDefault();

 // AI
    async function loadQuirks() {
        const response = await fetch("/api/quirks");
        const data = await response.json();
        return data;
        };

    async function loadTalents() {
        const response = await fetch("/api/talents");
        const data = await response.json();
        return data;
        };

    async function loadTraits() {
        const response = await fetch("/api/traits");
        const data = await response.json();
        return data;
        };

    const data = new FormData(form_personality);

    const quirks = await loadQuirks();
    const talents = await loadTalents();
    const traits = await loadTraits();

    let talents_cat = data.get('talents');
    let quirks_cat = data.get('quirks');
    let traits_cat = data.get('traits');

    const talents_options = document.querySelector('#talents').options;
    const quirks_options = document.querySelector('#quirks').options;
    const traits_options = document.querySelector('#traits').options;

    // console.log("traits options: ", traits_options);

    console.log("traits: ", traits);

    let talentsOutput = document.querySelector('#talents_output');
    let quirksOutput = document.querySelector('#quirks_output');
    let traitsOutput1 = document.querySelector('#traits_output1');
    let traitsOutput2 = document.querySelector('#traits_output2');


    // console.log("traits output: ", traitsOutput);

    if (!quirks_locked) {
        let generatedQuirk = randomizeOptionFromCat(quirks_cat, quirks_options, quirks, "quirk");
        quirksOutput.innerHTML = generatedQuirk.output;
        attributes.quirk = generatedQuirk.id;
    }
    if (!talents_locked) {
        let generatedTalents = randomizeOptionFromCat(talents_cat, talents_options, talents, "talent");
        talentsOutput.innerHTML = generatedTalents.output;
        attributes.talent = generatedTalents.id;
    }
    let traits_output = randomizeMultipleOptions(traits_cat, traits_options, traits, "trait", "trait_desc");

    if (!trait1_locked) {
        traitsOutput1.innerHTML = traits_output.output1
        attributes.trait1 = traits_output.id1;
    }
    if (!trait2_locked) {
        traitsOutput2.innerHTML = traits_output.output2;
        attributes.trait2 = traits_output.id2;
    }

    console.log("attributes: ", attributes); 
    personality_generated = true;

}

let form_basics = document.getElementById('basics-form');   
form_basics.addEventListener('submit', basic_generator);

let form_appearance = document.getElementById('appearance-form');
form_appearance.addEventListener('submit', appearance_generator);

let form_background = document.getElementById('background-form');
form_background.addEventListener('submit', background_generator);

let form_personality = document.getElementById('personality-form');
form_personality.addEventListener('submit', personality_generator);

// track locked fields - TODO: abstract away function

let bodyshape_btn_check = document.getElementById('btn-check-1a');
bodyshape_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        bodyshape_locked = true;
        document.querySelector('label[for="btn-check-1a"] div.svg').innerHTML = iconLock;
    } else {
        bodyshape_locked = false;
        document.querySelector('label[for="btn-check-1a"] div.svg').innerHTML = iconUnlock;
    }
})
let look_btn_check = document.getElementById('btn-check-1b');
look_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        look_locked = true;
        document.querySelector('label[for="btn-check-1b"] div.svg').innerHTML = iconLock;
    } else {
        look_locked = false;
        document.querySelector('label[for="btn-check-1b"] div.svg').innerHTML = iconUnlock;
    }
})

let attitude_btn_check = document.getElementById('btn-check-1c');
console.log("btn_check: ", attitude_btn_check);
attitude_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        attitude_locked = true;
        document.querySelector('label[for="btn-check-1c"] div.svg').innerHTML = iconLock;
    } else {
        attitude_locked = false;
        document.querySelector('label[for="btn-check-1c"] div.svg').innerHTML = iconUnlock;
    }
})

let style_btn_check = document.getElementById('btn-check-1d');
console.log("btn_check: ", style_btn_check);
style_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        style_locked = true;
        document.querySelector('label[for="btn-check-1d"] div.svg').innerHTML = iconLock;
    } else {
        style_locked = false;
        document.querySelector('label[for="btn-check-1d"] div.svg').innerHTML = iconUnlock;
    }
})

let social_btn_check = document.getElementById('btn-check-2a');
console.log("btn_check: ", social_btn_check);
social_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        social_locked = true;
        document.querySelector('label[for="btn-check-2a"] div.svg').innerHTML = iconLock;
    } else {
        social_locked = false;
        document.querySelector('label[for="btn-check-2a"] div.svg').innerHTML = iconUnlock;
    }
})
 
let environment_btn_check = document.getElementById('btn-check-2b');
console.log("btn_check: ", environment_btn_check);
environment_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        environment_locked = true;
        document.querySelector('label[for="btn-check-2b"] div.svg').innerHTML = iconLock;
    } else {
        environment_locked = false;
        document.querySelector('label[for="btn-check-2b"] div.svg').innerHTML = iconUnlock;
    }
})

let region_btn_check = document.getElementById('btn-check-2c');
console.log("btn_check: ", region_btn_check);
region_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        region_locked = true;
        document.querySelector('label[for="btn-check-2c"] div.svg').innerHTML = iconLock;
    } else {
        region_locked = false;
        document.querySelector('label[for="btn-check-2c"] div.svg').innerHTML = iconUnlock;
    }
})

let quirks_btn_check = document.getElementById('btn-check-3');
console.log("btn_check: ", quirks_btn_check);
quirks_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        quirks_locked = true;
        document.querySelector('label[for="btn-check-3"] div.svg').innerHTML = iconLock;
    } else {
        quirks_locked = false;
        document.querySelector('label[for="btn-check-3"] div.svg').innerHTML = iconUnlock;
    }
})

let talents_btn_check = document.getElementById('btn-check-4');
console.log("btn_check: ", talents_btn_check);
talents_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        talents_locked = true;
        document.querySelector('label[for="btn-check-4"] div.svg').innerHTML = iconLock;
    } else {
        talents_locked = false;
        document.querySelector('label[for="btn-check-4"] div.svg').innerHTML = iconUnlock;
    }
})
 
let trait1_btn_check = document.getElementById('btn-check-5a');
console.log("btn_check: ", trait1_btn_check);
trait1_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        trait1_locked = true;
        document.querySelector('.svg2 svg:nth-child(1)').innerHTML = iconLock;
    } else {
        trait1_locked = false;
        document.querySelector('.svg2 svg:nth-child(1)').innerHTML = iconUnlock;
    }
})

let trait2_btn_check = document.getElementById('btn-check-5b');
console.log("btn_check: ", trait2_btn_check);
trait2_btn_check.addEventListener('change', function(e){
    if (e.target.checked) {
        trait2_locked = true;
        document.querySelector('.svg2 svg:nth-child(2)').innerHTML = iconLock;
    } else {
        trait2_locked = false;
        document.querySelector('.svg2 svg:nth-child(2)').innerHTML = iconUnlock;
    }
})

async function saveNPC() {
    let name = document.querySelector('#NPCname').value;
    console.log("name: ", name);
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder');

    if(!basics_generated) {
        alertPlaceholder.innerHTML = `<div class="alert alert-danger alert-dismissible" role="alert">
        <div>Basics attributes missing!</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`

    } else if(!origin_generated) {
        alertPlaceholder.innerHTML = `<div class="alert alert-danger alert-dismissible" role="alert">
        <div>Origin attributes missing!</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`

    } else if(!personality_generated) {
        alertPlaceholder.innerHTML = `<div class="alert alert-danger alert-dismissible" role="alert">
        <div>Personality attributes missing!</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    } else if(!appearance_generated) {
        alertPlaceholder.innerHTML = `<div class="alert alert-danger alert-dismissible" role="alert">
        <div>Appearance attributes missing!</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    } else if(!name){
        // bootstrap JS
        alertPlaceholder.innerHTML = `<div class="alert alert-danger alert-dismissible" role="alert">
        <div>Character name missing!</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;

        // alertPlaceholder.append(wrapper);
        // const appendAlert = (message, type) => {
        //     const wrapper = document.createElement('div')
        //     wrapper.innerHTML = [
        //         `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        //         `   <div>${message}</div>`,
        //         '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        //         '</div>'
        //     ].join('')

        //     alertPlaceholder.append(wrapper)
        //     }
        console.log("Name missing")

    } else {
        attributes.name = name;
        
        console.log("fetch attributes: ", attributes); 
        try {
            const response = await fetch("/api/save_npc", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(attributes) 
            })

            const result = await response.json()
            if (!response.ok) {
                console.error("Server error:", result);
                alert("Error: " + result.error);
                return;
              }
        }
        // AI
        catch (err) {
            console.log("Error: ", err);
        }
    }
}
