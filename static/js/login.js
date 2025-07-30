const form = document.querySelector('.form');
const header = document.querySelector('header');
const footer = document.querySelector('footer');
if (window.innerHeight > document.querySelector('body').offsetHeight) {
    form.style.margin = Math.floor((window.innerHeight - header.offsetHeight - footer.offsetHeight - form.offsetHeight) / 2) + 'px auto';
} else {
    form.style.margin = '100px auto';
}
addEventListener("resize", (event) => {
    if (window.innerHeight > document.querySelector('body').offsetHeight) {
        form.style.margin = Math.floor((window.innerHeight - header.offsetHeight - footer.offsetHeight - form.offsetHeight) / 2) + 'px auto';
    } else {
        form.style.margin = '100px auto';
    }
})