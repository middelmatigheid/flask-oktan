// Getting certain divs
const admins = document.querySelector('.admins');
const header = document.querySelector('header');
const footer = document.querySelector('footer');
// Resizing admins' margin to center it
if (window.innerHeight > document.querySelector('body').offsetHeight) {
    admins.style.margin = Math.floor((window.innerHeight - header.offsetHeight - footer.offsetHeight - admins.offsetHeight) / 2) + 'px auto';
} else {
    admins.style.margin = '100px auto';
}
addEventListener("resize", (event) => {
    if (window.innerHeight > document.querySelector('body').offsetHeight) {
        admins.style.margin = Math.floor((window.innerHeight - header.offsetHeight - footer.offsetHeight - admins.offsetHeight) / 2) + 'px auto';
    } else {
        admins.style.margin = '100px auto';
    }
})

// Getting more logs from server when screen is scrolled to the end
const logs = document.querySelector('.logs');
posts_offset = 1;
window_height = null;
let flag = true;
window.addEventListener('scroll', function() {
    // Getting html objects
    let body = document.body;
    let html = document.documentElement;
    let height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
    if (window_height == height) {
        return false;
    }
    // Checking screen position
    if (height - window.scrollY < html.clientHeight * 2 && flag) {
        window_height = height;
        // Getting data from server
        let server_url = window.location.href + '/add-logs-' + (++posts_offset).toString();
        fetch(server_url)
        .then(res => res.json())
        .then(function(res) {
            logs.insertAdjacentHTML('beforeend', res[0]);
            flag = res[1];
        })
    }
});

// 'Add admin' button
const admin_add = document.querySelector('.admins-add');
const form = document.querySelector('.form');
admin_add.addEventListener('click', (event) => {
    console.log(form.style.display.length)
    if (form.style.display == 'none' || form.style.display.length == 0) {
        form.style.display = 'flex';
    } else {
        form.style.display = 'none';
    }
});