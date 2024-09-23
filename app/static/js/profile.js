function checkIfTokenPresent(){
    const h = new Headers().get('dom_explorer')
    console.log(h)
    const token = document.cookie
    console.log(token)
    console.log("hello world")
}

checkIfTokenPresent()