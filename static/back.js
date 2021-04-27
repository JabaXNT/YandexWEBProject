function f() {
    fetch('/bin').then(response => console.log(response.json()));
}