async function deleteClicked(npcID) {

const alertPlaceholder = document.getElementById('deleteAlertPlaceholder');
const successPlaceholder = document.getElementById('successAlertPlaceholder');

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