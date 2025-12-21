let FIRSTNAMES = {}

// random integer function
function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// function to put random name-parts together
function assembleName(firstPart, secondPart, lastnameFirstpart, lastnameSecondpart) {
    let firstname = firstPart[getRndInteger(0, firstPart.length - 1)] + secondPart[getRndInteger(0, secondPart.length - 1)];
    let lastname = lastnameFirstpart[getRndInteger(0, lastnameFirstpart.length - 1)] + lastnameSecondpart[getRndInteger(0, lastnameSecondpart.length - 1)];
    fullname = firstname + " " + lastname;
    return fullname;
}

// function to select the name parts from the database depending on selected species and gender
function namePartsSelector(species, gender) {
    let firstPart = FIRSTNAMES[species][gender].firstPart;
    let secondPart = FIRSTNAMES[species][gender].secondPart;
    let lastnameFirstpart = FIRSTNAMES[species]["Lastname"].firstPart;
    let lastnameSecondpart = FIRSTNAMES[species]["Lastname"].secondPart;

    return {
        firstPart,
        secondPart,
        lastnameFirstpart,
        lastnameSecondpart
    };
}

// AI code
fetch("/static/data/name_gen.JSON")
    .then(response => response.json())
    .then(data => {
        FIRSTNAMES = data;
    })

// function to generate a name output
function nameGenerator(event) {
    event.preventDefault();
    console.log("Click!")

    // const data = new FormData(form);
    // let gender = data.get('gender');
    let gender = document.getElementById('gender_output').innerHTML;
    let species = document.getElementById('species_output').innerHTML;
    console.log("species: ", species)
    console.log("gender: ", gender)

    if(gender && species) {

        let nameOutput = document.querySelector('#NPCname');
        // let species = data.get('species');
        let nameParts = namePartsSelector(species, gender)
    
        nameOutput.value = assembleName(nameParts.firstPart, nameParts.secondPart, nameParts.lastnameFirstpart, nameParts.lastnameSecondpart);
    } else {
        console.log("no gender/species")
    }
}

// function call on event
let button = document.getElementById('name_gen');
button.addEventListener('click', nameGenerator);


