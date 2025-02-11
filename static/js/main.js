function handleSubmit(formId) {
    const form = document.getElementById(formId);
    let clientName ='clientName'
    let intervenantNom ='intervenantNom'
    if (formId =='interventionFormupdate'){
        clientName = 'clientNameupdate'
        intervenantNom = 'intervenantNomupdate'
    }
    if (form.checkValidity() && est_no_vide(clientName) && est_no_vide(intervenantNom) ) {
        form.submit();
    } else {
        form.classList.add("was-validated");
    }
}
function est_no_vide(id){
    const clientNameField = document.getElementById(id);
    if (clientNameField.value.trim() === "") {
        clientNameField.setCustomValidity("Veuillez sélectionner un ID client valide.");
        clientNameField.classList.add("is-invalid");
        return false
    } else {
        clientNameField.setCustomValidity("");
        clientNameField.classList.remove("is-invalid");
        clientNameField.classList.add("is-valid");
        return true
    }
}

function handleAutocomplete(inputField, nameFieldId, suggestionContainerId, prefix, dataDictID) {
    const suggestionContainer = document.getElementById(suggestionContainerId);
    const nameField = document.getElementById(nameFieldId);
    const dataDict = JSON.parse(document.getElementById(dataDictID).textContent);

    if (!inputField.value.startsWith(prefix)) {
        inputField.value = prefix;
    }


    suggestionContainer.innerHTML = "";
 
    suggestionContainer.style.width = `${inputField.offsetWidth}px`;
    suggestionContainer.style.left = `${inputField.offsetLeft}px`;
    suggestionContainer.style.top = `${inputField.offsetTop + inputField.offsetHeight}px`;

    const idQuery = inputField.value.slice(prefix.length).trim();

    if (idQuery === "" || inputField.value === prefix) {
        nameField.value = "";
        return;
    }

    const fullQuery = prefix + idQuery;

    // تحديث حقل الاسم إذا كان هناك تطابق كامل
    if (dataDict.hasOwnProperty(fullQuery)) {
        nameField.value = dataDict[fullQuery];
    } else {
        nameField.value = ""; // إعادة تعيين حقل الاسم إذا لم يكن id موجودًا
    }

    // فلترة المفاتيح التي تبدأ بـ fullQuery
    const suggestions = Object.keys(dataDict).filter(id => id.startsWith(fullQuery));

    // عرض الاقتراحات
    suggestions.forEach(id => {
        const suggestion = document.createElement("div");
        suggestion.textContent = id;
        suggestion.style.padding = "5px";
        suggestion.style.borderBottom = "1px solid #ccc";
        suggestion.style.cursor = "pointer";

        // عند اختيار الاقتراح
        suggestion.addEventListener("click", function () {
            inputField.value = id; // إدخال كامل عند النقر
            nameField.value = dataDict[id];
            suggestionContainer.innerHTML = ""; // إخفاء الاقتراحات
        });

        suggestionContainer.appendChild(suggestion);
    });
}


function updateForm(button, classPrefix,nombreAtrubut) {
    const buttons = document.querySelectorAll(`.${classPrefix}`);
    
    const i = Array.prototype.indexOf.call(buttons, button);
    prefix=classPrefix.split('-')[0]  // role
    for (let j = 0; j < nombreAtrubut; j++)
        document.getElementById(`${prefix}-${j}`).value = document.getElementsByClassName(`${j}-${prefix}`)[i].innerHTML
    if (prefix == 'intervention') {
        const clientDict = JSON.parse(document.getElementById("clientDict").textContent);
        const intervenantDict = JSON.parse(document.getElementById("intervenantDict").textContent);
        idClient = document.getElementsByClassName(`${3}-${prefix}`)[i].innerHTML
        idInter = document.getElementsByClassName(`${2}-${prefix}`)[i].innerHTML
        nomClient=clientDict[idClient]
        nomInter = intervenantDict[idInter]
        document.getElementById('clientNameupdate').value = nomClient
        document.getElementById('intervenantNomupdate').value = nomInter
    }
}

function deleteItem(id,action) {

    const form = document.createElement('form');
    form.method = 'POST';
    form.action =`/Delete/${action}` 

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'id';
    input.value = id; 

    form.appendChild(input);

    document.body.appendChild(form);

    form.submit();
}

function confirmDelete(button, classPrefix) {

    const buttons = document.querySelectorAll(`.${classPrefix}`);
    const i = Array.prototype.indexOf.call(buttons, button);
    let prefix = classPrefix.split('-')[0]  
    let id=document.getElementsByClassName(`0-${prefix}`)[i].innerHTML
    let action;
    switch (id.split('-')[0]) {
        case 'CLI':
            action ='Client'
            break;
        case 'INT':
            action ='Intervenant'
            break;
        default:
            action ='Intervention'
            break;
    }
    Swal.fire({
        title: 'Êtes-vous sûr ?',
        text: "La suppression est irréversible !",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui, supprimer !',
        cancelButtonText: 'Annuler'
    }).then((result) => {
        if (result.isConfirmed) {
            deleteItem(id,action);
        }
    });
}
