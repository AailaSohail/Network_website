function toggle(id) {
    let element = document.getElementById(`edit_text${id}`);
    let save = document.getElementById(`save${id}`);
    let cancel = document.getElementById(`cancel${id}`);
    element.removeAttribute("hidden");
    save.removeAttribute("hidden");
    cancel.removeAttribute("hidden");
    let edit = document.getElementById(`edit${id}`);
    document.querySelector(`#content_edit${id}`).style.display = 'none';
    edit.setAttribute("hidden", "hidden");
  }

  function cancel(id) {
    let element = document.getElementById(`edit_text${id}`);
    let save = document.getElementById(`save${id}`);
    let cancel = document.getElementById(`cancel${id}`);
    element.setAttribute("hidden", "hidden");
    save.setAttribute("hidden", "hidden");
    cancel.setAttribute("hidden", "hidden");
    let edit = document.getElementById(`edit${id}`);
    document.querySelector(`#content_edit${id}`).style.display = 'block';
    edit.removeAttribute("hidden");
  }

  function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
  }

  function edit_content(id){
    const textcontent = document.getElementById(`edit_text${id}`).value
    fetch(`/edit/${id}`, {
      method: 'POST',
      headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
      body: JSON.stringify({
          post: textcontent,
      })
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#content_edit${id}`).innerHTML = result.data
        cancel(id);
    });
  }
  
  function like(id,liked){
    let button = document.querySelector(`#like${id}`)
    if(liked.indexOf(id)>=0){
      var like = true;
    }
    else{
      var like = false;
    }
    if(like === true){
      button.style.color="black";
    }
    else{
      button.style.color="red";
    }
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(result => {
      document.querySelector(`#post_liked${id}`).innerHTML = result.count
      button.style.color=result.color
      console.log(result.message)
    });
    like =!like
  }